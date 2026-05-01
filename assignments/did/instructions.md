# Getting Started: Difference in Differences Assignment

In order to submit your code, you need to make sure you're working on the right
branch. Otherwise, your work might get lost in the void and you won't get a
grade. Follow the instructions below to successfully submit your assignment.

## 1. Clone the Repository (Skip if you're already set up!)

If you haven't downloaded our class repository to your computer yet, you'll need
to do that first.

1. Open [VS Code](https://code.visualstudio.com/) (we installed this together
last semester!).

2. Go to Terminal > New Terminal.
  - Look for the `+` icon in the top right of the terminal panel.
  - Click the `⌄` icon next to it and select `Git Bash` (Windows) or `bash` or
  `zsh` (Mac).
  - **Avoid using PowerShell or Command Prompt.**

3. Navigate to the folder where you keep your class files using the `cd`
command.
  - Example: `cd Documents`

4. Clone the repository: `git clone <insert-repo-url-here> appec-s2-2025`

5. Move into the project folder: `cd appec-s2-2025`

## 2. Create Your Assignment Branch

If you already had the repo, or just cloned it, it's time to create the branch
where you'll be writing your code.

1. Open your terminal in VS Code (make sure you are inside the `appec-s2-2025`
folder!).

2. Switch to the `develop` branch: `git checkout develop`.

3. Pull the latest changes: `git pull origin develop`.
  - This ensures you have all the latest updates I've pushed to the class
  repository.

4. Create your assignment branch using the `git checkout -b` command.
  - The name format is strictly `assignment/did-<student-id-here>`.
  - Example: `git checkout -b assignment/did-130524` (Make sure to swap `130524`
  with your actual student ID!).

And done! Your workspace is ready to go. Just remember to activate your
environment (`conda activate appec`) when writing your Difference in Differences
assignment.

> [!IMPORTANT]
> You do **not** need to create a copy of `did.ipynb` or rename it! All you
> need to do is open the existing `did.ipynb` file and write your answers
> directly into it. Since you are working on your own branch, overwriting the
> file is perfectly safe and expected.

## 3. Pushing Your Code

Once you've finished the assignment, it's time to submit your work! Since this
assignment will be graded by hand, all you need to do is push your notebook with
the cell outputs included. Please make sure you haven't added any new cells to
the notebook.

1. Stage your notebook for commit:
  - Run `git add <your-notebook-name.ipynb>` (make sure to only add your
  notebook!).

2. Commit your changes with a descriptive message:
  - Run `git commit -m "Submit DiD assignment"`

3. Push your branch to the repository:
  - Run `git push origin assignment/did-<your-student-id>`

**Note:** We set up SSH access together last semester. You will need it to push
your code! If you don't have SSH access configured anymore, please check out
the [GitHub SSH help page](
  https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
) to set up SSH access again.
