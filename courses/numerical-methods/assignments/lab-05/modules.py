import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from algorithms import *

# QR Decomposition Tests
def test_orthogonality(vectors):
    """Test orthogonality of vectors after Gram-Schmidt"""
    orthonormal = gram_schmidt(vectors)
    n = len(orthonormal)
    dot_products = np.zeros((n, n))
    
    error = 0
    for i in range(n):
        for j in range(n):
            if i != j:
                dot_products[i,j] = np.abs(np.dot(orthonormal[i], orthonormal[j]))
            error = max(error, dot_products[i,j])
    return error  

# Approximation Tests
def test_approximation_error(f, n, a, b, metric="L2"):
    """Test approximation error for different polynomial degrees"""
    h = apoximation_in_unitary_space(f, n, a, b)
    errors = []
    if metric == "L2":
        error = np.sqrt(quad(lambda x: (f(x) - h(x))**2, a, b)[0])
        return error
    elif metric == "Chebyszew":
        x = np.linspace(a, b, (b-a)*100)
        error = np.max(np.abs(f(x) - h(x)))
    return error


# Quadratics Tests
def test_integration_methods(f, ns, a, b, exact_value=None):
    """Compare different integration methods"""
    if exact_value is None:
        exact_value = quad(f, a, b)[0]
    
    riemann_errors = []
    quadrics_errors = []
    divided_quadrics_errors = []
    quadrics_random_errors = []
    for n in ns:
        # Riemann sum
        riemann_val = riemann_sum(f, n, a, b)
        riemann_errors.append(abs(riemann_val - exact_value))
        
        # Basic quadrics
        quadrics_val = quadrics_highest_order(f, n, a, b)
        quadrics_errors.append(abs(quadrics_val - exact_value))
        
        # Divided quadrics
        divided_val = divided_quadrics_highest_order(f, n, a, b)
        divided_quadrics_errors.append(abs(divided_val - exact_value))
        
        # Quadrics random
        quadrics_random_val = quadrics_highest_order_random(f, n, a, b)
        quadrics_random_errors.append(abs(quadrics_random_val - exact_value))

    return {
        'riemann': np.array(riemann_errors),
        'quadrics': np.array(quadrics_errors),
        'divided_quadrics': np.array(divided_quadrics_errors),
        'quadrics_random': np.array(quadrics_random_errors)
    }

def test_functions():
    return {
        "sin": lambda x: np.sin(x) + x**2,
        "log": lambda x: np.log(x),
    }
def solutions():
    return {
        "sin": lambda x: -np.cos(x) + 1/3*x**3,
        "log": lambda x: x*np.log(x) - x,
    }

if __name__ == "__main__":
    pass