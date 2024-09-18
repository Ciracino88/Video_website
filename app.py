from boto3 import s3
from flask import Flask, render_template, request
from Calculator import Calculator
import boto3
from botocore.exceptions import NoCredentialsError
app = Flask(__name__)

# 현금 : 내가 넣은 돈만. 넣은 돈으로 벌어들인 추가금은 x
# 시드 : 내가 넣은 돈 + 내가 추가로 번 돈
# 결과 : 시드 * (1 + 수익률)
# 수익금 : 결과 - 현금

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/calculate', methods=['GET', 'POST'])
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
