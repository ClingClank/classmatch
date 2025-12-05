"""
Courses Command API - Write operations for courses (CQRS Command Side)
Handles: Create, Enroll, Unenroll
"""
from flask import Blueprint, jsonify, request
from sqlalchemy import text

from db import engine

bp_courses_commands = Blueprint("courses_commands", __name__)


@bp_courses_commands.post("")
def create_course():
    """Create a new course (admin operation)"""
    data = request.get_json(force=True)
    course_id = data.get("id")
    code = data.get("code")
    name = data.get("name")
    section = data.get("section")
    instructor = data.get("instructor")
    schedule = data.get("schedule")
    students = data.get("students", 0)
    building = data.get("building")
    room = data.get("room")

    if not all([course_id, code, name, section, instructor, schedule]):
        return jsonify({"error": "id, code, name, section, instructor, and schedule are required"}), 400

    try:
        with engine.begin() as conn:
            conn.execute(
                text(
                    """
                    INSERT INTO courses 
                    (id, code, name, section, instructor, schedule, students, building, room)
                    VALUES (:id, :code, :name, :section, :instructor, :schedule, :students, :building, :room)
                    """
                ),
                {
                    "id": course_id,
                    "code": code,
                    "name": name,
                    "section": section,
                    "instructor": instructor,
                    "schedule": schedule,
                    "students": students,
                    "building": building,
                    "room": room,
                }
            )

        return jsonify({"ok": True, "course_id": course_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_courses_commands.post("/<course_id>/enroll")
def enroll_in_course(course_id: str):
    """Enroll a user in a course"""
    data = request.get_json(force=True)
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    try:
        with engine.begin() as conn:
            # Check if course exists
            course = conn.execute(
                text("SELECT id FROM courses WHERE id = :cid"),
                {"cid": course_id}
            ).first()
            
            if not course:
                return jsonify({"error": "Course not found"}), 404

            # Check if user exists
            user = conn.execute(
                text("SELECT id FROM users WHERE id = :uid"),
                {"uid": user_id}
            ).first()
            
            if not user:
                return jsonify({"error": "User not found"}), 404

            # Check if already enrolled
            existing = conn.execute(
                text(
                    "SELECT user_id FROM enrollments WHERE user_id = :uid AND course_id = :cid"
                ),
                {"uid": user_id, "cid": course_id}
            ).first()
            
            if existing:
                return jsonify({"error": "Already enrolled in this course"}), 409

            conn.execute(
                text(
                    "INSERT INTO enrollments (user_id, course_id) VALUES (:uid, :cid)"
                ),
                {"uid": user_id, "cid": course_id}
            )

        return jsonify({"ok": True, "message": "Enrolled successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_courses_commands.delete("/<course_id>/enroll")
def unenroll_from_course(course_id: str):
    """Unenroll a user from a course"""
    data = request.get_json(force=True)
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    try:
        with engine.begin() as conn:
            result = conn.execute(
                text(
                    "DELETE FROM enrollments WHERE user_id = :uid AND course_id = :cid"
                ),
                {"uid": user_id, "cid": course_id}
            )
            
            if result.rowcount == 0:
                return jsonify({"error": "Enrollment not found"}), 404

        return jsonify({"ok": True, "message": "Unenrolled successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
