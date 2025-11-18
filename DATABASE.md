# ClassMatch Database Design Documentation

## Overview
The **ClassMatch** database supports a platform that helps students match with peers, join study groups, organize schedules, and communicate.  
This document explains the schema, relationships, and purpose of every table.

---

# 1. Conceptual Schema Diagram

users ───< enrollments >─── courses
│ │
│ └───────────────────────┐
│ │
├──< availability_text │
│ │
├──< groups (owner_user_id) >───< group_members >── users
│ │
└──< notifications │
│
groups ───< messages ─── users


---

# 2. Tables and Descriptions

## 2.1 `users`
Stores user accounts and profile information.

| Column | Type | Description |
|--------|-------|-------------|
| id | BIGINT UNSIGNED PK | Unique ID for each user |
| email | VARCHAR(255) UNIQUE | User login email |
| password_hash | VARCHAR(255) | Hashed password |
| name | VARCHAR(120) | Full name |
| major | VARCHAR(120) | Academic major |
| year | VARCHAR(40) | Academic year |
| avatar | VARCHAR(8) | Avatar short code |
| bio | TEXT | User biography |
| study_prefs | JSON | Preferences for time, location, and study style |
| created_at | TIMESTAMP | Creation timestamp |

**Purpose:** Stores user identities, preferences, and profile information.

---

## 2.2 `courses`
Stores course data.

| Column | Type | Description |
|--------|-------|-------------|
| id | VARCHAR(32) PK | Unique course ID |
| code | VARCHAR(32) | Course code |
| name | VARCHAR(255) | Full course name |
| section | VARCHAR(16) | Section number |
| instructor | VARCHAR(120) | Instructor name |
| schedule | VARCHAR(120) | Meeting time |
| students | INT | Number of enrolled students |
| building | VARCHAR(120) | Building name |
| room | VARCHAR(32) | Room number |

**Purpose:** Provides course information for enrollments and study groups.

---

## 2.3 `enrollments`
Maps users to their courses.

| Column | Type | Description |
|--------|-------|-------------|
| user_id | BIGINT UNSIGNED FK → users.id | Student ID |
| course_id | VARCHAR(32) FK → courses.id | Course ID |
| enrolled_at | TIMESTAMP | Timestamp of enrollment |

**Primary Key:** (user_id, course_id)

**Purpose:** Supports course-to-student relationships.

---

## 2.4 `availability_text`
Stores availability time slots written by users.

| Column | Type | Description |
|--------|-------|-------------|
| id | BIGINT UNSIGNED PK | Entry ID |
| user_id | BIGINT UNSIGNED FK | User ID |
| slot | VARCHAR(120) | Free-text availability description |
| created_at | TIMESTAMP | Timestamp |

**Purpose:** Helps match students based on schedules.

---

## 2.5 `groups`
Represents study groups created by users.

| Column | Type | Description |
|--------|-------|-------------|
| id | BIGINT UNSIGNED PK | Group ID |
| owner_user_id | BIGINT UNSIGNED FK | Group creator |
| course_id | VARCHAR(32) FK | Related course |
| name | VARCHAR(255) | Group name |
| description | TEXT | Group description |
| meeting_time | VARCHAR(120) | Meeting schedule |
| location | VARCHAR(160) | Meeting location |
| max_members | INT | Max allowed members |
| tags | JSON | Tags and topics |
| is_archived | TINYINT(1) | Archive flag |
| created_at | TIMESTAMP | Creation timestamp |

**Purpose:** Organizes students into course-based study groups.

---

## 2.6 `group_members`
Links users to the groups they join.

| Column | Type | Description |
|--------|-------|-------------|
| group_id | BIGINT UNSIGNED FK → groups.id | Group |
| user_id | BIGINT UNSIGNED FK → users.id | User |
| role | ENUM('member','admin') | Member role |
| status | ENUM('active','removed') | Member status |
| joined_at | TIMESTAMP | When they joined |

**Primary Key:** (group_id, user_id)

**Purpose:** Controls group membership and roles.

---

## 2.7 `messages`
Stores chat messages inside groups.

| Column | Type | Description |
|--------|-------|-------------|
| id | BIGINT UNSIGNED PK | Message ID |
| group_id | BIGINT UNSIGNED FK | Group ID |
| user_id | BIGINT UNSIGNED FK | Sender ID |
| content | TEXT | Message text |
| created_at | TIMESTAMP | Timestamp |

**Purpose:** Enables group chat functionality.

---

## 2.8 `notifications`
Stores system notifications for users.

| Column | Type | Description |
|--------|-------|-------------|
| id | BIGINT UNSIGNED PK | Notification ID |
| user_id | BIGINT UNSIGNED FK | Recipient |
| type | VARCHAR(64) | Notification type |
| data | JSON | Additional data |
| is_read | TINYINT(1) | Read/unread status |
| created_at | TIMESTAMP | Timestamp |

**Purpose:** Allows real-time alerts for events such as new messages or group activity.

---

# 3. Relationships Summary

### Users
- Has many: enrollments, availability entries, created groups, group memberships, messages, notifications.

### Courses
- Has many enrollments.
- Has many groups.

### Groups
- Has many group members.
- Has many messages.
- Belongs to a course.
- Belongs to an owner.

### Many-to-Many Relationships
- Users ↔ Courses (via `enrollments`)
- Users ↔ Groups (via `group_members`)

---

# 4. Data Integrity Rules

### Cascading Deletes
- Deleting a user removes all related:
  - enrollments  
  - availability entries  
  - groups they own  
  - group memberships  
  - messages  
  - notifications  

- Deleting a course removes:
  - enrollments  
  - groups tied to that course  

- Deleting a group removes:
  - messages  
  - group members  

### Composite Keys
- `enrollments(user_id, course_id)` prevents duplicate course enrollments.
- `group_members(group_id, user_id)` prevents duplicate group membership.

---

# 5. JSON Columns

### `users.study_prefs`
Example:
```json
{
  "times": ["Morning", "Afternoon"],
  "location": ["Library", "Coffee Shop"],
  "style": "Group Discussion"
}