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


#### 2. Callaway Sant'Anna at home


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
   