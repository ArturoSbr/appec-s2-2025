"""Final Econometrics II Assignment

This file contains the final Econometrics II assignment. Refer to file
/assignments/final/instructions.md for instructions."""

import os

import differences
from linearmodels.panel import PanelOLS
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind

# Read dataset
PATH = os.path.join('..', 'data', 'wages.csv')
df = pd.read_csv(PATH)


# ------------------------------- 1. Event Study -------------------------------

# Make a copy of `df`
es = df.copy()

# 1.1 Define event-time column ($year - \tau_i$)
es['k'] = None

# 1.2 Set unit and time columns as indexes
es.set_index([None, None], inplace=True)

# 1.3 Turn column `k` into dummies (only for treated units)
ks = pd.get_dummies(
    data=es.loc[None, ['k']],  # Filter out never-treated units
    columns=['k'],
    dtype=int
)

# 1.4 Do a Left Join between `es` and `ks`
es = pd.merge(
    left=None,
    right=None,
    how=None,
    left_index=True,
    right_index=True
)

# Store names of exogenous variables in list (also set k=-1 as reference)
exog = [col for col in es.columns if col.startswith('k_') and col != 'k_-1']

# 1.5 Replace NaN from the Left Join values with 0
es[exog] = None

# 1.6 Declare model
m1 = PanelOLS(
    dependent=None,  # Set dependent variable here
    exog=None,  # Set controls here
    entity_effects=None,
    time_effects=None,
    drop_absorbed=True,
    check_rank=True,
)

# Fit model
r1 = m1.fit(cov_type='clustered')

# Store parameters in `q1_params`
q1_res = r1.params.tolist()


# ----------------------- 2. Callaway-Sant'Anna At Home ------------------------

# Get all years and treatment cohorts in the dataset
T = df['year'].unique().tolist()
G = df.loc[df['first_treat'].ne(0), 'first_treat'].unique().tolist()

# Init list where we'll store all the results
data = []

# Iterate over all (g, t) pairs
for g in sorted(G):
    for t in sorted(T):

        # 2.1 Declare mask to select control units (conditions 1 and 2)
        mask_control = (
            None  # Year equals t
            & (
                # Condition 1: Never-treated units
                None  # treat column
                # Condition 2: Not-yet treated units
                | (
                    None  # Not-yet treated
                    & None  # Not cohort g
                )
            )
        )

        # 2.2 Declare mask to select treatment cohort (condition 3)
        mask_treatment = (
            None  # Year equals t
            # Condition 3: Treatment cohort
            & None  # 3. Treatment cohort
        )

        # Calculate number of observations
        n_control = mask_control.sum()
        n_treatment = mask_treatment.sum()

        # 2.3 Calculate observed difference in means
        diff = (
            None  # Avg. log_emp of treatment
            - None  # Avg. log_emp of control
        )

        # Calculate t-test
        ttest = ttest_ind(
            a=None,  # Treatment group
            b=None,  # Control group
            equal_var=False
        )

        # Append everything
        data.append([
            g, t, diff, ttest.statistic, ttest.pvalue, n_control, n_treatment
        ])

# Create dataframe using our calculation
q2_res = pd.DataFrame(
    data=data,
    columns=[
        'first_treat', 'year', 'effect', 't-stat', 'p-value', 'n_control',
        'n_treatment'
    ]
).sort_values(['first_treat', 'year']).reset_index()

# Display results
print(q2_res)

# ------------------ 3. Official Callaway Sant'Anna Estimator ------------------

# Create a copy of `df`
cs = df.copy()

# 3.1 Set units (county) and time (year) columns as indexes
cs.set_index([None, None], inplace=True)

# 3.2 Make never-treated units have np.nan instead of 0 in `first_treat` column
cs['first_treat'] = None

# 3.3 Declare CS model
m2 = differences.ATTgt(
    data=None,  # Pass indexed dataset
    cohort_column=None,  # Pass name of column that represents cohorts
    dosage_column=None,
    base_period='varying',
    anticipation=0
)

# Fit model
r2 = m2.fit(None)  # Pass name of dependent variable

# Aggregate fitted model at the event level
q3_res = r2.aggregate(type_of_aggregation='event')

# Display results
print(q3_res)
