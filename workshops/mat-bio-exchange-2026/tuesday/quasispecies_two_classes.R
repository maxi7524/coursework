# Deterministic two-class quasispecies model
#
# x0: exact master sequence
# x1: all mutant sequences pooled into one class
#

# One generation of mutation-selection dynamics 

quasispecies_step <- function(x, u, L, f0, f1 = 1) {
  stopifnot(length(x) == 2, u >= 0, u <= 1, L >= 1, f0 > 0, f1 > 0)

  # Probability that the master is copied without any mutation.
  q <- (1 - u)^L

  # Columns are parental classes; rows are offspring classes.
  # There is no back mutation from x1 to x0.
  Q <- matrix(
    c(q, 1 - q,
      0, 1),
    nrow = 2,
    ncol = 2
  )

  F <- diag(c(f0, f1))
#look at the compactness of matrix representation!
  offspring <- Q %*% F %*% x

  # Normalization converts abundances back into frequencies.
  as.vector(offspring / sum(offspring))
}


# Numerical equilibrium obtained by iteration ------------------------------

equilibrium_numeric <- function(
    u,
    L,
    f0,
    f1 = 1,
    x_initial = c(1, 0),
    tolerance = 1e-12,
    max_generations = 100000) {

  x <- x_initial / sum(x_initial)

  for (generation in seq_len(max_generations)) {
    x_new <- quasispecies_step(x, u, L, f0, f1)

    if (max(abs(x_new - x)) < tolerance) {
      return(c(x0 = x_new[1], x1 = x_new[2]))
    }

    x <- x_new
  }

  warning("Equilibrium was not reached within max_generations")
  c(x0 = x[1], x1 = x[2])
}


# Analytical equilibrium ---------------------------------------------------

equilibrium_analytic <- function(u, L, f0, f1 = 1) {
  q <- (1 - u)^L

  # Above the error threshold q*f0 <= f1, the master cannot be maintained.
  x0 <- ifelse(
    q * f0 > f1,
    (q * f0 - f1) / (f0 - f1),
    0
  )

  data.frame(
    u = u,
    q = q,
    genomic_mutation_probability = 1 - q,
    x0 = x0,
    x1 = 1 - x0,
    mean_fitness = ifelse(q * f0 > f1, q * f0, f1)
  )
}


# Parameters ---------------------------------------------------------------

L <- 20

# Choosing f0/f1 = exp(1) makes u_c approximately 1/L.
f1 <- 1
f0 <- exp(1)

# Exact and small-u approximate critical mutation probabilities.
u_critical_exact <- 1 - (f1 / f0)^(1 / L)
u_critical_approx <- log(f0 / f1) / L

cat("Sequence length L:", L, "\n")
cat("Master fitness f0:", f0, "\n")
cat("Mutant fitness f1:", f1, "\n")
cat("Exact critical u:", u_critical_exact, "\n")
cat("Approximate critical u:", u_critical_approx, "\n")
cat("1/L:", 1 / L, "\n")


# Scan of the per-site mutation probability --------------------------------

u_values <- seq(
  from = 0,
  to = 2 / L,
  length.out = 501
)

scan <- equilibrium_analytic(
  u = u_values,
  L = L,
  f0 = f0,
  f1 = f1
)


# Plot 1: equilibrium frequencies versus per-site mutation probability ------

matplot(
  scan$u,
  cbind(scan$x0, scan$x1),
  type = "l",
  lty = 1,
  lwd = 3,
  col = c("#2166AC", "#B2182B"),
  xlab = "Per-site mutation probability, u",
  ylab = "Equilibrium frequency",
  ylim = c(0, 1)
)

abline(
  v = u_critical_exact,
  col = "black",
  lty = 2,
  lwd = 2
)

abline(
  v = 1 / L,
  col = "grey50",
  lty = 3,
  lwd = 2
)

legend(
  "right",
  legend = c(
    expression(x[0]^"*"),
    expression(x[1]^"*"),
    expression("exact " * u[c]),
    expression(1 / L)
  ),
  col = c("#2166AC", "#B2182B", "black", "grey50"),
  lty = c(1, 1, 2, 3),
  lwd = c(3, 3, 2, 2),
  bty = "n"
)


# Plot 2: collapse for different sequence lengths --------------------------
#
# The natural horizontal variable is the genomic mutation rate U = L*u.
# For f0/f1 = exp(1), the threshold approaches U_c = 1.

L_values <- c(3,10, 20, 50, 100)
scaled_u <- seq(0, 2, length.out = 501)

x0_by_L <- sapply(
  L_values,
  function(current_L) {
    current_u <- scaled_u / current_L

    equilibrium_analytic(
      u = current_u,
      L = current_L,
      f0 = f0,
      f1 = f1
    )$x0
  }
)

matplot(
  scaled_u,
  x0_by_L,
  type = "l",
  lty = 1,
  lwd = 2.5,
  col = seq_along(L_values),
  xlab = expression("Scaled mutation rate  " * U == L * u),
  ylab = expression("Master frequency  " * x[0]^"*"),
  ylim = c(0, 1)
)

abline(v = 1, col = "black", lty = 2, lwd = 2)

legend(
  "topright",
  legend = c(paste("L =", L_values), expression(U[c] == 1)),
  col = c(seq_along(L_values), "black"),
  lty = c(rep(1, length(L_values)), 2),
  lwd = c(rep(2.5, length(L_values)), 2),
  bty = "n"
)


# Optional numerical check at three mutation probabilities -----------------

u_check <- c(
  0.5 * u_critical_exact,
  0.9 * u_critical_exact,
  1.1 * u_critical_exact
)

numeric_check <- t(vapply(
  u_check,
  equilibrium_numeric,
  FUN.VALUE = c(x0 = 0, x1 = 0),
  L = L,
  f0 = f0,
  f1 = f1
))

analytic_check <- equilibrium_analytic(
  u = u_check,
  L = L,
  f0 = f0,
  f1 = f1
)[, c("x0", "x1")]

comparison <- data.frame(
  u = u_check,
  numeric_x0 = numeric_check[, "x0"],
  analytic_x0 = analytic_check$x0,
  numeric_x1 = numeric_check[, "x1"],
  analytic_x1 = analytic_check$x1
)

print(comparison)
