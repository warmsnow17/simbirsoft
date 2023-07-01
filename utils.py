"""Модуль, предоставляющий вспомогательные функции для тестирования банковского приложения."""

import datetime


def get_fibonacci_amount() -> int:
    """Функция для получения числа Фибоначчи в зависимости от текущей даты.

    Используется для получения суммы средств при выполнении операций с депозитами и выводами.
    """
    current_day = datetime.datetime.now().day + 1
    fib_series = [0, 1]

    while len(fib_series) < current_day + 1:
        fib_series.append(fib_series[-1] + fib_series[-2])

    return fib_series[current_day]
