# app/routes/admin_routes.py

from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from ..services.supabase_service import fetch_data, update_data, delete_data

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.route("/", methods=["GET"])
def index():
    user = session.get("user")
    if not user or not user.get("is_admin"):
        flash("Unauthorized access.", "error")
        return redirect(url_for("auth.login"))

    users = fetch_data("users")
    return render_template("admin.html", users=users)

@bp.route("/activate/<user_id>", methods=["POST"])
def activate_user(user_id):
    user = session.get("user")
    if not user or not user.get("is_admin"):
        flash("Unauthorized access.", "error")
        return redirect(url_for("auth.login"))

    try:
        update_data("users", {"id": user_id}, {"status": "active"})
        flash("User activated successfully!", "success")
    except Exception as e:
        flash(f"Error activating user: {str(e)}", "error")
    return redirect(url_for("admin.index"))

@bp.route("/deactivate/<user_id>", methods=["POST"])
def deactivate_user(user_id):
    user = session.get("user")
    if not user or not user.get("is_admin"):
        flash("Unauthorized access.", "error")
        return redirect(url_for("auth.login"))

    try:
        update_data("users", {"id": user_id}, {"status": "inactive"})
        flash("User deactivated successfully!", "success")
    except Exception as e:
        flash(f"Error deactivating user: {str(e)}", "error")
    return redirect(url_for("admin.index"))

@bp.route("/delete/<user_id>", methods=["POST"])
def delete_user(user_id):
    user = session.get("user")
    if not user or not user.get("is_admin"):
        flash("Unauthorized access.", "error")
        return redirect(url_for("auth.login"))

    try:
        delete_data("users", {"id": user_id})
        flash("User deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting user: {str(e)}", "error")
    return redirect(url_for("admin.index"))
