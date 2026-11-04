# ops-judge-demo

[English](README.md) | **繁體中文**

這是一個很小的 repo，用來在真的 GitHub Actions 上看 [ops-judge](https://github.com/KJLavender/ops-judge) 怎麼運作。ops-judge 會看失敗的 CI job，判斷重跑能不能解決，這樣就不用每次偶發失敗都靠人去查。

## 怎麼組成的

- `CI` workflow 用 `python -m pytest -q` 跑測試，每個 PR 和每次推到 `main` 都會跑。
- `ops-judge` workflow 在 `CI` 失敗結束時啟動，對失敗的 job 執行 ops-judge 的 GitHub Action（`KJLavender/ops-judge@main`）。依它的判斷，它會重跑 job、在 PR 上留言說明失敗原因，或通知平台團隊。

## 兩種可以試的失敗

兩種都是刻意做的。各開一個 PR 來試。

1. 重跑就會好的失敗。在 `demo/registry-outage` 新增一個空檔案。之後每次 CI 的第一次執行都會出現 DNS 錯誤（「Failed to resolve 'registry.example.org'」），像套件 registry 短暫掛掉一樣；從第二次執行起，測試就會通過。邏輯寫在 `tests/test_registry.py`。
2. 重跑也沒用的失敗。把 `src/calc.py` 改壞，例如改掉 `total()` 裡算稅的部分，`tests/test_calc.py` 就會每次都失敗。

ops-judge 在這個 repo 的兩個 PR 上做了什麼：

- [#1](https://github.com/KJLavender/ops-judge-demo/pull/1)（registry 故障）：它判為基礎設施問題（0.81），重跑 job，第二次就過了。
- [#2](https://github.com/KJLavender/ops-judge-demo/pull/2)（測試被改壞）：它判為程式錯誤（0.78），在 PR 上說明原因，沒有重跑。之後有人手動重跑、又失敗了，ops-judge 也沒有多說什麼，因為它從來沒說過這是偶發。

## 複製這個 repo 時的設定

`ops-judge` workflow 需要 `actions: write`（重跑 job）、`pull-requests: write` 和 `issues: write`（留言）這幾個權限，`.github/workflows/ops-judge.yml` 裡已經設好了。

你也可以加一個叫 `CLAUDE_CODE_OAUTH_TOKEN` 的 secret，token 用 `claude setup-token` 產生。有了它，規則判斷不了的情況會交給 LLM。沒有的話只會跑規則那一層，大部分失敗會附上說明交給人，而不會被重跑。

## 檔案

```
.github/workflows/ci.yml          跑測試
.github/workflows/ops-judge.yml   CI 失敗時執行 ops-judge
src/calc.py                       可以拿來改壞的小函式（失敗 2）
tests/test_calc.py                calc.py 壞掉時會失敗的測試
tests/test_registry.py            模擬 registry 故障（失敗 1）
```
