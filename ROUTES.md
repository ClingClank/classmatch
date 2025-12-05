**ClassMatch API Routes (CQRS)**

- **Base URL:** `http://<host>:<port>` (example: `http://127.0.0.1:5000`)
- **Notes:** Commands are write operations (mutations). Queries are read-only. All endpoints accept and return JSON unless noted.

**Commands (Write endpoints)**

- **Prefix:** `/api/commands`

- **Groups** (`/api/commands/groups`):

  - **POST /** : Create a new group.
  - **PUT /<group_id>** : Update group metadata (name, description, meeting_time, etc.).
  - **DELETE /<group_id>** : Delete a group.
  - **POST /<group_id>/join** : Request / add a user to the group.
  - **POST /<group_id>/leave** : Remove a user from the group.
  - **POST /<group_id>/transfer** : Transfer group ownership to another user.

- **Messages** (`/api/commands/messages`):

  - **POST /group/<group_id>** : Post a new message to a group.
  - **DELETE /<message_id>** : Delete a message.

- **Users** (`/api/commands/users`):

  - **POST /register** : Register a new user.
  - **POST /login** : Authenticate a user (returns user info on success).
  - **PUT /<user_id>** : Update user profile fields.
  - **DELETE /<user_id>** : Delete a user account.

- **Courses** (`/api/commands/courses`):

  - **POST /** : Create a new course (admin).
  - **POST /<course_id>/enroll** : Enroll a user in a course.
  - **DELETE /<course_id>/enroll** : Unenroll a user from a course.

- **Availability** (`/api/commands/availability`):

  - **POST /<user_id>** : Add availability slot for `user_id` (body: `{ "slot": "..." }`).
  - **DELETE /<user_id>/<slot_id>** : Delete a user's availability slot.
  - **PUT /<user_id>** : Replace all availability slots for a user (body: `{ "slots": ["..."] }`).

- **Notifications** (`/api/commands/notifications`):
  - **POST /<user_id>** : Create a notification for a user.
  - **PATCH /<user_id>/<notification_id>/read** : Mark a notification read.
  - **PATCH /<user_id>/read-all** : Mark all notifications read for a user.
  - **DELETE /<user_id>/<notification_id>** : Delete a notification.

**Queries (Read endpoints)**

- **Prefix:** `/api/queries`

- **Groups** (`/api/queries/groups`):

  - **GET /** : List groups (filters supported via query params).
  - **GET /<group_id>** : Get group details.
  - **GET /<group_id>/members** : Get active members of a group.
  - **GET /<group_id>/messages** : Get recent messages for a group (read-only).

- **Messages** (`/api/queries/messages`):

  - **GET /group/<group_id>** : Get messages in a group (supports `limit`/`offset`).
  - **GET /<message_id>** : Get message details.

- **Users** (`/api/queries/users`):

  - **GET /** : List users (filter by `major`, `year`).
  - **GET /<user_id>** : Get a user's profile and public fields.
  - (additional query endpoints such as `matches`, `groups` may exist under this prefix in `users_queries.py`.)

- **Courses** (`/api/queries/courses`):

  - **GET /** : List courses (supports `search`, `instructor`).
  - **GET /<course_id>** : Course detail (includes `enrolled_count`).
  - **GET /<course_id>/students** : Get students enrolled in a course.
  - **GET /<course_id>/groups** : Get groups for a course.

- **Availability** (`/api/queries/availability`):

  - **GET /<user_id>** : Get availability slots for a user.

- **Notifications** (`/api/queries/notifications`):
  - **GET /<user_id>** : List notifications for a user (query `unread_only=true` to filter).
  - **GET /<user_id>/count** : Get unread notification count.

