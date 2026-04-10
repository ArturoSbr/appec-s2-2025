# Imports
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

# Read data
df = pd.read_csv("../data/df.csv")

# Start empty
df["match"] = np.nan

# Split groups
c0 = df.loc[df["treat"].eq(0)]
t1 = df.loc[df["treat"].eq(1)]

# Build distance matrix
p0 = c0[["p_hat"]].values
p1 = t1[["p_hat"]].values
dist = cdist(p0, p1, metric="euclidean")

THR = 0.05
BIG = 999999.0

# Match without replacement
for i in range(dist.shape[1]):
    a = dist[:, i]
    idx = np.argmin(a)
    val = a[idx]

    if val <= THR:
        idx_1 = t1.iloc[i].name
        idx_0 = c0.iloc[idx].name
        df.loc[idx_1, "match"] = idx_0

        # Make this control impossible to use again
        dist[idx, :] = BIG

print(df[["treat", "p_hat", "match"]])
