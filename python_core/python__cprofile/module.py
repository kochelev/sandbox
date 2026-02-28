# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring


def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

def run_several_times(n):

    for x in range(n):
        _ = fib(x)

if __name__ == "__main__":

    for i in range(10):
        run_several_times(30)
