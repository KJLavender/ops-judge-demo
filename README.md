# ops-judge-demo

**English** | [繁體中文](README.zh-TW.md)

This is a tiny repository for watching [ops-judge](https://github.com/KJLavender/ops-judge) work on real GitHub Actions runs. ops-judge looks at a failed CI job and decides whether a rerun would fix it, so people don't have to investigate every random failure.

## How it is set up

- The `CI` workflow runs the tests with `python -m pytest -q`, on every pull request and on pushes to `main`.
- The `ops-judge` workflow starts when `CI` finishes with a failure. It runs the ops-judge GitHub Action (`KJLavender/ops-judge@main`) on the failed job. Depending on what it decides, it reruns the job, explains the failure in a comment on the pull request, or notifies the platform team.

## Two failures to try

Both are made on purpose. Open a pull request for each.

1. A failure that a rerun fixes. Add an empty file at `demo/registry-outage`. The first attempt of every CI run then fails with a DNS error ("Failed to resolve 'registry.example.org'"), like a short outage of a package registry. From the second attempt on, the test passes. The logic is in `tests/test_registry.py`.
2. A failure that a rerun does not fix. Break `src/calc.py`, for example by changing the tax math in `total()`. `tests/test_calc.py` then fails on every attempt.

What ops-judge did on the two pull requests in this repo:

- [#1](https://github.com/KJLavender/ops-judge-demo/pull/1) (the registry outage): it called the failure infrastructure (0.81), reran the job, and attempt 2 passed.
- [#2](https://github.com/KJLavender/ops-judge-demo/pull/2) (the broken test): it called the failure a code bug (0.78), explained why on the pull request, and did not rerun. When someone reran it by hand and it failed again, ops-judge added nothing, because it had never called that one a flake.

## Setup if you copy this repository

The `ops-judge` workflow needs these permissions, and they are already set in `.github/workflows/ops-judge.yml`: `actions: write` (to rerun jobs), `pull-requests: write` and `issues: write` (to comment).

You can also add a secret named `CLAUDE_CODE_OAUTH_TOKEN`. Create the token with `claude setup-token`. With it, ops-judge uses an LLM for cases the rules can't decide. Without it, only the rule tier runs, so most failures are handed to a person with an explanation instead of being rerun.

## Files

```
.github/workflows/ci.yml          the tests
.github/workflows/ops-judge.yml   runs ops-judge when CI fails
src/calc.py                       a small function to break (failure 2)
tests/test_calc.py                tests that fail when calc.py is broken
tests/test_registry.py            simulates the registry outage (failure 1)
```
