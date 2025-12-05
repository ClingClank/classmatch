"""
Notifications Query API - Read operations for notifications (CQRS Query Side)
Handles: Get notifications, Get unread count
"""
from flask import Blueprint, jsonify, request
from sqlalchemy import text

from db import engine

bp_notifications_queries = Blueprint("notifications_queries", __name__)


@bp_notifications_queries.get("/<int:user_id>")
def get_user_notifications(user_id: int):
    """Get all notifications for a user"""
    unread_only = request.args.get("unread_only", "false").lower() == "true"
    
    try:
        query = """
            SELECT id, type, data, is_read, created_at
            FROM notifications
            WHERE user_id = :uid
        """
        
        if unread_only:
            query += " AND is_read = 0"
        
        query += " ORDER BY created_at DESC"
        
        with engine.connect() as conn:
            # Check if user exists
            user = conn.execute(
                text("SELECT id FROM users WHERE id = :uid"),
                {"uid": user_id}
            ).first()
            
            if not user:
                return jsonify({"error": "User not found"}), 404

            notifications = conn.execute(
                text(query),
                {"uid": user_id}
            ).mappings().all()

        return jsonify([dict(n) for n in notifications]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_notifications_queries.get("/<int:user_id>/count")
def get_unread_count(user_id: int):
    """Get count of unread notifications for a user"""
    try:
        with engine.connect() as conn:
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
                    SELECT COUNT(*) as unread_count
                    FROM notifications
                    WHERE user_id = :uid AND is_read = 0
                    """
                ),
                {"uid": user_id}
            ).mappings().first()

        return jsonify({"unread_count": result["unread_count"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
