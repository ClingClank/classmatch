import json
from sqlalchemy import text


def _register(client, email="u@example.com", password="pw", name="U"):
    resp = client.post(
        "/api/commands/users/register",
        data=json.dumps({"email": email, "password": password, "name": name}),
        content_type="application/json",
    )
    assert resp.status_code == 201
    return resp.get_json()["user_id"]


def _create_course(client, cid="C100"):
    resp = client.post(
        "/api/commands/courses",
        data=json.dumps({"id": cid, "code": "C 100", "name": "Course 100", "section": "001", "instructor": "Prof", "schedule": "MWF", "students": 0}),
        content_type="application/json",
    )
    assert resp.status_code == 201
    return cid


def test_availability_crud_and_overview(client, test_engine):
    uid = _register(client, "avuser@example.com")

    # missing slot
    resp = client.post(f"/api/commands/availability/{uid}", json={})
    assert resp.status_code == 400

    # add slot
    resp = client.post(f"/api/commands/availability/{uid}", json={"slot": "Mon 10-11"})
    assert resp.status_code == 201
    sid = resp.get_json()["slot_id"]

    # overview shows availability
    resp = client.get(f"/api/queries/users/{uid}/overview")
    if resp.status_code != 200:
        print(resp.get_data(as_text=True))
    assert resp.status_code == 200
    data = resp.get_json()
    assert any(a["slot"] == "Mon 10-11" for a in data["availability"])

    # update all with invalid type
    resp = client.put(f"/api/commands/availability/{uid}", json={"slots": "not-a-list"})
    assert resp.status_code == 400

    # update all properly
    resp = client.put(f"/api/commands/availability/{uid}", json={"slots": ["Tue 9-10", ""]})
    assert resp.status_code == 200

    resp = client.get(f"/api/queries/users/{uid}/overview")
    assert resp.status_code == 200
    data = resp.get_json()
    assert any(a["slot"] == "Tue 9-10" for a in data["availability"])

    # delete slot (use slot id exists via DB)
    with test_engine.begin() as conn:
        sid_row = conn.execute(text("SELECT id FROM availability_text WHERE user_id = :uid"), {"uid": uid}).first()
        assert sid_row is not None
        sid = sid_row.id

    resp = client.delete(f"/api/commands/availability/{uid}/{sid}")
    assert resp.status_code == 200

    # deleting again should give 404
    resp = client.delete(f"/api/commands/availability/{uid}/{sid}")
    assert resp.status_code == 404


def test_courses_create_enroll_unenroll_and_queries(client):
    cid = _create_course(client, "CCX1")
    # create course missing fields
    resp = client.post("/api/commands/courses", json={"id": "X"})
    assert resp.status_code == 400

    # enroll error cases
    uid = _register(client, "cenroll@example.com")
    # non-existing course
    resp = client.post(f"/api/commands/courses/NOPE/enroll", json={"user_id": uid})
    assert resp.status_code == 404

    # non-existing user
    resp = client.post(f"/api/commands/courses/{cid}/enroll", json={"user_id": 99999})
    assert resp.status_code == 404

    # successful enroll
    resp = client.post(f"/api/commands/courses/{cid}/enroll", json={"user_id": uid})
    assert resp.status_code == 201

    # duplicate enrollment -> 409
    resp = client.post(f"/api/commands/courses/{cid}/enroll", json={"user_id": uid})
    assert resp.status_code == 409

    # course detail shows enrolled_count
    resp = client.get(f"/api/queries/courses/{cid}")
    assert resp.status_code == 200
    assert resp.get_json().get("enrolled_count", 0) >= 1

    # students list
    resp = client.get(f"/api/queries/courses/{cid}/students")
    assert resp.status_code == 200
    assert any(s["id"] == uid for s in resp.get_json())

    # create group for course and check groups query
    resp = client.post(
        "/api/commands/groups",
        json={"owner_user_id": uid, "course_id": cid, "name": "Course Group"},
    )
    assert resp.status_code == 201

    resp = client.get(f"/api/queries/courses/{cid}/groups")
    assert resp.status_code == 200
    assert any(g["name"] == "Course Group" for g in resp.get_json())

    # unenroll
    resp = client.delete(f"/api/commands/courses/{cid}/enroll", json={"user_id": uid})
    assert resp.status_code == 200

    # unenroll again -> 404
    resp = client.delete(f"/api/commands/courses/{cid}/enroll", json={"user_id": uid})
    assert resp.status_code == 404


def test_users_queries_matches_groups_and_search(client):
    # users and courses to exercise matches and groups
    u1 = _register(client, "u1@example.com")
    u2 = _register(client, "u2@example.com")
    c1 = _create_course(client, "CMATCH1")
    c2 = _create_course(client, "CMATCH2")

    # enroll u1 in c1 and c2, u2 only in c1
    client.post(f"/api/commands/courses/{c1}/enroll", json={"user_id": u1})
    client.post(f"/api/commands/courses/{c2}/enroll", json={"user_id": u1})
    client.post(f"/api/commands/courses/{c1}/enroll", json={"user_id": u2})

    # matches for u1 should include u2 with shared_courses >=1
    resp = client.get(f"/api/queries/users/{u1}/matches")
    if resp.status_code != 200:
        print(resp.get_data(as_text=True))
    assert resp.status_code == 200
    matches = resp.get_json().get("matches", [])
    assert any(m["id"] == u2 and int(m["shared_courses"]) >= 1 for m in matches)

    # create group and add u1
    resp = client.post("/api/commands/groups", json={"owner_user_id": u1, "course_id": c1, "name": "MatchGroup"})
    gid = resp.get_json()["group_id"]
    client.post(f"/api/commands/groups/{gid}/join", json={"user_id": u1})

    resp = client.get(f"/api/queries/users/{u1}/groups")
    assert resp.status_code == 200
    assert any(g["id"] == gid for g in resp.get_json())

    # search users by name and filter
    resp = client.get("/api/queries/users/search?q=u1")
    assert resp.status_code == 200
    assert any(u["id"] == u1 for u in resp.get_json())


def test_availability_queries_and_not_found(client):
    uid = _register(client, "av2@example.com")
    client.post(f"/api/commands/availability/{uid}", json={"slot": "Fri 2-3"})

    resp = client.get(f"/api/queries/availability/{uid}")
    assert resp.status_code == 200
    assert any(s["slot"] == "Fri 2-3" for s in resp.get_json())

    resp = client.get("/api/queries/availability/99999")
    assert resp.status_code == 404


def test_courses_queries_search_and_not_found(client):
    # create courses with different instructors
    client.post("/api/commands/courses", json={"id": "SCH1", "code": "SCH 1", "name": "Searchable One", "section": "001", "instructor": "Dr X", "schedule": "MWF", "students": 1})
    client.post("/api/commands/courses", json={"id": "SCH2", "code": "SCH 2", "name": "Searchable Two", "section": "001", "instructor": "Dr Y", "schedule": "TTh", "students": 1})

    resp = client.get("/api/queries/courses?search=Searchable")
    assert resp.status_code == 200
    assert len(resp.get_json()) >= 2

    resp = client.get("/api/queries/courses?instructor=Dr X")
    assert resp.status_code == 200
    assert any(c["instructor"] == "Dr X" for c in resp.get_json())

    resp = client.get("/api/queries/courses/NOPE")
    assert resp.status_code == 404


def test_users_queries_detail_get_and_list(client):
    r_a = client.post("/api/commands/users/register", json={"email": "ud1@example.com", "password": "pw", "name": "UA"})
    assert r_a.status_code == 201
    u_a = r_a.get_json()["user_id"]

    r_b = client.post("/api/commands/users/register", json={"email": "ud2@example.com", "password": "pw", "name": "UB"})
    assert r_b.status_code == 201
    u_b = r_b.get_json()["user_id"]

    # update u_b major/year
    client.put(f"/api/commands/users/{u_b}", json={"major": "CS", "year": "Junior"})

    resp = client.get(f"/api/queries/users/detail/{u_a}")
    assert resp.status_code == 200
    assert resp.get_json()["email"] == "ud1@example.com"

    resp = client.get("/api/queries/users/detail?major=CS")
    assert resp.status_code == 200
    assert any(u["id"] == u_b for u in resp.get_json())

    resp = client.get("/api/queries/users/detail/99999")
    assert resp.status_code == 404
