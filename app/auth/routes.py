from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required
from . import auth_bp
from models import User
from app.models import User
from app.extension import db
