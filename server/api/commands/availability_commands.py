"""
Availability Command API - Write operations for availability (CQRS Command Side)
Handles: Add, Delete, Update availability slots
"""
from flask import Blueprint, jsonify, request
from sqlalchemy import text

from db import engine

bp_availability_commands = Blueprint("availability_commands", __name__)


@bp_availability_commands.post("/<int:user_id>")
def add_availability_slot(user_id: int):
    """Add a new availability slot for a user"""
    data = request.get_json(force=True)
    slot = data.get("slot")

    if not slot:
        return jsonify({"error": "slot is required"}), 400

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
                    INSERT INTO availability_text (user_id, slot)
                    VALUES (:uid, :slot)
                    """
                ),
                {"uid": user_id, "slot": slot}
            )
            slot_id = result.lastrowid

        return jsonify({"ok": True, "slot_id": slot_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_availability_commands.delete("/<int:user_id>/<int:slot_id>")
def delete_availability_slot(user_id: int, slot_id: int):
    """Delete a specific availability slot"""
    try:
        with engine.begin() as conn:
            result = conn.execute(
                text(
                    """
                    DELETE FROM availability_text
                    WHERE id = :sid AND user_id = :uid
                    """
                ),
                {"sid": slot_id, "uid": user_id}
            )
            
            if result.rowcount == 0:
                return jsonify({"error": "Availability slot not found"}), 404

        return jsonify({"ok": True, "message": "Availability slot deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_availability_commands.put("/<int:user_id>")
def update_all_availability(user_id: int):
    """Replace all availability slots for a user"""
    data = request.get_json(force=True)
    slots = data.get("slots")  # Array of slot strings

    if not isinstance(slots, list):
        return jsonify({"error": "slots must be an array"}), 400

    try:
        with engine.begin() as conn:
            # Check if user exists
            user = conn.execute(
                text("SELECT id FROM users WHERE id = :uid"),
                {"uid": user_id}
            ).first()
            
            if not user:
                return jsonify({"error": "User not found"}), 404

            # Delete existing slots
            conn.execute(
                text("DELETE FROM availability_text WHERE user_id = :uid"),
                {"uid": user_id}
            )

            # Insert new slots
            for slot in slots:
                if slot:  # Skip empty strings
                    conn.execute(
                        text(
                            """
                            INSERT INTO availability_text (user_id, slot)
                            VALUES (:uid, :slot)
                            """
                        ),
                        {"uid": user_id, "slot": slot}
                    )

        return jsonify({"ok": True, "message": "Availability updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
