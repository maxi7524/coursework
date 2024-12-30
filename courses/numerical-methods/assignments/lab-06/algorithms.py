import numpy as np


# quadrics 

#### finding zero places ####

# Bisection Method
def bisection_method(f, a, b, acc, n=None):
    '''
    Bisection method for finding roots of a function.
    
    Parameters:
    f : function
        The function for which we are trying to find a root.
    a : float
        The start of the interval.
    b : float
        The end of the interval.
    acc : float
        The desired accuracy for the root.

    Returns:
    float
        The root of the function or the closest point to the root.
    '''
    if n:
        i = 0
        while i < n:
            c = (a + b) / 2 
            if f(c) == 0:
                return c
            elif f(a) * f(c) < 0:
                b = c
            else:
                a = c 
            i += 1
        return c
    
    while abs(a - b) >= acc:
        c = (a + b) / 2 
        if f(c) == 0:
            return c
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c 
    return c
            
def falsi_method(f, z1, z2, acc, n = None):
    '''
    Falsi method for finding roots of a function.
    
    Parameters:
    f : function
        The function for which we are trying to find a root.
    z1 : float
        The first point of the interval.
    z2 : float
        The second point of the interval.
    acc : float
        The desired accuracy for the root.

    Returns:
    float
        The root of the function or the closest point to the root.
    '''
    if n:
        i = 0
        while i < n:
            c = (z1 * f(z2) - z2 * f(z1)) / (f(z2) - f(z1))
            if f(c) == 0:
                return c
            elif f(z1) * f(c) < 0: 
                z2 = c
            else:
                z1 = c
            i += 1
        return c
    
    
    while abs(z1 - z2) >= acc:
        c = (z1 * f(z2) - z2 * f(z1)) / (f(z2) - f(z1))
        if f(c) == 0:
            return c
        elif f(z1) * f(c) < 0: 
            z2 = c
        else:
            z1 = c
    return c

# Newton-Raphson Method
def newton_raphson_method(f, df, z0, n):
    '''
    Newton-Raphson method for finding roots of a function.
    
    Parameters:
    f : function
        The function for which we are trying to find a root.
    df : function
        The derivative of the function.
    z0 : float
        The initial guess for the root.
    n : int
        The number of iterations.

    Returns:
    numpy.ndarray
        An array of approximations to the root.
    '''
    
    z = np.zeros(n)
    z[0] = z0
    for i in range(1, n):
        z[i] = z[i-1] - f(z[i-1]) / df(z[i-1])
    return z[n-1]

# Secant Method
def secant_method(f, z0, z1, n):
    '''
    Secant method for finding roots of a function.
    
    Parameters:
    f : function
        The function for which we are trying to find a root.
    z0 : float
        The first initial guess.
    z1 : float
        The second initial guess.
    n : int
        The number of iterations.

    Returns:
    float
        The approximation to the root after n iterations.
    '''
    z = np.zeros(n)
    z[0], z[1] = z0, z1
    for i in range(2, n):
        z[i] = z[i-1] - (f(z[i-1]) * (z[i-1] - z[i-2])) / (f(z[i-1]) - f(z[i-2]))
    return z[n-1]
