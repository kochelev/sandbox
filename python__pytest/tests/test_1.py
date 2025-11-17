import sys
import pytest

# https://habr.com/ru/articles/835196/

def factorial(n: int) -> int:
    if n in [0, 1]:
        return 1
    return n * factorial(n - 1)

# Разные параметры для одной и той же функциональности

@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (0, 1),
        (1, 1),
        (5, 120)
    ]
)
def test_factorial_1(number: int, expected: int) -> None:
    got = factorial(number)

    assert expected == got

@pytest.mark.parametrize(
    ("number,expected"),
    [
        (0, 1),
        (1, 1),
        (5, 120)
    ]
)
def test_factorial_2(number: int, expected: int) -> None:
    got = factorial(number)

    assert expected == got

# Гибкая настройка параметров (зависимые параметры, пропуск теста)

@pytest.mark.parametrize(
    ("number", "expected"),
    [
        pytest.param(0, 1, id="return one if number equal zero"),
        (1, 1),
        (5, 120),
        pytest.param(
            10,
            3628800,
            marks=pytest.mark.skip(reason="Slow test"),
        ),
    ],
)
def test_factorial_3(number: int, expected: int) -> None:
    got = factorial(number)

    assert expected == got

# Комбинаторный перебор параметров тестирования

@pytest.mark.parametrize("number1", [1, 2, 3])
@pytest.mark.parametrize("number2", [4, 5, 6])
@pytest.mark.parametrize("number3", [7, 8, 9])
def test_sum(number1: int, number2: int, number3: int) -> None:
    got = sum([number1, number2, number3])
    assert got == number1 + number2 + number3

# Пропуск теста

@pytest.mark.skip(reason="Известная ошибка, исправление ожидается в следующем релизе")
def test_some_function_6756() -> None:
    assert True

# Пропуск теста с условием (под Windows не выполнится)

@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Тест не поддерживается на Windows",
)
def test_unix_specific_function() -> None:
    assert True

# Тесты должны завершаться неперехваченной ошибкой

@pytest.mark.xfail(reason="Исключение")
def test_exception() -> None:
    # raise IndexError
    assert True

# ФИКСТУРЫ

class Multiplier:

    def __init__(self, b: int) -> None:
        self.b = b

    def prod(self, multiplier: int) -> int:
        return multiplier * self.b

@pytest.fixture()
def get_multiplier() -> Multiplier:
    return Multiplier(b=10)

def test_multiplier(get_multiplier: Multiplier) -> None:
    assert get_multiplier.prod(multiplier=3) == 30

# Частота выполнения фикстуры

# Возможные значения: "session", "package", "module", "class", "function"
# По умолчанию установлено значение "function"

# scope="session" указывает на то, что эта фикстура 
# будет выполнена единожды за весь сеанс тестирования 
# @pytest.fixture(scope="session")
# def crate_test_db() -> None:
#     ...


# scope="function" указывает на то, что эта фикстура 
# будет выполняться для каждой тестовой функции 
# @pytest.fixture(scope="function")
# def async_session() -> AyncSession:
#     ...

# Фикстура в фикстуре

@pytest.fixture()
def a() -> int:
    return 5

@pytest.fixture()
def b(a: int) -> int:
    return 2 * a

@pytest.fixture()
def c(b: int, fixture_from_another_file: int) -> int:
    return fixture_from_another_file * b

def fixtures_test_1(c):
    assert c == 1001

# Передача аргументов в фикстуру ЯВНЫМ способом

class Addition:
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def sum(self) -> int:
        return self._x + self._y

@pytest.fixture()
def tester_1(request) -> Addition:
    return Addition(request.param[0], request.param[1])

@pytest.mark.parametrize('tester_1', [[1, 2], [3, 0]], indirect=True)
def test_addition_1(tester_1) -> None:
    assert 3 == tester_1.sum()

# Передача аргументов в фикстуру НЕЯВНЫМ способом

@pytest.fixture()
def tester_2(test_data: list[int]) -> Addition:
    return Addition(test_data[0], test_data[1])

class TestIt:
    @pytest.mark.parametrize('test_data', [[1, 2], [3, 0], [2, 1]])
    def test_addition_1(self, my_tester: Addition):
       assert 3 == my_tester.sum()
