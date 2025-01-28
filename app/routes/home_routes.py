# app/routes/home_routes.py
from flask import Blueprint, render_template, request, flash, redirect, url_for

bp = Blueprint("home", __name__, url_prefix="/")

@bp.route("/")
def index():
    return render_template("home.html")

@bp.route("/pricing")
def pricing():
    return render_template("pricing.html")

@bp.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@bp.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    
    # Process the contact data, e.g., save to a database or send an email
    flash('Your message has been sent successfully!', 'success')
    return redirect(url_for('home.index'))  # Redirect to the home page or a thank-you page
