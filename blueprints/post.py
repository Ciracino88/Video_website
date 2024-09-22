from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

post_bp = Blueprint('post', __name__)

@post_bp.route('/post', methods=["GET", "POST"])
def post():
    if request.method == "POST":
        post = Post(
            title = request.form['post_title'],
            content = request.form['post_content'],
            upload_date = datetime.now().strftime("%Y.%m.%d")
        )

        post.upload_post()
        return redirect(url_for('index'))

    return render_template('post.html')

class Post:
    def __init__(self, title, content, upload_date):
        self.title = title
        self.content = content
        self.upload_date = upload_date

    def upload_post(self):
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # 데이터 삽입
        c.execute('''
        INSERT INTO posts (title, content, upload_date)
        VALUES (?, ?, ?)
        ''', (self.title, self.content, self.upload_date))

        conn.commit()
        conn.close()