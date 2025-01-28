from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from ..services.supabase_service import update_data

bp = Blueprint("settings", __name__, url_prefix="/settings")


@bp.route("/", methods=["GET", "POST"])
def index():
    user = session.get("user")
    if not user:
        flash("You need to log in first.", "error")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        full_name = request.form.get("full_name")
        bio = request.form.get("bio")
        try:
            update_data("users", {"id": user["id"]}, {"full_name": full_name, "bio": bio})
            session["user"]["full_name"] = full_name  # Update session with new data
            flash("Profile updated successfully!", "success")
        except Exception as e:
            flash(f"Error updating profile: {str(e)}", "error")
    return render_template("settings.html", user=user)
