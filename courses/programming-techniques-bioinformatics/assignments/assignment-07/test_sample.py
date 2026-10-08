from math import isclose

# część pierwsza

def test_add():
    assert 2 + 3 == 5
    # dowolna liczba assert'ów

def test_div():
    assert isclose(5 / 2, 2.5)

def mask_sum(data, mask):
    res = 0
    for val, mask_val in zip(data, mask):
       if mask_val != 0:
            res += val
    return res

def test_sum():
    # values 
    values = [i for i in range(1, 11)]
    # summing positive mask
    assert mask_sum(values, [1]*10) == 55
    # summing partially 
    assert mask_sum([], []) == 0


# Run multiple tests
import functools
from typing import List

import pytest

# przypadek ze złożonymi tych sytuacji
@functools.lru_cache
def fibonacci(n: int):
    """Calculate n-th fibbonaci number"""
    if n < 0:
        raise ValueError("Unsupported value")
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)



## tutaj mamy jeden assert, który sprawdza wiele przypadków
@pytest.mark.parametrize("num,res", [(0, 0), (1, 1), (2, 1), (10, 55), (18, 2584)])
def test_fibonacci(num: int, res: int):
    assert fibonacci(num) == res


# ## tutaj dostajemy kombinacje. 
# @pytest.mark.parametrize("n_size", list(range(1, 10)))
# @pytest.mark.parametrize("m_size", list(range(1, 20, 2)))
# def test_zero_matrix(n_size, m_size):
#     matrix = zeros_matrix(n_size, m_size)
#     assert len(matrix) == n_size
#     assert all(map(lambda x: len(x) == m_size, matrix))
#     assert all([x == 0 for y in matrix for x in y])
#     matrix[0][0] = 1
#     assert all([x == 0 for y in matrix[1:] for x in y])
#     assert all([x == 0 for x in matrix[0][1:]])

def norm(vec: List[float], norm: int):
    return sum(pow(abs(v), norm) for v in vec)**(1/norm)


@pytest.mark.parametrize("vec_len", list(range(1, 10)))
@pytest.mark.parametrize("norm_num", list(range(1, 10)))
def test_norm(vec_len, norm_num):
    assert norm([1] * vec_len, norm_num) == vec_len**(1/norm_num)
    # powinno się sprawdzić warunek z potęgą 
def mask_aggregation(agg_operator: callable[[float, float], float], data: List[float], mask: List[bool]) -> float:
    
    pass    


# mock - open - imitacja otwierania pliku 
# chodzi o imitacje, żeby zapewnić bezpieczeństwo przed uszkodzeniem plików, odczytem i j nadpisaniem 
# narzucamy co taki plik ma zwracać 