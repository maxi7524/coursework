import numpy as np
from numpy import polynomial as P

def horner_eval(coeffs, z):
    """
    Evaluate a polynomial at a given point using Horner's method.
    
    Parameters:
    coeffs (array-like): Coefficients of the polynomial (in ascending order of degree).
    z (float or array-like): Point(s) at which to evaluate the polynomial.
    
    Returns:
    float or ndarray: Value of the polynomial at point(s) z.
    """
    result = coeffs[-1]  # Start with the highest degree coefficient
    for c in reversed(coeffs[:-1]):  # Iterate through remaining coefficients in reverse
        result = result * z + c
    return result

def standard_polynomial_eval(coeffs, z):
    """Standard polynomial evaluation method"""
    result = 0
    for i, coeff in enumerate(coeffs):
        result += coeff * (z ** i)
    return result


def neville(datax, datay, x):
    """
    Evaluate a polynomial at a given point using Neville's method.
    
    Parameters:
    datax (array-like): x-coordinates of the data points.
    datay (array-like): y-coordinates of the data points.
    x (float or array-like): Point(s) at which to evaluate the polynomial.
    
    Returns:
    float or ndarray: Value of the polynomial at point(s) x.
    """
    n = len(datax)
    p = np.array(datay, copy=True)
    for k in range(1, n):
        p[:n-k] = ((x - datax[k:]) * p[:n-k] + (datax[:n-k] - x) * p[1:n-k+1]) / (datax[:n-k] - datax[k:])
    return p[0]

def newton_polynomial(x, f):
    """
    Compute the coefficients of the interpolated polynomial in Newton's form.
    
    Parameters:
    x (array-like): x-coordinates of the data points.
    f (array-like): y-coordinates of the data points.
    
    Returns:
    ndarray: Coefficients of the polynomial in Newton's form.
    """
    # creating arrays
    x = np.array(x, copy=True)
    f = np.array(f, copy=True)

    n = len(x)
    divided_diff = np.array(f, copy=True)
    for k in range(1, n):
        divided_diff[k:] = (divided_diff[k:] - divided_diff[k-1:-1]) / (x[k:] - x[:-k])
    return divided_diff

def coef_change(x):
    """
    Convert polynomial coefficients to Chebyshev form.
    
    Parameters:
    x (array-like): Coefficients of the polynomial.
    
    Returns:
    ndarray: Coefficients in Chebyshev form.
    """
    poly = np.polynomial.Polynomial(x)
    poly_cheby = poly.convert(kind=P.Chebyshev)
    return poly_cheby.coef


def clenshaw_evaluate(coeffs, x):
    """
    Clenshaw algorithm for evaluating Chebyshev polynomials
    """
    b_k1 = 0
    b_k2 = 0
    
    for c in reversed(coeffs[1:]):
        b_k = 2 * x * b_k1 - b_k2 + c
        b_k2 = b_k1
        b_k1 = b_k
    
    return x * b_k1 - b_k2 + coeffs[0]