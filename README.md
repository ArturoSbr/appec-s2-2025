# Applied Econometrics II

Welcome! This is the repo where you'll find all the material seen in class.
It is also the place you'll be pushing all your assignments to.

## Syllabus

1. Predictive Modeling
2. A/B Testing
3. Matching
4. Instrumental Variables
5. Regression Discontinuity Design
6. Panel Data, Fixed Effects and Random Effects
7. Difference in Differences

## About this repo

This repo is meant to resemble a typical industry-grade project. This means
you'll have to pass a few tests for your code to be accepted.

## Why this workflow?

In this class, you're expected to submit your code by creating a new branch,
pushing your changes and passing a few builds. The goal of this workflow is
to help you understand how code is written and shared in modern companies.

By the end of this course, you'll be able to:
- Write clean, consistent, and well-documented code;
- Push your code to your own branch; and
- Pass builds.

By following these guidelines, you won't be taken by surprise when someone
asks you to open a PR to squash a bug or implement a new feature.

## Structure of this repo

```
.
├── .github                  # Build configuration (ignore this)
├── assignments              # Model assignments
│   ├── did                    # Diff-in-diff assignment
│   ├── final                  # Final assignment
│   └── psm                    # Propensity Score Matching assignment
├── lectures                 # Lecture notes
├── .flake8                  # Linting configuration (ignore this)
├── .gitignore               # Files ignored by git (ignore this)
├── environment.yml          # Use this to create your environment
├── grader-requirements.txt  # Development environment (ignore this)
└── README.md                # Intro to this repo
```

## Virtual Environment

In order for our code to run the same way across devices (i.e., **my** Mac Mini
and **your** MacBook Air), we need to be processing the code with the same
Python and library versions. Otherwise, your results might differ from what the
autograder expects and you'll get a low grade. You therefore need to write your
code using the same environment as the autograder, and you can do this by
following these steps:

1. Open [VS Code](https://code.visualstudio.com/) (we installed this together
last semester!).

2. Go to Terminal > New Terminal.
  - Look for the `+` icon in the top right of the terminal panel.
  - Click the `⌄` icon next to it and select `Git Bash` (Windows) or
  `bash` or `zsh` (Mac).
  - **Avoid using PowerShell or Command Prompt.**

3. Type `conda` and press `enter`.
  - If it says `command not found`, go to the [Miniconda downloads
  page](https://docs.anaconda.com/miniconda/), install it, and **restart
  VS Code**.
  - If it works, move to the next step.

4. Navigate to your project folder using the `cd` command.
  - Example: `cd Documents/appec-s2-2025` (make sure the path matches
  where you cloned the repo).

5. Delete last semester's environment.
  - Run `conda env remove --name=appec`.
  - If it says `EnvironmentLocationNotFound`, that's perfect—it means
  you're starting fresh.

6. Create the new environment: `conda env create -f environment.yml`.
  - This takes time. Let it finish until you see the cursor again.

7. Install the Jupyter Extension.
  - Click the "Extensions" icon on the left (or `Ctrl+Shift+X`).
  - Search for "Jupyter" (the one by Microsoft) and hit Install.

8. Setting the Kernel:
  - Open a `.ipynb` file.
  - In the top right, click "Select Kernel" > "Python Environments"
  and pick `appec (Python 3.11.x)`.

And done! Your computer is ready to go. Just remember to activate your
environment when writing code.

- If you're writing a Python file (.py extension), run `conda activate appec`.
- If you're writing a Jupyter Notebook (.ipynb extension), open the notebook and
go to the top right hand corner, click on "Select Kernel" and choose "appec
(Pyton 3.11.3).

## Contributing (AKA submitting your homework)

1. Clone the repo to your local (if you haven't done so already)
3. Switch to `develop` (`git checkout develop`)
2. Pull the latest changes (`git pull origin develop`)
3. Create a branch (`git checkout -b assignment/{homework id}-{student id}`)
    - For example `git checkout -b assignment/ivs-659402`
4. Submit a single Python file
    - Must be named `{homework id}-{student id}.py` (eg, `ivs-659402.py`)
    - Must be placed in the corresponding homework's `code` directory (eg,
    `./assignments/ivs/code/`)
    - Submit the file by addig, commiting and pushing your code
5. If your branch and Python script are named correctly (steps 3 and 4), your
branch will trigger a few Actions, which will in turn grade your code.

## Resources
- [Mostly Harmless Econometrics](https://www.mostlyharmlesseconometrics.com/)
- [An Introduction to Statistical Learning](https://www.statlearning.com/)

## Participation Tracker

|      Name | Score |
|-----------|-------|
|      Aldo |     7 |
|   Eduardo |    20 |
|     Savio |     9 |
|   Elideth |    10 |
|    Alexis |    10 |
|    Astrid |     9 |
|     Karen |     5 |
