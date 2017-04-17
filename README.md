# BRISE
Benchmark Reduction via Adaptive Instance Selection

See measurements directory for benchmarking results.

Usage:
python start.py FILENAME DATA_TYPE CONFIGS_START_COUNT DELTA MAX_CONFIGS_COUNT

Calculate a regression model and near optimal configuration from an experiment's csv-file FILENAME. DATA_TYPE corresponds to Name column of the csv-file. Minimal starting training-testing set corresponds to CONFIGS_START_COUNT number, amount of configurations already measured. DELTA corresponds to an amount of new configurations to be measured/retrieved from csv in one iteration. MAX_CONFIGS_COUNT is the maximal possible amount of configurations in the current search space.

The csv-file have the following mandatory fields:
FR - CPU frequency
TR - number of threads
EN - energy consumption using the respective configuration
TIM - algorithms runtime using the respective configuration
Name - name of the algorithm/performed action
