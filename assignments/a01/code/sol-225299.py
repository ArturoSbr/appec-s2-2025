### Code added as part of the homework will be preceded by 3 hashtags "###"
### I used the base of the PSM code and added the correspondign code ###

# Imports
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

# Read data
df = pd.read_csv('../data/df.csv')

# Initialize the match column with NaNs
df['match'] = np.nan

### Assignment matching start
### Create control column
df['used'] = 0

# Declare 2D probability arrays for each group
p0 = df.loc[df['treat'].eq(0), ['p_hat']].values
p1 = df.loc[df['treat'].eq(1), ['p_hat']].values

# Declare distance matrix (Rows: Controls, Columns: Treated)
dist = cdist(p0, p1, metric='euclidean')

# Define the Caliper (Maximum allowable distance)
# If the closest neighbor is further away than this value, we consider
# it a bad match and leave the treated unit unmatched.
THR = 0.05

# Iterate through columns (each column i represents the i-th treated worker)
for i in range(dist.shape[1]):

    # 1. Find index of the control unit that best matches with treated unit i
    #Extract the column of distances for the i-th treated unit
    # This vector contains its distance to every control unit
    a = dist[:, i]  # All rows (:), i-th column

    ### Use only values that contain 'used' values as 0
    new_mask = (df.loc[df['treat'].eq(0), 'used'].eq(0))

    # 4. Remove the matched observation from the pool of candidates
    new_a = np.where(new_mask, a, np.inf)

    # Find the index of the smallest distance (the 'Nearest Neighbor')
    ### Adjusted to use the new mask remaining distance values
    idx = np.argmin(new_a)
    val = new_a[idx]  # Fetch distance between the two

    # 2. Fetch the index of the best match as it appears in `df`
    if val <= THR:

        # Identify the original DataFrame index for the treated unit
        idx_1 = df[df['treat'].eq(1)].iloc[i].name.item()

        # Identify the original DataFrame index for the chosen control unit
        idx_0 = df[df['treat'].eq(0)].iloc[idx].name.item()

        # 3. Write this index in column `match`
        ### Mark control unit as used
        df.loc[idx_0, 'used'] = 1

        # Store the match: link the treated ID to the control ID
        df.loc[idx_1, 'match'] = idx_0


