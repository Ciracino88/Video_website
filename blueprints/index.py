from flask import Blueprint, render_template
import sqlite3

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 데이터 최신순으로 3개만 가져옴
    posts = cur.execute('SELECT * FROM posts ORDER BY id DESC LIMIT 3').fetchall()
    conn.close()

    print("index page")
    return render_template('index.html', posts=posts)