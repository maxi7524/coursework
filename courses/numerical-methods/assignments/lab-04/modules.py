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
    x = np.array(x, copy=True)
    f = np.array(f, copy=True)
    n = len(x)
    divided_diff = np.array(f, copy=True)
    for k in range(1, n):
        divided_diff[k:] = (divided_diff[k:] - divided_diff[k-1:-1]) / (x[k:] - x[:-k])
    return divided_diff

def standard_to_chebyshev(x):
    """
    Convert polynomial coefficients from standard to Chebyshev form.
    
    Parameters:
    x (array-like): Coefficients in standard form.
    
    Returns:
    ndarray: Coefficients in Chebyshev form.
    """
    poly = np.polynomial.Polynomial(x)
    poly_cheby = poly.convert(kind=P.Chebyshev)
    return poly_cheby.coef

def clenshaw_evaluate(coeffs, x):
    """
    Evaluate a Chebyshev series using Clenshaw's algorithm.
    
    Parameters:
    coeffs (array-like): Coefficients of the Chebyshev series.
    x (float): Point at which to evaluate the series.
    
    Returns:
    float: Value of the Chebyshev series at point x.
    """
    b_k1 = 0
    b_k2 = 0
    
    for c in reversed(coeffs[1:]):
        b_k = 2 * x * b_k1 - b_k2 + c
        b_k2 = b_k1
        b_k1 = b_k
    
    return x * b_k1 - b_k2 + coeffs[0]

def trigonometric_interpolation(f, m):
    """
    Compute trigonometric interpolation for function f with parameter m.
    
    Parameters:
    f (callable): Function to interpolate
    m (int): Parameter determining number of coefficients
    
    Returns:
    callable: Interpolating function
    """
    n = 2 * m
    z = np.array([(2 * np.pi * k) / (n + 1) for k in range(n + 1)])
    f_values = f(z)
    
    c = (1 / (n + 1)) * np.sum(f_values)
    
    a = np.zeros(m + 1)
    b = np.zeros(m + 1)
    
    for k in range(1, m + 1):
        a[k] = (2 / (n + 1)) * np.sum(f_values * np.cos(k * z))
        b[k] = (2 / (n + 1)) * np.sum(f_values * np.sin(k * z))
    
    def interpolant(x):
        result = c
        for s in range(1, m + 1):
            result += a[s] * np.cos(s * x) + b[s] * np.sin(s * x)
        return result
    
    return interpolant