# Vehicle Maintenance Scheduler & Priority Notification Engine

A production-grade, highly modular backend designed to optimize vehicle maintenance schedules and prioritize incoming notifications. The project is implemented using Python, Django, and Django REST Framework, adhering to clean, layered architectural boundaries.

The optimization logic solves task scheduling using a **0/1 Knapsack Dynamic Programming** algorithm to maximize maintenance impact within bounded mechanic hours, while the priority ranking utilizes a **Min-Heap** structure to dynamically extract the highest-priority events in real-time.

---

## Technical Architecture

The codebase separates responsibilities into distinct layers to enforce high cohesion and low coupling:

*   **Controllers (API views)**: Expose thin endpoints, validate incoming request parameters, and format standardized JSON payloads.
*   **Services**: Orchestrate business logic, coordinate repository communications, and invoke mathematical engines.
*   **Repositories**: Abstract external network communication. Responsible for querying the Afformed Evaluation APIs, performing sanitization, and filtering resources locally.
*   **Algorithms**: Pure, isolated mathematical layers (e.g., Knapsack DP solver and dynamic Heap prioritizer).
*   **Middleware**: Intercepts boundary transactions for global custom exceptions and transparent, background logging.
*   **Logging Middleware Package**: Decoupled, asynchronous package executing log dispatches on background worker threads with exponential backoff and payload validation.

### Directory Structure

```text
vehicle_maintenance_scheduler/
├── logging_middleware/        # Decoupled standalone logging package
│   ├── api_client.py          # Staged, asynchronous log dispatcher
│   ├── logger.py              # Main Log() interface with auto-truncation logic
│   └── validators.py          # Schema & payload format enforcement
├── core/                      # Project configuration & settings
├── src/
│   ├── algorithms/            # Dynamic Programming & Heap algorithms
│   ├── config/                # Environment variables and dynamic secrets loader
│   ├── controllers/           # Slim HTTP routing views
│   ├── handlers/              # Centralized exception handlers
│   ├── middleware/            # Logging and exception middlewares
│   ├── repositories/          # Decoupled HTTP API repository clients
│   ├── routes/                # API router URL mapping
│   ├── serializers/           # Request/response validation schemas
│   ├── services/              # Core workflow orchestrations
│   ├── tests/                 # Full unit test suites
│   └── utils/                 # Structured responses & base HTTP clients
├── requirements.txt           # Dependency definition
└── manage.py
```

---

## Algorithmic Details

### 1. 0/1 Knapsack Maintenance Optimizer
To select the optimal combination of vehicle tasks that yield the highest impact under a fixed budget of mechanic hours ($W$):
*   **Mathematical Modeling**: Standard $O(n \times W)$ Dynamic Programming.
*   **Refinements**: Zero-duration tasks are filtered out early to prevent wasted iterations. 
*   **Backtracking**: A pointer backtracking algorithm rebuilds the exact selected array of tasks in $O(n)$ to ensure full traceability in API responses.

### 2. $O(n \log k)$ Notification Priority Ranking
To select the Top $K=10$ notifications sorted by Priority (`Placement` > `Result` > `Event`) and Recency:
*   **Complexity**: Rather than performing a heavy $O(n \log n)$ full sort on unbounded datasets, we maintain a **Min-Heap** bounded at size $k$.
*   **Execution**: Incoming items are evaluated in $O(n \log k)$ time, discarding lower priority events dynamically to ensure high scaling performance.

---

## Setup & Execution

### Prerequisites
*   Python 3.11+
*   Virtual environment (`venv`)

### 1. Virtual Environment & Dependencies
```bash
# Create and activate environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Secrets
Create a `.env` file at the root of `vehicle_maintenance_scheduler`:
```ini
BASE_URL=http://4.224.186.213/evaluation-service
ACCESS_TOKEN=your_jwt_here

CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret

DJANGO_SECRET_KEY=dev-secret-key-change-in-prod
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

### 3. Start Development Server
```bash
python manage.py migrate
python manage.py runserver
```

---

## Verification & API Endpoints

All endpoints are standardized under the `/api/v1/` prefix:

*   **`GET /api/v1/depots`**: Fetches all depots and their respective operational mechanic capacities.
*   **`GET /api/v1/tasks`**: Retrieves global vehicle tasks ready for scheduling.
*   **`GET /api/v1/schedule/<depot_id>`**: Resolves the depot ID locally, loads global tasks, computes the optimal schedule, and logs execution details.
*   **`GET /api/v1/priority-notifications`**: Renders the top-10 sorted priority notifications using the dynamic heap ranker.

---

## Test Coverage

A full unittest suite is located under `src/tests` covering business logic, repositories, and math algorithms. Run tests using:

```bash
$env:DJANGO_SETTINGS_MODULE="core.settings"
venv\Scripts\python.exe -m unittest discover -s src/tests -p "test_*.py"
```

---

## Verification Gallery & Screenshots

Below are verification screenshots showcasing real-time API execution, validation structures, and successful endpoint operations against the Afformed Evaluation APIs.

### Endpoint: Schedule Generation Pipeline
Optimal task scheduling computation ($W=188$ Mechanic Hours) executing DP algorithms:
![Schedule Generation Endpoint Output](./screenshot/Screenshot%202026-05-18%20163957.png)

### Endpoint: Ranked Priority Notifications
Retrieving top notifications sorted strictly by category priority and timestamp recency:
![Priority Notifications Endpoint Output](./screenshot/Screenshot%202026-05-18%20164056.png)

### Endpoint: Depot Resolution
Listing all available depots along with their allocated mechanic capacities:
![Depots Endpoint Output](./screenshot/Screenshot%202026-05-18%20163703.png)

### Live Server Logs & Daemon Process Execution
Showing background daemon threads successfully dispatching logs with auto-truncation:
![Console Logs Background Execution](./screenshot/Screenshot%202026-05-18%20163545.png)

### Global Task API Response
Listing global vehicle tasks fetched and formatted from the external evaluation service:
![Tasks Endpoint Output](./screenshot/Screenshot%202026-05-18%20163635.png)

### Algorithmic Test Suite Verification
Showing all dynamic programming, min-heap routing, and repository integration tests passing:
![Unit Test Suite Execution](./screenshot/Screenshot%202026-05-18%20152004.png)
