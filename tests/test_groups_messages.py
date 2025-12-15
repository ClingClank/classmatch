import json


def _register(client, email="u@example.com", password="pw", name="U"):
    resp = client.post(
        "/api/commands/users/register",
        data=json.dumps({"email": email, "password": password, "name": name}),
        content_type="application/json",
    )
    assert resp.status_code == 201
    return resp.get_json()["user_id"]


def test_create_group_creates_notification(client):
    owner_id = _register(client, "owner@example.com", "pw", "Owner")

    # create a minimal course first (so group has a course_id)
    client.post(
        "/api/commands/courses",
        data=json.dumps({"id": "TST100", "code": "TST 100", "name": "Test Course", "section": "001", "instructor": "Prof", "schedule": "MWF", "students": 1}),
        content_type="application/json",
    )

    resp = client.post(
        "/api/commands/groups",
        data=json.dumps({"owner_user_id": owner_id, "course_id": "TST100", "name": "Study Group"}),
        content_type="application/json",
    )
    assert resp.status_code == 201
    gid = resp.get_json()["group_id"]

    # owner should have a group_created notification
    notif_resp = client.get(f"/api/queries/notifications/{owner_id}")
    assert notif_resp.status_code == 200
    notifs = notif_resp.get_json()
    types = [n["type"] for n in notifs]
    assert "group_created" in types


def test_join_and_message_notifications(client):
    owner_id = _register(client, "own2@example.com", "pw", "Owner2")
    member_id = _register(client, "mem@example.com", "pw", "Member")

    # create course and group
    client.post(
        "/api/commands/courses",
        data=json.dumps({"id": "TST200", "code": "TST 200", "name": "Test Course 2", "section": "001", "instructor": "Prof", "schedule": "MWF", "students": 1}),
        content_type="application/json",
    )
    resp = client.post(
        "/api/commands/groups",
        data=json.dumps({"owner_user_id": owner_id, "course_id": "TST200", "name": "Study Group 2"}),
        content_type="application/json",
    )
    assert resp.status_code == 201
    gid = resp.get_json()["group_id"]

    # member joins directly
    resp = client.post(f"/api/commands/groups/{gid}/join", data=json.dumps({"user_id": member_id}), content_type="application/json")
    assert resp.status_code == 201

    # owner should receive a group_joined notification
    notif_resp = client.get(f"/api/queries/notifications/{owner_id}")
    assert notif_resp.status_code == 200
    notifs = notif_resp.get_json()
    assert any(n["type"] == "group_joined" for n in notifs)

    # member posts a message
    resp = client.post(
        "/api/commands/messages",
        data=json.dumps({"group_id": gid, "user_id": member_id, "content": "Hello"}),
        content_type="application/json",
    )
    assert resp.status_code == 201

    # owner should have a group_message_posted notification
    notif_resp = client.get(f"/api/queries/notifications/{owner_id}")
    notifs = notif_resp.get_json()
    assert any(n["type"] == "group_message_posted" for n in notifs)

    # messages query should return the message
    msgs = client.get(f"/api/queries/messages/group/{gid}")
    if msgs.status_code != 200:
        print("messages endpoint status:", msgs.status_code, msgs.get_data(as_text=True))
    assert msgs.status_code == 200
    data = msgs.get_json()
    assert any(m["content"] == "Hello" for m in data)
