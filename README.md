# ops-judge-demo

**English** | [繁體中文](README.zh-TW.md)

A small repository for trying [ops-judge](https://github.com/KJLavender/ops-judge) on real GitHub Actions runs.

`CI` runs the tests. When it fails, the `ops-judge` workflow looks at the failed job and decides what to do: rerun it, explain the failure on the pull request, or tell the platform team.

Two kinds of failure are set up on purpose:

- Creating `demo/registry-outage` makes the first attempt of every CI run fail with a DNS error, the way a short registry outage would. A rerun passes.
- Breaking `src/calc.py` makes `tests/test_calc.py` fail on every attempt. A rerun doesn't help.

Without the `CLAUDE_CODE_OAUTH_TOKEN` secret only the rule tier runs, so most failures are handed to a person with an explanation. Add the secret (from `claude setup-token`) to enable the LLM tier.
