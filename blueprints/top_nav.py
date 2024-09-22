from flask import Blueprint, render_template

top_nav_bp = Blueprint('top_nav', __name__)

@top_nav_bp.route('/')
def top_nav():
    return render_template('top_nav.html')