def test_create_seminar(client):
    # create auth user and get token
    client.post("/auth/signup", json={"username": "admin", "password": "pw"})
    login_resp = client.post("/auth/login", data={"username": "admin", "password": "pw"})
    token = login_resp.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/seminars",
        json={"title": "Test Seminar", "description": "Test Desc", "max_capacity": 10},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Seminar"
    assert response.json()["max_capacity"] == 10

def test_list_seminars(client):
    response = client.get("/seminars")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_seminar_detail(client):
    # login (assuming user is already created from test_create_seminar, but to be safe, create again or handle it)
    client.post("/auth/signup", json={"username": "admin2", "password": "pw"})
    login_resp = client.post("/auth/login", data={"username": "admin2", "password": "pw"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # create
    create_resp = client.post(
        "/seminars",
        json={"title": "Detail Seminar", "description": "Desc", "max_capacity": 5},
        headers=headers
    )
    seminar_id = create_resp.json()["id"]
    
    # get detail
    response = client.get(f"/seminars/{seminar_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Detail Seminar"
