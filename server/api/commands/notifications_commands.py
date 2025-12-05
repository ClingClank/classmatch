"""
Notifications Command API - Write operations for notifications (CQRS Command Side)
Handles: Create, Mark as read, Delete
"""
from flask import Blueprint, jsonify, request
from sqlalchemy import text

from db import engine

bp_notifications_commands = Blueprint("notifications_commands", __name__)


@bp_notifications_commands.post("/<int:user_id>")
def create_notification(user_id: int):
    """Create a new notification for a user"""
    data = request.get_json(force=True)
    notif_type = data.get("type")
    notif_data = data.get("data")

    if not notif_type:
        return jsonify({"error": "type is required"}), 400

    try:
        with engine.begin() as conn:
            # Check if user exists
            user = conn.execute(
                text("SELECT id FROM users WHERE id = :uid"),
                {"uid": user_id}
            ).first()
            
            if not user:
                return jsonify({"error": "User not found"}), 404

            result = conn.execute(
                text(
                    """
                    INSERT INTO notifications (user_id, type, data)
                    VALUES (:uid, :type, :data)
                    """
                ),
                {"uid": user_id, "type": notif_type, "data": notif_data}
            )
            notification_id = result.lastrowid

        return jsonify({"ok": True, "notification_id": notification_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_notifications_commands.patch("/<int:user_id>/<int:notification_id>/read")
def mark_notification_read(user_id: int, notification_id: int):
    """Mark a notification as read"""
    try:
        with engine.begin() as conn:
            result = conn.execute(
                text(
                    """
                    UPDATE notifications
                    SET is_read = 1
                    WHERE id = :nid AND user_id = :uid
                    """
                ),
                {"nid": notification_id, "uid": user_id}
            )
            
            if result.rowcount == 0:
                return jsonify({"error": "Notification not found"}), 404

        return jsonify({"ok": True, "message": "Notification marked as read"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_notifications_commands.patch("/<int:user_id>/read-all")
def mark_all_notifications_read(user_id: int):
    """Mark all notifications as read for a user"""
    try:
        with engine.begin() as conn:
            # Check if user exists
            user = conn.execute(
                text("SELECT id FROM users WHERE id = :uid"),
                {"uid": user_id}
            ).first()
            
            if not user:
                return jsonify({"error": "User not found"}), 404

            result = conn.execute(
                text(
                    """
                    UPDATE notifications
                    SET is_read = 1
                    WHERE user_id = :uid AND is_read = 0
                    """
                ),
                {"uid": user_id}
            )

        return jsonify({"ok": True, "updated_count": result.rowcount}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_notifications_commands.delete("/<int:user_id>/<int:notification_id>")
def delete_notification(user_id: int, notification_id: int):
    """Delete a specific notification"""
    try:
        with engine.begin() as conn:
            result = conn.execute(
                text(
                    """
                    DELETE FROM notifications
                    WHERE id = :nid AND user_id = :uid
                    """
                ),
                {"nid": notification_id, "uid": user_id}
            )
            
            if result.rowcount == 0:
                return jsonify({"error": "Notification not found"}), 404

        return jsonify({"ok": True, "message": "Notification deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
