from flask import Blueprint, render_template
import sqlite3

thinking_bp = Blueprint('thinking', __name__)

@thinking_bp.route('/thinking')
def thinking():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    posts = cur.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('thinking.html', posts=posts)