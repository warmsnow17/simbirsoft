import datetime


def get_fibonacci_amount() -> int:
    n = datetime.datetime.now().day + 1
    fib_series = [0, 1]

    while len(fib_series) < n + 1:
        fib_series.append(fib_series[-1] + fib_series[-2])

    return fib_series[n]
