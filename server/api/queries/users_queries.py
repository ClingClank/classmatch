"""
Users Query API - Read operations for users (CQRS Query Side)
Handles: Get user details, overview, matches, search
"""
from flask import Blueprint, jsonify, request
from sqlalchemy import text

from db import engine

bp_users_queries = Blueprint("users_queries", __name__)


@bp_users_queries.get("/<int:user_id>/overview")
def get_user_overview(user_id: int):
    """Returns a user's basic profile, their availability, and enrolled courses"""
    try:
        with engine.connect() as conn:
            user = conn.execute(
                text(
                    """
                    SELECT id, email, name, major, year, avatar, bio, 
                           study_prefs, created_at
                    FROM users WHERE id = :uid
                    """
                ),
                {"uid": user_id},
            ).mappings().first()

            if not user:
                return jsonify({"error": "User not found"}), 404

            avail = conn.execute(
                text(
                    """
                    SELECT id, slot, created_at
                    FROM availability_text 
                    WHERE user_id = :uid 
                    ORDER BY created_at
                    """
                ),
                {"uid": user_id},
            ).mappings().all()

            courses = conn.execute(
                text(
                    """
                    SELECT c.id, c.code, c.name, c.instructor, c.schedule,
                           e.enrolled_at
                    FROM enrollments e
                    JOIN courses c ON e.course_id = c.id
                    WHERE e.user_id = :uid
                    ORDER BY c.code
                    """
                ),
                {"uid": user_id},
            ).mappings().all()

        return jsonify(
            {
                "user": dict(user),
                "availability": [dict(a) for a in avail],
                "courses": [dict(c) for c in courses],
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_users_queries.get("/<int:user_id>/matches")
def get_user_matches(user_id: int):
    """Finds other users who share enrolled courses with the given user"""
    try:
        with engine.connect() as conn:
            user_exists = conn.execute(
                text("SELECT id FROM users WHERE id = :uid"),
                {"uid": user_id},
            ).first()
            if not user_exists:
                return jsonify({"error": "User not found"}), 404

            q = text(
                """
                WITH user_courses AS (
                    SELECT course_id
                    FROM enrollments
                    WHERE user_id = :uid
                )
                SELECT u.id, u.name, u.email, u.avatar, u.major, u.year,
                       COUNT(*) AS shared_courses,
                       GROUP_CONCAT(c.code ORDER BY c.code SEPARATOR ', ') AS shared_course_codes
                FROM enrollments e
                JOIN user_courses uc ON e.course_id = uc.course_id
                JOIN users u ON e.user_id = u.id
                JOIN courses c ON e.course_id = c.id
                WHERE e.user_id <> :uid
                GROUP BY u.id, u.name, u.email, u.avatar, u.major, u.year
                ORDER BY shared_courses DESC, u.name
                LIMIT 50
                """
            )
            rows = conn.execute(q, {"uid": user_id}).mappings().all()

        matches = [dict(r) for r in rows]
        return jsonify({"matches": matches})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_users_queries.get("/<int:user_id>/groups")
def get_user_groups(user_id: int):
    """Get all groups that a user is a member of"""
    try:
        with engine.connect() as conn:
            user_exists = conn.execute(
                text("SELECT id FROM users WHERE id = :uid"),
                {"uid": user_id}
            ).first()
            
            if not user_exists:
                return jsonify({"error": "User not found"}), 404

            groups = conn.execute(
                text(
                    """
                    SELECT g.id, g.name, g.description, g.meeting_time, g.location,
                           c.code AS course_code, c.name AS course_name,
                           u.name AS owner_name,
                           gm.role, gm.joined_at,
                           COUNT(DISTINCT gm2.user_id) as member_count
                    FROM group_members gm
                    JOIN `groups` g ON gm.group_id = g.id
                    JOIN courses c ON g.course_id = c.id
                    JOIN users u ON g.owner_user_id = u.id
                    LEFT JOIN group_members gm2 ON g.id = gm2.group_id AND gm2.status = 'active'
                    WHERE gm.user_id = :uid AND gm.status = 'active' AND g.is_archived = 0
                    GROUP BY g.id, g.name, g.description, g.meeting_time, g.location,
                             c.code, c.name, u.name, gm.role, gm.joined_at
                    ORDER BY gm.joined_at DESC
                    """
                ),
                {"uid": user_id}
            ).mappings().all()

        return jsonify([dict(g) for g in groups]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_users_queries.get("/search")
def search_users():
    """Search users by name, email, major, or year"""
    query_str = request.args.get("q", "").strip()
    major = request.args.get("major")
    year = request.args.get("year")
    limit = request.args.get("limit", 20, type=int)
    
    try:
        query = """
            SELECT id, name, email, avatar, major, year, bio
            FROM users
            WHERE 1=1
        """
        params = {}
        
        if query_str:
            query += " AND (name LIKE :search OR email LIKE :search)"
            params["search"] = f"%{query_str}%"
        
        if major:
            query += " AND major = :major"
            params["major"] = major
        
        if year:
            query += " AND year = :year"
            params["year"] = year
        
        query += " ORDER BY name LIMIT :limit"
        params["limit"] = limit
        
        with engine.connect() as conn:
            rows = conn.execute(text(query), params).mappings().all()

        return jsonify([dict(r) for r in rows]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
