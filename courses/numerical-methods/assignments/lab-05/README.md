# Numerical Methods Implementation

This repository contains implementations of various numerical methods for linear algebra and approximation problems, along with comprehensive testing and visualization tools.

## Table of Contents
- [Problems and Theoretical Background](#problems-and-theoretical-background)
- [Algorithms](#algorithms)
- [Tests](#tests)
- [Modules Description](#modules-description)
- [Test Results](#test-results)

## Problems and Theoretical Background

### QR Decomposition

#### Problem Statement
For any matrix $A \in \mathbb{R}^{n \times n}$, find matrices $Q$ and $R$ such that:

$$A = QR$$

where $Q$ is orthogonal ($Q^TQ = I$) and $R$ is upper triangular.

#### Theoretical Foundation
- Every square matrix $A$ has a QR decomposition
- If $A$ has full column rank, the decomposition is unique
- Based on Gram-Schmidt orthogonalization process
- Preserves matrix properties while providing numerical stability

#### Solution Method
Using Gram-Schmidt process on columns $a_1, ..., a_n$ of $A$:

$$q_1 = \frac{a_1}{||a_1||}$$

$$q_k = \frac{a_k - \sum_{i=1}^{k-1} \langle a_k, q_i \rangle q_i}{||a_k - \sum_{i=1}^{k-1} \langle a_k, q_i \rangle q_i||}$$

The $R$ matrix is constructed as:

$$r_{ij} = \begin{cases} 
\langle a_j, q_i \rangle & \text{if } i \leq j \\
0 & \text{if } i > j
\end{cases}$$

#### Matrix Formulation
For a matrix $A = [a_1 | a_2 | ... | a_n]$, we get:

$$Q = [q_1 | q_2 | ... | q_n]$$

$$R = \begin{bmatrix}
r_{11} & r_{12} & \cdots & r_{1n} \\
0 & r_{22} & \cdots & r_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
0 & 0 & \cdots & r_{nn}
\end{bmatrix}$$

### Approximation in Unitary Space

#### Problem Statement
We aim to find $h^*$ such that:

$$||h^*-f|| = \inf\{||u -f|| u \in U\}$$

#### Theoretical Foundation
- Solution exists and is unique (based on UJ lecture)
- $h^*$ is optimal if and only if $f-h^*$ is perpendicular to $U$
- Uniqueness is guaranteed
- Operates on $V$ function space

#### Solution Method
Let $\{f_i\}_{i \in I}$ be base of $U$. Since $f_i \in U$:

$$
\left<f-h^*, f_i\right> = 0, \text{ so}  \left<f, f_i\right> = \left<h^*, f_i\right> 
$$

As $h^* \in U$, we can express it as a linear combination:

$$
\exists! \{a_i\}_{i \in I}: h^* = \sum_{i \in I} a_if_i
$$

Combining these terms yields:

$$
\left<h^*, f_i\right> = \sum_{j \in I} a_j \left<f_j, f_i\right> = \left<f, f_i\right> 
$$

#### Matrix Formulation
The problem reduces to solving $Aa = b$:

$$
\begin{bmatrix} 
\left<f_1, f_1\right> & \left<f_2, f_1\right> & \cdots & \left<f_n, f_1\right> \\ 
\left<f_1, f_2\right> & \left<f_2, f_2\right> & \cdots & \left<f_n, f_2\right> \\ 
\vdots & \vdots & \ddots & \vdots \\ 
\left<f_1, f_n\right> & \left<f_2, f_n\right> & \cdots & \left<f_n, f_n\right> \\ 
\end{bmatrix} 
\begin{bmatrix} 
a_1 \\ a_2 \\ \vdots \\ a_n \\ 
\end{bmatrix} = 
\begin{bmatrix} 
\left<f, f_1\right> \\ 
\left<f, f_2\right> \\ 
\vdots \\ 
\left<f, f_n\right> \\ 
\end{bmatrix}
$$

The solution vector $a$ determines $h^*$ in terms of our chosen basis.

### Quadratics Integration

#### Problem Statement
Find weights $Z_i$ and points $L_i$ such that:

$$\int_a^b f(x)dx \approx \sum_{i=1}^n f(L_i)Z_i$$

where points $L_i$ are evenly spaced in $[a,b]$.

#### Theoretical Foundation
- Uses evenly spaced points for simplicity
- Solves linear system to find optimal weights
- System constructed to be exact for polynomials up to degree n-1
- Can be divided into subintervals for better accuracy

#### Solution Method
1. Create evenly spaced points: $L_i = a + i\frac{b-a}{n-1}$
2. Construct system $AZ = B$ where:
   - $A_{ij} = L_j^i$
   - $B_i = \frac{b^i - a^i}{i}$
3. Solve for weights $Z$

#### Matrix Formulation

$$\begin{bmatrix}
1 & 1 & \cdots & 1 \\
L_1 & L_2 & \cdots & L_n \\
L_1^2 & L_2^2 & \cdots & L_n^2 \\
\vdots & \vdots & \ddots & \vdots \\
L_1^{n-1} & L_2^{n-1} & \cdots & L_n^{n-1}
\end{bmatrix}
\begin{bmatrix}
Z_1 \\
Z_2 \\
\vdots \\
Z_n
\end{bmatrix} =
\begin{bmatrix}
b-a \\
\frac{b^2-a^2}{2} \\
\frac{b^3-a^3}{3} \\
\vdots \\
\frac{b^n-a^n}{n}
\end{bmatrix}$$

## Algorithms

### Gram-Schmidt Orthogonalization
- **Complexity**: O(n²) where n is the number of vectors
- **Description**: Converts a set of vectors into an orthonormal basis
- **Implementation**: Uses iterative projection and normalization

### Approximation in Unitary Space
- **Complexity**: O(n³) for solving linear system
- **Description**: Finds best approximation of function f in polynomial space
- **Implementation**: Constructs and solves system of linear equations using inner products

### Riemann Sums
- **Complexity**: O(n) where n is number of partitions
- **Description**: Approximates definite integrals using middle-point method
- **Implementation**: Divides interval into n subintervals and sums function values

### Quadrics Integration
- **Complexity**: O(n³) for solving linear system
- **Description**: High-order numerical integration using interpolation points
- **Implementation**: Combines interpolation with exact integration of basis functions

## Tests

### QR Decomposition Tests
- **Orthogonality Test**: Measures the orthogonality error of vectors after Gram-Schmidt process
- **Matrix Size Impact**: Analyzes how error grows with matrix size
- **Matrix Type Comparison**: Compares performance between regular and dominant diagonal matrices

### Approximation Tests
- **Error Metrics**:
  - L2 norm error measurement
  - Chebyshev norm error measurement
- **Function Comparisons**: Tests on different function types (trigonometric and logarithmic)
- **Convergence Analysis**: Studies error behavior with increasing number of interpolation points

### Integration Tests
- **Method Comparison**: Analyzes different integration approaches:
  - Riemann sums
  - Quadrature methods
  - Divided quadrature methods
  - Scipy's quad method
  - Integration of interpolated functions
- **Precision Analysis**: Studies points needed for desired precision levels
- **Function Type Impact**: Compares performance on different function types

## Modules Description

### algorithms.py
Contains core implementations of numerical methods:

#### Gram-Schmidt Orthogonalization



#### Unitary Space Approximation


#### Integration Methods
- `riemann_sum`: Middle-point Riemann sum implementation
- `quadrics_highest_order`: Quadrature integration method
- `divided_quadrics_highest_order`: Divided interval quadrature method

### modules.py
Contains testing and utility functions:

#### Testing Functions
- `test_orthogonality`: Measures orthogonality of vectors
- `test_approximation_error`: Calculates approximation errors in different metrics
- `test_integration_methods`: Compares different integration methods
- `test_functions`: Provides test functions (sin+x², log)
- `solutions`: Provides analytical solutions for test functions

## Test Results

### QR Decomposition
- Orthogonality error grows with matrix size
- Dominant diagonal matrices show better stability

### Approximation
- Both L2 and Chebyshev errors decrease with more interpolation points
- Logarithmic function shows better convergence than trigonometric
- Error behavior depends significantly on function smoothness

### Integration
- Quadrature methods generally outperform Riemann sums
- Divided quadrature shows better stability
- Integration of interpolated functions provides competitive accuracy
- Required points for precision follows expected theoretical patterns


## Requirements
- NumPy
- SciPy
- Matplotlib

