import uuid
import pytest
from app.execution.harness import (
    ExactEvaluator,
    FloatToleranceEvaluator,
    ArrayToleranceEvaluator,
    ShapeEvaluator,
    MetricEvaluator
)
from app.models.user import User
from app.models.challenge import Challenge, ChallengeTest, ChallengeHint
from app.models.submission import Submission
from tests.test_execution import get_auth_headers, seed_test_challenge_if_missing

def seed_sigmoid_challenge_if_missing(db):
    challenge = db.query(Challenge).filter(Challenge.slug == "sigmoid-activation").first()
    if challenge:
        return challenge
        
    challenge = Challenge(
        title="Sigmoid Activation Function",
        slug="sigmoid-activation",
        difficulty="Easy",
        category="Mathematics",
        description="...",
        starter_code="import math\ndef sigmoid(z): pass",
        constraints="None",
        status="active"
    )
    db.add(challenge)
    db.commit()
    db.refresh(challenge)
    
    t1 = ChallengeTest(
        challenge_id=challenge.id,
        input_data="0.0",
        expected_output="0.5",
        visibility="PUBLIC",
        evaluation_type="FLOAT_TOLERANCE",
        tolerance=1e-5
    )
    t2 = ChallengeTest(
        challenge_id=challenge.id,
        input_data="2.0",
        expected_output="0.880797",
        visibility="PUBLIC",
        evaluation_type="FLOAT_TOLERANCE",
        tolerance=1e-5
    )
    t3 = ChallengeTest(
        challenge_id=challenge.id,
        input_data="-2.0",
        expected_output="0.1192029",
        visibility="HIDDEN",
        evaluation_type="FLOAT_TOLERANCE",
        tolerance=1e-5
    )
    db.add(t1)
    db.add(t2)
    db.add(t3)
    db.commit()
    return challenge

# ==================== EVALUATOR TESTS ====================

def test_exact_evaluator():
    evaluator = ExactEvaluator()
    passed, _ = evaluator.evaluate("test", "test")
    assert passed is True
    passed, info = evaluator.evaluate(123, 456)
    assert passed is False
    assert "Expected" in info

def test_float_tolerance_evaluator():
    evaluator = FloatToleranceEvaluator()
    passed, _ = evaluator.evaluate(0.880797, 0.88079, tolerance=1e-4)
    assert passed is True
    passed, info = evaluator.evaluate(0.880797, 0.89, tolerance=1e-4)
    assert passed is False
    passed, _ = evaluator.evaluate(float("inf"), float("inf"))
    assert passed is True
    passed, _ = evaluator.evaluate(float("nan"), float("nan"))
    assert passed is True
    passed, _ = evaluator.evaluate(0.5, float("nan"))
    assert passed is False

def test_array_tolerance_evaluator():
    evaluator = ArrayToleranceEvaluator()
    passed, _ = evaluator.evaluate([0.6, 0.8], [0.6, 0.8], tolerance=1e-5)
    assert passed is True
    passed, info = evaluator.evaluate([0.6, 0.8], [0.6, 0.8, 1.0], tolerance=1e-5)
    assert passed is False
    assert "Expected shape" in info or "Expected" in info

def test_shape_evaluator():
    evaluator = ShapeEvaluator()
    passed, _ = evaluator.evaluate([[1, 2], [3, 4]], [2, 2])
    assert passed is True
    passed, info = evaluator.evaluate([[1, 2], [3, 4]], [3, 2])
    assert passed is False
    assert "Expected shape" in info

def test_metric_evaluator():
    evaluator = MetricEvaluator()
    passed, _ = evaluator.evaluate(0.95, 0.90, comparison="GTE")
    assert passed is True
    passed, info = evaluator.evaluate(0.85, 0.90, comparison="GTE")
    assert passed is False
    assert "too low" in info

# ==================== API & SUBMISSIONS TESTS ====================

def test_auth_requirement_for_submissions(client):
    response = client.post("/api/submissions?challenge_slug=sigmoid-activation", json={
        "code": "def sigmoid(z): pass",
        "language": "python"
    })
    assert response.status_code == 401

def test_invalid_challenge_slug_submission(client, db):
    headers = get_auth_headers(client, "subslug@neuracode.com")
    response = client.post("/api/submissions?challenge_slug=missing-slug", headers=headers, json={
        "code": "def test(): pass",
        "language": "python"
    })
    assert response.status_code == 404

def test_oversized_code_submission(client, db):
    headers = get_auth_headers(client, "subsize@neuracode.com")
    seed_test_challenge_if_missing(db, "matrix-multiplication")
    huge_code = "def matrix_multiply(A, B):\n" + "    pass\n" * 20000
    response = client.post("/api/submissions?challenge_slug=matrix-multiplication", headers=headers, json={
        "code": huge_code,
        "language": "python"
    })
    assert response.status_code == 400
    assert "exceeds limit" in response.json()["detail"]

def test_accepted_submission_sigmoid(client, db):
    headers = get_auth_headers(client, "subacc@neuracode.com")
    seed_sigmoid_challenge_if_missing(db)

    code = (
        "import math\n"
        "def sigmoid(z):\n"
        "    return 1.0 / (1.0 + math.exp(-z))\n"
    )

    response = client.post("/api/submissions?challenge_slug=sigmoid-activation", headers=headers, json={
        "code": code,
        "language": "python"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ACCEPTED"
    assert data["passed_tests"] == data["total_tests"]
    assert data["score"] == 1.0
    assert data["runtime_ms"] > 0
    assert len(data["results"]) > 0

def test_wrong_answer_submission_sigmoid(client, db):
    headers = get_auth_headers(client, "subwa@neuracode.com")
    seed_sigmoid_challenge_if_missing(db)
    
    code = (
        "def sigmoid(z):\n"
        "    return z\n"
    )

    response = client.post("/api/submissions?challenge_slug=sigmoid-activation", headers=headers, json={
        "code": code,
        "language": "python"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "WRONG_ANSWER"
    assert data["score"] < 1.0

def test_runtime_error_submission_sigmoid(client, db):
    headers = get_auth_headers(client, "subre@neuracode.com")
    seed_sigmoid_challenge_if_missing(db)
    
    code = (
        "def sigmoid(z):\n"
        "    raise ValueError('Custom crash')\n"
    )

    response = client.post("/api/submissions?challenge_slug=sigmoid-activation", headers=headers, json={
        "code": code,
        "language": "python"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "RUNTIME_ERROR"

def test_timeout_submission_sigmoid(client, db):
    headers = get_auth_headers(client, "subtimeout@neuracode.com")
    seed_sigmoid_challenge_if_missing(db)
    
    code = (
        "import time\n"
        "def sigmoid(z):\n"
        "    while True:\n"
        "        time.sleep(0.1)\n"
    )

    response = client.post("/api/submissions?challenge_slug=sigmoid-activation", headers=headers, json={
        "code": code,
        "language": "python"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "TIME_LIMIT_EXCEEDED"
    
    # Settle down container
    import time
    time.sleep(2)

def test_submissions_history_listing_and_ownership(client, db):
    headers = get_auth_headers(client, "subowner@neuracode.com")
    seed_sigmoid_challenge_if_missing(db)
    
    code = "def sigmoid(z):\n    return 1.0 / (1.0 + 2.71828**-z)"
    response = client.post("/api/submissions?challenge_slug=sigmoid-activation", headers=headers, json={
        "code": code,
        "language": "python"
    })
    sub_id = response.json()["id"]

    # Retrieve history list
    list_res = client.get("/api/submissions?challenge_slug=sigmoid-activation", headers=headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) > 0
    assert list_res.json()[0]["id"] == sub_id

    # Retrieve single detail
    get_res = client.get(f"/api/submissions/{sub_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["id"] == sub_id

    # Try retrieving from user 2
    headers2 = get_auth_headers(client, "subowner2@neuracode.com")
    get_res2 = client.get(f"/api/submissions/{sub_id}", headers=headers2)
    assert get_res2.status_code in [403, 404]
