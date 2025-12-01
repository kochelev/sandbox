"""Цикл в цикле и цикл после цикла."""


def add_complexity(n):
    res = 1
    # O(n) операций здесь
    for i in range(n):
        res += i
    # и O(n) операций здесь
    for i in range(n):
        res *= i
    # в сумме O(n + n) = O(n) операций
    return res


def multiply_complexity(n):
    res = 1
    # O(n) операций тут
    for i in range(n):
        # и O(n) на каждой из операций
        # итого O(n * n) = O(n^2)
        for j in range(n):
            res += i * j
    # еще добавить O(n)
    for j in range(n):
        res += j % 13
    # итогово: O(n^2 + n) = O(n^2)
    return res


if __name__ == "__main__":
    from lesson_2.dyn_plot import blocking_animation

    # blocking_animation(add_complexity, lambda n: (n,))
    blocking_animation(multiply_complexity, lambda n: (n,))
