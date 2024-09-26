from openai import OpenAI
from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
from dotenv import load_dotenv
import os

# db : catto, comments, posts
# bot : 0이면 사람. 나머지 양수는 봇 코드번호
# catto code : 1
# 나중에 bot 코드를 이용해 어떤 봇이 댓글을 생성했나 확인할 수 있음.

catto_bp = Blueprint('catto', __name__)

load_dotenv()

@catto_bp.route('/catto', methods=['GET', 'POST'])
def catto():
    # api key 설정
    client = OpenAI(
        api_key=os.getenv("CATTO_API_KEY"),
    )

    generated_comments, intro = init_catto(client)

    # 댓글 생성 요청이 있다면
    if request.method == 'POST':
        generate_comment(client)
        return redirect(url_for('catto.catto'))

    # 생성한 댓글 데이터를 로드
    return render_template('catto.html', generated_comments=generated_comments, intro=intro)

# catto 가 생성한 답변을 채택
@catto_bp.route('/value_generated_comment', methods=['GET', 'POST'])
def value_generated_comment():
    if request.form['value_generated_comment'] == 'save':
        pass
    if request.form['value_generated_comment'] == 'delete':
        pass
    return render_template('catto.html', generated_comments=init_catto())

# 초기 화면 구성
def init_catto(client):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 화면에 반환할 데이터들
    generated_comments = cur.execute('SELECT * FROM catto ORDER BY id DESC').fetchall()
    conn.close()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "너는 글을 읽고 댓글을 다는 catto 라는 이름의 유저야."},
            {"role": "user", "content": "너를 소개하는 문장을 30자 이내로 작성해봐. 예를 들어, '저는 멋진 글을 찾아다니는 catto 라고 합니다' 처럼 말이야."}
        ],
        temperature=0.5,  # 출력을 낮춰 예시를 최대한 따라가게 해보기
        max_tokens=100
    )

    intro = response.choices[0].message.content

    return generated_comments, intro

# 댓글 생성
def generate_comment(client):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    post = cur.execute('SELECT * FROM posts ORDER BY RANDOM() LIMIT 1').fetchall()[0]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user",
             "content": f"다음 글을 읽고 글의 주제에 맞게 적절한 댓글을 100자 이내로 작성해줘.\n{post['title']}\n{post['content']}"}
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

    return