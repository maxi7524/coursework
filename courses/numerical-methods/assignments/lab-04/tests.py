import numpy as np
from modules import horner_method, neville, newton_polynomial, coef_change, clenshaw_algorithm

def test_horner_method():
    x = np.array([0, 1, 2])
    coeffs = np.array([1, 2, 3])
    z = 1.5
    assert np.isclose(horner_method(x, coeffs, z), 7.25)

def test_neville():
    datax = np.array([0, 1, 2])
    datay = np.array([1, 2, 3])
    x = 1.5
    assert np.isclose(neville(datax, datay, x), 2.5)

def test_newton_polynomial():
    x = np.array([0, 1, 2])
    f = np.array([1, 2, 3])
    expected_coeffs = np.array([1, 1, 0])
    assert np.allclose(newton_polynomial(x, f), expected_coeffs)

def test_coef_change():
    x = np.array([1, 2, 3])
    expected_cheby_coeffs = np.array([2, 1, 0])
    assert np.allclose(coef_change(x), expected_cheby_coeffs)

def test_clenshaw_algorithm():
    coeffs = np.array([1, 2, 3])
    x = 0.5
    assert np.isclose(clenshaw_algorithm(coeffs, x), 2.75)

if __name__ == "__main__":
    test_horner_method()
    test_neville()
    test_newton_polynomial()
    test_coef_change()
    test_clenshaw_algorithm()
    print("All tests passed!") 