from flask import request, redirect, url_for, session

def init_middleware(app):
    @app.before_request
    def check_authentication():
        protected_routes = ["dashboard.index", "settings.index", "admin.index"]
        if request.endpoint in protected_routes and not session.get("user"):
            return redirect(url_for("auth.login"))
