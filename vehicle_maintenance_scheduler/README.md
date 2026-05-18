# Vehicle Maintenance Scheduler API 🚛

![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django)
![DRF](https://img.shields.io/badge/DRF-3.14-092E20?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![Architecture](https://img.shields.io/badge/Architecture-Layered-FF6F00?style=for-the-badge)

## 1. Project Overview
A production-grade backend system designed to optimize vehicle maintenance schedules across various depots. The system models vehicle task assignments as a 0/1 Knapsack problem, ensuring maximum operational impact within strictly bounded mechanic hours.

## 2. Afformed Evaluation Context
This project serves as the submission for the Afformed Campus Hiring Backend Evaluation. It rigorously implements layered architecture, extensive global logging, algorithmic problem solving, and strict exception handling.

## 3. Architecture Overview
The application strictly adheres to Clean Architecture:
*   **Controllers (`views`)**: Thin layer handling HTTP and DRF routing.
*   **Services**: Core business logic bridging algorithms and data.
*   **Repositories**: External data access layer wrapping external API calls.
*   **Algorithms**: Mathematical engine (0/1 Knapsack DP, Top-K Heap).
*   **Logging Middleware**: Standalone asynchronous error-tracking package.

## 4. Folder Structure
```text
vehicle_maintenance_scheduler/
├── logging_middleware/    # Externalized decoupled logging package
├── core/                  # Django Settings and ASGI/WSGI
├── src/
│   ├── algorithms/        # DP Knapsack & Heaps
│   ├── config/            # Env loaders
│   ├── controllers/       # HTTP Request/Response handling
│   ├── handlers/          # DRF Exception Catchers
│   ├── middleware/        # Global Django Request/Exception middlewares
│   ├── models/            # Domain definitions
│   ├── repositories/      # External HTTP abstractions
│   ├── routes/            # Django path definitions
│   ├── serializers/       # Payload Validation
│   ├── services/          # Core Business Workflows
│   ├── tests/             # Pytest/Unittest suite
│   └── utils/             # HTTP Client, Response Formatting
├── manage.py
└── requirements.txt
```

## 5. Technology Stack
*   **Framework**: Python 3.11+, Django 4.2+, Django REST Framework
*   **Environment**: `python-dotenv`
*   **Network**: `requests`

## 6. Setup Instructions
### 7. Virtual Environment Setup
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 8. Dependency Installation
```bash
pip install -r requirements.txt
```

### 9. Environment Variables
Create a `.env` file at the project root:
```dotenv
BASE_URL=http://4.224.186.213/evaluation-service
EMAIL=
NAME=
ROLL_NO=
ACCESS_CODE=
GITHUB_USERNAME=

CLIENT_ID=
CLIENT_SECRET=
ACCESS_TOKEN=

DJANGO_SECRET_KEY=secure-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

### 10. Running the Project
```bash
python manage.py migrate
python manage.py runserver
```

## 11. API Documentation
All endpoints share the `/api/v1/` prefix.
*   `GET /api/v1/depots`: Fetch all depots.
*   `GET /api/v1/tasks`: Fetch all tasks.
*   `GET /api/v1/schedule/<depot_id>`: Run the optimizer for a depot.
*   `GET /api/v1/priority-notifications`: Retrieve the top-10 ranked notifications.

### Standardized Response Schema
**SUCCESS:**
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {}
}
```
**ERROR:**
```json
{
  "success": false,
  "message": "Validation failed",
  "errors": {"detail": "Error string"}
}
```

## 12. Logging Middleware Explanation
Built as a completely decoupled python package (`logging_middleware`).
*   **Non-Blocking**: Uses `threading.Thread(daemon=True)` to offload API calls.
*   **Strict Validation**: Enforces Allowed Stacks, Levels, and Packages before transmission.
*   **Exception Safe**: Employs deep try/except blocks to guarantee logging failures never crash the main thread.

## 13. Knapsack Optimization Explanation
The core requirement, maximizing task impact within constrained mechanic hours, is modeled identically to the `0/1 Knapsack Problem`.
*   **Complexity**: $O(n \times W)$ Time and Space via 2D array.
*   **Execution**: Iterates over all tasks, computing optimal sub-structures. A backtracking loop rebuilds the exact selected array of tasks.

## 14. Notification Priority Engine Explanation
*   **Problem**: Returning the top 10 notifications ranked by Priority (`Placement > Result > Event`) and Recency.
*   **Implementation**: A Min-Heap (via `heapq`) maintaining exactly $k=10$ elements.
*   **Complexity**: $O(n \log k)$. Considerably more scalable than $O(n \log n)$ full sorting for large datasets.

## 15. Middleware Architecture
Django `MiddlewareMixin` is used to capture data at the network boundary.
1.  **RequestLoggingMiddleware**: Traces `start_time` and emits success/warning/error logs to Afformed tracking the route and execution MS.
2.  **GlobalExceptionMiddleware**: Operates as the last line of defense, intercepting 500s and standardizing them into JSON.

## 16. Exception Handling Strategy
Custom DRF exception handlers trap `APIException`s at the view layer. Repositories throw custom `ExternalAPIException`. Unhandled Python crashes hit the Global Exception Middleware.

## 17. Scalability Considerations
*   Stateless architecture allows horizontal pod scaling.
*   Algorithm isolation prevents heavy math from blocking web threads.

## 18. Design Decisions
*   **Repository Pattern**: Abstracts external APIs away from business logic, making testing via mocks easy.
*   **Centralized Config**: `Environment` class ensures missing env vars fail gracefully on boot.

## 19. Future Improvements
*   Implement Redis for caching external depot data.
*   Migrate logging dispatch to Celery for absolute thread isolation.
*   Add PostgreSQL for persistent audit trails.

## 20. Testing Instructions
Navigate to the `vehicle_maintenance_scheduler` directory and run:
```bash
python manage.py test src.tests
```

## 21. Screenshots Section
*(Place your generated screenshots in `vehicle_maintenance_scheduler/screenshots/`)*

## 22. Postman Collection Usage
1.  Import the APIs.
2.  Test `GET /api/v1/schedule/1` and observe the `"selectedTasks"` array.
3.  Test `GET /api/v1/priority-notifications` to view dynamic heap sorts.

## 23. Performance Optimizations
*   Using $O(n \log k)$ Heap instead of standard array sorting.
*   Dropping zero-duration tasks from DP loops early to bypass iteration.

## 24. Retry & Timeout Strategy
`BaseHttpClient` uses **Exponential Backoff**:
*   Timeout is strictly capped to `5.0s`.
*   Fails sequentially, sleeping `backoff_factor ** attempt`.
*   Raises `ExternalAPIException` after maximum limits breached.

---

## Final Project Checklist
- [x] Environment variables securely loaded.
- [x] Middlewares validating schemas properly.
- [x] Repositories clean of business logic.
- [x] `requirements.txt` generated.
- [x] `.gitignore` deployed.

## Screenshot Checklist for Evaluator
- [ ] Registration API Success
- [ ] Auth Token Generation Body
- [ ] Logging API Hit via Request Logger
- [ ] Schedule API JSON Response ($W=60$)
- [ ] Priority Notifications (Sorted output)
- [ ] Console showing Afformed Background Logs executing safely.
