"""Рекурсии и space complexity."""


def loop(n):
    # O(n)
    res = 0
    for i in range(n):
        res += i
    return res


def simplest(n):
    # O(1)
    return n << 1


def sum_(n):
    """O(n) времени.

    содержит n вызовов одновременно - O(n) памяти
    sum_(4)
      -> sum_(3)
        -> sum_(2)
          -> sum_(1)
            -> sum_(0)
    """
    if n == 0:
        return 0
    return n + sum_(n - 1)


def pair_sum(a, b):
    return a + b


def pair_sum_for_seq(n):
    """Но если n вызовов не одновременно в памяти, то по памяти будет O(1)
    i = 0 -> один вызов pair_sum(0, 1) в памяти, затем выход из него
    i = 1 -> один вызов pair_sum(1, 2) в памяти, затем выход из него
    ...
    """
    res = 0
    for i in range(n):
        res += pair_sum(i, i + 1)

    return res


if __name__ == "__main__":
    import sys

    from lesson_2.dyn_plot import blocking_animation

    sys.setrecursionlimit(100_000)

    # blocking_animation(simplest, lambda n: (n,), iterations=1000)
    # blocking_animation(loop, lambda n: (n,))
    blocking_animation(sum_, lambda n: (n,), start_n=10, factor=1.1, iterations=80)
    # blocking_animation(pair_sum_for_seq, lambda n: (n,))
