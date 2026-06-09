def test_create_reservation(client):
    # Setup user
    client.post("/auth/signup", json={"username": "res_user", "password": "pw"})
    token = client.post("/auth/login", data={"username": "res_user", "password": "pw"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Setup seminar
    create_resp = client.post(
        "/seminars",
        json={"title": "Res Seminar", "description": "Desc", "max_capacity": 1},
        headers=headers
    )
    seminar_id = create_resp.json()["id"]
    
    # Reserve
    res_resp = client.post(
        f"/seminars/{seminar_id}/reservations",
        headers=headers
    )
    assert res_resp.status_code == 200
    assert res_resp.json()["seminar_id"] == seminar_id
    
    # Reserve again should fail due to capacity
    client.post("/auth/signup", json={"username": "res_user2", "password": "pw"})
    token2 = client.post("/auth/login", data={"username": "res_user2", "password": "pw"}).json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}
    
    res_resp2 = client.post(
        f"/seminars/{seminar_id}/reservations",
        headers=headers2
    )
    assert res_resp2.status_code == 400
    assert "capacity" in res_resp2.json()["detail"].lower()
