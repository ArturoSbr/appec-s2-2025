# Imports
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

# Read data
df = pd.read_csv('../data/df.csv')

# Initialize the match column with NaNs
df['match'] = np.nan

# Declare 2D probability arrays for each group
p0 = df.loc[df['treat'].eq(0), ['p_hat']].values
p1 = df.loc[df['treat'].eq(1), ['p_hat']].values

# Declare distance matrix (Rows: Controls, Columns: Treated)
dist = cdist(p0, p1, metric='euclidean')

# Iterate through columns (each column i represents the i-th treated worker)
for i in range(dist.shape[1]):

    # 1. Find index of the control unit that best matches with treated unit i
    # 2. Fetch the index of the best match as it appears in `df`
    # 3. Write this index in column `match`
    # 4. Remove the matched observation from the pool of candidates
