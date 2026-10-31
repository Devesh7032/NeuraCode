import uuid
import json
import pytest
from app.models.user import User
from app.models.challenge import Challenge, ChallengeTest
from app.models.execution import Execution

def get_auth_headers(client, email="execuser@neuracode.com"):
    reg_data = {"email": email, "password": "password123"}
    client.post("/api/auth/register", json=reg_data)
    login_res = client.post("/api/auth/login", json=reg_data)
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def seed_test_challenge_if_missing(db, slug):
    challenge = db.query(Challenge).filter(Challenge.slug == slug).first()
    if challenge:
        return
        
    if slug == "matrix-multiplication":
        challenge = Challenge(
            title="Matrix Multiplication",
            slug="matrix-multiplication",
            difficulty="Easy",
            category="Mathematics",
            description="Multiply two 2D matrices A and B using NumPy.",
            starter_code="import numpy as np\ndef matrix_multiply(A, B):\n    pass\n",
            constraints="None",
            status="active"
        )
        db.add(challenge)
        db.commit()
        db.refresh(challenge)
        
        t1 = ChallengeTest(
            challenge_id=challenge.id,
            input_data="[[1, 2], [3, 4]] | [[5, 6], [7, 8]]",
            expected_output="[[19, 22], [43, 50]]",
            is_public=True
        )
        t2 = ChallengeTest(
            challenge_id=challenge.id,
            input_data="[[1, 2]] | [[3], [4]]",
            expected_output="[[11]]",
            is_public=True
        )
        db.add(t1)
        db.add(t2)
        db.commit()
        
    elif slug == "linear-regression-prediction":
        challenge = Challenge(
            title="Linear Regression Prediction",
            slug="linear-regression-prediction",
            difficulty="Easy",
            category="Machine Learning",
            description="Perform linear regression prediction.",
            starter_code="import numpy as np\ndef predict(X, weights, bias):\n    pass\n",
            constraints="None",
            status="active"
        )
        db.add(challenge)
        db.commit()
        db.refresh(challenge)
        
        t1 = ChallengeTest(
            challenge_id=challenge.id,
            input_data="[[1, 2], [3, 4]] | [0.5, -0.5] | 1.0",
            expected_output="[0.5, 0.5]",
            is_public=True
        )
        t2 = ChallengeTest(
            challenge_id=challenge.id,
            input_data="[[0, 0], [1, 1]] | [2.0, 3.0] | -1.0",
            expected_output="[-1.0, 4.0]",
            is_public=True
        )
        db.add(t1)
        db.add(t2)
        db.commit()

    elif slug == "single-step-gradient-descent":
        challenge = Challenge(
            title="Gradient Descent Step",
            slug="single-step-gradient-descent",
            difficulty="Easy",
            category="Machine Learning",
            description="Perform a single gradient descent update step.",
            starter_code="def gradient_update(w: float, dw: float, learning_rate: float) -> float:\n    pass\n",
            constraints="None",
            visualization_type="GRADIENT_DESCENT",
            visualization_config='{"learning_rate_default": 0.1, "iterations_default": 20}',
            status="active"
        )
        db.add(challenge)
        db.commit()
        db.refresh(challenge)
        
        t1 = ChallengeTest(
            challenge_id=challenge.id,
            input_data="0.0 | -4.0 | 0.1",
            expected_output="0.4",
            is_public=True
        )
        db.add(t1)
        db.commit()

def test_auth_requirement_for_execution(client):
    # Unauthenticated executions call
    response = client.post("/api/executions", json={
        "challenge_slug": "matrix-multiplication",
        "code": "def matrix_multiply(A, B): pass",
        "language": "python"
    })
    assert response.status_code == 401

def test_invalid_challenge_slug(client, db):
    headers = get_auth_headers(client, "sluguser@neuracode.com")
    response = client.post("/api/executions", headers=headers, json={
        "challenge_slug": "missing-slug-name",
        "code": "def test(): pass",
        "language": "python"
    })
    assert response.status_code == 404

def test_code_size_exceeded(client, db):
    headers = get_auth_headers(client, "sizeuser@neuracode.com")
    seed_test_challenge_if_missing(db, "matrix-multiplication")
    # Extremely long code
    huge_code = "def matrix_multiply(A, B):\n" + "    pass\n" * 20000
    response = client.post("/api/executions", headers=headers, json={
        "challenge_slug": "matrix-multiplication",
        "code": huge_code,
        "language": "python"
    })
    assert response.status_code == 400
    assert "exceeds limit" in response.json()["detail"]

def test_valid_execution_matrix_multiply(client, db):
    headers = get_auth_headers(client, "validuser@neuracode.com")
    seed_test_challenge_if_missing(db, "matrix-multiplication")
    code = (
        "import numpy as np\n"
        "def matrix_multiply(A, B):\n"
        "    return np.matmul(A, B).tolist()\n"
    )

    response = client.post("/api/executions", headers=headers, json={
        "challenge_slug": "matrix-multiplication",
        "code": code,
        "language": "python"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "COMPLETED"
    assert len(data["tests"]) > 0
    assert data["tests"][0]["status"] == "passed"
    assert data["runtime_ms"] > 0
    assert data["exit_code"] == 0

def test_numpy_linear_regression(client, db):
    headers = get_auth_headers(client, "lruser@neuracode.com")
    seed_test_challenge_if_missing(db, "linear-regression-prediction")
    code = (
        "import numpy as np\n"
        "def predict(X, weights, bias):\n"
        "    return (np.array(X) @ np.array(weights) + bias).tolist()\n"
    )

    response = client.post("/api/executions", headers=headers, json={
        "challenge_slug": "linear-regression-prediction",
        "code": code,
        "language": "python"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "COMPLETED"
    assert data["tests"][0]["status"] == "passed"

def test_invalid_python_code_syntax_error(client, db):
    headers = get_auth_headers(client, "syntaxuser@neuracode.com")
    seed_test_challenge_if_missing(db, "matrix-multiplication")
    code = "def matrix_multiply(A, B):\n    return np.matmul(A, B) invalid syntax here"

    response = client.post("/api/executions", headers=headers, json={
        "challenge_slug": "matrix-multiplication",
        "code": code,
        "language": "python"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "FAILED"
    assert "SyntaxError" in data["stderr"] or "SyntaxError" in data["error_type"]

def test_runtime_error_execution(client, db):
    headers = get_auth_headers(client, "runuser@neuracode.com")
    seed_test_challenge_if_missing(db, "matrix-multiplication")
    code = (
        "def matrix_multiply(A, B):\n"
        "    raise ValueError('Custom Execution Error')\n"
    )

    response = client.post("/api/executions", headers=headers, json={
        "challenge_slug": "matrix-multiplication",
        "code": code,
        "language": "python"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "COMPLETED" or data["status"] == "FAILED"
    assert data["tests"][0]["status"] == "error"
    assert "ValueError: Custom Execution Error" in data["tests"][0]["error"]

def test_execution_timeout(client, db):
    headers = get_auth_headers(client, "timeuser@neuracode.com")
    seed_test_challenge_if_missing(db, "matrix-multiplication")
    code = (
        "import time\n"
        "def matrix_multiply(A, B):\n"
        "    while True:\n"
        "        time.sleep(0.1)\n"
    )

    response = client.post("/api/executions", headers=headers, json={
        "challenge_slug": "matrix-multiplication",
        "code": code,
        "language": "python"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "TIMEOUT"
    assert "timed out" in data["stderr"].lower()
    
    # Allow Docker and WSL 2 seconds to settle teardown
    import time
    time.sleep(2)

def test_output_limit_exceeded(client, db):
    headers = get_auth_headers(client, "limituser@neuracode.com")
    seed_test_challenge_if_missing(db, "matrix-multiplication")
    code = (
        "def matrix_multiply(A, B):\n"
        "    for _ in range(10000):\n"
        "        print('A' * 100)\n"
        "    return [[19, 22], [43, 50]]\n"
    )

    response = client.post("/api/executions", headers=headers, json={
        "challenge_slug": "matrix-multiplication",
        "code": code,
        "language": "python"
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["stdout"]) <= 70000

def test_rate_limiting_concurrent_runs(client, db):
    headers = get_auth_headers(client, "rateuser@neuracode.com")
    seed_test_challenge_if_missing(db, "matrix-multiplication")
    user = db.query(User).filter(User.email == "rateuser@neuracode.com").first()
    challenge = db.query(Challenge).filter(Challenge.slug == "matrix-multiplication").first()

    # Clear existing executions for user
    db.query(Execution).filter(Execution.user_id == user.id).delete()
    db.commit()

    # Add 2 active running executions
    for _ in range(2):
        execution = Execution(
            user_id=user.id,
            challenge_id=challenge.id,
            status="RUNNING",
            code="def test(): pass"
        )
        db.add(execution)
    db.commit()

    # Attempt third execution - should get 429
    response = client.post("/api/executions", headers=headers, json={
        "challenge_slug": "matrix-multiplication",
        "code": "def matrix_multiply(A, B): pass",
        "language": "python"
    })
    assert response.status_code == 429
    assert "Too many executions" in response.json()["detail"]

    # Clean up
    db.query(Execution).filter(Execution.user_id == user.id).delete()
    db.commit()

def test_execution_status_retrieval_and_ownership(client, db):
    headers = get_auth_headers(client, "owneruser@neuracode.com")
    seed_test_challenge_if_missing(db, "matrix-multiplication")
    # Make a run
    code = "def matrix_multiply(A, B):\n    return [[19, 22], [43, 50]]"
    response = client.post("/api/executions", headers=headers, json={
        "challenge_slug": "matrix-multiplication",
        "code": code,
        "language": "python"
    })
    exec_id = response.json()["id"]

    # Get status by ID
    get_res = client.get(f"/api/executions/{exec_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["id"] == exec_id

    # Try fetching as another user
    headers2 = get_auth_headers(client, "owneruser2@neuracode.com")
    get_res2 = client.get(f"/api/executions/{exec_id}", headers=headers2)
    assert get_res2.status_code == 404

def test_execution_visualization_generation(client, db):
    headers = get_auth_headers(client, "visuser@neuracode.com")
    
    # Seed Sigmoid challenge for testing
    challenge = db.query(Challenge).filter(Challenge.slug == "sigmoid-activation").first()
    if not challenge:
        challenge = Challenge(
            title="Sigmoid Activation Function",
            slug="sigmoid-activation",
            difficulty="Easy",
            category="Machine Learning",
            description="Implement the sigmoid function.",
            starter_code="import math\ndef sigmoid(z: float) -> float:\n    pass\n",
            constraints="None",
            visualization_type="FUNCTION",
            visualization_config='{"x_min": -10, "x_max": 10}',
            status="active"
        )
        db.add(challenge)
        db.commit()
        db.refresh(challenge)
        
        t1 = ChallengeTest(
            challenge_id=challenge.id,
            input_data="0.0",
            expected_output="0.5",
            is_public=True
        )
        db.add(t1)
        db.commit()
        
    code = (
        "import math\n"
        "def sigmoid(z: float) -> float:\n"
        "    return 1.0 / (1.0 + math.exp(-z))\n"
    )
    
    response = client.post("/api/executions", headers=headers, json={
        "challenge_slug": "sigmoid-activation",
        "code": code,
        "language": "python",
        "custom_inputs": {"z": 2.0}
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "COMPLETED"
    
    # Check that visualization trace exists and is correct
    assert data["visualization"] is not None
    vis = data["visualization"]
    assert vis["type"] == "FUNCTION"
    assert vis["custom_x"] == 2.0
    assert abs(vis["custom_y"] - 0.880797) < 1e-4
    assert len(vis["x"]) > 0
    assert len(vis["y"]) > 0

def test_gradient_descent_visualization(client, db):
    headers = get_auth_headers(client, "gdvisuser@neuracode.com")
    seed_test_challenge_if_missing(db, "single-step-gradient-descent")
    
    # 1. Verify get_challenge returns visualization_type and visualization_config
    res = client.get("/api/challenges/single-step-gradient-descent")
    assert res.status_code == 200
    ch_data = res.json()
    assert ch_data["visualization_type"] == "GRADIENT_DESCENT"
    assert ch_data["visualization_config"] is not None

    # 2. Verify execution returns real trace data with w_new and steps
    code = "def gradient_update(w, dw, learning_rate):\n    return w - learning_rate * dw\n"
    response = client.post("/api/executions", headers=headers, json={
        "challenge_slug": "single-step-gradient-descent",
        "code": code,
        "language": "python",
        "custom_inputs": {"learning_rate": 0.1, "iterations": 10}
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "COMPLETED"
    assert data["visualization"] is not None
    vis = data["visualization"]
    assert vis["type"] == "GRADIENT_DESCENT"
    assert vis["learning_rate"] == 0.1
    assert len(vis["steps"]) == 10
    step0 = vis["steps"][0]
    assert "weight" in step0
    assert "derivative" in step0
    assert "w_new" in step0
    assert abs(step0["w_new"] - (step0["weight"] - 0.1 * step0["derivative"])) < 1e-4

