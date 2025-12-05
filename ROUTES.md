# API Routes (Flask Backend)

This document lists the Flask backend API endpoints, their paths (including blueprint prefixes), HTTP methods, expected parameters or request bodies, and brief descriptions of what they do.

Note: The Flask app registers two blueprints with prefixes:

- `api/query` — read/query endpoints (GET)
- `api/command` — command/write endpoints (POST)

Also the app exposes a root health endpoint at `/health`.

---

**Root Health**:

- **Path**: `/health`
- **Method**: `GET`
- **Description**: Basic server health check for the Flask app.
- **Response**: JSON `{ "ok": true, "message": "Flask server is running" }` (200)

---

All blueprint endpoints are prefixed by their registered url_prefix. When calling, prepend the prefix to the paths below.

**Query Blueprint Prefix**: `/api/query`

- **GET** `/api/query/health`

  - **Description**: Health check for the query layer (blueprint).
  - **Response**: JSON `{ "ok": true, "message": "query layer active" }` (200)

- **GET** `/api/query/users/<user_id>/overview`

  - **Path params**: `user_id` (integer)
  - **Description**: Returns a user's basic profile, their availability (text slots), and the courses they are enrolled in.
  - **Response (success)**: JSON object with keys:
    - `user`: object with `id`, `email`, `name`, `major`, `year`
    - `availability`: array of availability slot strings (ordered by creation time)
    - `courses`: array of course objects `{ id, code, name }`
  - **Errors**:
    - `404` with `{ "error": "User not found" }` if the user id does not exist
    - `500` with `{ "error": "<message>" }` on server/database errors

- **GET** `/api/query/users/<user_id>/matches`

  - **Path params**: `user_id` (integer)
  - **Description**: Finds other users who share enrolled courses with the given user. Returns matches ordered by most shared courses.
  - **Response (success)**: JSON `{ "matches": [ { "id": ..., "name": ..., "email": ..., "shared_courses": <count> }, ... ] }`
  - **Errors**:
    - `404` with `{ "error": "User not found" }` if the user id does not exist
    - `500` on server/database errors

- **GET** `/api/query/groups`

  - **Description**: Returns a list of groups with basic information joined to their course code and owner name.
  - **Response (success)**: JSON array where each item includes `id`, `name`, `description`, `meeting_time`, `location`, `max_members`, `course_code`, `owner_name`.
  - **Errors**: `500` with `{ "error": "<message>" }` on errors

- **GET** `/api/query/groups/<group_id>`
  - **Path params**: `group_id` (integer)
  - **Description**: Returns detailed information for a specific group including members and recent messages.
  - **Response (success)**: JSON object with group fields plus:
    - `members`: array of `{ id, name, email, role, status }`
    - `messages`: array of `{ id, content, created_at, author_name }` ordered by `created_at` descending
  - **Errors**:
    - `404` with `{ "error": "Group not found" }` if the group id does not exist
    - `500` on server/database errors

---

**Command Blueprint Prefix**: `/api/command`

- **POST** `/api/command/groups`

  - **Description**: Create a new group and automatically add the owner as an admin member.
  - **Request JSON** (required fields shown):
    - `owner_user_id` (int) — required
    - `course_id` (int) — required
    - `name` (string) — required
    - `description` (string) — optional (defaults to empty string)
    - `meeting_time` (string) — optional
    - `location` (string) — optional
    - `max_members` (int) — optional (defaults to 5)
  - **Response (success)**: `{ "ok": true, "group_id": <new id> }` (201)
  - **Errors**:
    - `400` if required fields are missing with `{ "error": "owner_user_id, course_id, and name are required" }`
    - `500` on server/database errors
  - **Side effects**: Inserts the group row, inserts an initial `group_members` row with role `'admin'` and status `'active'`, and publishes a `GroupCreated` event on the internal event bus.

- **POST** `/api/command/groups/<group_id>/join`

  - **Path params**: `group_id` (integer)
  - **Description**: Adds a user as an active member to the group if it's not full.
  - **Request JSON**: `{ "user_id": <int> }` (required)
  - **Response (success)**: `{ "ok": true, "message": "Joined group" }` (201)
  - **Errors**:
    - `400` if `user_id` not provided: `{ "error": "user_id is required" }`
    - `404` if group not found: `{ "error": "Group not found" }`
    - `400` if group is full: `{ "error": "Group is full" }`
    - `500` on server/database errors
  - **Side effects**: Inserts a `group_members` row and publishes a `GroupJoined` event on the event bus.

- **POST** `/api/command/groups/<group_id>/messages`
  - **Path params**: `group_id` (integer)
  - **Description**: Post a message in a group.
  - **Request JSON**: `{ "user_id": <int>, "content": <string> }` (both required)
  - **Response (success)**: `{ "ok": true, "message_id": <new id> }` (201)
  - **Errors**:
    - `400` if required fields missing: `{ "error": "user_id and content are required" }`
    - `500` on server/database errors
  - **Side effects**: Inserts a `messages` row and publishes a `GroupMessagePosted` event on the event bus.

---

Notes and implementation details:

- Endpoints use SQLAlchemy `text()` SQL queries against the configured `engine` (see `server/db.py`).
- Errors typically return 500 with an error message string when exceptions occur during DB or processing.
- The command endpoints use `engine.begin()` for transactional writes.
- The code publishes domain events (`GroupCreated`, `GroupJoined`, `GroupMessagePosted`) to an in-process `event_bus` defined in `server/domain/event_bus.py`.
