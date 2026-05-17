# Final Assignment

This assignment will dive deeper into Difference in Differences (DiD). Our
goal is to see how gradual refinements in the methodology yield different
(and cleaner) estimates of a treatment effect. We will start off by
estimating the ATT with an event study, then with a simplified version of
the Callaway Sant'Anna estimator, and then with the actual Callaway
Sant'Anna library.

## About the Experiment

[Callaway and Sant'Anna (2021)](
    https://www.sciencedirect.com/science/article/abs/pii/S0304407620303948
) study the causal impact of state-level minimum wage increases on
county-level teen employment using data from 2003 to 2007. Because states
rolled out these policies gradually, counties are grouped into cohorts
based on the specific year their wage increase began (2004, 2006 or 2007).
These treatment groups are compared against a control group of
never-treated counties as well as *valid* not-yet treated counties to
isolate average treatment effects.

## Dataset

The data is available in file `assignments/final/data/wages.csv`. It
contains a balanced panel tracking county-level teen employment and we
will use it to estimate the causal effect of increasing the minimum wage.

## Step-by-Step Instructions

### Setting things up

1. [Set up your virtual environment](
    https://github.com/ArturoSbr/appec-s2-2025#virtual-environment
).
2. Open the repo in VS Code with File > Open Folder > [Choose the location
   where you cloned this repo].
3. Open a new Terminal in VS Code with Terminal > New Terminal.
    * Look for the `+` icon in the top right of the terminal panel.
    * Click the `⌄` icon next to it and select Git Bash (if you use
      Windows) or bash or zsh (if you use Mac).
    * Avoid using PowerShell or Command Prompt!
4. Switch to the `main` branch with `git checkout main`.
5. Update the branch with `git pull origin main`.
6. Create **your own branch** with `git checkout -b final/<your ID here>`.
   For example: `git checkout -b final/130524`.
7. Open file `assignments/final/code/main.py` and edit it by answering the
   questions described in the following section.

### Questions

#### 1. Event Study

1. Declare column `k` as $year - \tau_i$. This new Event-Time column represents
the number of periods *to* or *after* treatment.
2. Set units and years as the indexes of dataframe `es`. This structures the
dataframe in a format that's compatible with `PanelOLS`.
3. Turn column `k` to dummies and store this result in object `ks`.
4. Do a Left Join between `es` (left) and `ks` right. This way, you get to keep
the original version of column `k` as well as its one-hot-encoded (i.e., dummy)
representation.
5. The Left Join from the previous question resulted in some entries having Null
values in the encoded columns. Fill those Null values with `0`.
6. Declare `m1` using the following spec:

$$
    Y_i = \alpha_i + \lambda_t + \sum_{k \ne -1} \delta_k D_{it}^k +
    \varepsilon_{it}
$$

These steps will store your estimated effects in an array named `q1_res` :)

#### 2. Callaway Sant'Anna at home

In Callaway and Sant'Anna (2021), a *cohort* is a group of observations that
started getting treated in the same time period. For example, counties that
increased the minimum wage in $\tau_i = 2004$ belong to cohort $g = 2004$.

For each cohort $g$ and time period $t$, they compare group $g$ against:

a. Never-treated units at time $t$, and
b. Eventually-treated units that are not-yet treated at time $t$ and are not
   part of $g$.

This way, the authors can calculate the Average Treatment Effect on the Treated
(ATT) of group $g$ at time $t$. They call this estimate $ATT(g, t)$ and
calculate it for all cohorts $g \in G$ and time periods $t \in T$.

In our dataset, $G = \{2004, 2006, 2007\}$ and $T = \{2003, 2004, ..., 2007\}$,
which implies we will have $3 \times 5 = 15$ different values for $ATT(g, t)$,
and we can aggregate them by event-time (time to treatment), by calendar year,
by cohort, etc.

We kick things off by getting the list of all years and cohorts available in the
data (I already did this for you). We will iterate for each $g \in G$ and
$t \in T$.

1. Declare `mask_control` as rows where:
    * $year = t$ (time condition)
    * Unit is never treated (condition 1)
    * Unit hasn't begun treatment yet by year $t$ and is not cohort $g$
      (condition 2)
2. Declare `mask_treatment` as rows where:
    * $year = t$ (time condition)
    * Cohort is $g$ (condition 3)
3. Apply `mask_control` and `mask_treatment` to `df` to calculate the observed
   difference in `log_emp` between both groups.
4. Use `mask_control` and `mask_treatment` on `df` to calculate a $t$-test
   between both groups.

In the original paper, the authors calculate $ATT(g, t)$ using a doubly robust
estimator. In this homemade recreation of the CS estimator, we manually built
all 15 different combinations of $t$ and $g$ and used a $t$-test to check if the
average employment is different between the treatment and control groups.

The takeaway here is how the groups are built. Namely, we built a valid
control group for each pair $(g, t)$ using never-treated units as well as
treatment units that are not yet treated (and that also belong to a different
cohort because it doesn't make sense to compare $g$ against itself!).

So there you go! The Callaway Sant'Anna estimator is not rocket science! It is
actually much simpler than the old Event Studies that economists used for
over 20 years!

Your results will be automatically stored in `q2_res`.

#### 3. Official CS Library

### Submitting your code

Follow these steps once you think your code is good to go.

1. Verify that you are on **your own branch** by running `git branch`.
This command lists all local branches; your branch name,
`final/<your ID here>`, should be clearly highlighted with an asterisk.
2. Save your file in VS Code (`File > Save`) and add your code to the staging
area by running: `git add assignments/final/code/main.py`.
    * This command only adds `main.py` to the staging area. Please **DO NOT**
    stage any other files. All you need to upload is your version of
    `main.py`. **DO NOT** run `git add .` or `git add *`, as this will
    upload extra background files that should not be tracked.
3. Commit your changes with a clear message:
`git commit -m "Type a useful message here"`. For example:
`git commit -m "First attempt at Q1 and Q2"`. Avoid vague messages like
`git commit -m "Attempt 79 NEW v4"`.
4. Push your changes to GitHub.
   * **First time pushing your branch:**
    `git push --set-upstream origin final/<your ID here>`
    For example: `git push --set-upstream origin final/130524`.
   * **Subsequent pushes (after fixing a mistake):** `git push`
5. Check your results in the repository's [Actions tab](
   https://github.com/ArturoSbr/appec-s2-2025/actions
   ) by clicking on your latest commit message. If you do not get full
   points, read the error logs in your workflow run to see what failed,
   modify your code locally, and repeat steps 2 through 5 to try again!
