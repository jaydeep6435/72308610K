# FINAL VALIDATION & SUBMISSION PREPARATION GUIDE

This guide serves as your master checklist before submitting the Afformed Backend Evaluation. It guarantees your project is evaluator-ready, production-clean, and submission-safe.

---

## STEP 36 — VERIFY DJANGO PROJECT EXECUTION

**Startup Verification Checklist:**
- [ ] `python manage.py runserver` starts without `ImportError`. (Already verified: server is currently running locally).
- [ ] No warnings about unapplied migrations. If seen, run `python manage.py migrate`.
- [ ] `core/settings.py` correctly loads `.env` variables via `dotenv`.
- [ ] `rest_framework` is in `INSTALLED_APPS`.
- [ ] `RequestLoggingMiddleware` and `GlobalExceptionMiddleware` are registered at the bottom of `MIDDLEWARE`.

**Common Runtime Fixes:**
- *ModuleNotFoundError*: Ensure your virtual environment is activated (`.\venv\Scripts\activate`) before running the server.
- *Environment Variable Missing*: Verify `.env` is at `vehicle_maintenance_scheduler/.env` and `BASE_URL` is populated.

---

## STEP 37 — VERIFY ALL API ENDPOINTS

**Endpoint Verification Guide:**

1.  **GET /api/v1/depots**
    *   *Expected Status*: `200 OK`
    *   *Expected Output*: `{"success": true, "message": "Operation completed successfully", "data": [...]}`
2.  **GET /api/v1/tasks**
    *   *Expected Status*: `200 OK`
    *   *Expected Output*: Similar standard response with tasks list.
3.  **GET /api/v1/schedule/1**
    *   *Expected Status*: `200 OK` (if depot 1 exists) or `400 Bad Request` (if external API fails).
    *   *Expected Output*: `{"success": true, "data": {"depotId": 1, "availableHours": 60, "usedHours": 58, "totalImpact": 96, "selectedTasks": [...]}}`
4.  **GET /api/v1/priority-notifications**
    *   *Expected Status*: `200 OK`
    *   *Expected Output*: Top 10 notifications sorted by Priority (`Placement > Result > Event`) and Time.

**Edge-Case Tests to Try:**
- Hit `/api/v1/schedule/999` (Invalid ID). Ensure the Global Exception Middleware catches it or it returns a clean `400` JSON response, without crashing the server.

---

## STEP 38 — VERIFY LOGGING MIDDLEWARE INTEGRATION

**Logging Validation Checklist:**
Monitor your server console and ensure Afformed API logs are firing asynchronously:
- [ ] *Request Start/End*: `[info] middleware: Incoming request...` and `[debug] middleware: Request completed...`
- [ ] *Optimization Engine*: `[info] utils: Optimization algorithm started`
- [ ] *Repository Layer*: `[info] repository: Fetching depot data for ID 1`
- [ ] *Exceptions*: Force an error and verify `[fatal] middleware: Unhandled Server Exception`

**Expected Logging Payload Sent to Afformed:**
```json
{
  "stack": "backend",
  "level": "info",
  "package": "controller",
  "message": "Schedule generation request received for depot 1"
}
```

---

## STEP 39 — POSTMAN EXECUTION FLOW (FOR EVALUATOR)

Prepare your Postman collection in this exact sequence:

1.  **POST Registration API** (Afformed direct API) -> Returns credentials.
2.  **POST Auth API** (Afformed direct API) -> Returns `ACCESS_TOKEN`.
    *   *Action*: Set `ACCESS_TOKEN` as Bearer Token for the Collection.
3.  **POST Logging API (Manual Test)** -> Prove basic logging works.
4.  **GET Local Depots API** (`localhost:8000/api/v1/depots`).
5.  **GET Local Tasks API** (`localhost:8000/api/v1/tasks`).
6.  **GET Local Schedule API** (`localhost:8000/api/v1/schedule/1`).
    *   *Note*: Point out the algorithm's optimal task selection.
7.  **GET Local Priority Notifications** (`localhost:8000/api/v1/priority-notifications`).
    *   *Note*: Point out the Heap-sorted output.

---

## STEP 40 — SCREENSHOT EXECUTION PLAN

You must capture and save these in `vehicle_maintenance_scheduler/screenshots/`:

1.  `1_successful_registration.png`: Postman showing 200 OK from Afformed register.
2.  `2_auth_token_generation.png`: Postman showing JWT payload.
3.  `3_manual_logging_api.png`: Postman showing successful manual log push.
4.  `4_depots_api_response.png`: Local API showing standardized success JSON.
5.  `5_tasks_api_response.png`: Local API returning tasks.
6.  `6_schedule_optimization.png`: Critical. Must show `usedHours`, `totalImpact`, and the `selectedTasks` array.
7.  `7_priority_notifications.png`: Must show notifications clearly sorted (Placement first).
8.  `8_middleware_logging_terminal.png`: Screenshot of your IDE terminal showing the asynchronous logs being dispatched cleanly without breaking the flow.

---

## STEP 41 — VERIFY TEST SUITE

Run the test suite to ensure algorithmic and repository logic holds up:
```bash
cd vehicle_maintenance_scheduler
python manage.py test src.tests
```
**Expected Output:**
`Ran 4 tests in X.XXXs. OK`
This validates: Knapsack edge cases, DP output constraints, and Repository mock failures.

---

## STEP 42 — FINAL CODEBASE CLEANUP

- [ ] Remove all `print()` statements. Use `Log()` exclusively.
- [ ] Verify no secrets (`CLIENT_SECRET`, `ACCESS_TOKEN`) are hardcoded in `api_client.py`. They must be read via `get_env_variable`.
- [ ] Remove unused `import` statements if your IDE highlights them.
- [ ] Ensure `.gitignore` is in the root directory (already done) so `.env` and `__pycache__` are NOT pushed to GitHub.

---

## STEP 43 — AFFORMED RULES COMPLIANCE AUDIT

- **Logging**: Mandatory `Log(stack, level, package, message)` implemented? **YES**.
- **Architecture**: Modular layered structure (Controllers, Services, Repos)? **YES**.
- **Optimizer**: 0/1 Knapsack problem implemented dynamically? **YES**.
- **Priority Inbox**: $O(n \log k)$ Heap implementation used instead of `sort()`? **YES**.
- **Documentation**: `notification_system_design.md` covers SQL, scaling, queues? **YES**.

---

## STEP 44 — FINAL GIT WORKFLOW

Once everything above is verified, run these exact commands from `e:\72308610K\`:

```bash
# 1. Ensure you are at the repository root
cd e:\72308610K

# 2. Stage all polished files (including screenshots)
git add .

# 3. Commit the final production release
git commit -m "chore: final production polish, screenshots, and documentation"

# 4. Push to main branch
git push origin main
```

---

## STEP 45 — FINAL SUBMISSION CHECKLIST

### Repository
- [x] Correct folder structure `ROLLNUMBER/vehicle_maintenance_scheduler`.
- [x] `.env` is ignored by Git.

### Backend
- [ ] API Endpoints tested and returning `200 OK` locally.
- [ ] Terminal shows no unhandled Python exceptions during execution.
- [ ] Afformed Logging API is receiving your traces successfully.

### Documentation
- [x] `README.md` is formatted, professional, and contains setup guides.
- [x] `notification_system_design.md` answers all 6 theoretical stages.
- [ ] Screenshots populated in the `screenshots/` directory.

### Code Quality
- [x] Controllers are thin.
- [x] Global Exception handling wraps the entire architecture.
- [x] Magic strings avoided via `constants.py`.

**You are now fully prepared for submission. Excellent work.**
