# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案現況

本儲存庫提供一個 agent skill：`explain-as-webpage`。它讓代理把陌生的技術、設計或主題做成單一、RTD 風格的 HTML 知識網頁。材料分三種模式：使用者的專案（以真實程式碼、資料與報告為例）、使用者給的文件（網頁文章、PDF、Markdown，讀取全文），或只有主題（查證並為來源分級）；使用者追問時，可補進原頁或延伸為「主頁＋子頁」的頁面樹。頁面可用英文或繁體中文產出。繪圖規則另放在 `explainer-figure` skill，只由 explain-as-webpage 以相對路徑讀取，兩個 skill 資料夾必須並列。Claude Code 與 Codex 共用同一份 `skills/*/SKILL.md`，兩個平台只各自附 plugin manifest，格式仿照 addyosmani/agent-skills。

需求與取捨記錄在 `docs/ideas/explain-as-webpage.md`（第一輪）、`docs/ideas/explain-as-webpage-v2.md`（第二輪）、`docs/specs/explain-as-webpage-v3.md`（第三輪規格：材料模式，已實作）與 `docs/ideas/figure-values.md`（圖中數值的意義），實作計畫與進度記錄在 `tasks/plan.md`、`tasks/todo.md`（第三輪）。第四輪（視覺表現形式）的構想、計畫與待辦在 `docs/ideas/visual-forms.md`、`visual-forms-plan.md`、`visual-forms-todo.md`。

## 架構

- `skills/explain-as-webpage/SKILL.md`：7 步流程（收集材料 → 學習摘要 → 選擇層級 L0／L1／L2 → 一次性確認 → 產出 → 自我檢查 → 回報）。第 1 步依材料分成 project／document／topic 三種模式。只放流程與判準，細節放在 references，需要時才讀。
- `references/sources-and-research.md`：document 與 topic 模式的規則：取得全文（`curl`、`pdftotext`、缺中繼憑證、JavaScript 頁面）、長篇材料與計畫、查證深度、來源等級 g1–g4、輔助 skill、高風險主題、輸出路徑。
- `references/page-types.md`：7 種頁型（機制、套件、程式導讀、論證、路線圖或計畫、實務指南、演進）各自的骨架與圖 1。
- `references/writing-rules.md`：頁面骨架、圖文綁定與讀圖四問、術語定義、讀者設定、英文與台灣用語規則、固定標籤中英對照、篇幅預算。
- `references/extending-pages.md`：依追問延伸頁面的落點判準（`<details>`／子頁／修訂主頁）、兩層頁面樹、子頁命名 `<hub>--<child>.html`、側欄同步與篇幅檢查指令。
- `assets/template.html`：單檔模板，包含內嵌 CSS、共用箭頭 marker、自動側欄目錄、可選的側欄頁面樹（`.pages`），以及通用 stepper 元件（`data-step="n"`／`"n+"`）。**不可引入外部資源。**字型堆疊中拉丁字型需排在 CJK 字型之前，否則 Linux 上英文引號會變全形。
- `skills/explainer-figure/SKILL.md`：圖說明單格式、圖型選擇、繪圖步驟、單圖自檢（只看圖與單幀的截圖指令）。frontmatter 設 `disable-model-invocation: true`、`user-invocable: false`，不會被自動觸發。
- `skills/explainer-figure/references/svg-recipes.md`：SVG 網格與尺寸規則、顏色語意、圖形配方、座標軸與刻度、逐步動畫（stepper）與滑桿的寫法。
- `examples/autoresearch/`：以 karpathy/autoresearch 為例的英文範例（主頁＋兩個程式導讀子頁），同時是延伸流程的驗證案例。
- `examples/explain-as-webpage/`：說明本儲存庫的單頁範例（L0），有英文（`explain-as-webpage.html`）與繁中（`explain-as-webpage.zh-TW.html`）兩版；兩版的開頭畫面（側欄、結論與圖 1 的 7 步流程）分別是 `README.md` 與 `README.zh-TW.md` 的封面圖 `docs/images/cover-process.png`、`cover-process.zh-TW.png`（以 `--force-device-scale-factor=1.5 --window-size=1247,<高度>` 截取，高度截到圖 1 圖說下方）。
- `examples/llm-wiki/`、`examples/starship-reusability/`：繁中範例，分別示範 document 模式與 topic 模式。`README.md` 只列英文範例，`README.zh-TW.md` 只列繁中範例。
- `.claude-plugin/`、`.codex-plugin/`、`.agents/plugins/`：plugin 與 marketplace manifest，版本號需同步。

修改規則時，兩個 `SKILL.md` 都維持精簡（約 130 行以內），細節放進 references。跨 skill 的路徑從 skill 根目錄寫起，例如 `../explainer-figure/SKILL.md`。

## 驗證指令

本儲存庫沒有建置系統或測試套件。修改後可用下列指令驗證：

```bash
# manifest
for f in .claude-plugin/*.json .codex-plugin/plugin.json .agents/plugins/marketplace.json; do python3 -m json.tool "$f" >/dev/null && echo "ok $f"; done
claude plugin validate .                                    # --strict 會因根目錄的 CLAUDE.md 報警告，屬預期
claude --plugin-dir . plugin details sphinx-style-notes-maker   # 確認 skill 被載入與 token 成本

# 模板：不可有外部資源，並在兩種寬度截圖檢查（Chrome 視窗最窄 500px，窄版放進 390px 的 iframe 量測）
F=$PWD/skills/explain-as-webpage/assets/template.html
grep -nE '(src=|url\()["'\'']?https?://' "$F"               # 應無輸出
google-chrome --headless=new --disable-gpu --window-size=1280,1400 --screenshot=/tmp/wide.png "file://$F"
printf '<iframe id="f" src="file://%s" width="390" height="1600" style="border:0"></iframe><script>f.onload=function(){var d=f.contentDocument.documentElement;document.title=d.scrollWidth>d.clientWidth?"OVERFLOW":"ok"}</script>' "$F" > /tmp/explain-as-webpage-narrow.html
google-chrome --headless=new --disable-gpu --allow-file-access-from-files --virtual-time-budget=3000 --dump-dom file:///tmp/explain-as-webpage-narrow.html | grep -o '<title>[^<]*'   # 應為 <title>ok
google-chrome --headless=new --disable-gpu --allow-file-access-from-files --window-size=500,1600 --screenshot=/tmp/narrow.png file:///tmp/explain-as-webpage-narrow.html; rm /tmp/explain-as-webpage-narrow.html
```

修改 `SKILL.md` 中的 shell 範例後，要實際執行一次。曾發生 sed 分隔字元與內容衝突，導致範例無法執行的問題。
