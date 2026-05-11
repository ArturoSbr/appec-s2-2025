# Difference in Differences

Difference in Differences (DiD) is a statistical technique used to estimate the
causal effect of a specific intervention or treatment (such as a law change, a
new policy or a marketing campaign) by comparing the changes in outcomes over
time between a "treatment" group and a "control" group.

---

Imports
"""

!pip install linearmodels
from linearmodels.panel.model import PanelOLS
import numpy as np
import pandas as pd

"""## Minimum Wages and Employment (Card and Krueger, 1994)

In 1992, the state of New Jersey raised the minimum wage, while the neighboring
state of Pennsylvania did not. Card and Krueger use this natural experiment to
study the effect that increasing the minimum wage has on employment.

To do so, they use fast-food restaurants in both states to see how the number
of full-time employees changed between 1991 (before the policy took place) and
1992 (after the policy kicked in).

## Q1. No Controls

We will start off with a $2 \times 2$ design and no controls.

$$
    E(Y_{it} | t, D_i) = \beta_0 + \beta_1 D_i + \beta_2 t +
    \beta_3 (t \cdot D_i)
$$
"""

# Load Data
URL = 'https://raw.githubusercontent.com/ArturoSbr/econometrics-ii-2025/refs/heads/main/assignments/did/data/card-krueger.csv'
df1 = pd.read_csv(URL)[[
    'i', 't', 'empft', 'state', 'psoda', 'pfry', 'pentree', 'nmgrs', 'status_1',
    'pctaff'
]].dropna()
df1.head()

# Only keep restaurants that answered the second interview
df1 = df1[df1['status_1'].eq(1)]  # Keep rows where `status_1` equals `1`

# Declare post-treatment indicator column
df1['post'] = np.where(
    df1['state'].eq(1) & df1['t'].eq(1),  # New Jersey and t=1
    1,  # Value if condition holds
    0,  # Value if condition doesn't hold
)  # 1 if `t` equals 1, 0 otherwise

# Set `i` and `t` as indexes
df1 = df1.set_index(['i','t'])  # Columns `i` and `t` used as indexes

# Declare model with entity and time fixed effects
m1 = PanelOLS(
    dependent=df1['empft'],
    exog=df1[['post']],
    entity_effects=True,
    time_effects=True
)

# Fit model
r1 = m1.fit(cov_type='clustered')

# Print estimated effect on employment
print(f"\nEstimated effect: {r1.params['post'].item():.2f}\n")

"""## 2. Adding Controls

First off, we should only include controls that vary over time. Otherwise,
they are already absorbed by each unit's fixed effect ($\alpha_i$). Beyond
that, there's a major risk of adding "bad controls." For example, if raising
the minimum wage causes restaurants to hike prices, adding `pfry` would
soak up some of the policy's effect and bias our estimate for `treat`.

In practice, we solve this by controlling for covariates **before** the
policy took place. We record the characteristics of restaurants in 1991 to
capture a baseline that is unaffected by the subsequent wage hike.
Mathematically, instead of using $X_{it}$, we use $X_i$ (the 1991 values).

Since $X_i$ is constant over time, it would normally be absorbed by the
entity fixed effects. To prevent these *snapshots* from being absorbed, we
interact them with time ($t$). This allows the model to account for
different trends based on initial characteristics without introducing
endogeneity.

$$
    E(Y_{it} | t, D_i, X_i) = \beta_0 + \beta_1 D_i + \beta_2 t +
    \beta_3 (t \cdot D_i) + \gamma (t \cdot X_i)
$$

---

You don't need to do anything here. Just take a look at the code and try to
understand it.
"""

# Get snapshot (no need to do anything here)
controls = ['psoda', 'pfry', 'pentree', 'nmgrs', 'pctaff']
snapshot = df1.sort_index(level=['i', 't']).groupby(level='i')[controls].first()

# Join snapshot back to df
df1 = pd.merge(
    left=df1.drop(columns=controls),
    right=snapshot,
    left_index=True,
    right_index=True
)

# Interact snapshot columns with time
df1[controls] = df1[controls].multiply(
    df1.index.get_level_values(1),
    axis=0
)

# Init model
m2 = PanelOLS(
    dependent=df1['empft'],
    exog=df1[['post'] + controls],
    entity_effects=True,
    time_effects=True
)

# Fit model
r2 = m2.fit(cov_type='clustered')

# View results
print(f"Estimated effect: {r2.params['post'].item():.2f}.")

"""## 3. Multiple Periods and Heterogeneous Treatment Effect

An Event Study is a version of DiD that models heterogeneous treatment
effects across time. $t$ is used to model time-level FEs, while $k$ is
a new variable that models the number of periods until a unit gets
treated. Mathematically, for a unit treated in period $t = \tau$, its
new time variable is calculated using $k = t - \tau$.

Periods where $k \lt 0$ are called *leads* (think of the periods *leading*
up to the policy), and periods where $k \ge 0$ are called *lags*. We normally
set $k = -1$ as the baseline because it represents the last period before the
treatment began, though any other $k$ could be set as the baseline.

$$
    Y_{it} = \alpha_i + \lambda_t + \sum_{k \neq -1} \delta_k D_{it}^k
    + \varepsilon_{it}
$$

* $\alpha_i$: Unit fixed effects (soaks up person/entity baselines).
* $\lambda_t$: Time fixed effects (soaks up shocks common to everyone).
* $k$: "Event time" (periods relative to treatment).
* $D_{it}^k$: A dummy that is 1 if unit $i$ is exactly $k$ periods away
from their treatment date at time $t$.
* $\delta_k$: The dynamic treatment effect at period $k$.

A **strong assumption** made by this model is that the treatment group remains
treated after the first time they receive the treatment. In other words, units
cannot switch their treatment status back to control after they've been treated.

### Testing Parallel Trends (Anticipated Treatment Effects)

Notice that this model allows us to test for pre-treatment effects! Ideally,
we want no anticipated effects, because in theory, the treatment effects should
begin **after** a unit becomes affected by a policy, **not before**!

To test for anticipated treatment effects, we must perform an $F$-test to check
that $\delta_l = 0 \space \forall \space l \lt 1$. Performing individual
$t$-tests is not enough because the hypothesis must test the significance of all
leading periods simultaneously.

### A Word of Caution

Event Studies were introduced in 1999, and for about 22 years, researchers
used them to study natural experiments where adoption was staggered (e.g.,
unit $i$ is treated in 2005, and unit $j$ in 2007).

However, recent work—most notably by Goodman-Bacon (2021)—showed that
standard TWFE regressions can produce biased results in this setting. The
problem is the "Forbidden Comparison": the model often uses **already-treated**
units as controls for **newly-treated** units (e.g., a unit treated in 2005
is used as a counterfactual for a unit treated in 2007).

If the effect of the treatment changes over time (e.g., if the policy gets
stronger the longer it's in place), using an already-treated unit as a
benchmark will attenuate the estimated effect on units treated later. In
other words, you end up subtracting the *change* in the early-adopters'
outcome from the *change* in the late-adopters' outcome.

This can lead to "negative weights," where a positive treatment effect
actually shows up as negative in your results. Essentially, the OLS
estimator gets confused by time-varying treatment effects when calculating
the average. Today, we use "clean" estimators (like Callaway & Sant'Anna)
that explicitly forbid using already-treated units as controls.

In summary, if the treatment is rolled out gradually (i.e., adoption is
staggered), **DO NOT USE EVENT STUDIES**! Use a more modern method, such as
the one proposed by [Callaway & Stant'Anna (2021)](
    https://www.sciencedirect.com/science/article/abs/pii/S0304407620303948
).
"""

# Read data
URL_CS = 'https://raw.githubusercontent.com/ArturoSbr/econometrics-ii-2025/refs/heads/main/assignments/did/data/callaway-santanna.csv'
df2 = pd.read_csv(URL_CS)
df2.head()

#borrar
df2['first.treat'].describe()

# Only keep rows that are never treated or treated in 2006
df2 = df2[df2['treat'].eq(0) | df2['first.treat'].eq(2006)]

# Declare event-time variable (k)
df2['k'] = np.where(
    df2['treat'].eq(1),  # Only declare 'k' for treatment group
    df2['year'] - df2['first.treat'],  # Declare column k as year - tau
    np.nan  # Set to NaN for control group
)
df2.head()

# Turn k into dummies
df2 = pd.get_dummies(data=df2, columns=['k'], dtype=int)  # Only column 'k'

# Set indexes
df2 = df2.set_index(['countyreal', 'year'])  # Set county and year as multi-index

# Declare regressors (only columns with 'k_' in their name and k != -1)
# Hint: the baseline column is named 'k_-1.0'
exog = [col for col in df2.columns if col.startswith('k_') and col != 'k_1.0']

# Decalre model
m3 = PanelOLS(
    dependent=df2['lemp'],
    exog=df2[exog],
    entity_effects=True,
    time_effects=True
)

# Fit model
r3 = m3.fit(cov_type='clustered')

# View results
print(r3)