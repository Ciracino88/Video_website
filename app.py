import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from Calculator import Calculator
from Post import Post
from datetime import datetime

app = Flask(__name__)

# 현금 : 내가 넣은 돈만. 넣은 돈으로 벌어들인 추가금은 x
# 시드 : 내가 넣은 돈 + 내가 추가로 번 돈
# 결과 : 시드 * (1 + 수익률)
# 수익금 : 결과 - 현금

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 데이터 최신순으로 3개만 가져옴
    posts = cur.execute('SELECT * FROM posts ORDER BY id DESC LIMIT 3').fetchall()
    conn.close()

    return render_template('index.html', posts=posts)

@app.route('/post', methods=["GET", "POST"])
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

@app.route('/post/<int:post_id>')
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

@app.route('/thinking')
def thinking():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    posts = cur.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('thinking.html', posts=posts)

@app.route('/calculator', methods=['GET', 'POST'])
def calculate():
    # post 이전 : 페이지 초기값
    cal = Calculator(cash=0, div_rate_for_m=0, additional_cash_for_m=0)

    if request.method == 'POST':
        _result = float(request.form['result'])

        # 결과값이 없으면
        if _result == 0:
            init_cal = Calculator(
                cash=float(request.form['seed']),
                div_rate_for_m=float(request.form['div_rate_for_m']),
                additional_cash_for_m=float(request.form['additional_cash_for_m']),
            )

            init_cal.init_data() # 계산 한 번 끝남

            # 연 계산을 누르면
            if 'calculate_per_y' in request.form:
                for i in range(11):
                    init_cal.update_data()

            return render_calculator_page(init_cal.data)

        # 결과값이 있다면
        else:
            load_cal = Calculator(
                cash=float(request.form['cash']),
                div_rate_for_m=float(request.form['div_rate_for_m']),
                additional_cash_for_m=float(request.form['additional_cash_for_m']),
                seed=_result,
                result=_result,
                profit=float(request.form['profit']),
                recur_count= int(request.form['recur_count'])
            )

            load_cal.update_data()

            if 'calculate_per_y' in request.form:
                for i in range(11):
                    load_cal.update_data()

            return render_calculator_page(load_cal.data)

    return render_calculator_page(cal.data)

def render_calculator_page(data):
    return render_template(
        'calculator.html',
        cash=data[0],
        div_rate_for_m=data[1],
        additional_cash_for_m=data[2],
        seed=data[3],
        result=data[4],
        profit=data[5],
        recur_count=data[6],
    )

if __name__ == '__main__':
    app.run(debug=True)
