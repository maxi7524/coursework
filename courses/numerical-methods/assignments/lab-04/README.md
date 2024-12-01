## Functions

### 1. Horner's Method

Implements Horner's scheme for efficient polynomial evaluation by factoring out powers of x.

**Features:**
- Numerically stable for low to moderate degree polynomials
- Minimizes number of arithmetic operations
- Time complexity: O(n)
- Reduces multiplication operations from O(n²) to O(n)
- Suitable for real-time applications

### 2. Neville's Algorithm

An iterative algorithm for polynomial interpolation that directly computes the value of the interpolating polynomial at a given point without explicitly finding polynomial coefficients.

**Features:**
- Constructs interpolating polynomial using recursive divided differences
- Works by progressively building higher-degree polynomials from lower-degree ones
- Time complexity: O(n²)
- Numerically stable for moderate-sized datasets
- Particularly efficient for single-point evaluation
- Handles both equally and unequally spaced data points

**How it works:**
1. Starts with 0-degree polynomials (points themselves)
2. Combines pairs of lower-degree polynomials to form higher-degree ones
3. Weights each combination based on distances to interpolation point
4. Repeats until reaching the final polynomial of degree n-1

**Example:**

### 3. Newton's Divided Differences

Computes coefficients for Newton's form of the interpolation polynomial using divided differences.

**Features:**
- Returns coefficients in Newton basis
- Useful for incremental polynomial construction
- Time complexity: O(n²)

### 4. Chebyshev Conversion

Converts polynomial coefficients from standard basis to Chebyshev basis.

**Features:**
- Improves numerical stability
- Useful for function approximation
- Leverages numpy's polynomial package

### 5. Clenshaw Algorithm

Evaluates Chebyshev series using Clenshaw's recurrence formula.

**Features:**
- Numerically stable evaluation of Chebyshev polynomials
- Linear time complexity O(n)
- More efficient than direct evaluation

## Dependencies
- NumPy
- Python 3.x

## Mathematical Background

### Polynomial Interpolation
The library provides multiple approaches to polynomial interpolation:
1. **Newton's Form** - Uses divided differences for incremental construction
2. **Neville's Algorithm** - Direct interpolation without explicit coefficient computation
3. **Chebyshev Basis** - Provides better numerical stability for high-degree polynomials

### Polynomial Evaluation
Two efficient methods are implemented:
1. **Horner's Method** - For standard polynomial basis
2. **Clenshaw's Algorithm** - For Chebyshev series

## Notes
- All functions support both scalar and array inputs where appropriate
- Input validation is assumed to be handled by the calling code
- For best numerical stability, use Chebyshev forms for high-degree polynomials
- The implementation focuses on readability and numerical stability

## Function Signatures

```python
def horner_method(x: np.ndarray, coeffs: np.ndarray, z: float) -> float
def neville(datax: np.ndarray, datay: np.ndarray, x: float) -> float
def newton_polynomial(x: np.ndarray, f: np.ndarray) -> np.ndarray
def coef_change(x: np.ndarray) -> np.ndarray
def clenshaw_algorithm(coeffs: np.ndarray, x: float) -> float
```

This library is particularly useful for numerical analysis, scientific computing, and educational purposes where polynomial interpolation and evaluation are needed.
