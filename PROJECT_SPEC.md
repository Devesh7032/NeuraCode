# Project Specification: NeuraCode

NeuraCode is an interactive coding laboratory inspired by the "LeetCode" experience but tailored specifically for **AI/ML Engineers and Researchers**. It shifts the focus from generic algorithmic problems (e.g., dynamic programming, array rotations) to real-world machine learning implementations, mathematical functions, neural layers, and MLOps exercises.

## 1. Project Vision & Loop

The core user experience is structured around the following progression:
> **Concept → Code → Run → Execute → Visualize → Experiment → Submit**

Unlike generic text-only websites, users:
1. **Learn Concepts:** Read core mathematical breakdowns of algorithms (e.g., Backpropagation, Attention weights, Convolution steps).
2. **Implement in Code:** Write complete mathematical operations in standard Python (optionally PyTorch/NumPy).
3. **Execute:** Run the code in isolated Docker environments (Phase 3) that capture stdout, stderr, run metrics, and intermediate variable values.
4. **Visualize Results:** Inspect output plots (e.g., loss curves, weight histograms, decision boundaries) dynamically plotted from their actual matrix calculations.
5. **Experiment:** Change hyperparameters in real-time to observe changes in the training cycle.
6. **Submit:** Validate against comprehensive private test suites to complete challenges and earn badges.

---

## 2. Technology Stack

- **Frontend:**
  - React (v19) + Vite + TypeScript (v6)
  - Tailwind CSS (Utility styles)
  - Lucide Icons (Icon assets)
  - React Router DOM (v7) (Single Page App routing)
  - TanStack Query (v5) (Server state management)
  - Monaco Editor (vs-dark theme code editor)
- **Backend:**
  - Python (v3.13)
  - FastAPI (REST APIs, routing, and Swagger documentation)
  - SQLAlchemy (ORM)
  - PostgreSQL (Production database) / SQLite (Local-first fallback)
  - pytest (Backend testing framework)
  - Vitest + jsdom (Frontend testing framework)

---

## 3. Architecture Overview

```text
  ┌─────────────────────────────────────────────────────────────┐
  │                        React Frontend                       │
  │     (Monaco Editor, Visualizations, Dashboards, Router)      │
  └──────────────────────────────┬──────────────────────────────┘
                                 │ HTTP / JSON
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                        FastAPI Server                       │
  │     (Authentication, Challenge Services, User Progress)     │
  └──────────────┬──────────────────────────────┬───────────────┘
                 │ SQLAlchemy                   │ Task Queue (Phase 3)
                 ▼                              ▼
  ┌─────────────────────────────┐        ┌──────────────────────┐
  │      Relational DB          │        │   Execution Queue    │
  │ (PostgreSQL/SQLite schemas) │        │ (Celery / Redis / WS)│
  └─────────────────────────────┘        └──────────┬───────────┘
                                                    │
                                                    ▼
                                         ┌──────────────────────┐
                                         │   Isolated Workers   │
                                         │   (Docker Sandbox)   │
                                         └──────────────────────┘
```

---

## 4. Phase 1 - Foundation & Shell Scope

The scope of Phase 1 is strictly dedicated to establishing the technically robust foundation and the interactive web shell without running user code:
- **Modular Backend:** Structuring database schemas with complete entities (User, Profile, Challenge, Test, Hint, Submission, Result, Progress, Paths, Streaks, Badges, UserBadge) using UUIDs, constraints, and relationships.
- **Authed APIs:** Setting up registration, login, session cookies, and authentication middleware.
- **Problems Registry:** Seeding challenges directly from relational records.
- **Monaco Workspace Shell:** Building the twin-panel challenge workspace with Monaco Editor loading template code.
- **Client Routers:** Mapping `/dashboard`, `/problems`, `/problems/:slug`, `/learn`, `/leaderboard`, and `/profile`.

---

## 5. Non-Negotiable Requirements

1. **No Arbitrary Execution in Server Process:** Arbitrary user code must NEVER run directly inside the FastAPI API process. An isolated sandbox is required for future phases.
2. **Original Branding:** No mentions of LeetCode, trademarks, or copies of its logo. Brand configuration must be centralized in `brand.ts` for quick changes.
3. **Database Relational Integrity:** High-fidelity DB schema utilizing foreign keys, cascading deletes, index optimization, and timezone-aware default timestamps. No dumping of relational statistics into single JSON blobs.

---

## 6. Phase 3 - Real Python Execution & Secure Sandbox

In Phase 3, we replace mock execution with a secure, isolated sandbox engine:
- **Sandbox Isolation:** Running code inside a dedicated Docker container (`neuracode-executor`) built from a `python:3.11-slim` base containing NumPy, Pandas, Matplotlib, and Scikit-learn.
- **Strict Resources & Safety Constraints:**
  - Network: Disabled (`--network none`).
  - CPU: Limited to 1.0 core.
  - Memory: Limited to 256 MB.
  - Timeout: 5 seconds (enforced via Linux `timeout` utility inside WSL).
  - Writeability: Temp read-write filesystem (`--tmpfs /tmp:rw,size=16m,mode=1777`), unprivileged user (`coder` / UID 1000).
- **Execution Harness (`harness.py`):** Orchestrates dynamic imports of solutions, parses string input variables securely via `ast.literal_eval`, compares float outputs recursively within `1e-4` precision, and serializes array results.
- **Traceback Sanitization:** Parses container logs and filters out full local host paths, replacing them with clean relative imports.
- **Rate Limiting:** Protects resources by preventing users from scheduling more than 2 concurrent runs simultaneously.

---

## 7. Phase 6 - Interactive AI/ML Visualization Engine

We introduced a real data-driven visualization engine to explain algorithm executions to users.
- **Trace Execution Pipeline:** Captured intermediate calculation traces (loss convergence lists, cluster assignments, attention heatmaps) inside secure sandboxes and returned them to frontend.
- **Trace Size Limits:** Enforces standard constraints (`MAX_TRACE_STEPS` = 500, `MAX_TRACE_SIZE` = 1 MB) to prevent browser buffer crashes.
- **Interactive controls:** play/pause, step next/prev, reset, parameter sliders (z-parameter, vector components, learning rates) recalculate outputs live using user-written logic.

