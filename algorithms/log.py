import random

from lesson_2.dyn_plot import blocking_animation


def merge(left: list, right: list) -> list:
    i, j = 0, 0
    result = []
    while i < len(left) or j < len(right):
        if i == len(left):
            result.append(right[j])
            j += 1
            continue
        if j == len(right):
            result.append(left[i])
            i += 1
            continue
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    return result


def merge_sort(arr: list) -> list:
    if not arr:
        return []
    if len(arr) == 1:
        return arr
    left = arr[: len(arr) // 2]
    right = arr[len(arr) // 2 :]
    rv = merge(merge_sort(left), merge_sort(right))
    return rv


def gen(n: int):
    arr = list(range(n))
    random.shuffle(arr)
    return (arr,)


if __name__ == "__main__":
    random.seed(42)
    blocking_animation(merge_sort, gen)
