# Notification System Design (Concise Overview)

## STAGE 1 — API DESIGN
* **GET `/api/v1/notifications`**: Retrieves JWT-authorized student alerts. Supports pagination and filtering.
* **PATCH `/api/v1/notifications/{id}/read`**: Marks a notification as read.
* Uses WebSocket (`ws://`) connections for pushing instant real-time updates to active clients.

---

## STAGE 2 — DATABASE DESIGN
* **Database Choice**: PostgreSQL for ACID compliance, relational stability, and dynamic JSONB support.
* **Optimized Schema**:
  ```sql
  CREATE TABLE notifications (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      student_id BIGINT NOT NULL,
      type VARCHAR(50) NOT NULL, -- Placement, Result, Event
      message TEXT NOT NULL,
      is_read BOOLEAN DEFAULT false,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
  );
  CREATE INDEX idx_student_unread ON notifications (student_id, is_read, created_at DESC);
  ```
* **Scaling**: Use horizontal partitioning on `created_at` and cache the `unread_count` values inside Redis.

---

## STAGE 3 — QUERY OPTIMIZATION
* **Slow Query Scenario**: Running `SELECT * FROM notifications WHERE student_id = 1042 AND is_read = false ORDER BY created_at DESC` triggers a Sequential Scan or heavy memory sort if unindexed.
* **Optimization**: Add a composite B-Tree index:
  ```sql
  CREATE INDEX idx_student_unread_sort ON notifications (student_id, is_read, created_at DESC);
  ```
* **Tradeoff**: Massively increases read performance; slightly slows down write operations due to index rebuilding.

---

## STAGE 4 — SCALING STRATEGY
To handle 10k+ concurrent connections efficiently:
1. **Reduce Polling**: Utilize event-driven WebSockets rather than constant HTTP API polling.
2. **Redis Caching**: Store recent user notification feeds in cache for rapid sub-millisecond retrieval.
3. **Task Queuing**: Offload heavy database inserts to background task processors.

---

## STAGE 5 — DISTRIBUTED NOTIFICATION ARCHITECTURE
* **Design Pattern**: Switch from blocking synchronous dispatches to an asynchronous event-driven model using Kafka or RabbitMQ.
* **Execution Flow**: The API publishes alert events to the queue and instantly returns `202 Accepted` to the client.
* **Asynchronous Workers**: Independent consumers pull from the queue to concurrently save to database, send external push notifications, and dispatch candidate emails.

---

## STAGE 6 — PRIORITY INBOX
* **Optimization Engine**: Replaces slow `O(n log n)` full memory sorts with a bounded **Min-Heap** ($K=10$).
* **Ranking Factors**: Prioritized by notification urgency category (`Placement` > `Result` > `Event`) and message timestamp recency.
* **Efficiency**: Bounded heap operation runs in $O(n \log k)$ time and operates within $O(k)$ memory limits.
