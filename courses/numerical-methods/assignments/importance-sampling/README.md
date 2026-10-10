# Importance sampling

Winter 2024/2025. Legacy comparison of Monte Carlo and importance sampling (IS) for increasingly rare events. Original calculations and conclusions remain unreviewed during this migration.

## Experiments

Efficiency gain estimates how many Monte Carlo samples are needed to match the precision of IS. The original study used evenly spaced points on `[0.01, 10]` and a logarithmic gain axis:

$$\Gamma = \frac{p_t(1-p_t)}{E_*[\chi_{X>t}(X)W^2(X)]-p_t^2}.$$

Absolute-error experiments start near the fifth point (`p_t ≈ 0.03`), use 30 samples, substitute optimized parameters, and average the errors from three replicates. The original notes attribute the Monte Carlo error plateau to missing rare events.

| Transformation | Distribution | Original parameters / reported maximum error |
|---|---|---|
| Scaling | Weibull | `b=1`, `mu=2`; `3.486882562314591e-08`; analytic search |
| Scaling | Normal | `mu=0`, `sigma=1`; `1.328265402247495e-08`; numerical minimization with bounded search |
| Translation | Weibull | Same distribution parameters; original search constrained to `c <= t` |
| Translation | Normal | Described as more efficient in the original notes |

## Numerical remarks retained for later review

The original notes warn that tail integration with `quad` can be unreliable far from the distribution centre. They also record an unresolved disagreement between theoretical gain and observed errors for translation versus scaling. These are historical observations, not validated accuracy guarantees.

## Material and TODOs

Browse the retained analysis and scratch notebooks. They contain NumPy, pandas, SciPy and Matplotlib calculations, estimator definitions and simulation plots. Execution outputs and figures are in the local migration archive.

- Combine scaling and translation.
- Investigate the disagreement between the comparisons.

[Course index](../../README.md).

[Polish report and English translation](report/README.md).
