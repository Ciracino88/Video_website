from flask import Blueprint, render_template, request, session, redirect, url_for
import sqlite3


post_detail_bp = Blueprint('post_detail', __name__)

@post_detail_bp.route('/post/<int:post_id>')
def post_detail(post_id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # sqlite3 에서는 SQL 쿼리의 파라미터를 바인딩할 때 튜플로 받음.
    post = cur.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    comments = cur.execute('SELECT * FROM comments WHERE post_id = ?', (post_id,)).fetchall()
    conn.close()

    # 게시물 데이터가 존재하면
    if post:
        return render_template('post_detail.html', post=post, comments=comments)
    else:
        return "Post not found", 404

@post_detail_bp.route('/post/<int:post_id>/comment', methods=['POST'])
def comment(post_id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if request.method == 'POST':
        cur.execute('''INSERT INTO comments (post_id, content, name)
        VALUES (?, ?, ?)
        ''', (post_id, request.form['comment'], session['username']))
        conn.commit()
        conn.close()

        return redirect(url_for("post_detail.post_detail", post_id=post_id))