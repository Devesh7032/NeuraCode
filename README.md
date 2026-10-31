# NeuraCode — AI/ML Coding Platform

NeuraCode is an interactive, LeetCode-inspired coding laboratory designed specifically for AI/ML engineers. Users learn machine learning concepts by implementing them, executing calculations, inspecting outputs, and validating operations against structured test suites.

## 📁 Key Documentation

- [Project Specification (PROJECT_SPEC.md)](file:///c:/Users/Devesh/OneDrive/Pictures/certificates/AIML%20Leetcode/PROJECT_SPEC.md)
- [Architecture & Design Details (ARCHITECTURE.md)](file:///c:/Users/Devesh/OneDrive/Pictures/certificates/AIML%20Leetcode/ARCHITECTURE.md)

---

## 🚀 Setup & Execution

### Prerequisites
- Node.js (v20+ recommended)
- Python (3.11+ recommended)

### 1. Backend Setup & Run

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - **Windows PowerShell:**
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux:**
     ```bash
     source .venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   *Note: On first startup, the application automatically initializes the SQLite database (`neuracode.db`) and seeds standard coding challenges.*

### 2. Frontend Setup & Run

1. Open a new terminal and navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the Vite development server:
   ```bash
   npm run dev
   ```
4. Open your browser and navigate to: `http://localhost:5173`

### 3. Docker Sandbox Setup (Phase 3 Real Execution)

To enable real, secure Python code execution:
1. Ensure WSL2 is enabled on your Windows machine.
2. Start the Docker service inside the WSL Ubuntu distribution:
   ```powershell
   wsl -d Ubuntu -u root service docker start
   ```
3. Build the isolated execution container image:
   ```powershell
   wsl -d Ubuntu -u root docker build -t neuracode-executor "/mnt/c/Users/Devesh/OneDrive/Pictures/certificates/AIML Leetcode/backend/app/execution"
   ```
   *This builds a lightweight Python 3.11 sandbox containing NumPy, Pandas, Matplotlib, and Scikit-learn, run under an unprivileged `coder` user with no network access.*

---

## 🧪 Testing

### Running Backend Tests
Navigate to the `backend` directory with the virtual environment active and run:
```bash
python -m pytest
```

### Running Frontend Tests
Navigate to the `frontend` directory and run:
```bash
npm run test
```
This launches the Vitest suite in single-run mode and prints results.
