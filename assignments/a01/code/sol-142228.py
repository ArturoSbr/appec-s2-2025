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

# Caliper
THR = 0.05

disponibles = np.ones(dist.shape[0], dtype=bool)

for i in range(dist.shape[1]):
        
    a = dist[:, i].copy()
    a[~disponibles] = np.inf   
    idx = np.argmin(a)
    val = a[idx]
    
    if val <= THR:
        
        idx_1 = df[df['treat'].eq(1)].iloc[i].name.item()
        idx_0 = df[df['treat'].eq(0)].iloc[idx].name.item()
        df.loc[idx_1, 'match'] = idx_0
        disponibles[idx] = False