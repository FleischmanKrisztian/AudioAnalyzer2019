from app import application

from flask import render_template

@application.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin/dashboard.html")

@application.route("/admin/profile")
def admin_profile():
    return "<h1>Admin Profile<h1>"