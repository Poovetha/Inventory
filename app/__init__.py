import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Global extensions

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    load_dotenv()
    app = Flask(
        __name__,
        instance_relative_config=False,
        static_folder='static',
        template_folder='templates',
    )

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
    database_url = os.getenv('DATABASE_URL', 'sqlite:///inventory.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .views import main_bp
    app.register_blueprint(main_bp)

    # CLI seed command
    @app.cli.command('seed')
    def seed_command():
        from .seed import run_seed
        run_seed()
        print('Seed data inserted.')

    return app



