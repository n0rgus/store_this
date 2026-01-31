# app.py
from __future__ import annotations
import os
from flask import Flask

# Local modules
from db import init_app as init_db
from routes_auth import auth_bp
from routes_ui import ui_bp
from images import images_bp

def create_app():
    app = Flask(__name__)
    # ---- Configuration ----
    app.config["SECRET_KEY"] = os.environ.get("STORE_THIS_SECRET_KEY", "dev-key-change-me")
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB uploads
    app.config["STORE_THIS_DB"] = os.environ.get("STORE_THIS_DB", os.path.abspath("Store-This.db"))
    app.config["STORE_THIS_ADMIN_PASSWORD"] = os.environ.get("STORE_THIS_ADMIN_PASSWORD", "admin")

    # Init DB teardown + helpers
    init_db(app)

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(ui_bp)
    app.register_blueprint(images_bp)

    return app

app = create_app()

if __name__ == "__main__":
    # Fail fast if DB missing
    if not os.path.exists(app.config["STORE_THIS_DB"]):
        raise SystemExit(f"Database not found: {app.config['STORE_THIS_DB']}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
