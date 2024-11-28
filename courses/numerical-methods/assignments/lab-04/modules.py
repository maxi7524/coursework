import numpy as np
from numpy import polynomial as P

def horner_method(x, coeffs, z):
    """
    Evaluate a polynomial at a given point using Horner's method.
    
    Parameters:
    x (array-like): Points of the polynomial.
    coeffs (array-like): Coefficients of the polynomial.
    z (float or array-like): Point(s) at which to evaluate the polynomial.
    
    Returns:
    float or ndarray: Value of the polynomial at point(s) z.
    """
    result = np.zeros_like(z, dtype=float)
    for c in reversed(coeffs):
        result = result * (z - x) + c
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

def clenshaw_algorithm(coeffs, x):
    """
    Evaluate a Chebyshev series at a given point using the Clenshaw algorithm.
    
    Parameters:
    coeffs (array-like): Coefficients of the Chebyshev series.
    x (float or array-like): Point(s) at which to evaluate the series.
    
    Returns:
    float or ndarray: Value of the series at point(s) x.
    """
    b_n2 = 0
    b_n1 = 0
    for c in reversed(coeffs[1:]):
        b_n2, b_n1 = b_n1, 2 * x * b_n1 - b_n2 + c
    return x * b_n1 - b_n2 + coeffs[0]