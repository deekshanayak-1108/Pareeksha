import os
from flask import Flask, render_url_rule, render_template
from config import config_map
from extensions import db, migrate, login_manager

def create_app(config_name=None):
    """Application factory for creating Flask app instance."""
    if not config_name:
        # Fallback to FLASK_ENV or default to development
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    
    # Load configuration
    config_class = config_map.get(config_name, config_map['default'])
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints (placeholder for future blueprints)
    register_blueprints(app)

    # Home route
    @app.route('/')
    def index():
        return render_template('index.html')

    return app

def register_blueprints(app):
    """Registers blueprints. Placeholder for future routes."""
    # Example: from routes.auth import auth_bp; app.register_blueprint(auth_bp)
    pass

if __name__ == '__main__':
    app = create_app()
    app.run()
