"""
Courses Query API - Read operations for courses (CQRS Query Side)
Handles: List courses, Get course detail, Get students, Get groups
"""
from flask import Blueprint, jsonify, request
from sqlalchemy import text

from db import engine

bp_courses_queries = Blueprint("courses_queries", __name__)


@bp_courses_queries.get("")
def list_courses():
    """List all courses with optional search/filter"""
    search = request.args.get("search")  # Search in code or name
    instructor = request.args.get("instructor")
    
    try:
        query = """
            SELECT id, code, name, section, instructor, schedule, 
                   students, building, room
            FROM courses
            WHERE 1=1
        """
        params = {}
        
        if search:
            query += " AND (code LIKE :search OR name LIKE :search)"
            params["search"] = f"%{search}%"
        
        if instructor:
            query += " AND instructor LIKE :instructor"
            params["instructor"] = f"%{instructor}%"
        
        query += " ORDER BY code, section"
        
        with engine.connect() as conn:
            rows = conn.execute(text(query), params).mappings().all()

        return jsonify([dict(r) for r in rows]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_courses_queries.get("/<course_id>")
def get_course(course_id: str):
    """Get detailed course information"""
    try:
        with engine.connect() as conn:
            course = conn.execute(
                text(
                    """
                    SELECT id, code, name, section, instructor, schedule,
                           students, building, room
                    FROM courses WHERE id = :cid
                    """
                ),
                {"cid": course_id}
            ).mappings().first()

            if not course:
                return jsonify({"error": "Course not found"}), 404

            # Get enrolled students count
            enrolled_count = conn.execute(
                text(
                    "SELECT COUNT(*) as count FROM enrollments WHERE course_id = :cid"
                ),
                {"cid": course_id}
            ).mappings().first()

        result = dict(course)
        result["enrolled_count"] = enrolled_count["count"]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_courses_queries.get("/<course_id>/students")
def get_course_students(course_id: str):
    """Get list of students enrolled in a course"""
    try:
        with engine.connect() as conn:
            # Check if course exists
            course = conn.execute(
                text("SELECT id FROM courses WHERE id = :cid"),
                {"cid": course_id}
            ).first()
            
            if not course:
                return jsonify({"error": "Course not found"}), 404

            students = conn.execute(
                text(
                    """
                    SELECT u.id, u.name, u.email, u.major, u.year, u.avatar,
                           e.enrolled_at
                    FROM enrollments e
                    JOIN users u ON e.user_id = u.id
                    WHERE e.course_id = :cid
                    ORDER BY u.name
                    """
                ),
                {"cid": course_id}
            ).mappings().all()

        return jsonify([dict(s) for s in students]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_courses_queries.get("/<course_id>/groups")
def get_course_groups(course_id: str):
    """Get all study groups for a specific course"""
    try:
        with engine.connect() as conn:
            groups = conn.execute(
                text(
                    """
                    SELECT g.id, g.name, g.description, g.meeting_time, 
                           g.location, g.max_members, g.created_at,
                           u.name as owner_name,
                           COUNT(gm.user_id) as member_count
                    FROM `groups` g
                    JOIN users u ON g.owner_user_id = u.id
                    LEFT JOIN group_members gm ON g.id = gm.group_id AND gm.status = 'active'
                    WHERE g.course_id = :cid AND g.is_archived = 0
                    GROUP BY g.id, g.name, g.description, g.meeting_time, 
                             g.location, g.max_members, g.created_at, u.name
                    ORDER BY g.created_at DESC
                    """
                ),
                {"cid": course_id}
            ).mappings().all()

        return jsonify([dict(g) for g in groups]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
