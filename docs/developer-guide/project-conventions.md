# DRN Alpha project conventions

## Git branching model

We follow a loose version of the [Git flow branching model](https://nvie.com/posts/a-successful-git-branching-model/).

- Make pull requests against: `main`
- The release prep branch is: `main`
- The client QA branch is: `staging`
- The internal QA branch is: `develop`
- Do not treat the following branches as merge sources: `develop`, `staging`

1. Make changes on a new branch, including a broad category and the ticket number if relevant e.g. `feature/123-extra-squiggles`, `fix/newsletter-signup`.
2. Push your branch to the remote.
3. Create a Pull Request using the GitHub interface
4. Edit details as necessary.

If you need to preview work on `staging`, this can be merged and deployed manually without making a pull request. You can still make the pull request as above, but add a note to say that this is on `staging`, and not yet ready to be merged to `main`.

## Deployment Cycle

### Simple flavour

Make sure `main` contains all the desired changes (and is pushed to the remote repository and has passed CI). Deploy to production (see [deployment documentation](deployment.md)).
