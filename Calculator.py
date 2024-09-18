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