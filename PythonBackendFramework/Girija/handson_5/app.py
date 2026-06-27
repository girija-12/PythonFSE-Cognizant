from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from extensions import db

# Task 1: Define SQLAlchemy Models and Migrations

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from courses.routes import courses_bp
    app.register_blueprint(courses_bp)

    migrate = Migrate(app, db)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "message": "Resource not found"
        }), 404

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)