"""
Users Query API - Read operations for users (CQRS Query Side)
Handles: Get user, List users
"""
from flask import Blueprint, jsonify, request
from sqlalchemy import text

from db import engine

bp_users_queries = Blueprint("users_queries_detail", __name__)


@bp_users_queries.get("/<int:user_id>")
def get_user(user_id: int):
    """Get user profile by ID"""
    try:
        with engine.connect() as conn:
            user = conn.execute(
                text(
                    """
                    SELECT id, email, name, major, year, avatar, bio, created_at
                    FROM users WHERE id = :uid
                    """
                ),
                {"uid": user_id}
            ).mappings().first()

            if not user:
                return jsonify({"error": "User not found"}), 404

        return jsonify(dict(user)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_users_queries.get("")
def list_users():
    """List all users with optional filtering"""
    major = request.args.get("major")
    year = request.args.get("year")
    
    try:
        query = "SELECT id, email, name, major, year, avatar FROM users WHERE 1=1"
        params = {}
        
        if major:
            query += " AND major = :major"
            params["major"] = major
        
        if year:
            query += " AND year = :year"
            params["year"] = year
        
        query += " ORDER BY name"
        
        with engine.connect() as conn:
            rows = conn.execute(text(query), params).mappings().all()

        return jsonify([dict(r) for r in rows]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
