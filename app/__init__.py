# __init__.py or app.py
from flask import Flask, render_template
from .routes import auth_routes, dashboard_routes, home_routes, settings_routes, admin_routes
from .middleware import init_middleware
from .client.supabase_client import init_supabase_client
import os
import logging
from logging.handlers import RotatingFileHandler

def create_app():
    app = Flask(__name__)

    # Load configuration from the config.py file
    app.config.from_object(os.getenv("FLASK_CONFIG", "config.DevelopmentConfig"))

    # Initialize Supabase client and store it in app context
    init_supabase_client(app)

    # Set up logging
    if not app.debug:
        handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)
    
    # Register Routes
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(dashboard_routes.bp)
    app.register_blueprint(home_routes.bp)  # Home blueprint will handle pricing as well
    app.register_blueprint(settings_routes.bp)
    app.register_blueprint(admin_routes.bp)

    # Initialize Middleware
    init_middleware(app)

    # Error Handling for 404 and other common errors
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("500.html"), 500

    return app
