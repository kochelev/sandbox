"""https://matplotlib.org/2.0.2/examples/animation/animate_decay.html."""
import random
import time
from functools import partial
from typing import Any, Callable

import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")


def time_it(f):
    """Замер времени выполнения функции БЕЗ сохранения результата."""

    def wrapper(*args, **kwargs):
        start = time.time()
        f(*args, **kwargs)
        return time.time() - start

    return wrapper


def to_check(n):
    res = 0
    for i in n:
        for j in n:
            res += i * j % 13
    # n.sort()
    # for i in range(n):
    #     a.append(n**2 % 13 + n ** 3 % 47)


def blocking_animation(
    f: Callable,
    generator: Callable[[int], Any],
    start_n: int = 100,
    factor: float = 1.05,
    iterations: int = 1000,
):
    """Функция для отрисовки красивого графика времени выполнения.

    Пример:
    >>> def my_sum(arr_1: list, arr_2: list):
    >>>     return sum(arr_1) * sum(arr_2)
    >>> def gen(n: int):
    >>>     return [x^2 for x in range(n)], [x^3 for x in range(n)]
    >>> blocking_animation(my_sum, gen)

    :param f: функция, чье время мерим
    :param generator: функция, принимающая целое n и выдающая tuple из всех аргументов f
    :param start_n: начальный n
    :param factor: на сколько умножать n для подсчета следующей точки на графике
    :param iterations: количество точек на графике
    :return:
    """
    fig, ax = plt.subplots()
    (line,) = ax.plot([], [], lw=2)
    ax.grid()
    ax.set_ylabel("Время выполнения")
    ax.set_xlabel("n")
    ax.set_title("Замер времени выполнения функции")

    xdata, ydata = [], []

    def init():
        ax.set_ylim(-0.005, 0.005)
        del xdata[:]
        del ydata[:]
        line.set_data(xdata, ydata)
        return line

    def run(data):
        # update the data
        t, y = data
        xdata.append(t)
        ydata.append(y)
        # Увеличить в 2 раза границы по достижении
        xmin, xmax = ax.get_xlim()
        if t >= xmax:
            ax.set_xlim(xmin, 2 * xmax)
            ax.figure.canvas.draw()
        y_max = ax.get_ylim()[-1]
        if ydata[-1] >= y_max:
            ax.set_ylim(0, 2 * y_max)
            ax.figure.canvas.draw()

        line.set_data(xdata, ydata)
        return line

    def data_gen(t: int, factor: float = 1.05, iterations: int = 5_000):
        cnt = 0
        while cnt < iterations:
            cnt += 1
            t = int(factor * t)
            args = generator(t)
            yield t, time_it(f)(*args)

    data_gen_ = partial(data_gen, t=start_n, factor=factor, iterations=iterations)
    ani = animation.FuncAnimation(
        fig, run, data_gen_, blit=False, interval=5, repeat=False, init_func=init
    )
    plt.show()


if __name__ == "__main__":
    import sys

    sys.setrecursionlimit(5_000)
    random.seed(42)
    blocking_animation(to_check, lambda t: (list(range(t)),))
