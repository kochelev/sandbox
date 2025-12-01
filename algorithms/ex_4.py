"""Несколько входных параметров."""


def print_pairs(arr_1: list, arr_2: list):
    # O(ab), a = len(arr_1), b = len(arr_2)
    for i in arr_1:
        for j in arr_2:
            print("({}, {})".format(i, j))


if __name__ == "__main__":
    from lesson_2.dyn_plot import blocking_animation

    # не очень отражает положение дел, т.к. a = n, b = 2n
    blocking_animation(
        print_pairs, lambda n: (list(range(n)), list(range(2 * n, -2 * n, -1)))
    )
