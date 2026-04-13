# 1. Create a distance matrix (Rows: Controls, Columns: Treated)
# This calculates the squared difference between every treated unit's
# propensity score and every control unit's propensity score.
y0 = df.loc[df['treat'].eq(0), ['p_hat']].values  # Probas of control units
y1 = df.loc[df['treat'].eq(1), ['p_hat']].values  # Probas of treatment units
dist = cdist(y0, y1, metric='euclidean')

# 2. Define the Caliper (Maximum allowable distance)
# If the closest neighbor is further away than this value, we consider
# it a bad match and leave the treated unit unmatched.
THR = 0.05

# 3. Iterate through each treated unit (each column in our matrix)
for i in range(dist.shape[1]):

    # Extract the column of distances for the i-th treated unit
    # This vector contains its distance to every control unit
    a = dist[:, i]  # All rows (:), i-th column

    #vu son vecinos ya usados
    vu = np.where(np.isin(df[df['treat'].eq(0)].index, df['match'].dropna()))[0]
    
    # A esos ya usados, les ponemos mas distancia para que no salgan en el argm
    a[vu] = np.inf

    # Find the index of the smallest distance (the 'Nearest Neighbor')
    idx = np.argmin(a)
    val = a[idx]  # Fetch distance between the two

    # 4. Apply the Caliper constraint
    if val <= THR:

        # Identify the original DataFrame index for the treated unit
        idx_1 = df[df['treat'].eq(1)].iloc[i].name.item()
        
        # Identify the original DataFrame index for the chosen control unit
        idx_0 = df[df['treat'].eq(0)].iloc[idx].name.item()
        
        # Store the match: link the treated ID to the control ID
        df.loc[idx_1, 'match'] = idx_0
        