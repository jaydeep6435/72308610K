# Vehicle Maintenance Scheduler & Priority Notification Engine

This repository contains a production-grade backend application built with Python, Django, and Django REST Framework. The system optimizes vehicle maintenance schedules across various depots using an optimized 0/1 Knapsack dynamic programming algorithm. It also prioritizes incoming operational notifications using a Min-Heap ranking engine and implements an asynchronous logging middleware.

---

## Setup & Execution

```bash
# Create and activate environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python manage.py migrate
python manage.py runserver
```

---

## Verification Screenshots & Gallery

### 1. Identity & Auth Token Registration API Output
Successful authentication handshake generating the JWT access token for secure communication.
![Auth Initial Registration Output](../screenshot/Screenshot%202026-05-18%20151654.png)

### 2. Refreshed Auth Token & Signature Validation
JWT token structure verification including validated signatures and candidate information.
![Refreshed Active Auth Output](../screenshot/Screenshot%202026-05-18%20163957.png)

### 3. Local Depots Endpoint Output (`GET /api/v1/depots`)
Returns the resolved list of operational depots along with their mechanic capacity constraints.
![Local Depots Endpoint Response](../screenshot/Screenshot%202026-05-18%20163505.png)

### 4. Local Tasks Endpoint Output (`GET /api/v1/tasks`)
Retrieves global vehicle tasks currently queued for scheduling.
![Local Tasks Endpoint Response](../screenshot/Screenshot%202026-05-18%20163545.png)

### 5. Local Optimal Schedule Generation Endpoint Output (`GET /api/v1/schedule/4`)
Optimized maintenance schedule outputs displaying chosen tasks under capacity constraints.
![Local Schedule Generation Response](../screenshot/Screenshot%202026-05-18%20163635.png)

### 6. Local Ranked Priority Notifications Endpoint Output (`GET /api/v1/priority-notifications`)
Top 10 sorted operational alerts ranked strictly by type category urgency and timestamps.
![Local Priority Notifications Response](../screenshot/Screenshot%202026-05-18%20163703.png)

### 7. External Direct Depot Resolution Verification
Direct API query output verifying live connections to the external depot service.
![External Depots API Direct Response](../screenshot/Screenshot%202026-05-18%20155511.png)

### 8. External Direct Logging Validation API Payload
Raw verification structure validating package, stack, level, and message formats.
![External Logs API Query Output](../screenshot/Screenshot%202026-05-18%20152004.png)

### 9. External Direct Logging Submission Success Confirmation
Success confirmation showing background logged events safely recorded on remote logging servers.
![External Logs API Output](../screenshot/Screenshot%202026-05-18%20164056.png)
