from flask import Flask, jsonify
from flask_cors import CORS

# CQRS Command APIs (Write operations)
from api.commands.groups_commands import bp_groups_commands
from api.commands.messages_commands import bp_messages_commands
from api.commands.users_commands import bp_users_commands
from api.commands.courses_commands import bp_courses_commands
from api.commands.availability_commands import bp_availability_commands
from api.commands.notifications_commands import bp_notifications_commands

# CQRS Query APIs (Read operations)
from api.queries.groups_queries import bp_groups_queries
from api.queries.users_queries import bp_users_queries
from api.queries.users_queries_detail import bp_users_queries as bp_users_queries_detail
from api.queries.courses_queries import bp_courses_queries
from api.queries.availability_queries import bp_availability_queries
from api.queries.notifications_queries import bp_notifications_queries
from api.queries.messages_queries import bp_messages_queries

from domain.event_bus import event_bus
from domain.handlers import register_handlers


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register CQRS Command blueprints (Write operations)
    app.register_blueprint(bp_groups_commands, url_prefix="/api/commands/groups")
    app.register_blueprint(bp_messages_commands, url_prefix="/api/commands/messages")
    app.register_blueprint(bp_users_commands, url_prefix="/api/commands/users")
    app.register_blueprint(bp_courses_commands, url_prefix="/api/commands/courses")
    app.register_blueprint(bp_availability_commands, url_prefix="/api/commands/availability")
    app.register_blueprint(bp_notifications_commands, url_prefix="/api/commands/notifications")

    # Register CQRS Query blueprints (Read operations)
    app.register_blueprint(bp_groups_queries, url_prefix="/api/queries/groups")
    app.register_blueprint(bp_users_queries, url_prefix="/api/queries/users")
    app.register_blueprint(bp_users_queries_detail, url_prefix="/api/queries/users/detail")
    app.register_blueprint(bp_courses_queries, url_prefix="/api/queries/courses")
    app.register_blueprint(bp_availability_queries, url_prefix="/api/queries/availability")
    app.register_blueprint(bp_notifications_queries, url_prefix="/api/queries/notifications")
    app.register_blueprint(bp_messages_queries, url_prefix="/api/queries/messages")

    register_handlers(event_bus)

    @app.get("/health")
    def health_root():
        return jsonify({"ok": True, "message": "Flask server is running"}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
