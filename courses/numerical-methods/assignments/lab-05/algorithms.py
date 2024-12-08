import numpy as np
from scipy.integrate import quad


# Gram schmidt
def gram_schmidt(vec: list) -> list:
    """
    Performs Gram-Schmidt orthogonalization process on a set of vectors.
    
    The function takes a list of vectors and returns their orthonormalized versions.
    The process ensures that the resulting vectors are orthogonal to each other
    and have unit length (normalized).
    
    Args:
        vec (list): List of input vectors to be orthonormalized
        
    Returns:
        list: List of orthonormalized vectors
        
    Example:
        >>> vectors = [[1, 0, 1], [0, 1, 1]]
        >>> orthonormal = gram_schmidt(vectors)
    """
    # empty array for w 
    rtn_val = list()
    # creating iterable
    v_iter = iter(vec)
    for i in range(len(vec)):
        # getting new vector
        u = next(v_iter)
        for j in range(i):
        # normalizing our new vector and appending it to list
            v = rtn_val[j]
            # substracing projections
            u += -np.dot(u, v)/np.dot(v, v) * (v)
        # adding normalize vector to new base
        rtn_val.append(u/np.linalg.norm(u))
    # returning list of vectors 
    return rtn_val




# aproximation in unitary spaces
def apoximation_in_unitary_space(f, n, a_lim, b_lim):
    """
    Approximates a function in unitary space using polynomial basis functions.
    
    Uses the method of least squares to find the best polynomial approximation
    of degree n-1 for the given function f on the interval [a_lim, b_lim].
    
    Args:
        f (callable): Function to approximate
        n (int): Number of basis functions (degree of polynomial + 1)
        a_lim (float): Lower bound of the interval
        b_lim (float): Upper bound of the interval
        
    Returns:
        callable: Approximating polynomial function
        
    Example:
        >>> f = lambda x: np.sin(x)
        >>> h = apoximation_in_unitary_space(f, 5, 0, 2*np.pi)
    """
    # creating b vector
    b = np.zeros(n)
    A = np.zeros([n, n])
    for i in range(n):
        # column vector 
        b[i] = quad(lambda x: f(x)*x**(i), a=a_lim, b=b_lim)[0]
        for j in range(n):
            A[i, j] = quad(lambda x: x**(j)*x**(i), a=a_lim, b=b_lim)[0]
    # finding vector a
    a = np.linalg.solve(A, b)
    def h(x, a=A):
        return sum(a[i] * x**i for i in range(n))
    return h


# Riemanns Sums  
def riemann_sum(f, n, a, b):
    """
    Calculates the definite integral using the midpoint Riemann sum method.
    
    Divides the interval [a,b] into n subintervals and approximates the integral
    by summing the areas of rectangles with heights equal to function values
    at midpoints.
    
    Args:
        f (callable): Function to integrate
        n (int): Number of subintervals
        a (float): Lower bound of integration
        b (float): Upper bound of integration
        
    Returns:
        float: Approximated value of the definite integral
        
    Example:
        >>> f = lambda x: x**2
        >>> integral = riemann_sum(f, 100, 0, 1)
    """
    # calculating lenght
    lenght, val = (b-a)/n, 0
    # iterating through function
    for i in range(n):
        # taking value in middle of interval
        val += f(a + lenght*i + lenght/2) * lenght
    return val
        
# Quadrics (lesson)
def quadrics_highest_order(f, n, a, b):
    """
    Performs numerical integration using high-order quadrature method.
    
    Uses polynomial interpolation of degree n-1 to approximate the integral.
    The method is exact for polynomials of degree up to n-1.
    
    Args:
        f (callable): Function to integrate
        n (int): Number of points (determines order of quadrature)
        a (float): Lower bound of integration
        b (float): Upper bound of integration
        
    Returns:
        float: Approximated value of the definite integral
        
    Example:
        >>> f = lambda x: np.exp(x)
        >>> integral = quadrics_highest_order(f, 5, 0, 1)
    """
    # creating evenly spaced points 
    L = np.linspace(a, b, n)
    # creating matrices
    A = np.array(
        [[L[j]**i for j in range(len(L))] for i in range(len(L))]
    )
    B = [(b**i - a**i)/i for i in range(1, len(L)+1)]
    # solving system
    Z = np.linalg.solve(A,B)
    # creating quadrative, with placement for L vector
    return sum((f(L[i])*Z[i] for i in range(len(L)))) 

def quadrics_highest_order_random(f, n, a, b):
    """
    Performs numerical integration using high-order quadrature method.
    
    Uses polynomial interpolation of degree n-1 to approximate the integral.
    The method is exact for polynomials of degree up to n-1.
    
    Args:
        f (callable): Function to integrate
        n (int): Number of points (determines order of quadrature)
        a (float): Lower bound of integration
        b (float): Upper bound of integration
        
    Returns:
        float: Approximated value of the definite integral
        
    Example:
        >>> f = lambda x: np.exp(x)
        >>> integral = quadrics_highest_order(f, 5, 0, 1)
    """
    # creating evenly spaced points 
    L = np.random.rand(n) * (b-a) + a
    # creating matrices
    A = np.array(
        [[L[j]**i for j in range(len(L))] for i in range(len(L))]
    )
    B = [(b**i - a**i)/i for i in range(1, len(L)+1)]
    # solving system
    Z = np.linalg.solve(A,B)
    # creating quadrative, with placement for L vector
    return sum((f(L[i])*Z[i] for i in range(len(L)))) 


# divide into smaller regions 
def divided_quadrics_highest_order(f, n, a, b, m=3):
    """
    Performs numerical integration using divided interval quadrature method.
    
    Divides the integration interval into n-1 subintervals and applies
    quadrature method of order m on each subinterval. This approach often
    provides better accuracy for non-polynomial functions.
    
    Args:
        f (callable): Function to integrate
        n (int): Number of subintervals + 1
        a (float): Lower bound of integration
        b (float): Upper bound of integration
        m (int, optional): Order of quadrature on each subinterval. Defaults to 3.
        
    Returns:
        float: Approximated value of the definite integral
        
    Example:
        >>> f = lambda x: 1/x
        >>> integral = divided_quadrics_highest_order(f, 10, 1, 2)
    """
    L = np.linspace(a, b, n)
    value = 0
    for i in range(len(L)-1):
        value += quadrics_highest_order(f, m, L[i], L[i +1])
    return value 


