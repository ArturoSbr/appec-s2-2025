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

# Iterate through columns (each column i represents the i-th treated worker)
for i in range(dist.shape[1]):
    # 1. Find index of the control unit that best matches with treated unit i
    a = dist[:, i] #me da el vector de distancias del tratado actual contra todos los controles
    idx = np.argmin(a) #me da la posición del control más cercano dentro del grupo de controles
    
    # 2. Fetch the index of the best match as it appears in `df`
    idx_0 = df[df['treat'].eq(0)].iloc[idx].name #identificador en el dataframe por posición y regresa nombre

    # 3. Write this index in column `match`
    idx_1 = df[df['treat'].eq(1)].iloc[i].name #defino idx_1 para encontrar el índice del i tratado
    df.loc[idx_1, 'match'] = idx_0 

    # 4. Remove the matched observation from the pool of candidates
    dist[idx, :] = 1e6 #elijo distancia grande para que no se vuleva a elegir que se sale de 0 y 1
