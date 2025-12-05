"""
Availability Query API - Read operations for availability (CQRS Query Side)
Handles: Get user availability slots
"""
from flask import Blueprint, jsonify, request
from sqlalchemy import text

from db import engine

bp_availability_queries = Blueprint("availability_queries", __name__)


@bp_availability_queries.get("/<int:user_id>")
def get_user_availability(user_id: int):
    """Get all availability slots for a user"""
    try:
        with engine.connect() as conn:
            # Check if user exists
            user = conn.execute(
                text("SELECT id FROM users WHERE id = :uid"),
                {"uid": user_id}
            ).first()
            
            if not user:
                return jsonify({"error": "User not found"}), 404

            slots = conn.execute(
                text(
                    """
                    SELECT id, slot, created_at
                    FROM availability_text
                    WHERE user_id = :uid
                    ORDER BY created_at
                    """
                ),
                {"uid": user_id}
            ).mappings().all()

        return jsonify([dict(s) for s in slots]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
