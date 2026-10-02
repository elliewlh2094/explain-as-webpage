# 實作計畫：`explain-as-webpage` skill

## Context

使用者在與 AI 代理協作時，常遇到不熟悉的技術（例如 RANSAC 幾何驗證、批量實驗用的 ROS2 套件、RTF），只能全盤接受代理的提議。既有的解法（網路文章、代理撰寫的長篇 Markdown 報告、Markdown 搭配 matplotlib 圖）都不夠：`starlab_swarm/docs/notebooks/` 中的報告長達 833～1674 行，而且已經有附圖的 `LANDMARK_PRIMER_2_GEOMETRIC_VERIFICATION.md`，使用者仍然看不懂。

經 /idea-refine 釐清後，使用者確認的痛點是：**篇幅太長、文字太密、缺少因果主線、圖與論述脫節**。目標是建立一個 skill，讓代理以使用者專案的真實資料與程式碼為例，產出**單一、輕量、RTD 風格的知識網頁**，並依主題性質選擇最低成本但足夠的呈現層級，而且產出前必須先與使用者確認。

### 已確認的決策

| 項目 | 決策 |
|---|---|
| 結構 | 單一 skill，附 `references/` 與 `assets/`；不拆成多個 skill，也不附產生器腳本 |
| 平台 | Claude Code 與 Codex 共用同一份 `SKILL.md`，只各自附 plugin manifest（仿 addyosmani/agent-skills 0.6.11） |
| Skill 名稱 | `explain-as-webpage` |
| Skill 語言 | 英文；description 加入中文觸發詞；產出的網頁跟隨使用者的語言 |
| 最高層級 | L2：瀏覽器內逐步動畫（SVG ＋ 少量 JS）；不做影片 |
| 外觀 | 只仿照 sphinx_rtd_theme 的外觀，以內嵌 CSS 實現；不用 Sphinx 建置 |
| 產出位置 | 產出前詢問使用者；預設為 `~/Documents/explainers/<repo-name>/<topic-slug>.html` |
| 相依 | 不引入外部 CDN 或字型，單一 HTML 檔可離線開啟；公式用 HTML 上下標與 Unicode 表示 |

## 架構（儲存庫產出物）

```
sphinx-style-notes-maker/
├── skills/explain-as-webpage/
│   ├── SKILL.md                 # 流程 + 層級判準表，目標 ≤ ~180 行
│   ├── references/
│   │   ├── writing-rules.md     # 頁面結構與寫作規則（下詳）
│   │   └── svg-recipes.md       # 因果鏈、前後對照、管線、逐步動畫的 SVG 畫法與版面規則
│   └── assets/
│       └── template.html        # RTD 風格外殼 + 提示框 + figure + stepper 元件
├── .claude-plugin/{plugin.json, marketplace.json}
├── .codex-plugin/plugin.json
├── .agents/plugins/marketplace.json
├── docs/ideas/explain-as-webpage.md   # idea-refine 一頁摘要
├── tasks/{plan.md, todo.md}           # planning skill 規定的輸出
├── README.md                          # 兩個平台的安裝與使用方式
└── CLAUDE.md                          # 更新專案現況與驗證指令
```

### SKILL.md 流程（代理執行時的步驟）

1. **收集背景**：讀取使用者指定的來源（報告、套件目錄、程式碼），只讀需要的部分。擷取專案中的具體事實與數字，並記下來源路徑。
2. **建立學習摘要（learning brief）**：
   - 3～5 個「讀者真正卡住的疑問」
   - 一條因果鏈：問題成因 → 機制 → 後果 → 對策 → 實測改善
   - 反事實對照：用專案真實數據比較「不做 X」與「做了 X」
   - 必要的前置術語，不超過 5 個
3. **選擇呈現層級**：依判準表選出能回答所有核心疑問的**最低層級**。
4. **一次性確認**：在同一則訊息中請使用者確認疑問清單、建議層級（附替代選項與成本說明）、產出路徑。若平台有結構化提問工具就使用（Claude Code 為 `AskUserQuestion`），否則用一般訊息詢問。**取得回覆後才開始產出。**
5. **產出頁面**：複製 `assets/template.html`，依 `writing-rules.md` 與 `svg-recipes.md` 填入內容。
6. **自我檢查**：逐項核對檢查清單（無外部 URL、每張圖都緊鄰並被其說明段落引用、結論在最前、篇幅在預算內、事實附來源、推論明確標示）。若有 headless Chrome，截圖後實際檢視，修正重疊或溢出。
7. **回報**：說明檔案路徑、開啟方式，以及頁面回答了哪些疑問。

### 層級判準（寫入 SKILL.md）

| 層級 | 形式 | 適用的疑問類型 | 例子（使用者的三個案例） |
|---|---|---|---|
| L0 | 文字＋靜態 inline SVG | 結構、組成、因果鏈、前後對照 | `swarm_experiment` 套件各模組的職責與資料流 |
| L1 | L0＋`<details>` 展開、分頁切換、單一滑桿 | 結果隨參數變化的取捨關係 | RTF 與牆鐘時間的換算、門檻值的取捨 |
| L2 | L1＋stepper 控制的多幀 SVG | 迭代演算法、隨時間演進的過程 | RANSAC 的逐次抽樣與內點計數、lockstep 的時序 |

規則：預設採用最低層級；只有當某個核心疑問本身屬於「過程」或「參數相依」類型時，才升級。

### writing-rules.md 重點

- 結論先行；每一節只回答一個疑問，節標題直接寫成該疑問。
- 先畫出因果鏈圖，正文順著圖上的節點逐一展開。
- 每張圖緊鄰它所說明的段落，正文必須明確引用該圖（例如「見圖 2 的紅色箭頭」）；圖說寫出「這張圖要讓讀者看出什麼」。
- 寫作風格約為「八成的 ASD-STE100」：短句、一句只講一件事、主動語態、同一概念始終使用同一個詞。
- 篇幅預算：全頁閱讀時間 ≤ 15 分鐘；權威範圍、閱讀指南之類的前置內容一律省略。
- 事實附來源路徑；推論與建議需明確標示為推論或建議。

### template.html 重點

- RTD 外觀：深色左側欄、藍色標題列、麵包屑、內容最大寬度約 800px、`note`／`warning`／`tip` 提示框、帶編號的 `figure`。
- 系統字型堆疊，不載入網路字型；有列印樣式；窄螢幕（約 390px）時側欄改為頂部選單。
- 少量 JS（目標 ≤ 60 行）：依 `h2`／`h3` 自動產生側欄目錄；通用 stepper 元件（`<g data-step="n" data-caption="...">`，提供上一步／下一步／播放）。L1 的滑桿屬於頁面專屬 JS，寫法放在 `svg-recipes.md`。
- 檔案大小預算：產出頁面 ≤ 約 150 KB。

## 任務清單（依 incremental-implementation 逐片實作）

> 本儲存庫目前沒有建置或測試系統。以下的「驗證」皆為可實際執行的指令或檢查。依照使用者的全域規則，**未經使用者要求不建立 commit**，在檢查點詢問是否要提交。

### 第 0 階段：記錄
- **T0（XS）** 寫入 `docs/ideas/explain-as-webpage.md`、`tasks/plan.md`、`tasks/todo.md`（先確認不存在，目前也確實不存在）。
  驗證：檔案存在，內容與本計畫一致。

### 第 1 階段：高風險部分先做（模板）
- **T1（S）** `assets/template.html`：RTD 外殼、提示框、figure、自動目錄、stepper 元件，並附一個示範用的 3 步 SVG。
  驗收：可離線開啟；在 1280px 與 390px 寬度下版面正常；stepper 可切換。
  驗證：`python3` 的 `html.parser` 解析無誤；`grep -E 'https?://'` 沒有外部資源；`google-chrome --headless --screenshot --window-size=1280,900` 與 `390,844` 各截一張圖，實際檢視截圖。
- **T2（M）** `SKILL.md`、`references/writing-rules.md`、`references/svg-recipes.md`。
  驗收：frontmatter 的 `name` 與目錄名稱一致；description ≤ 1024 字元並含中英文觸發詞；`SKILL.md` ≤ 約 180 行；內文提及的路徑都存在。
  驗證：以腳本檢查 frontmatter、計算行數、grep 所有被引用的路徑並確認存在。

**檢查點 A**：把模板截圖與 `SKILL.md` 給使用者檢視，視需要調整；詢問是否提交 commit。

### 第 2 階段：實際試用（驗證核心假設）
- **T3（M）** 依照 `SKILL.md` 的流程，以 `LANDMARK_OBSERVATION_CONFIDENCE_ANALYSIS.md` 與 `LANDMARK_PRIMER_2_GEOMETRIC_VERIFICATION.md` 為來源，產出 RANSAC 頁面（預期為 L2）。過程中照常執行第 4 步，向使用者確認。
  驗證：自我檢查清單逐項通過；兩種寬度的截圖；**使用者閱讀後回饋是否看懂**（核心假設 1）。
- **T4（S）** 依 T3 的回饋修正 `SKILL.md`、references 與模板。
- **T5（M）** 產出 RTF 頁面（來源為 `SIMULATION_PERFORMANCE_ANALYSIS.md`，預期 L1）與 `swarm_experiment` 套件頁面（來源為該套件的原始碼與 `docs/`，預期 L0），藉此確認三個層級都能運作。
  驗證：同 T3。

**檢查點 B**：三頁皆經使用者確認可讀。

### 第 3 階段：打包
- **T6（M）** 建立 `.claude-plugin/`、`.codex-plugin/`、`.agents/plugins/marketplace.json`（格式照抄 agent-skills 0.6.11），撰寫 README 的安裝與使用說明，更新 `CLAUDE.md`。
  驗證：`python3 -m json.tool` 檢查每個 JSON；若可用則執行 `claude plugin validate .`；**經使用者同意後**，以 `codex plugin marketplace add <repo>` 搭配 `codex plugin add` 實際安裝，開新的 Codex session 確認 `@explain-as-webpage` 可被找到（此步驟會修改 `~/.codex`）；Claude Code 端以 `/plugin marketplace add <repo>` 安裝後確認 `/explain-as-webpage` 可用。

**檢查點 C**：完成所有驗收條件，詢問是否提交 commit 或推送。

## 風險與對策

| 風險 | 影響 | 對策 |
|---|---|---|
| 代理手寫的 SVG 版面錯位 | 高 | `svg-recipes.md` 規定固定 `viewBox` 與網格座標、文字預留寬度；產出後必須截圖自我檢查 |
| skill 本身寫得太長，代理無法遵守 | 中 | `SKILL.md` 只放流程與判準，細節放進 references 並在需要時才讀取 |
| Codex 的觸發或提問方式與 Claude Code 不同 | 中 | 第 4 步寫成與工具無關的說法；在 T6 實際安裝測試 |
| 試用頁面的品質取決於來源報告 | 中 | 頁面中的事實一律附來源路徑；推論明確標示 |

## 試用頁面的產出位置

`~/Documents/explainers/starlab_swarm/`。產出前仍依 skill 的流程向使用者確認；這些頁面不會放進本儲存庫。
