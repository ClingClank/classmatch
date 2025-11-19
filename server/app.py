from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database connection string
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "classmatch")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)


@app.route("/health")
def health():
    """Simple health check."""
    return jsonify({"ok": True, "message": "Flask server is running"}), 200


@app.route("/courses", methods=["GET"])
def get_courses():
    """Fetch all courses."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, code, name, section, instructor FROM courses"))
            courses = [dict(row) for row in result.mappings()]
        return jsonify(courses)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/users", methods=["GET"])
def get_users():
    """Return all users (safe subset)."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, email, name, major, year FROM users"))
            users = [dict(row) for row in result.mappings()]
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/groups", methods=["GET"])
def get_groups():
    """Return all groups with course name and owner."""
    try:
        query = text("""
            SELECT g.id, g.name, g.description, g.meeting_time, g.location, g.max_members,
                   g.tags, c.code AS course_code, u.name AS owner_name
            FROM `groups` g
            JOIN courses c ON g.course_id = c.id
            JOIN users u ON g.owner_user_id = u.id
        """)
        with engine.connect() as conn:
            result = conn.execute(query)
            groups = [dict(row) for row in result.mappings()]
        return jsonify(groups)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/groups/<int:group_id>", methods=["GET"])
def get_group_details(group_id):
    """Fetch group details and members."""
    try:
        with engine.connect() as conn:
            group_q = text("""
                SELECT g.id, g.name, g.description, g.meeting_time, g.location, g.max_members,
                       g.tags, c.name AS course_name, u.name AS owner_name
                FROM `groups` g
                JOIN courses c ON g.course_id = c.id
                JOIN users u ON g.owner_user_id = u.id
                WHERE g.id = :gid
            """)
            group = conn.execute(group_q, {"gid": group_id}).mappings().first()

            if not group:
                return jsonify({"error": "Group not found"}), 404

            members_q = text("""
                SELECT u.name, u.email, gm.role, gm.status
                FROM group_members gm
                JOIN users u ON gm.user_id = u.id
                WHERE gm.group_id = :gid
            """)
            members = [dict(row) for row in conn.execute(members_q, {"gid": group_id}).mappings()]

        group_data = dict(group)
        group_data["members"] = members
        return jsonify(group_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/join", methods=["POST"])
def join_group():
    """Join an existing group."""
    data = request.get_json()
    user_id = data.get("user_id")
    group_id = data.get("group_id")

    if not user_id or not group_id:
        return jsonify({"error": "Missing user_id or group_id"}), 400

    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO group_members (group_id, user_id, role, status) VALUES (:gid, :uid, 'member', 'active')"),
                {"gid": group_id, "uid": user_id},
            )
        return jsonify({"ok": True, "message": "User joined group"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/create_group", methods=["POST"])
def create_group():
    """Create a new study group."""
    data = request.get_json()
    owner_user_id = data.get("owner_user_id")
    course_id = data.get("course_id")
    name = data.get("name")
    description = data.get("description", "")
    meeting_time = data.get("meeting_time", "")
    location = data.get("location", "")
    max_members = data.get("max_members", 5)
    tags = data.get("tags", [])

    if not (owner_user_id and course_id and name):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        with engine.begin() as conn:
            result = conn.execute(
                text("""
                    INSERT INTO `groups` 
                    (owner_user_id, course_id, name, description, meeting_time, location, max_members, tags)
                    VALUES (:owner_user_id, :course_id, :name, :description, :meeting_time, :location, :max_members, JSON_ARRAY(:tags))
                """),
                {
                    "owner_user_id": owner_user_id,
                    "course_id": course_id,
                    "name": name,
                    "description": description,
                    "meeting_time": meeting_time,
                    "location": location,
                    "max_members": max_members,
                    "tags": ",".join(tags),
                },
            )
            new_id = result.lastrowid
        return jsonify({"ok": True, "group_id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
