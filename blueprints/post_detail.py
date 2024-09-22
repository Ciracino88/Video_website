from flask import Blueprint, render_template
import sqlite3

post_detail_bp = Blueprint('post_detail', __name__)

@post_detail_bp.route('/post/<int:post_id>')
def post_detail(post_id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # sqlite3 에서는 SQL 쿼리의 파라미터를 바인딩할 때 튜플로 받음.
    post = cur.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()

    if post:
        return render_template('post_detail.html', post=post)
    else:
        return "Post not found", 404