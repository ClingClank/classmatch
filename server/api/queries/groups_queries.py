"""
Groups Query API - Read operations for groups (CQRS Query Side)
Handles: List, Get details, Search groups
"""
from flask import Blueprint, jsonify, request
from sqlalchemy import text

from db import engine

bp_groups_queries = Blueprint("groups_queries", __name__)


@bp_groups_queries.get("")
def list_groups():
    """Returns a list of groups with basic information"""
    course_id = request.args.get("course_id")
    
    try:
        query = """
            SELECT g.id, g.name, g.description,
                   g.meeting_time, g.location, g.max_members,
                   c.code AS course_code, c.name AS course_name,
                   u.name AS owner_name,
                   COUNT(gm.user_id) as member_count
            FROM `groups` g
            JOIN courses c ON g.course_id = c.id
            JOIN users u ON g.owner_user_id = u.id
            LEFT JOIN group_members gm ON g.id = gm.group_id AND gm.status = 'active'
            WHERE g.is_archived = 0
        """
        params = {}
        
        if course_id:
            query += " AND g.course_id = :course_id"
            params["course_id"] = course_id
        
        query += " GROUP BY g.id, g.name, g.description, g.meeting_time, g.location, g.max_members, c.code, c.name, u.name"
        query += " ORDER BY g.created_at DESC"
        
        with engine.connect() as conn:
            rows = conn.execute(text(query), params).mappings().all()
        
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_groups_queries.get("/<int:group_id>")
def get_group_detail(group_id: int):
    """Returns detailed information for a specific group including members and recent messages"""
    try:
        with engine.connect() as conn:
            g = conn.execute(
                text(
                    """
                    SELECT g.id, g.name, g.description,
                           g.meeting_time, g.location, g.max_members,
                           g.tags, g.created_at,
                           c.id AS course_id, c.code AS course_code, c.name AS course_name,
                           u.id AS owner_id, u.name AS owner_name
                    FROM `groups` g
                    JOIN courses c ON g.course_id = c.id
                    JOIN users u ON g.owner_user_id = u.id
                    WHERE g.id = :gid
                    """
                ),
                {"gid": group_id},
            ).mappings().first()

            if not g:
                return jsonify({"error": "Group not found"}), 404

            members = conn.execute(
                text(
                    """
                    SELECT u.id, u.name, u.email, u.avatar, u.major, u.year,
                           gm.role, gm.status, gm.joined_at
                    FROM group_members gm
                    JOIN users u ON gm.user_id = u.id
                    WHERE gm.group_id = :gid
                    ORDER BY 
                        CASE WHEN gm.role = 'admin' THEN 0 ELSE 1 END,
                        gm.joined_at
                    """
                ),
                {"gid": group_id},
            ).mappings().all()

            msgs = conn.execute(
                text(
                    """
                    SELECT m.id, m.content, m.created_at, 
                           u.id AS user_id, u.name AS author_name, u.avatar AS author_avatar
                    FROM messages m
                    JOIN users u ON m.user_id = u.id
                    WHERE m.group_id = :gid
                    ORDER BY m.created_at DESC
                    LIMIT 50
                    """
                ),
                {"gid": group_id},
            ).mappings().all()

        data = dict(g)
        data["members"] = [dict(m) for m in members]
        data["messages"] = [dict(m) for m in msgs]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_groups_queries.get("/<int:group_id>/members")
def get_group_members(group_id: int):
    """Get all members of a specific group"""
    try:
        with engine.connect() as conn:
            # Check if group exists
            group = conn.execute(
                text("SELECT id FROM `groups` WHERE id = :gid"),
                {"gid": group_id}
            ).first()
            
            if not group:
                return jsonify({"error": "Group not found"}), 404

            members = conn.execute(
                text(
                    """
                    SELECT u.id, u.name, u.email, u.avatar, u.major, u.year,
                           gm.role, gm.status, gm.joined_at
                    FROM group_members gm
                    JOIN users u ON gm.user_id = u.id
                    WHERE gm.group_id = :gid
                    ORDER BY 
                        CASE WHEN gm.role = 'admin' THEN 0 ELSE 1 END,
                        gm.joined_at
                    """
                ),
                {"gid": group_id}
            ).mappings().all()

        return jsonify([dict(m) for m in members]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_groups_queries.get("/<int:group_id>/messages")
def get_group_messages(group_id: int):
    """Get all messages for a specific group"""
    limit = request.args.get("limit", 50, type=int)
    offset = request.args.get("offset", 0, type=int)
    
    try:
        with engine.connect() as conn:
            # Check if group exists
            group = conn.execute(
                text("SELECT id FROM `groups` WHERE id = :gid"),
                {"gid": group_id}
            ).first()
            
            if not group:
                return jsonify({"error": "Group not found"}), 404

            messages = conn.execute(
                text(
                    """
                    SELECT m.id, m.content, m.created_at,
                           u.id AS user_id, u.name AS author_name, u.avatar AS author_avatar
                    FROM messages m
                    JOIN users u ON m.user_id = u.id
                    WHERE m.group_id = :gid
                    ORDER BY m.created_at DESC
                    LIMIT :limit OFFSET :offset
                    """
                ),
                {"gid": group_id, "limit": limit, "offset": offset}
            ).mappings().all()

        return jsonify([dict(m) for m in messages]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
