# Architecture Documentation: NeuraCode

This document provides a technical overview of **NeuraCode**, covering folder structures, core database schemas, security models, testing routines, and design considerations for the future execution engine.

---

## 1. Directory Structure

```text
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI App & lifespan initialization
│   │   ├── core/              # Global configs, DB settings, security
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── api/               # API Router endpoints
│   │   │   ├── auth.py
│   │   │   ├── challenges.py
│   │   │   ├── executions.py
│   │   │   └── ...
│   │   ├── execution/         # Docker Sandboxing & Telemetry
│   │   │   ├── Dockerfile
│   │   │   ├── harness.py
│   │   │   └── executor.py
│   │   ├── models/            # SQLAlchemy 2.0 relational models
│   │   │   ├── user.py
│   │   │   ├── challenge.py
│   │   │   ├── execution.py
│   │   │   ├── submission.py
│   │   │   └── progress.py
│   │   ├── schemas/           # Pydantic schemas (Request/Response)
│   │   │   ├── user.py
│   │   │   ├── challenge.py
│   │   │   ├── execution.py
│   │   │   └── submission.py
│   │   └── seed.py            # DB seeding script (invoked on lifespan startup)
│   └── tests/                 # pytest suite (conftest.py + API tests)
└── frontend/
    ├── src/
    │   ├── config/            # Central branding settings (brand.ts)
    │   ├── context/           # AuthContext (React auth provider)
    │   ├── components/        # Layout & global components
    │   ├── pages/             # Page components (/dashboard, /problems, etc.)
    │   ├── App.tsx            # Routes configurations
    │   ├── main.tsx           # React mounting & css injection
    │   └── style.css          # Tailwind imports & variables
    └── package.json           # Frontend packages & vitest config
```

---

## 2. Database Schema

The database model is designed as a relational system with clean normalization constraints:

### User & Profile Component
- `User`: Handles identity credentials (`email`, `hashed_password`). Has a one-to-one relationship with `Profile` and `UserStreak`, and one-to-many relationships with `UserBadge`, `Submission`, and `UserProgress`.
- `Profile`: Holds profile data (`display_name`, `avatar_url`, `bio`, `xp`).
- `UserStreak`: Tracks logins (`current_streak`, `longest_streak`, `last_active` timestamp).
- `Badge` & `UserBadge`: Many-to-many mapping storing achievements.

### Challenge & Learning Component
- `Challenge`: Stores content, starter templates, difficulty, and metadata.
- `ChallengeTest`: Holds tests mapping input to output, flagging public vs. hidden assertions.
- `ChallengeHint`: Holds tips for users, sorted by `order_index`.
- `LearningPath` & `LearningPathItem`: Standard linear curricula pointing to specific challenges.
- `UserProgress`: Tracks completion records of challenges by users.

### Code Submission Component
- `Submission`: Records code text and status (`Pending`, `Running`, `Passed`, `Failed`, `Error`).
- `SubmissionResult`: Collects stdout, stderr, execution times, memory usage, and assertion summaries.

---

## 3. Security Design

1. **Password Hashing:** Directly uses the standard `bcrypt` library (using `bcrypt.gensalt()` and `bcrypt.hashpw()`), escaping the compatibility bugs of `passlib` on newer Python runtimes.
2. **Access Tokens:** Session handling uses standard JSON Web Tokens (JWT) signed with `HS256` using a secret key.
3. **Double Token Protection:** Frontend credentials can be passed as standard HTTP Bearer headers (SPA friendly) or extracted from cookies (`access_token`), creating compatibility for both mobile clients and desktop browsers.
4. **Data Isolation:** All submission fetching routes enforce authorization checks so only the author of the code (or a superuser admin) can access its contents.

---

## 4. Future Sandbox Architecture

The design for code evaluation in Phase 3 strictly segregates arbitrary code execution from the main API process:

```text
  User submits code 
       │
       ▼
  [FastAPI Server] ────► [Creates Submission in DB (status: Pending)]
       │
       ▼
  [Celery Task Queue] ────► [Pushed to execution worker]
                                  │
                                  ▼
                        [Spawns Docker Container]
                        (No network access, memory/CPU caps)
                                  │
                                  ▼
                        [Runs TestRunner script]
                        (Executes code against ChallengeTests)
                                  │
                                  ▼
                        [Results returned to Worker]
                                  │
                                  ▼
  [FastAPI WS/Poll] ◄──── [Updates DB Submission status & result]
```

This prevents malicious script submissions (e.g., infinite loops, filesystem access, database tampering) from affecting the API server or database.

---

## 5. Verification Configurations

- **Backend tests:** Run `python -m pytest` inside `/backend` which sets up an in-memory SQLite database instance on the fly, seeds it, and evaluates route operations.
- **Frontend tests:** Run `npm run test` inside `/frontend` to verify branding configuration values using Vitest and JSDOM.

---

## 6. Security Model & Sandbox Limits

User-submitted code is inherently untrusted. NeuraCode guarantees host environment safety using a layered sandbox security model:

1. **Process Isolation:** The FastAPI server never runs or evaluates (`eval`/`exec`) code inside its own process. Code runs inside standard, temporary Docker containers (`neuracode-executor`).
2. **Network Isolation:** Sandbox containers are executed with `--network none` disabled. They cannot connect to external services, scrape internet resources, or connect to internal application databases.
3. **Resource Caps (cgroups):** Enforces strict limits:
   - Memory: `256 MB`
   - CPU: `1.0` cores
   - PIDS: `100` maximum concurrent threads
   - Filesystem: Writes are confined to `/tmp` via a small `--tmpfs /tmp:rw,size=16m,mode=1777` mount, with the rest of the image filesystem locked as read-only.
4. **Teardown & Cleanup:** Every execution folder created on the host is deleted immediately upon termination, and docker containers are forcefully destroyed.
5. **Execution Timeout:** Enforces a strict 5-second timeout inside the Linux WSL kernel via the `timeout` command. Runaway threads or infinite loops (`while True: pass`) are killed immediately.

---

## 7. Visualization System Architecture

We separate execution, evaluation, and visual tracing subsystems:
1. **Schema Exponentiation:** Challenge model defines `visualization_type` and `visualization_config`.
2. **Sandbox Instrumentation:** `harness.py` dynamically runs tracing loops on math operations and logs them to sandbox standard output.
3. **Execution Routing:** FastAPI intercepts visual traces in the stdout parser, storing them in SQL execution rows.
4. **Interactive SVG Renderers:** Custom SVG/Canvas charts and slider hooks map parameters and calculate output graphs.

