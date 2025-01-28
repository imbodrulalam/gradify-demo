from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from ..services.supabase_service import insert_data, fetch_data

bp = Blueprint("auth", __name__, url_prefix="/auth")


# Route for Login
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            # Authenticate user with Supabase
            response = current_app.supabase_client.auth.sign_in_with_password(
                credentials={"email": email, "password": password}
            )

            user = response.user  # Extract user data

            if user:
                # Store all user attributes in session
                session["user"] = {
                    "id": user.id,
                    "email": user.email,
                    "metadata": user.user_metadata,  # Includes custom metadata like 'otp'
                    "created_at": user.created_at,  # User creation timestamp
                    "updated_at": user.updated_at   # Last updated timestamp
                }

                flash("Login successful!", "success")
                return redirect(url_for("dashboard.index"))
            else:
                flash("Invalid email or password.", "error")
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
    return render_template("login.html")


# Route for Signup with OTP Verification
@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            # Sign up the user with Supabase (email and password)
            response = current_app.supabase_client.auth.sign_up(
                credentials={"email": email, "password": password}
            )

            user = response.user  # Extract user data

            if user:
                # Store user data or handle it as needed
                session["user"] = {
                    "id": user.id,
                    "email": user.email,
                    "metadata": user.user_metadata,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at
                }

                flash(
                    "Signup successful! An OTP has been sent to your email.", "success")
                return redirect(url_for('auth.verify_otp'))
            else:
                flash("Error during signup. Please try again.", "error")
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            
    elif request.method == "GET":
        user_data = session.get("user")
        if user_data :
            flash("You are already logged in.", "info")
            return redirect(url_for("dashboard.index"))

        else: render_template("signup.html")


# OTP Verification Route
@bp.route("/verify_otp", methods=["GET", "POST"])
def verify_otp():
    if request.method == "GET":
        return render_template("verify_otp.html")
    
    if request.method == "POST":
        otp = request.form.get("otp")  # Retrieve OTP entered by the user

        # Check if the user session contains the necessary user data
        user_data = session.get("user")

        if not user_data or not isinstance(user_data, dict):
            flash("No user session found. Please sign up first.", "error")
            return redirect(url_for("auth.signup"))

        # Extract the email from session data (using the user object from session)
        email = user_data.get("email")

        if not email:
            flash("Email is missing from session data.", "error")
            return redirect(url_for("auth.signup"))

        try:
            # Correct method for OTP verification
            response = current_app.supabase_client.auth.verify_otp(
                {"email": email, "token": otp, "type": "email"}
            )

            # Check for the presence of an error in the response
            if "error" in response:
                flash("Invalid OTP. Please try again.", "error")
                return render_template("verify_otp.html")

            # OTP verified successfully, proceed to dashboard
            flash("OTP verified successfully!", "success")
            return redirect(url_for("dashboard.index"))

        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return render_template("verify_otp.html")


# Logout Route
@bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("auth.login"))
