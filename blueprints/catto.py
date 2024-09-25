from openai import OpenAI
from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3 # catto, comments, posts
from dotenv import load_dotenv
import os

catto_bp = Blueprint('catto', __name__)

load_dotenv()

@catto_bp.route('/catto', methods=['GET', 'POST'])
def catto():
    # api key 설정
    client = OpenAI(
        api_key=os.getenv("CATTO_API_KEY"),
    )

    # 댓글 생성 요청이 있다면
    if request.method == 'POST':
        print('request')
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        post = cur.execute('SELECT * FROM posts ORDER BY RANDOM() LIMIT 1').fetchall()[0]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 글을 읽고 댓글을 다는 유저야."},
                {"role": "user", "content": f"다음 글을 읽고 글의 주제에 맞게 적절한 댓글을 100자 이내로 작성해줘.\n{post['title']}\n{post['content']}"}
            ],
            temperature=0.7,  # 출력의 창의성 조절
            max_tokens=100  # 출력될 토큰 수의 최대값 설정
        )

        print(response.choices[0].message.content)
        comment = response.choices[0].message.content

        # 생성한 답변은 바로 comment db 에 저장하지 않고, 사용자의 평가를 받게 함.
        # 작성한 댓글을 catto 에 저장

        cur.execute('''INSERT INTO catto (post_id, content, name)
        VALUES (?, ?, ?)''', (post['id'], comment, 'catto'))
        conn.commit()
        conn.close()

        return redirect(url_for('catto.catto'))

    # 생성한 댓글 데이터를 로드
    return render_template('catto.html', generated_comments=init_catto())

def init_catto():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    generated_comments = cur.execute('SELECT * FROM catto ORDER BY id DESC').fetchall()
    conn.close()

    return generated_comments