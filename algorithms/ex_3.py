"""Полноценные рекурсии и типичные алгоритмы."""


def fib(n: int) -> int:
    """ветвится на две ветки, потом еще на две, потом еще -- O(2^n)"""
    # 1, 1, 2, 3, 5, 8, 13, 21, 34
    # f(n) = f(n-1) + f(n-2)
    if n < 1:
        raise ValueError("n must be >= 1")
    if n == 1:
        return 1
    if n == 2:
        return 1
    return fib(n - 1) + fib(n - 2)


def binary_search_recursive(arr, elem, start=0, end=None):
    # сложность O(log N), где N - число элементов в массиве
    if end is None:
        end = len(arr) - 1
    if start > end:
        return False

    mid = (start + end) // 2
    if elem == arr[mid]:
        return mid
    if elem < arr[mid]:
        return binary_search_recursive(arr, elem, start, mid - 1)
    return binary_search_recursive(arr, elem, mid + 1, end)


if __name__ == "__main__":
    from lesson_2.dyn_plot import blocking_animation

    # blocking_animation(fib, lambda n: (n,), start_n=10, factor=1.1, iterations=50)
    blocking_animation(
        binary_search_recursive,
        lambda n: (list(range(0, n, 2)) + list(range(1, n, 2)), n // 3),
        start_n=10_000,
        factor=1.3,
    )
