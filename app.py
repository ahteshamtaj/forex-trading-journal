# =========================================================
# FOREX TRADING JOURNAL
# app.py
# =========================================================

import os

from dotenv import load_dotenv
from flask import Flask, render_template

# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# CONFIG
# =========================================================

from config import Config


# =========================================================
# DATABASE
# =========================================================

from utils.database import init_database


# =========================================================
# BLUEPRINT IMPORTS
# =========================================================

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.journal import journal_bp
from routes.analytics import analytics_bp
from routes.profile import profile_bp


# =========================================================
# CREATE FLASK APP
# =========================================================

app = Flask(__name__)


# =========================================================
# LOAD CONFIGURATION
# =========================================================

app.config.from_object(Config)


# =========================================================
# BLUEPRINTS
# =========================================================

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(journal_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(profile_bp)


# =========================================================
# HOME / LANDING PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "landing.html"
    )


# =========================================================
# 404 ERROR
# =========================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "errors/404.html"
    ), 404


# =========================================================
# 500 ERROR
# =========================================================

@app.errorhandler(500)
def internal_server_error(error):

    return render_template(
        "errors/500.html"
    ), 500


# =========================================================
# LOCAL DEVELOPMENT
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )