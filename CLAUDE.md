# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案現況

本儲存庫是 plugin `explain-as-webpage`（版本 0.4.0），提供兩個 agent skill：`explainer-page` 與它的繪圖輔助 skill `explainer-figure`。它讓代理把陌生的技術、設計或主題做成單一、RTD 風格的 HTML 知識網頁。材料分三種模式：使用者的專案（以真實程式碼、資料與報告為例）、使用者給的文件（網頁文章、PDF、Markdown，讀取全文），或只有主題（查證並為來源分級）；代理讀不到的材料（影片、需權限的論文）改由使用者提供全文、逐字稿或 NotebookLM 這類工具的筆記；使用者追問時，可補進原頁或延伸為「主頁＋子頁」的頁面樹。頁面可用英文或繁體中文產出。繪圖規則另放在 `explainer-figure` skill，只由 explainer-page 以相對路徑讀取，兩個 skill 資料夾必須並列。Claude Code 與 Codex 共用同一份 `skills/*/SKILL.md`，兩個平台只各自附 plugin manifest，格式仿照 addyosmani/agent-skills。

各輪的需求、取捨、實作計畫與進度記錄在 `docs/plan/`，索引見 `docs/plan/README.md`。命名規則見下方「計畫文件」。

## 架構

- `skills/explainer-page/SKILL.md`：7 步流程（收集材料 → 學習摘要 → 選擇層級 L0／L1／L2 → 一次性確認 → 產出 → 自我檢查 → 回報）。第 1 步依材料分成 project／document／topic 三種模式。只放流程與判準，細節放在 references，需要時才讀。
- `references/sources-and-research.md`：document 與 topic 模式的規則：取得全文（`curl`、`pdftotext`、缺中繼憑證、JavaScript 頁面）、讀不到的材料與 AI 筆記、整理方式（依原材料順序或問題導向）與候選問題、長篇材料與計畫、查證深度、來源等級 g1–g4、輔助 skill、高風險主題、輸出路徑。
- `references/page-types.md`：7 種頁型（機制、套件、程式導讀、論證、路線圖或計畫、實務指南、演進）各自的骨架與圖 1。
- `references/writing-rules.md`：頁面骨架、圖文綁定與讀圖四問、術語定義、讀者設定、英文與台灣用語規則、固定標籤中英對照、篇幅預算。
- `references/extending-pages.md`：依追問延伸頁面的落點判準（`<details>`／子頁／修訂主頁）、兩層頁面樹、子頁命名 `<hub>--<child>.html`、側欄同步與篇幅檢查指令。
- `assets/template.html`：單檔模板，包含內嵌 CSS（語意色、概念色 `c1`–`c5`、`.chip`、歸納卡 `.card-grid`、具象插圖用的 `outline`／`lead`／`edge`／`area` 等 class）、共用箭頭 marker 與圖示區塊（`<!-- icons:start -->`）、自動側欄目錄、可選的側欄頁面樹（`.pages`），以及通用 stepper 元件（`data-step="n"`／`"n+"`）。**不可引入外部資源。**字型堆疊中拉丁字型需排在 CJK 字型之前，否則 Linux 上英文引號會變全形。
- `skills/explainer-figure/SKILL.md`：圖說明單格式、圖型選擇（逐列對照圖型表）、繪圖步驟、單圖自檢（WCAG 對比檢查、只看圖與單幀的截圖指令）。frontmatter 設 `disable-model-invocation: true`、`user-invocable: false`，不會被自動觸發。
- `skills/explainer-figure/references/svg-recipes.md`：SVG 網格與尺寸規則、語意色與概念色、圖形配方、座標軸與刻度、逐步動畫（stepper）與滑桿的寫法。
- `skills/explainer-figure/references/cards.md`：歸納卡的使用時機、結構、上限與檢查；`pictorial.md`：具象插圖 P1–P4（分層容器與其加上角色與流向的變化、剪影、物件與組成、介面示意）與共同規則；`icons.md`：圖示名稱表與同步指令（把頁面用到的 symbol 與授權聲明寫進圖示區塊）。
- `skills/explainer-figure/assets/icons/`：Lucide 圖示子集 `lucide.svg`（lucide-static 1.52.0，106 個，開頭是授權聲明）與 `LICENSE`。新增圖示時從同版本的 npm 套件複製，不在產頁時下載。
- `examples/autoresearch/`：以 karpathy/autoresearch 為例的英文範例（主頁＋兩個程式導讀子頁），同時是延伸流程的驗證案例。
- `examples/explain-as-webpage/`：說明本儲存庫的單頁範例（L0），有英文（`explain-as-webpage.html`）與繁中（`explain-as-webpage.zh-TW.html`）兩版；兩版的開頭畫面（側欄、結論與圖 1 的 7 步流程）分別是 `README.md` 與 `README.zh-TW.md` 的封面圖 `docs/images/cover-process.png`、`cover-process.zh-TW.png`（以 `--force-device-scale-factor=1.5 --window-size=1247,<高度>` 截取，高度截到圖 1 圖說下方）。
- `examples/llm-wiki/`、`examples/starship-reusability/`：繁中範例，分別示範 document 模式與 topic 模式，兩頁都用到歸納卡、具象插圖、概念色與圖示。`README.md` 只列英文範例，`README.zh-TW.md` 只列繁中範例。
- `.claude-plugin/`、`.codex-plugin/`、`.agents/plugins/`：plugin 與 marketplace manifest，版本號需同步。

修改規則時，兩個 `SKILL.md` 都維持精簡（約 130 行以內），細節放進 references。跨 skill 的路徑從 skill 根目錄寫起，例如 `../explainer-figure/SKILL.md`。

## 計畫文件

本規則優先於規劃 skill（例如 `idea-refine`、`spec-driven-development`、`planning-and-task-breakdown`）的預設輸出路徑。不寫入 `docs/ideas/`、`docs/specs/`、`tasks/`。

- 所有計畫文件直接放在 `docs/plan/`，不建立子目錄。
- 檔名為 `<兩位數輪次>-<主題 slug>-<文件類型>.md`，例如 `05-citations-plan.md`。
- 文件類型固定為 `idea`（構想）、`spec`（規格）、`plan`（實作計畫）、`todo`（待辦）。某一輪中途另外整理的構想，用描述性名稱取代文件類型，例如 `03-material-modes-figure-values.md`。
- 開始新的一輪時，輪次取現有最大值加 1，並在 `docs/plan/README.md` 的表格新增一列；狀態改變時更新同一列。
- 文件內互相引用時寫完整路徑，例如 `docs/plan/04-visual-forms-plan.md`。

## 驗證指令

本儲存庫沒有建置系統或測試套件。修改後可用下列指令驗證：

```bash
# manifest
for f in .claude-plugin/*.json .codex-plugin/plugin.json .agents/plugins/marketplace.json; do python3 -m json.tool "$f" >/dev/null && echo "ok $f"; done
claude plugin validate .                                    # --strict 會因根目錄的 CLAUDE.md 報警告，屬預期
claude --plugin-dir . plugin details explain-as-webpage   # 確認 skill 被載入與 token 成本

# 模板：不可有外部資源，並在兩種寬度截圖檢查（Chrome 視窗最窄 500px，窄版放進 390px 的 iframe 量測）
F=$PWD/skills/explainer-page/assets/template.html
grep -nE '(src=|url\()["'\'']?https?://' "$F"               # 應無輸出
google-chrome --headless=new --disable-gpu --window-size=1280,1400 --screenshot=/tmp/wide.png "file://$F"
printf '<iframe id="f" src="file://%s" width="390" height="1600" style="border:0"></iframe><script>f.onload=function(){var d=f.contentDocument.documentElement;document.title=d.scrollWidth>d.clientWidth?"OVERFLOW":"ok"}</script>' "$F" > /tmp/explainer-page-narrow.html
google-chrome --headless=new --disable-gpu --allow-file-access-from-files --virtual-time-budget=3000 --dump-dom file:///tmp/explainer-page-narrow.html | grep -o '<title>[^<]*'   # 應為 <title>ok
google-chrome --headless=new --disable-gpu --allow-file-access-from-files --window-size=500,1600 --screenshot=/tmp/narrow.png file:///tmp/explainer-page-narrow.html; rm /tmp/explainer-page-narrow.html
```

修改 `SKILL.md` 中的 shell 範例後，要實際執行一次。曾發生 sed 分隔字元與內容衝突，導致範例無法執行的問題。
