"""
Messages Command API - Write operations for messages (CQRS Command Side)
Handles: Create, Update, Delete messages
"""
from flask import Blueprint, jsonify, request
from sqlalchemy import text

from db import engine
from domain.event_bus import event_bus
from domain.events import GroupMessagePosted

bp_messages_commands = Blueprint("messages_commands", __name__)


@bp_messages_commands.post("")
def post_message():
    """Post a message in a group"""
    data = request.get_json(force=True)
    group_id = data.get("group_id")
    user_id = data.get("user_id")
    content = data.get("content")

    if not (group_id and user_id and content):
        return jsonify({"error": "group_id, user_id and content are required"}), 400

    try:
        with engine.begin() as conn:
            mres = conn.execute(
                text(
                    """
                    INSERT INTO messages (group_id, user_id, content)
                    VALUES (:gid, :uid, :content)
                    """
                ),
                {"gid": group_id, "uid": user_id, "content": content},
            )
            message_id = mres.lastrowid

        event_bus.publish(
            GroupMessagePosted(
                group_id=group_id,
                user_id=user_id,
                message_id=message_id,
            )
        )
        return jsonify({"ok": True, "message_id": message_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_messages_commands.delete("/<int:message_id>")
def delete_message(message_id: int):
    """Delete a specific message"""
    try:
        with engine.begin() as conn:
            result = conn.execute(
                text("DELETE FROM messages WHERE id = :mid"),
                {"mid": message_id}
            )
            
            if result.rowcount == 0:
                return jsonify({"error": "Message not found"}), 404

        return jsonify({"ok": True, "message": "Message deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
