# Stochastic Simulations: week-11

- [algorithms_PF_and_FFBS.ipynb](algorithms_PF_and_FFBS.ipynb)
- [exercise.ipynb](exercise.ipynb)
- [utils_algorithms_PF_and_FFBS.py](utils_algorithms_PF_and_FFBS.py)

`exercise.ipynb` uses 1,000 and 2,000 particles (originally 10,000 and 100,000) with the original 20-step horizon. The retained resampling implementation allocates a quadratic particle-comparison array; 100,000 particles would require roughly 10 GB for its boolean comparison alone. These smaller demonstration runs retain the model and algorithm and produce fresh plots. Results describe the reduced simulation, not the original large run.

Open notebooks from this assignment directory so relative paths resolve correctly. Use the source environment or the nearest existing requirements/pyproject file; legacy dependencies were not upgraded.


[Course index](../../README.md)
