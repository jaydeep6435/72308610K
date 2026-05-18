# Comprehensive Notification System Architecture

This document answers the specific system design evaluation stages for the Afformed Backend.

---

## STAGE 1 — API DESIGN

### Endpoints
**1. Fetch Notifications**
`GET /api/v1/notifications`
*   **Headers**: `Authorization: Bearer <JWT>`
*   **Query Params**: 
    *   `page=1&limit=20`
    *   `type=Placement`
    *   `unreadOnly=true`
*   **Response Schema**:
    ```json
    {
      "success": true,
      "data": {
         "items": [...],
         "meta": {"total": 500, "unreadCount": 12, "page": 1}
      }
    }
    ```

**2. Mark as Read**
`PATCH /api/v1/notifications/{id}/read`

### Architecture Elements
*   **JWT Auth**: Protects route. User ID is extracted from claims to filter the DB directly.
*   **Websockets**: A WSS connection (`ws://domain/notifications`) pushes real-time JSON payloads using channels.

---

## STAGE 2 — DATABASE DESIGN

**Database Choice:** PostgreSQL
PostgreSQL is highly optimized for complex querying, indexing, and JSONB payloads.

### Schema Design (3NF)
```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id BIGINT NOT NULL,
    type VARCHAR(50) NOT NULL, -- Placement, Result, Event
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexing Strategy
CREATE INDEX idx_notifications_student_unread ON notifications (student_id, is_read, created_at DESC);
```

### Scaling Challenges & Solutions
*   **Partitioning**: As the table grows beyond 50M rows, partition by `created_at` (e.g., monthly).
*   **Read Replicas**: Direct all `GET` API queries to read replicas. Keep `PATCH` (mark as read) on the primary master node.
*   **Caching**: Cache the `unread_count` integer in Redis, invalidating only when a new row is inserted.

---

## STAGE 3 — QUERY OPTIMIZATION

**Target Query:**
```sql
SELECT * FROM notifications
WHERE studentID = 1042 AND isRead = false
ORDER BY createdAt DESC;
```

### Why it becomes slow:
Without a specific index, Postgres runs a Sequential Scan (seq scan) across the entire table or filters heavily on a weak index. Sorting (`ORDER BY`) an unindexed result set causes heavy in-memory/disk sorts.

### Optimization (Composite Index)
```sql
CREATE INDEX idx_student_unread_sort 
ON notifications (studentID, isRead, createdAt DESC);
```
**Tradeoffs:**
Indexes speed up read operations massively but impose write overhead. Every `INSERT` and `UPDATE` must reorganize the B-Tree. Given notifications are read-heavy, this is a highly acceptable tradeoff.

---

## STAGE 4 — SCALING STRATEGY

To handle 10k concurrent users:
1.  **Polling Reduction**: Deprecate HTTP polling. Switch to WebSocket push events.
2.  **Redis Caching**: Store recent notifications in Redis Lists. Check Redis first; fallback to Postgres.
3.  **CDN**: Static payloads or notification icons must be delivered via CDN.
4.  **Async Processing**: When a professor pushes a Result, it should not hit the DB synchronously. It must be fired into a queue.

---

## STAGE 5 — DISTRIBUTED NOTIFICATION ARCHITECTURE

**Bad Sequential Implementation:**
```python
# Synchronous, blocks the API thread. Fails if SMTP is down.
def send_notification(student_id, msg):
    save_to_db(student_id, msg)
    send_email(student_id, msg) 
    push_websocket(student_id, msg)
```

**Scalable Event-Driven Redesign:**
Using **RabbitMQ** or **Apache Kafka**:
1.  API receives request -> Publishes `{event: "result_posted"}` to Kafka -> Returns `202 Accepted`.
2.  **Worker A (DB Node)**: Consumes event -> Saves to Postgres.
3.  **Worker B (Email Node)**: Consumes event -> Dispatches Email. Handles retries and pushes to Dead Letter Queue (DLQ) if failed permanently.
4.  **Worker C (WS Node)**: Pushes message to active WebSocket connections.

*Idempotency is maintained by attaching unique Event UUIDs.*

---

## STAGE 6 — PRIORITY INBOX

To return the top 10 notifications based on dynamic ranking:

**Why sorting fails:**
`O(n log n)` sort on 100,000 notifications is extremely CPU intensive.

**Implemented Solution:**
We implemented a **Min-Heap** bounded strictly to $k=10$.
1.  Assign Priority score: `Placement (3) > Result (2) > Event (1)`.
2.  Parse `created_at` timestamp.
3.  Push tuple `(priority, timestamp, item)` to `heapq`.
4.  If `len(heap) > 10`, execute `heappushpop()`.

**Complexity:** $O(n \log k)$. Because $k=10$, this approaches $O(n)$ time complexity, utilizing a negligible $O(k)$ memory footprint.
