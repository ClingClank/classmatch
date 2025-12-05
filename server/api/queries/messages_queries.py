"""
Messages Query API - Read operations for messages (CQRS Query Side)
Handles: Get group messages, Get message detail
"""
from flask import Blueprint, jsonify, request
from sqlalchemy import text

from db import engine

bp_messages_queries = Blueprint("messages_queries", __name__)


@bp_messages_queries.get("/group/<int:group_id>")
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
                    SELECT m.id, m.content, m.posted_at,
                           u.id as user_id, u.name as user_name, u.avatar as user_avatar
                    FROM messages m
                    JOIN users u ON m.user_id = u.id
                    WHERE m.group_id = :gid
                    ORDER BY m.posted_at DESC
                    LIMIT :limit OFFSET :offset
                    """
                ),
                {"gid": group_id, "limit": limit, "offset": offset}
            ).mappings().all()

        return jsonify([dict(m) for m in messages]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_messages_queries.get("/<int:message_id>")
def get_message(message_id: int):
    """Get a specific message detail"""
    try:
        with engine.connect() as conn:
            message = conn.execute(
                text(
                    """
                    SELECT m.id, m.group_id, m.content, m.posted_at,
                           u.id as user_id, u.name as user_name, u.avatar as user_avatar
                    FROM messages m
                    JOIN users u ON m.user_id = u.id
                    WHERE m.id = :mid
                    """
                ),
                {"mid": message_id}
            ).mappings().first()

            if not message:
                return jsonify({"error": "Message not found"}), 404

        return jsonify(dict(message)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
