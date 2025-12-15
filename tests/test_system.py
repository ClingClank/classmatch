def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body.get("ok") is True


def test_notifications_unread_filter_and_user_not_found(client):
    # user not found
    resp = client.get("/api/queries/notifications/99999")
    assert resp.status_code == 404

    # create user and notifications then filter
    resp = client.post(
        "/api/commands/users/register",
        json={"email": "nfilter@example.com", "password": "pw", "name": "NF"},
    )
    uid = resp.get_json()["user_id"]

    # create notifications
    client.post(
        "/api/commands/notifications",
        json={"user_id": uid, "type": "test", "data": {"x": 1}},
    )

    resp = client.get(f"/api/queries/notifications/{uid}?unread_only=true")
    assert resp.status_code == 200
