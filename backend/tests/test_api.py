import pytest
from app.models.challenge import Challenge, ChallengeTest

def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["project"] == "NeuraCode"

def test_user_registration_and_login(client):
    # 1. Register new user
    reg_data = {"email": "test@neuracode.com", "password": "securepassword123"}
    response = client.post("/api/auth/register", json=reg_data)
    assert response.status_code == 200
    assert response.json()["email"] == "test@neuracode.com"
    assert "id" in response.json()
    assert response.json()["profile"]["display_name"] == "test"

    # 2. Prevent duplicate registration
    response = client.post("/api/auth/register", json=reg_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

    # 3. Login (sets cookie and returns token)
    login_data = {"email": "test@neuracode.com", "password": "securepassword123"}
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    token = response.json()["access_token"]

    # 4. Get current user profile (authenticated with header)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test@neuracode.com"
    assert response.json()["streak"]["current_streak"] == 1

    # 5. Clear cookies to simulate unauthenticated client
    client.cookies.clear()

    # 6. Get current user profile (unauthenticated)
    response = client.get("/api/auth/me")
    assert response.status_code == 401

def test_challenges_flow(client, db):
    # Seed a challenge manually in the test database
    challenge = Challenge(
        title="Sigmoid Activation Function",
        slug="sigmoid-activation",
        difficulty="Easy",
        category="Mathematics",
        description="Implement sigmoid.",
        starter_code="def sigmoid(z): pass",
        constraints="None",
        status="active"
    )
    db.add(challenge)
    db.commit()

    # 1. Fetch active challenges
    response = client.get("/api/challenges")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["slug"] == "sigmoid-activation"

    # 2. Filter challenges by category
    response = client.get("/api/challenges", params={"category": "Mathematics"})
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get("/api/challenges", params={"category": "Deep Learning"})
    assert response.status_code == 200
    assert len(response.json()) == 0

    # 3. Fetch specific challenge by slug
    response = client.get("/api/challenges/sigmoid-activation")
    assert response.status_code == 200
    assert response.json()["title"] == "Sigmoid Activation Function"
    assert response.json()["starter_code"] == "def sigmoid(z): pass"

    # 4. Fetch non-existent challenge
    response = client.get("/api/challenges/non-existent")
    assert response.status_code == 404

def test_code_execution_and_submission(client, db):
    # Register and login first to get token
    reg_data = {"email": "coder@neuracode.com", "password": "password123"}
    client.post("/api/auth/register", json=reg_data)
    login_res = client.post("/api/auth/login", json=reg_data)
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Seed challenge
    challenge = Challenge(
        title="Mean Squared Error",
        slug="mean-squared-error",
        difficulty="Easy",
        category="Machine Learning",
        description="Compute MSE.",
        starter_code="def mse(y, y_hat): pass",
        constraints="None",
        status="active"
    )
    db.add(challenge)
    db.commit()
    db.refresh(challenge)
    
    t1 = ChallengeTest(
        challenge_id=challenge.id,
        input_data="[1, 2] | [1, 2]",
        expected_output="0.0",
        visibility="PUBLIC"
    )
    db.add(t1)
    db.commit()

    # 1. Post to execute endpoint (Run)
    exec_data = {"code": "def mse(y, y_hat): return 0.0", "language": "python", "challenge_slug": "mean-squared-error"}
    response = client.post("/api/executions", json=exec_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "COMPLETED"

    # 2. Post to submit endpoint
    response = client.post("/api/submissions?challenge_slug=mean-squared-error", json={"code": "def mse(y, y_hat): return 0.0", "language": "python"}, headers=headers)
    assert response.status_code == 200
    sub_data = response.json()
    assert sub_data["status"] == "ACCEPTED"
    assert sub_data["code"] == "def mse(y, y_hat): return 0.0"
    assert "id" in sub_data

    # 3. Retrieve submission details
    sub_id = sub_data["id"]
    response = client.get(f"/api/submissions/{sub_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "ACCEPTED"

    # 4. Clear cookies to simulate unauthenticated client
    client.cookies.clear()

    # 5. Unauthenticated submission attempt
    response = client.post("/api/submissions?challenge_slug=mean-squared-error", json={"code": "def mse(y, y_hat): return 0.0", "language": "python"})
    assert response.status_code == 401

def test_bookmarks_flow(client, db):
    reg_data = {"email": "bookmarker@neuracode.com", "password": "password123"}
    client.post("/api/auth/register", json=reg_data)
    login_res = client.post("/api/auth/login", json=reg_data)
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    challenge = Challenge(
        title="Test Attention",
        slug="test-attention",
        difficulty="Hard",
        category="Transformers",
        description="Compute attention.",
        starter_code="def attention(): pass",
        constraints="None",
        status="active"
    )
    db.add(challenge)
    db.commit()

    response = client.get("/api/bookmarks", headers=headers)
    assert response.status_code == 200
    assert response.json() == []

    response = client.post("/api/challenges/test-attention/bookmark", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"bookmarked": True}

    response = client.get("/api/bookmarks", headers=headers)
    assert response.status_code == 200
    assert response.json() == ["test-attention"]

    response = client.post("/api/challenges/test-attention/bookmark", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"bookmarked": False}

    response = client.get("/api/bookmarks", headers=headers)
    assert response.status_code == 200
    assert response.json() == []

    client.cookies.clear()
    response = client.post("/api/challenges/test-attention/bookmark")
    assert response.status_code == 401
