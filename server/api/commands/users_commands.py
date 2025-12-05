"""
Users Command API - Write operations for users (CQRS Command Side)
Handles: Register, Login, Update, Delete
"""
from flask import Blueprint, jsonify, request
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash

from db import engine

bp_users_commands = Blueprint("users_commands", __name__)


@bp_users_commands.post("/register")
def register_user():
    """Register a new user account"""
    data = request.get_json(force=True)
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    major = data.get("major")
    year = data.get("year")
    bio = data.get("bio")

    if not (email and password and name):
        return jsonify({"error": "email, password, and name are required"}), 400

    try:
        password_hash = generate_password_hash(password)
        
        with engine.begin() as conn:
            # Check if email already exists
            existing = conn.execute(
                text("SELECT id FROM users WHERE email = :email"),
                {"email": email}
            ).first()
            
            if existing:
                return jsonify({"error": "Email already registered"}), 409
            
            result = conn.execute(
                text(
                    """
                    INSERT INTO users (email, password_hash, name, major, year, bio)
                    VALUES (:email, :password_hash, :name, :major, :year, :bio)
                    """
                ),
                {
                    "email": email,
                    "password_hash": password_hash,
                    "name": name,
                    "major": major,
                    "year": year,
                    "bio": bio,
                },
            )
            user_id = result.lastrowid

        return jsonify({"ok": True, "user_id": user_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_users_commands.post("/login")
def login_user():
    """Authenticate user and return user info"""
    data = request.get_json(force=True)
    email = data.get("email")
    password = data.get("password")

    if not (email and password):
        return jsonify({"error": "email and password are required"}), 400

    try:
        with engine.connect() as conn:
            user = conn.execute(
                text(
                    """
                    SELECT id, email, password_hash, name, major, year, avatar, bio
                    FROM users WHERE email = :email
                    """
                ),
                {"email": email}
            ).mappings().first()

            if not user:
                return jsonify({"error": "Invalid credentials"}), 401

            if not check_password_hash(user["password_hash"], password):
                return jsonify({"error": "Invalid credentials"}), 401

            # Return user info without password hash
            user_data = {
                "id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "major": user["major"],
                "year": user["year"],
                "avatar": user["avatar"],
                "bio": user["bio"],
            }

        return jsonify({"ok": True, "user": user_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_users_commands.put("/<int:user_id>")
def update_user(user_id: int):
    """Update user profile"""
    data = request.get_json(force=True)
    
    # Build dynamic update query based on provided fields
    allowed_fields = ["name", "major", "year", "avatar", "bio", "study_prefs"]
    update_fields = []
    params = {"uid": user_id}
    
    for field in allowed_fields:
        if field in data:
            update_fields.append(f"{field} = :{field}")
            params[field] = data[field]
    
    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400

    try:
        with engine.begin() as conn:
            # Check user exists
            exists = conn.execute(
                text("SELECT id FROM users WHERE id = :uid"),
                {"uid": user_id}
            ).first()
            
            if not exists:
                return jsonify({"error": "User not found"}), 404
            
            query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = :uid"
            conn.execute(text(query), params)

        return jsonify({"ok": True, "message": "User updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_users_commands.delete("/<int:user_id>")
def delete_user(user_id: int):
    """Delete user account"""
    try:
        with engine.begin() as conn:
            result = conn.execute(
                text("DELETE FROM users WHERE id = :uid"),
                {"uid": user_id}
            )
            
            if result.rowcount == 0:
                return jsonify({"error": "User not found"}), 404

        return jsonify({"ok": True, "message": "User deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
