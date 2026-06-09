def test_signup(client):
    response = client.post(
        "/auth/signup",
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert "id" in response.json()

def test_login(client):
    # Setup user
    client.post("/auth/signup", json={"username": "testlogin", "password": "testpassword"})
    
    # Test login
    response = client.post(
        "/auth/login",
        data={"username": "testlogin", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
