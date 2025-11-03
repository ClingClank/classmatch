/**
 * API Integration Guide
 *
 * This file provides templates for integrating with the Flask backend.
 * Replace the functions in AuthContext.jsx and sampleData.js with these API calls.
 */

// Base API URL - update this when backend is deployed
const API_BASE_URL = process.env.VITE_API_URL || "http://localhost:5000/api";

// Helper function for API requests
async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem("auth_token");

  const config = {
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
    ...options,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "API request failed");
  }

  return response.json();
}

// ==================== Authentication APIs ====================

export async function apiLogin(email, password) {
  const data = await apiRequest("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

  // Store token
  if (data.token) {
    localStorage.setItem("auth_token", data.token);
  }

  return data.user;
}

export async function apiSignup(userData) {
  const data = await apiRequest("/auth/signup", {
    method: "POST",
    body: JSON.stringify(userData),
  });

  // Store token
  if (data.token) {
    localStorage.setItem("auth_token", data.token);
  }

  return data.user;
}

export async function apiLogout() {
  await apiRequest("/auth/logout", { method: "POST" });
  localStorage.removeItem("auth_token");
}

export async function apiGetCurrentUser() {
  return apiRequest("/auth/me");
}

export async function apiUpdateProfile(updates) {
  return apiRequest("/users/profile", {
    method: "PATCH",
    body: JSON.stringify(updates),
  });
}

// ==================== Course APIs ====================

export async function apiGetAllCourses(filters = {}) {
  const queryParams = new URLSearchParams(filters).toString();
  return apiRequest(`/courses?${queryParams}`);
}

export async function apiGetCourse(courseId) {
  return apiRequest(`/courses/${courseId}`);
}

export async function apiEnrollCourse(courseId) {
  return apiRequest(`/courses/${courseId}/enroll`, {
    method: "POST",
  });
}

export async function apiUnenrollCourse(courseId) {
  return apiRequest(`/courses/${courseId}/unenroll`, {
    method: "DELETE",
  });
}

export async function apiGetMyCourses() {
  return apiRequest("/users/courses");
}

// ==================== Matching APIs ====================

export async function apiGetMatches(filters = {}) {
  const queryParams = new URLSearchParams(filters).toString();
  return apiRequest(`/matches?${queryParams}`);
}

export async function apiGetUserProfile(userId) {
  return apiRequest(`/users/${userId}`);
}

// ==================== Study Group APIs ====================

export async function apiGetGroups(filters = {}) {
  const queryParams = new URLSearchParams(filters).toString();
  return apiRequest(`/groups?${queryParams}`);
}

export async function apiGetGroup(groupId) {
  return apiRequest(`/groups/${groupId}`);
}

export async function apiCreateGroup(groupData) {
  return apiRequest("/groups", {
    method: "POST",
    body: JSON.stringify(groupData),
  });
}

export async function apiUpdateGroup(groupId, updates) {
  return apiRequest(`/groups/${groupId}`, {
    method: "PATCH",
    body: JSON.stringify(updates),
  });
}

export async function apiDeleteGroup(groupId) {
  return apiRequest(`/groups/${groupId}`, {
    method: "DELETE",
  });
}

export async function apiJoinGroup(groupId) {
  return apiRequest(`/groups/${groupId}/join`, {
    method: "POST",
  });
}

export async function apiLeaveGroup(groupId) {
  return apiRequest(`/groups/${groupId}/leave`, {
    method: "DELETE",
  });
}

export async function apiGetMyGroups() {
  return apiRequest("/users/groups");
}

// ==================== Messaging APIs (Future) ====================

export async function apiSendMessage(recipientId, message) {
  return apiRequest("/messages", {
    method: "POST",
    body: JSON.stringify({ recipientId, message }),
  });
}

export async function apiGetMessages(conversationId) {
  return apiRequest(`/messages/${conversationId}`);
}

export async function apiGetConversations() {
  return apiRequest("/messages/conversations");
}

// ==================== Expected Backend Endpoints ====================

/**
 * Flask Backend API Endpoints to Implement:
 *
 * Authentication:
 * POST   /api/auth/signup          - Create new user account
 * POST   /api/auth/login           - Login user
 * POST   /api/auth/logout          - Logout user
 * GET    /api/auth/me              - Get current user info
 *
 * Users:
 * GET    /api/users/:id            - Get user profile
 * PATCH  /api/users/profile        - Update current user profile
 * GET    /api/users/courses        - Get current user's enrolled courses
 * GET    /api/users/groups         - Get current user's groups
 *
 * Courses:
 * GET    /api/courses              - Get all courses (with filters)
 * GET    /api/courses/:id          - Get specific course
 * POST   /api/courses/:id/enroll   - Enroll in course
 * DELETE /api/courses/:id/unenroll - Unenroll from course
 * POST   /api/courses              - Create new course (admin only)
 *
 * Matching:
 * GET    /api/matches              - Get matched students based on courses
 *
 * Groups:
 * GET    /api/groups               - Get all groups (with filters)
 * GET    /api/groups/:id           - Get specific group
 * POST   /api/groups               - Create new group
 * PATCH  /api/groups/:id           - Update group (owner only)
 * DELETE /api/groups/:id           - Delete group (owner only)
 * POST   /api/groups/:id/join      - Join group
 * DELETE /api/groups/:id/leave     - Leave group
 *
 * Messages (Future):
 * GET    /api/messages/conversations      - Get all conversations
 * GET    /api/messages/:conversationId    - Get messages in conversation
 * POST   /api/messages                    - Send message
 */

// ==================== Expected Database Schema ====================

/**
 * MySQL Tables:
 *
 * users:
 *   - id (INT, PRIMARY KEY, AUTO_INCREMENT)
 *   - email (VARCHAR, UNIQUE, NOT NULL)
 *   - password_hash (VARCHAR, NOT NULL)
 *   - name (VARCHAR, NOT NULL)
 *   - major (VARCHAR)
 *   - year (VARCHAR)
 *   - bio (TEXT)
 *   - avatar (VARCHAR)
 *   - created_at (TIMESTAMP)
 *   - updated_at (TIMESTAMP)
 *
 * courses:
 *   - id (VARCHAR, PRIMARY KEY) e.g., 'CS2201'
 *   - code (VARCHAR, NOT NULL) e.g., 'CS 2201'
 *   - name (VARCHAR, NOT NULL)
 *   - section (VARCHAR)
 *   - instructor (VARCHAR)
 *   - schedule (VARCHAR)
 *   - building (VARCHAR)
 *   - room (VARCHAR)
 *   - students (INT)
 *   - created_at (TIMESTAMP)
 *
 * enrollments:
 *   - id (INT, PRIMARY KEY, AUTO_INCREMENT)
 *   - user_id (INT, FOREIGN KEY -> users.id)
 *   - course_id (VARCHAR, FOREIGN KEY -> courses.id)
 *   - enrolled_at (TIMESTAMP)
 *   - UNIQUE(user_id, course_id)
 *
 * study_groups:
 *   - id (INT, PRIMARY KEY, AUTO_INCREMENT)
 *   - name (VARCHAR, NOT NULL)
 *   - course_id (VARCHAR, FOREIGN KEY -> courses.id)
 *   - owner_id (INT, FOREIGN KEY -> users.id)
 *   - description (TEXT)
 *   - meeting_time (VARCHAR)
 *   - location (VARCHAR)
 *   - max_members (INT)
 *   - tags (JSON or separate table)
 *   - created_at (TIMESTAMP)
 *
 * group_members:
 *   - id (INT, PRIMARY KEY, AUTO_INCREMENT)
 *   - group_id (INT, FOREIGN KEY -> study_groups.id)
 *   - user_id (INT, FOREIGN KEY -> users.id)
 *   - joined_at (TIMESTAMP)
 *   - UNIQUE(group_id, user_id)
 *
 * study_preferences (embedded in users or separate table):
 *   - user_id (INT, FOREIGN KEY -> users.id)
 *   - preferred_times (JSON) e.g., ['Morning', 'Evening']
 *   - preferred_locations (JSON) e.g., ['Library', 'Online']
 *   - study_style (VARCHAR) e.g., 'Group Discussion'
 *
 * messages (Future):
 *   - id (INT, PRIMARY KEY, AUTO_INCREMENT)
 *   - sender_id (INT, FOREIGN KEY -> users.id)
 *   - recipient_id (INT, FOREIGN KEY -> users.id)
 *   - message (TEXT)
 *   - read (BOOLEAN)
 *   - created_at (TIMESTAMP)
 */
