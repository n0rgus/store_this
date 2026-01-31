# routes_auth.py
from __future__ import annotations
from functools import wraps
from flask import Blueprint, request, session, flash, redirect, url_for, render_template_string, current_app
from lookups import choices
from templates import TPL_BASE, TPL_LOGIN

auth_bp = Blueprint("auth", __name__)

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Please log in to perform that action.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        return fn(*args, **kwargs)
    return wrapper

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        pw = request.form.get("password","")
        if pw == current_app.config["STORE_THIS_ADMIN_PASSWORD"]:
            session["logged_in"] = True
            flash("Logged in.", "success")
            return redirect(request.args.get("next") or url_for("ui.home"))
        flash("Incorrect password.", "danger")
    ch = choices()
    return render_template_string(TPL_BASE, content=render_template_string(TPL_LOGIN, **ch), **ch)

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("ui.home"))
