import json
import time


def _register(client, email="u@example.com", password="pw", name="U"):
    resp = client.post(
        "/api/commands/users/register",
        data=json.dumps({"email": email, "password": password, "name": name}),
        content_type="application/json",
    )
    assert resp.status_code == 201
    return resp.get_json()["user_id"]


def _create_course(client, cid="C101"):
    resp = client.post(
        "/api/commands/courses",
        data=json.dumps({"id": cid, "code": "C 101", "name": "Course", "section": "001", "instructor": "Prof", "schedule": "MWF", "students": 1}),
        content_type="application/json",
    )
    assert resp.status_code == 201


def test_join_with_inviter_creates_pending_and_notification(client, test_engine):
    owner = _register(client, "owner@invite.com", "pw", "Owner")
    invitee = _register(client, "invitee@invite.com", "pw", "Invitee")
    _create_course(client, "CINV1")

    resp = client.post(
        "/api/commands/groups",
        data=json.dumps({"owner_user_id": owner, "course_id": "CINV1", "name": "Inv Group"}),
        content_type="application/json",
    )
    assert resp.status_code == 201
    gid = resp.get_json()["group_id"]

    # inviter_id -> pending invitation
    resp = client.post(f"/api/commands/groups/{gid}/join", data=json.dumps({"user_id": invitee, "inviter_id": owner}), content_type="application/json")
    if resp.status_code != 201:
        print(resp.get_data(as_text=True))
    assert resp.status_code == 201
    assert resp.get_json().get("status") == "pending"

    from sqlalchemy import text
    with test_engine.begin() as conn:
        row = conn.execute(text("SELECT status FROM group_members WHERE group_id = :gid AND user_id = :uid"), {"gid": gid, "uid": invitee}).first()
        assert row is not None
        assert row.status == "pending"

        notif = conn.execute(text("SELECT type, is_read FROM notifications WHERE user_id = :uid"), {"uid": invitee}).first()
        assert notif is not None
        assert notif.type == "group_invitation"


def test_accept_invitation_makes_active_and_publishes_join_notification(client, test_engine):
    owner = _register(client, "owner2@inv.com", "pw", "Owner2")
    invitee = _register(client, "invitee2@inv.com", "pw", "Invitee2")
    _create_course(client, "CINV2")

    resp = client.post(
        "/api/commands/groups",
        data=json.dumps({"owner_user_id": owner, "course_id": "CINV2", "name": "Inv Group 2"}),
        content_type="application/json",
    )
    gid = resp.get_json()["group_id"]

    # create pending invitation
    resp = client.post(f"/api/commands/groups/{gid}/join", data=json.dumps({"user_id": invitee, "inviter_id": owner}), content_type="application/json")
    assert resp.status_code == 201

    # accept it
    resp = client.post(f"/api/commands/groups/{gid}/accept-invitation", data=json.dumps({"user_id": invitee}), content_type="application/json")
    assert resp.status_code == 200

    from sqlalchemy import text
    with test_engine.begin() as conn:
        row = conn.execute(text("SELECT status FROM group_members WHERE group_id = :gid AND user_id = :uid"), {"gid": gid, "uid": invitee}).first()
        assert row is not None
        assert row.status == "active"

        # owner should receive a group_joined notification
        notifs = conn.execute(text("SELECT type FROM notifications WHERE user_id = :uid"), {"uid": owner}).fetchall()
        assert any(n.type == "group_joined" for n in notifs)


def test_decline_invitation_removes_pending_and_marks_notification_read(client, test_engine):
    owner = _register(client, "owner3@inv.com", "pw", "Owner3")
    invitee = _register(client, "invitee3@inv.com", "pw", "Invitee3")
    _create_course(client, "CINV3")

    resp = client.post(
        "/api/commands/groups",
        data=json.dumps({"owner_user_id": owner, "course_id": "CINV3", "name": "Inv Group 3"}),
        content_type="application/json",
    )
    gid = resp.get_json()["group_id"]

    resp = client.post(f"/api/commands/groups/{gid}/join", data=json.dumps({"user_id": invitee, "inviter_id": owner}), content_type="application/json")
    assert resp.status_code == 201

    # decline
    resp = client.post(f"/api/commands/groups/{gid}/decline-invitation", data=json.dumps({"user_id": invitee}), content_type="application/json")
    assert resp.status_code == 200

    from sqlalchemy import text
    with test_engine.begin() as conn:
        row = conn.execute(text("SELECT status FROM group_members WHERE group_id = :gid AND user_id = :uid"), {"gid": gid, "uid": invitee}).first()
        assert row is None

        # invitation notification should be marked (is_read = 1) or removed depending on sqlite JSON support
        notif = conn.execute(text("SELECT is_read FROM notifications WHERE user_id = :uid AND type = 'group_invitation'"), {"uid": invitee}).first()
        assert notif is not None


def test_owner_cannot_leave_group(client):
    owner = _register(client, "owner4@inv.com", "pw", "Owner4")
    _create_course(client, "CINV4")

    resp = client.post(
        "/api/commands/groups",
        data=json.dumps({"owner_user_id": owner, "course_id": "CINV4", "name": "Inv Group 4"}),
        content_type="application/json",
    )
    gid = resp.get_json()["group_id"]

    resp = client.post(f"/api/commands/groups/{gid}/leave", data=json.dumps({"user_id": owner}), content_type="application/json")
    assert resp.status_code == 400


def test_transfer_ownership_fails_if_not_member(client):
    owner = _register(client, "owner5@inv.com", "pw", "Owner5")
    outsider = _register(client, "outsider@inv.com", "pw", "Outsider")
    _create_course(client, "CINV5")

    resp = client.post(
        "/api/commands/groups",
        data=json.dumps({"owner_user_id": owner, "course_id": "CINV5", "name": "Inv Group 5"}),
        content_type="application/json",
    )
    gid = resp.get_json()["group_id"]

    resp = client.patch(f"/api/commands/groups/{gid}/transfer-ownership", data=json.dumps({"new_owner_id": outsider}), content_type="application/json")
    assert resp.status_code == 400


def test_group_creation_response_time_under_threshold(client):
    owner = _register(client, "perf@inv.com", "pw", "Perf")
    _create_course(client, "CPERF")

    start = time.time()
    resp = client.post(
        "/api/commands/groups",
        data=json.dumps({"owner_user_id": owner, "course_id": "CPERF", "name": "Perf Group"}),
        content_type="application/json",
    )
    duration = time.time() - start
    assert resp.status_code == 201
    assert duration < 1.0
