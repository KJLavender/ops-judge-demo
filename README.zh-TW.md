# ops-judge-demo

[English](README.md) | **繁體中文**

用來在真的 GitHub Actions 上試 [ops-judge](https://github.com/KJLavender/ops-judge) 的小 repo。

`CI` 負責跑測試。測試失敗時，`ops-judge` 這個 workflow 會去看失敗的 job，決定要怎麼處理：重跑、在 PR 上說明失敗原因，或通知平台團隊。

這裡刻意準備了兩種失敗：

- 建立 `demo/registry-outage` 這個檔案後，每次 CI 的第一次執行都會出現 DNS 錯誤，模擬 registry 短暫掛掉的情況。重跑就會過。
- 改壞 `src/calc.py` 之後，`tests/test_calc.py` 每次都會失敗，重跑也沒用。

如果沒有設定 `CLAUDE_CODE_OAUTH_TOKEN` 這個 secret，就只會跑規則那一層，大部分失敗會附上說明交給人處理。把 `claude setup-token` 產生的 token 加進 secret，就能啟用 LLM 那一層。
