from flask import Blueprint, render_template, request, redirect, url_for

calculator_bp = Blueprint('calculator', __name__)

@calculator_bp.route('/calculator', methods=['GET', 'POST'])
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

class Calculator:
    def __init__(self, cash, div_rate_for_m, additional_cash_for_m, seed=0, result=0, profit=0, recur_count=0):
        self.cash = cash
        self.div_rate_for_m = div_rate_for_m
        self.additional_cash_for_m = additional_cash_for_m

        self.seed = seed
        self.result = result
        self.profit = profit
        self.recur_count = recur_count

        self.data = [
            self.cash,
            self.div_rate_for_m,
            self.additional_cash_for_m,
            self.seed,
            self.result,
            self.profit,
            self.recur_count
        ]

    def init_data(self):
        data = self.data
        _cash = data[0] + data[2]
        _seed = _cash
        _result = _seed * (1 + 0.01 * data[1])

        self.data = [
            _cash,
            data[1],
            data[2],
            round(_seed, 2),
            round(_result, 2),
            round(_result - _cash, 2),
            1
        ]

    def update_data(self):
        data = self.data
        _cash = data[0] + data[2]
        _seed = round(data[3] + data[2], 2)
        _result = round(_seed * (1 + 0.01 * data[1]), 2)
        data[-1] += 1
        _profit = round(_result - _cash, 2)

        self.data = [
            _cash,
            data[1],
            data[2],
            _seed,
            _result,
            _profit,
            data[-1]
        ]

        print(self.data)