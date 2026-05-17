"""Final Econometrics II Assignment

This file contains the final Econometrics II assignment. Refer to file
/assignments/final/instructions.md for instructions."""

import os

import differences
from linearmodels.panel import PanelOLS
import numpy as np
import pandas as pd

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
    left=None,  # Use `es` as Left
    right=None,  # User `ks` as Right
    how=None,  # Use a Left Join
    left_index=True,
    right_index=True
)

# Store names of exogenous variables in list (also set k=-1 as reference)
exog = [col for col in es.columns if col.startswith('k_') and col != 'k_-1']

# 1.5 Replace NaN from the Left Join values with 0
es[exog] = None  # Use .fillna() method

# 1.6 Declare model
m1 = PanelOLS(
    dependent=None,  # Set dependent variable here
    exog=None,  # Set controls here
    entity_effects=None,  # Use entity effects
    time_effects=None,  # Use time effects
    drop_absorbed=True,
    check_rank=True,
)

# Fit model
r1 = m1.fit(cov_type='clustered')

# Store parameters in `q1_params`
q1_res = r1.params.tolist()

# Display results
print(q1_res)


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
        n0 = mask_control.sum()
        n1 = mask_treatment.sum()

        # 2.3 Calculate observed difference in means
        # Use mask_control to calculate average log_emp of control group
        y0 = None
        # Use mask_treatment to calculate average log_emp of treatment group
        y1 = None

        # Append everything
        data.append([g, t, n0, n1, y0, y1])

# Create dataframe using our calculations
q2_res = pd.DataFrame(
    data=data,
    columns=[
        'cohort', 'year', 'n_control', 'n_treatment', 'y_control', 'y_treatment'
    ]
).sort_values(['first_treat', 'year']).reset_index()
q2_res['relative_time'] = q2_res['year'] - q2_res['cohort']

# Display results
print(q2_res)

# ------------------ 3. Official Callaway Sant'Anna Estimator ------------------

# Create a copy of `df`
cs = df.copy()

# 3.1 Set units (county) and time (year) columns as indexes
cs.set_index([None, None], inplace=True)

# 3.2 Make never-treated units have np.nan instead of 0 in `first_treat` column
cs['first_treat'] = None  # Use .replace() method

# 3.3 Declare CS model
m2 = differences.ATTgt(
    data=None,  # Pass indexed dataset
    cohort_column=None,  # Pass name of column that represents cohorts
    dosage_column=None,  # Don't do anything here
    base_period='varying',  # Don't do anything here
    anticipation=0  # Don't do anything here
)

# Fit model
r2 = m2.fit(None)  # Pass name of dependent variable here

# Aggregate fitted model at the event level
q3_res = r2.aggregate(type_of_aggregation='event')

# Display results
print(q3_res)
