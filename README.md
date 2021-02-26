# TransportEd
Warehouse automation using autonomous robots

### Things not to do
- Do not merge any branches directly into the main branch without using a GitHub pull request
- Do not merge pull requests without a reviewer approving it

### Workflow guide
1. Switch to the main branch with `git checkout main` then `git pull` from console or do the same using your IDE, to make sure your main branch is up to date.
2. On console, `git checkout main` then `git checkout -b short_descriptive_name` to create a new branch to work on your task. Name examples: server_setup, robot_itnegration.
3. Complete your task, adding files and committing whenever you want
4. If main has been updated on GitHub since you started, `git fetch`, then either merge `git merge origin/main` and fix any merge errors if you need to.
5. Push your changes with `git push`.
6. Create a pull request on GitHub, add any descriptions or explanations as necessary, and mention the appropriate reviewers to request a review. Link the pull request to the issue it is for.
7. If the reviewer requested changes, make them and push again, it will update the pull request. Then re-request a review.
8. Once the reviewer has accepted your changes, merge the pull request on GitHub and delete the branch.

### Review guide
1. `git fetch` and checkout the branch that the work was done on, and test it.
2. Go to files changed and review the changes, making comments and requesting changes if necessary. Consider if the goal has been achieved, code style, clarity, comments, etc.
3. Test the code. E.g. if it is a change in the simulation, check if the simulation is still working. Do appropriate tests based on the context in which the changes were made.
4. If you request changes, make a comment and tag the person on it again.
5. If you are happy, feel free to merge!
