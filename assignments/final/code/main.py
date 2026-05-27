"""Final Econometrics II Assignment

This file contains the final Econometrics II assignment. Refer to file
/assignments/final/instructions.md for instructions."""

#!pip install differences
#!pip install linearmodels
import os

import differences
from linearmodels.panel import PanelOLS
import numpy as np
import pandas as pd


# Read dataset
PATH = os.path.join('..', 'data', 'wages.csv')
df = pd.read_csv(PATH)

# Strip whitespace from column names (defensive fix)
df.columns = df.columns.str()


# ------------------------------- 1. Event Study -------------------------------

# Make a copy of `df`
es = df.copy()

# 1.1 Define event-time column ($year - \tau_i$)
es['k'] = es['year'] - es['first_treat']

# 1.2 Set unit and time columns as indexes
es.set_index(['county', 'year'], inplace=True)

# 1.3 Turn column `k` into dummies (only for treated units)
ks = pd.get_dummies(
    data=es.loc[es['treat'] == 1, ['k']],  # Filter out never-treated units
    columns=['k'],
    dtype=int
)

# 1.4 Do a Left Join between `es` and `ks`
es = pd.merge(
    left=es,
    right=ks,
    how='left',
    left_index=True,
    right_index=True
)

# Store names of exogenous variables in list (also set k=-1 as reference)
exog = [col for col in es.columns if col.startswith('k_') and col != 'k_-1']

# 1.5 Replace NaN from the Left Join values with 0
es[exog] = es[exog].fillna(0)

# 1.6 Declare model
m1 = PanelOLS(
    dependent=es['log_emp'],
    exog=es[exog],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True,
    check_rank=True,
)

# Fit model
r1 = m1.fit(cov_type='clustered')

# Store results in a dataframe
q1_res = pd.concat([r1.params, r1.pvalues], axis=1).reset_index(names=['k'])


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
            (df['year'] == t)
            & (
                (df['treat'] == 0)
                | (
                    (df['first_treat'] > t)
                    & (df['first_treat'] != g)
                )
            )
        )

        # 2.2 Declare mask to select treatment cohort (condition 3)
        mask_treatment = (
            (df['year'] == t)
            & (df['first_treat'] == g)
        )

        # 2.3 Calculate number of observations used as control
        n0 = mask_control.sum()

        # 2.4 Calculate number of treated units
        n1 = mask_treatment.sum()

        # 2.5 Use mask_control to calculate average log_emp of control group
        y0 = df.loc[mask_control, 'log_emp'].mean()

        # 2.6 Use mask_treatment to calculate average log_emp of treatment group
        y1 = df.loc[mask_treatment, 'log_emp'].mean()

        # Append everything
        data.append([g, t, n0, n1, y0, y1])

# Create dataframe using our calculations
q2_res = pd.DataFrame(
    data=data,
    columns=[
        'cohort', 'year', 'n_control', 'n_treatment', 'y_control', 'y_treatment'
    ]
).sort_values(['cohort', 'year']).reset_index(drop=True)

# Declare first-differences column for each cohort
q2_res[['d1_control', 'd1_treatment']] = (
    q2_res.groupby('cohort')[['y_control', 'y_treatment']].diff(periods=1)
)

# Declare Diff-in-Diffs column (delta)
q2_res['delta'] = q2_res['d1_treatment'] - q2_res['d1_control']


# ------------------ 3. Official Callaway Sant'Anna Estimator ------------------

# Create a copy of `df`
cs = df.copy()

# 3.1 Set units (county) and time (year) columns as indexes
cs.set_index(['county', 'year'], inplace=True)

# 3.2 Make never-treated units have np.nan instead of 0 in `first_treat` column
cs['first_treat'] = cs['first_treat'].replace(0, np.nan)

# 3.3 Declare CS model
m2 = differences.ATTgt(
    data=cs,
    cohort_column='first_treat',
    dosage_column=None,
    base_period='varying',
    anticipation=0
)

# Fit model
r2 = m2.fit('log_emp')

# Aggregate fitted model at the event level
q3_res = r2.aggregate(type_of_aggregation='event')
q3_res = pd.concat(
    [
        q3_res['EventAggregation']['']['ATT'],
        q3_res['EventAggregation']['analytic']['std_error']
    ],
    axis=1
).reset_index()
