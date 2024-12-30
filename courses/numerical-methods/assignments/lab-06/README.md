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



### Tests
- To be added later.

