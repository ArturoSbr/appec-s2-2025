# Propensity Score Matching
In class, we wrote the following naive algorithm, which matches each treatment
unit to the control unit nearest to them based on the propensity score
predicted by our classifier.

```python
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
```

Notice that we are matching **with replacement**, meaning multiple treatment
units could be matched with the same control unit. This can lead to a few
control units carrying too much weight, potentially biasing our results.

## Your Job
Modify our original algorithm to match **without replacement**. Once a control
unit is matched, it is permanently removed from the set of candidates for
future treatment units.

Your algorithm should:
1. Initialize a new column `df['match']` filled with `np.nan`.
2. Calculate the euclidean distance matrix between all control and treatment
   units.
3. Iterate through each treated unit:
    a. Find the closest control unit that **has not been used yet**.
    b. If the distance is within the caliper (`THR`), pair them up.
    c. Ensure that this specific control unit cannot be picked again in
       subsequent iterations of the loop.
    d. Store the **index** of the control unit in `df['match']`.

## Handing in Your Assignment
1. Clone the repo: `git clone git@github.com:ArturoSbr/appec-s2-2025.git`.
You can skip this step in case you already have a copy.
2. Set the working directory: `cd appec-s2-2025`.
3. Update to the latest version: `git pull`.
4. Create your branch: `git checkout -b a01-<your ID here>`.
5. Create your solution file from the skeleton:
   `cp assignments/a01/skeleton.py assignments/a01/sol-<your ID here>.py`.
6. Implement your logic in your new file and submit:
    - `git add assignments/a01/sol-<your ID here>.py`
    - `git commit -m "My PSM solution"`
    - `git push origin a01-<your ID here>`

## Tips
I suggest you upload the data and skeleton code to Google Colab and play with
it there. Once your Colab notebook is working as intended, copy and paste the
code to your `sol-<your ID here>.py` file and upload your homework (step 6).

I'll be reviewing these manually. Please don't send me the generic slop that
Gemini or ChatGPT spits out; I'd much rather see your own logic, even if it's
a bit messy.
