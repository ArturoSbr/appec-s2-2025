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

# Caliper distancia maxima permitida
THR = 0.05

# Iteramos por cada columna para trabajador tratado
for i in range(dist.shape[1]):
    # encontrar el control mas cercano al tratado i
    idx = np.argmin(dist[:, i])

    # checamos si la distancia esta dentro del caliper
    if dist[idx, i] <= THR:
        # sacamos el indice original del tratado en el dataframe
        idx_1 = df[df['treat'].eq(1)].iloc[i].name
        # sacamos el indice original del control en el dataframe
        idx_0 = df[df['treat'].eq(0)].iloc[idx].name
        

        # guardamos el match
        df.loc[idx_1, 'match'] = idx_0

        # le ponemos inf para que ya no lo puedan agarrar en la siguiente iteracion ya que al poner infito 
        # es la distancia máxima y nada va a superar al infinito entonces por default se quita del pool de reemplazo 
        dist[idx, :] = np.inf
print(df[['treat', 'match']].head(20))
print('Matches:', df['match'].notna().sum())
print('Duplicados:', df['match'].dropna().duplicated().sum())