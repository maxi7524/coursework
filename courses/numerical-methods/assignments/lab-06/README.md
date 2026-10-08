## File Descriptions
- **algorithms.py**: Contains implementations of various root-finding algorithms including Bisection, Falsi, Newton-Raphson, and Secant methods.


## Prerequisites
- Python version: 3.x
- Required modules: 
  - `numpy`
  - `matplotlib` (for future visualizations)


## algorithms
### Bisection Method
- **Assumptions**:
  - The function is continuous on the interval [a, b].
  - There exists at least one root in the interval such that \( f(a) \cdot f(b) < 0 \).

- **Complexity**: 
  - Time complexity: \( O(\log(\frac{b-a}{\text{acc}})) \)
  - Space complexity: \( O(1) \)

- **Formula**:
  $$ c = \frac{a + b}{2} $$

- **Formula Derivation**:
  The method repeatedly bisects the interval and selects the subinterval that contains the root, narrowing down the possible locations of the root until the desired accuracy is achieved.

### Falsi Method
- **Assumptions**:
  - There exists only one root in the interval [z1, z2].
  - \( f(z1) \cdot f(z2) < 0 \).
  - The function is continuous.

- **Complexity**: 
  - Time complexity: \( O(\log(\frac{b-a}{\text{acc}})) \)
  - Space complexity: \( O(1) \)

- **Formula**:
  $$ c = \frac{a \cdot f(b) - b \cdot f(a)}{f(b) - f(a)} $$

- **Formula Derivation**:
  This method uses a secant line to approximate the root, improving the estimate based on the function values at the endpoints.

### Newton-Raphson Method
- **Assumptions**:
  - The function must be differentiable in the neighborhood of the root.
  - An initial guess \( z0 \) is required.

- **Complexity**: 
  - Time complexity: \( O(n) \) where n is the number of iterations until convergence.
  - Space complexity: \( O(1) \)

- **Formula**:
  $$ x_{i + 1} = x_i - \frac{f(x_i)}{f'(x_i)} $$

- **Formula Derivation**:
  The method uses the first-order Taylor series expansion to find the root iteratively.

### Secant Method
- **Assumptions**:
  - The function does not need to be differentiable.
  - Two initial points \( z0 \) and \( z1 \) are required.

- **Complexity**: 
  - Time complexity: \( O(n) \) where n is the number of iterations until convergence.
  - Space complexity: \( O(1) \)

- **Formula**:
  $$ x_{i+1} = x_i - \frac{f(x_i)(x_i - x_{i-1})}{f(x_i) - f(x_{i-1})} $$

- **Formula Derivation**:
  This method approximates the derivative using the difference quotient, allowing for root finding without explicit derivatives.

### Newton-Cotes Complex Quadrature
- **Purpose**: Numerical integration using Newton-Cotes formula with composite intervals
- **Parameters**:
  - `f`: Function to integrate
  - `a, b`: Integration interval bounds
  - `n`: Number of points for interpolation
  - `m`: Number of subintervals
  
- **Formula**:
  $$ \int_a^b f(x)dx \approx \frac{b-a}{mn} \sum_{k=0}^n B_k \sum_{s=0}^{m-1} f(a + \frac{(ns + k)(b-a)}{mn}) $$
  where Bk are the Newton-Cotes coefficients calculated through Lagrange basis polynomials.

- **Key Features**:
  - Uses multiple subintervals (m) to reduce Runge's phenomenon
  - Higher accuracy than simple Newton-Cotes for same number of points
  - Adaptive to both smooth and non-smooth functions

### Tests
The test suite in tests.ipynb covers several key aspects:

#### Quadrature Tests
- **Basic Validation**: Tests integration of x² over [0,10] against known analytical solution
- **Error Analysis**: Compares performance for two test functions:
  - Smooth function: sin(x) + cos²(x) - x² + 7x
  - Non-smooth function: 1/(1+x²)
- **Parameters tested**:
  - m values: 1 to 4 (number of subintervals)
  - n range: 2 to 42 (number of points)
- **Visualization**: Error plots showing convergence behavior for different m values

#### Root-Finding Tests
- **Test Functions**: Two polynomials with known roots at x=0.23 and x=0.53
- **Methods Compared**:
  - Bisection method
  - Falsi method
  - Newton-Raphson method
  - Secant method
- **Analysis Metrics**:
  - Error convergence over iterations
  - Computation time
  - Accuracy achievement for different error tolerances (10⁻¹ to 10⁻³²)
- **Test Scenarios**:
  - Small interval: [0,1]
  - Large interval: [0,100]

