# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案現況

本儲存庫提供一個 agent skill：`explain-as-webpage`。它讓代理以使用者專案的真實程式碼、資料與報告為例，把陌生的技術或設計做成單一、RTD 風格的 HTML 知識網頁。Claude Code 與 Codex 共用同一份 `skills/explain-as-webpage/SKILL.md`，兩個平台只各自附 plugin manifest，格式仿照 addyosmani/agent-skills。

需求與取捨記錄在 `docs/ideas/explain-as-webpage.md`，實作計畫與進度記錄在 `tasks/plan.md`、`tasks/todo.md`。

## 架構

- `skills/explain-as-webpage/SKILL.md`：7 步流程（收集背景 → 學習摘要 → 選擇層級 L0／L1／L2 → 一次性確認 → 產出 → 自我檢查 → 回報）。只放流程與判準，細節放在 references，需要時才讀。
- `references/writing-rules.md`：頁面骨架、圖文綁定、術語定義、台灣用語、篇幅預算。
- `references/svg-recipes.md`：SVG 網格與尺寸規則、顏色語意、圖形配方、逐步動畫（stepper）與滑桿的寫法。
- `assets/template.html`：單檔模板，包含內嵌 CSS、共用箭頭 marker、自動側欄目錄，以及通用 stepper 元件（`data-step="n"`／`"n+"`）。**不可引入外部資源。**
- `.claude-plugin/`、`.codex-plugin/`、`.agents/plugins/`：plugin 與 marketplace manifest，版本號需同步。

修改規則時，`SKILL.md` 維持精簡（約 130 行以內），細節放進 references。

## 驗證指令

本儲存庫沒有建置系統或測試套件。修改後可用下列指令驗證：

```bash
# manifest
for f in .claude-plugin/*.json .codex-plugin/plugin.json .agents/plugins/marketplace.json; do python3 -m json.tool "$f" >/dev/null && echo "ok $f"; done
claude plugin validate .                                    # --strict 會因根目錄的 CLAUDE.md 報警告，屬預期
claude --plugin-dir . plugin details sphinx-style-notes-maker   # 確認 skill 被載入與 token 成本

# 模板：不可有外部資源，並在兩種寬度截圖檢查
F=skills/explain-as-webpage/assets/template.html
grep -nE '(src=|url\()["'\'']?https?://' "$F"               # 應無輸出
google-chrome --headless=new --disable-gpu --window-size=1280,1400 --screenshot=/tmp/wide.png "file://$PWD/$F"
google-chrome --headless=new --disable-gpu --window-size=390,1600 --screenshot=/tmp/narrow.png "file://$PWD/$F"
```

修改 `SKILL.md` 中的 shell 範例後，要實際執行一次。曾發生 sed 分隔字元與內容衝突，導致範例無法執行的問題。
