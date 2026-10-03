# 實作計畫：explain-as-webpage 第三輪（材料模式）

> 第二輪（英文支援、頁面樹延伸、autoresearch 範例）已完成，內容見 git 歷史。本輪規格見 `docs/specs/explain-as-webpage-v3.md`。

## Overview
依 v3 規格擴充 `explain-as-webpage`，新增三項能力：
- 第 1 步依材料分流（project／document／topic）。
- 依內容類型切換主軸圖。
- 加入查證深度、來源等級、讀者設定與高風險規則，並經同意後借助輔助 skill。

每一組規則寫完後，立刻用規格中的驗證案例實際跑一次 skill（V1–V8）。以這種「規則＋案例」的垂直切片推進，在檢查點由使用者判讀。

需求與任務的對應：

| 規格需求 | 規則任務 | 驗證案例任務 |
|---|---|---|
| R1 材料模式分流 | T2 | T3（V1）、T6（V2）、T8（V8） |
| R2 長篇材料 | T2、T5 | T6（V2） |
| R3 主題模式的查證 | T9 | T10（V3）、T11（V7）、T13（V4） |
| R4 頁型與主軸圖 | T4 | T6、T8、T11、T14、T15 |
| R5 共識程度標示 | T9 | T10、T11、T15 |
| R6 讀者設定與高風險主題 | T12 | T13、T14、T15 |
| R7 確認步驟與觸發條件 | T2（之後由 T9、T12 補上第 3、4 題） | 所有案例 |
| R8 輔助 skill | T1、T2、T16 | T6、T13（使用輔助 skill）、T10（拒絕後走內建做法） |

## Architecture Decisions
| 項目 | 決策 | 理由 |
|---|---|---|
| 切片方式 | 依模式由簡到繁：短文件 → 長文件與頁型 → 主題模式 → 高風險主題 → Codex 與打包；每個切片都以驗證案例收尾 | 每個階段結束時，都留下一份可判讀的成品 |
| 風險探測先做 | T1 先確認：web fetch 能否取得全文、可見的輔助 skill 有哪些、Codex 的行為 | 這三點會決定 `sources-and-research.md` 的讀取規則 |
| 騰出 `SKILL.md` 行數 | 把「單一圖或 stepper 幀截圖」的 `sed` 範例移到 `svg-recipes.md` 的 Stepper 段落；其餘細節放進新的 references | 目前已有 128 行，上限約 130 行 |
| 「注意」框 | 重用 `admonition danger`，標題為 Note／注意 | 不新增 CSS |
| 「新興說法」框 | 重用預設的 `admonition`（藍），標題為 Emerging view／新興說法 | 與 Inference（`warning`）區分 |
| 來源等級標籤 | 在模板新增 `.grade` 樣式，分 4 種變體，放在 Sources 每筆來源之後 | 這是唯一新增的 CSS |
| 驗證頁面的位置 | 全部輸出到 `~/Documents/explainers/<topic-slug>/`，不放進儲存庫 | 依 R1 的預設路徑；第三方材料不公開 |
| commit | 由使用者在各檢查點自行提交，我只提供 `git add` 範圍與提交訊息 | 依使用者的規則 |

## Task List

### 第 0 階段：風險探測

**T1（S）取得材料與環境探測**
- 說明：
  1. 用 WebFetch 取得 PG 長文（https://paulgraham.com/greatwork.html）與 Karpathy gist，再用 `curl` 加上 Python 去除標籤後計算字數，比較 WebFetch 是否回傳全文。
  2. 用 `pdftotext` 抽出 Ronin PDF 並計算字數。
  3. 列出 Claude Code 中可見的輔助 skill，分讀取網頁、讀取 PDF、深度研究三類。
  4. 經使用者同意後，用 `codex exec` 詢問 Codex 能看到哪些 skill、是否有網路工具。這一步會把提示送到外部服務，所以要先取得同意。
- 驗收：
  - [ ] 上述 4 個問題都有記錄的答案，寫在本檔「探測結果」一節
  - [ ] 決定網頁讀取的優先順序：WebFetch、`curl` 退路或輔助 skill
- 驗證：比較兩種取得方式的字數；探測時使用的暫存檔放在 scratchpad，結束後刪除
- 相依：無
- 檔案：`tasks/plan.md`

### 第 1 階段：document 模式（短文）

**T2（M）`SKILL.md` 分流，並新增 `sources-and-research.md` 的 document 部分**
- 說明：
  - `SKILL.md`：
    - 重寫 `description`（R7）。
    - When NOT to use 加入影片。
    - 第 1 步改為模式表（依規格 §5）。
    - 第 4 步改為最多 4 題的確認，內容包括候選疑問、涵蓋方式、輔助 skill 與非專案的輸出路徑。
    - 第 7 步回報實際用了哪些輔助 skill。
    - 把 `sed` 範例移到 `svg-recipes.md`。
  - 新增 `references/sources-and-research.md`，涵蓋：
    - 模式與輸出路徑
    - 網址、PDF、文字檔的讀取方式（依 T1 的結果）
    - 長篇材料的兩種做法（頁面樹細節留到 T5）
    - 引用長度
    - R8 的輔助 skill：例子、取得同意的方式、使用限制
  - `writing-rules.md`：「Facts, inferences, sources」一節改為依模式區分，專案模式的規則不變。
- 驗收：
  - [ ] `SKILL.md` ≤ 約 130 行，`description` ≤ 1024 字元，`SKILL.md` 中沒有寫死任何 skill 名稱
  - [ ] 比對 diff，專案模式的語意不變
  - [ ] 移動後的 `sed` 範例實際執行過一次
- 驗證：
  - 執行規格 §3 的行數與 `description` 長度指令
  - `claude plugin validate .`
  - 用 `grep` 確認文中引用的路徑都存在
- 相依：T1
- 檔案：`SKILL.md`、`references/sources-and-research.md`（新增）、`references/writing-rules.md`、`references/svg-recipes.md`

**T3（M）V1：Karpathy LLM Wiki gist**
- 說明：以一般使用者的請求執行 skill，輸出到 `~/Documents/explainers/llm-wiki/`。
- 驗收：
  - [ ] 確認訊息只發一次，最多 4 題，且包含候選疑問與輔助 skill 清單
  - [ ] 通過第 6 步的全部自我檢查
  - [ ] 每個事實都標出 gist 中的章節
- 驗證：
  - 執行自我檢查指令
  - 截取 1280 px 與 390 px 兩種寬度的圖
  - 使用者閱讀並判讀
- 相依：T2
- 檔案：無（輸出在儲存庫外）

**檢查點 A**：使用者檢視規則 diff 與 V1 頁面，依回饋修正規則，並提供 `git add` 建議。

### 第 2 階段：頁型與長文

**T4（M）新增 `page-types.md` 與 4 種主軸圖配方**
- 說明：
  - 新增 `references/page-types.md`：
    - 從 `writing-rules.md` 移入現有的套件頁型與程式導讀頁型。
    - 新增論述、路線圖、實務指南、演進 4 種頁型。每種頁型都寫明：適用時機、圖 1 的主軸、章節骨架、用什麼取代反事實對照。
  - `writing-rules.md`：骨架第 2 點改為「主軸圖（見 `page-types.md`）」，反事實對照只在專案模式中必備。
  - `svg-recipes.md`：新增配方 6–9，分別是論點地圖、路線圖、決策樹或檢查清單、演進圖。
  - `SKILL.md`：第 2 步加入選擇頁型。
- 驗收：
  - [ ] 每個配方都有符合網格規則的 SVG 片段
  - [ ] 4 個片段在截圖中沒有溢出或重疊
- 驗證：在 scratchpad 中複製模板，貼上 4 個片段，截取兩種寬度的圖後刪除複本；確認 `SKILL.md` 仍 ≤ 約 130 行
- 相依：檢查點 A
- 檔案：`references/page-types.md`（新增）、`references/writing-rules.md`、`references/svg-recipes.md`、`SKILL.md`

**T5（S）第一次產出就建立頁面樹（忠實導讀）**
- 說明：`extending-pages.md` 新增一節，內容包括：
  - 忠實導讀在第一次產出時，就建立主頁加上最多約 6 個子頁。
  - 主頁放材料結構圖。
  - 內部摘要列出「原文章節 → 頁面章節」的對照表。
  - 自我檢查時逐條核對這張對照表。
- 驗收：
  - [ ] 新內容與 §2–§5 沒有矛盾
  - [ ] `SKILL.md` 中的入口說明同時涵蓋「追問」與「忠實導讀」
- 驗證：通讀並交叉比對 `extending-pages.md`、`SKILL.md` 與 `sources-and-research.md`
- 相依：T4
- 檔案：`references/extending-pages.md`、`SKILL.md`

**T6（M）V2：Ronin PDF，忠實導讀，使用 PDF 輔助 skill**
- 說明：輸出到 `~/Documents/explainers/robotics-engineer-6-months/`。這個案例用來驗證 R8 的「使用輔助 skill」情況。
- 驗收：
  - [ ] 確認訊息事先列出 PDF 輔助 skill
  - [ ] 主頁使用路線圖主軸
  - [ ] 原文的每一章都在對照表中有對應
  - [ ] 每頁都在篇幅預算內
- 驗證：
  - `extending-pages.md` §5 的頁面樹同步、current 標記與連結檢查
  - 用字數腳本檢查每一頁
  - 每頁截取兩種寬度的圖
  - 使用者判讀
- 相依：T5
- 檔案：無（輸出在儲存庫外）

**T7（S）V8 的前提：與使用者互動產出 C++ 學習計畫**
- 說明：
  - 依序執行 `idea-refine` 與 `planning-and-task-breakdown`，對象是有 Python 基礎的 C++ 初學者。
  - 輸出到 `~/Documents/explainers/cpp-learning/plan.md`。
  - 必須指定這個輸出路徑，不可寫入儲存庫的 `tasks/`。
  - 這個步驟不屬於 skill 的流程。
- 驗收：
  - [ ] 計畫的 Markdown 已存在，而且儲存庫的 `tasks/` 沒有被改動
- 驗證：`git status` 沒有變動
- 相依：無（可以與 T4–T6 並行）
- 檔案：無

**T8（S）V8：把 C++ 學習計畫轉成網頁**
- 說明：以 document 模式讀取 T7 產出的 `plan.md`，輸出到同一個目錄。
- 驗收：
  - [ ] 使用路線圖主軸
  - [ ] 計畫的每個階段都有對應的內容
  - [ ] 通過自我檢查
- 驗證：
  - 執行自我檢查指令
  - 截取兩種寬度的圖
  - 使用者判讀
- 相依：T5、T7
- 檔案：無

**檢查點 B**：使用者判讀 V2 與 V8，依回饋修正頁型與頁面樹規則，並提供 `git add` 建議。

### 第 3 階段：topic 模式

**T9（M）topic 模式查證與來源等級**
- 說明：
  - `sources-and-research.md` 新增：
    - topic 模式：先找原始文件；確認前先做少量搜尋；輕量或深度查證；詢問是否另存 `research.md`，預設不另存；沒有網路工具時的退路；模型知識只能當「一般背景」。
    - R5：來源分 4 級，每筆附存取日期，加上「新興說法」框與「截至 <日期>」。
  - `template.html`：新增 `.grade` 的 4 種樣式，Sources 的示範列加上等級與日期。
  - `writing-rules.md`：固定標籤表新增 Emerging view／新興說法、Note／注意、Accessed／存取日期，以及 4 個等級的中英名稱。
  - `SKILL.md`：第 4 步的第 4 題加入查證深度；第 6 步新增「每筆來源都有等級與日期」的檢查指令。
- 驗收：
  - [ ] 模板沒有外部資源，兩種寬度的截圖正常
  - [ ] 新增的檢查指令實際執行過一次：符合時沒有輸出，有缺漏時會列出
  - [ ] `SKILL.md` ≤ 約 130 行
- 驗證：
  - 用 `grep` 檢查外部資源
  - 截取兩種寬度的圖
  - 在 scratchpad 建立兩份假頁面，測試檢查指令
- 相依：檢查點 B
- 檔案：`references/sources-and-research.md`、`assets/template.html`、`references/writing-rules.md`、`SKILL.md`

**T10（M）V3：EKF，輕量查證，拒絕輔助 skill**
- 說明：輸出到 `~/Documents/explainers/extended-kalman-filter/`。確認時拒絕輔助 skill，驗證 R8 的內建退路。
- 驗收：
  - [ ] 原始來源優先：論文、教科書或官方文件
  - [ ] 用 L2 stepper 呈現預測與更新迴圈
  - [ ] 每筆來源都有等級與日期
  - [ ] 回報中寫明使用了內建做法
- 驗證：
  - 執行自我檢查指令
  - 對 stepper 逐幀截圖
  - 使用者判讀
- 相依：T9
- 檔案：無

**T11（M）V7：first principle**
- 說明：輸出到 `~/Documents/explainers/first-principles/`。
- 驗收：
  - [ ] 使用論點地圖主軸
  - [ ] 每句引述 Musk 的話都有出處與等級
  - [ ] 只有新興或個人說法支撐的主張都放在「新興說法」框中
- 驗證：
  - 執行自我檢查指令
  - 截取兩種寬度的圖
  - 使用者判讀
- 相依：T9
- 檔案：無

**檢查點 C**：使用者判讀 V3 與 V7，並決定 EKF 是否做成公開範例；如果要公開，在 T17 搬進 `examples/`。提供 `git add` 建議。

### 第 4 階段：讀者設定與高風險主題

**T12（S）R6 規則**
- 說明：
  - `writing-rules.md` 新增讀者設定，分為一般大眾、非本科大學生、工程師三種，並規定類比必須說明在哪裡不成立。
  - `sources-and-research.md` 新增高風險主題規則：只用權威來源、加上「注意」框、不寫劑量、醫療主題要有「何時就醫」、至少做輕量查證。
  - `SKILL.md` 第 4 步的第 3 題加入讀者設定。
- 驗收：
  - [ ] 專案模式的預設讀者為「工程師」
  - [ ] 高風險主題的確認訊息中，沒有「只靠模型知識」的選項
  - [ ] `SKILL.md` ≤ 約 130 行
- 驗證：通讀並交叉比對；確認行數
- 相依：檢查點 C
- 檔案：`references/writing-rules.md`、`references/sources-and-research.md`、`SKILL.md`

**T13（M）V4：甲狀腺衛教，繁中，一般大眾，深度研究並使用研究類輔助 skill**
- 說明：輸出到 `~/Documents/explainers/thyroid-health/`。驗證 R8 的「使用研究類 skill」情況，以及輔助 skill 的提問是否已在確認訊息中預告。
- 驗收：
  - [ ] 頁面有「注意」框與「何時就醫」段落
  - [ ] 來源都是權威來源，台灣讀者優先採用台灣資料
  - [ ] 頁面中沒有劑量
- 驗證：
  - 用 `grep -nE '[0-9]+ ?(mg|mcg|µg|微克|毫克)'` 檢查劑量，應該沒有輸出
  - 執行自我檢查指令
  - 使用者判讀
- 相依：T12
- 檔案：無

**T14（M）V6：緊急避難包（台灣）**
- 說明：輸出到 `~/Documents/explainers/emergency-go-bag/`。
- 驗收：
  - [ ] 使用實務指南主軸，即決策樹或檢查清單
  - [ ] 頁面有「注意」框
  - [ ] 引用台灣機關的來源
- 驗證：
  - 執行自我檢查指令
  - 截取兩種寬度的圖
  - 使用者判讀
- 相依：T12
- 檔案：無

**T15（M）V5：SpaceX Starship 與可復用火箭**
- 說明：讀者設定為非本科大學生，輸出到 `~/Documents/explainers/starship-reusability/`。
- 驗收：
  - [ ] 結論寫明「截至 <日期>」
  - [ ] 每個類比都說明在哪裡不成立
  - [ ] 使用機制頁型，主軸為因果鏈
- 驗證：
  - 執行自我檢查指令
  - 截取兩種寬度的圖
  - 使用者判讀
- 相依：T12
- 檔案：無

**檢查點 D**：使用者判讀 V4、V5、V6，並提供 `git add` 建議。

### 第 5 階段：Codex 與打包

**T16（S）Codex 實測**
- 說明：
  - 先取得使用者同意。
  - 依 README 的 Codex 安裝方式載入本機 plugin。
  - 用一個短案例（V1 的請求）確認 4 件事：skill 是否觸發、是否有網路工具、能否看到 skill 清單、沒有網路工具時的退路能否運作。
  - 依結果修正 `sources-and-research.md`。
- 驗收：
  - [ ] 規格 §6 中與 Codex 相關的兩個假設都有結論，並寫在本檔
- 驗證：保存 Codex 的輸出摘要；依結果修改 references 後，再執行一次 `SKILL.md` 的行數檢查
- 相依：檢查點 D
- 檔案：`references/sources-and-research.md`（視結果而定）、`tasks/plan.md`

**T17（M）README 雙語版**
- 說明：
  - 「使用方式」加入 document 與 topic 模式的例句。
  - 「刻意不做的事」的影片條目改寫為「不支援影片材料」。
  - 「目錄結構」加入兩份新的 reference 與 `docs/specs/`。
  - 如果檢查點 C 決定公開 EKF，就把它放進 `examples/ekf/`，並在範例段落列出。
- 驗收：
  - [ ] 兩份 README 的內容互相對應
  - [ ] README 中提到的路徑都存在
- 驗證：逐段比對兩份 README；用 `grep` 檢查路徑
- 相依：T16
- 檔案：`README.md`、`README.zh-TW.md`，以及 `examples/ekf/`（視檢查點 C 的決定）

**T18（S）manifest、CLAUDE.md、規格狀態、暫存檔刪除方式與回歸檢查**
- 說明：
  - 三份 manifest 的版本號升為 `0.3.0`。
  - `CLAUDE.md` 的架構段落加入兩份新的 reference 與三種模式。另外，模板驗證指令中的窄版截圖改用 iframe 方法（檢查點 A 第 3 點）。
  - 把規格開頭的狀態改為「已實作」。
  - 修正暫存檔的刪除方式（檢查點 A 第 6 點）：`SKILL.md` 第 6 步會用 `rm "$P"` 刪除暫存檔，這種以變數組成路徑的刪除指令可能被 Claude Code 的安全檢查擋下。改寫方向：把暫存的探測頁放在固定的字面路徑（例如 `/tmp/explain-as-webpage-narrow.html`），用絕對的 `file://` 路徑嵌入 iframe，再用字面路徑刪除。`svg-recipes.md` 的單幀截圖範例已經使用字面路徑 `/tmp/frame.html`，要一併確認。
  - 回歸檢查：比對專案模式的 diff，並重新截圖 `examples/` 中的 4 個既有頁面。
- 驗收：
  - [ ] 所有 manifest 的 JSON 都合法，而且版本號一致
  - [ ] plugin 驗證通過
  - [ ] 既有範例頁面沒有變化
  - [ ] 在 Claude Code 中原樣執行第 6 步與單幀截圖的指令，不被安全檢查擋下，暫存檔也確實被刪除
- 驗證：
  - 執行 `CLAUDE.md` 中的 manifest 迴圈
  - `claude plugin validate .`
  - `claude --plugin-dir . plugin details sphinx-style-notes-maker`
  - 截圖
- 相依：T17
- 檔案：`.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json`、`.codex-plugin/plugin.json`、`.agents/plugins/marketplace.json`、`CLAUDE.md`、`docs/specs/explain-as-webpage-v3.md`（只改機械性的欄位）、`SKILL.md`、`references/svg-recipes.md`

**檢查點 E**：確認規格 §8 的成功條件全部達成，並提供 `git add` 範圍與提交訊息建議。

## Risks and Mitigations
| 風險 | 影響 | 對策 |
|---|---|---|
| WebFetch 只回傳摘要，取不到全文 | 高 | T1 先探測；退路依序為 `curl` 加上本機轉文字、讀取網頁類輔助 skill，最後才請使用者存成 PDF |
| `SKILL.md` 超過約 130 行 | 中 | 細節一律放進 references；每個修改 `SKILL.md` 的任務都檢查行數 |
| 新增的主軸圖 SVG 錯位 | 中 | T4 先在 scratchpad 截圖驗證配方，再交給案例使用 |
| 輔助 skill 自帶的提問或輸出檔破壞單次確認 | 中 | 在確認訊息中預告；把中間檔放在暫存目錄；在 T6、T13 實際觀察 |
| 驗證案例多，耗時與 token 成本高 | 中 | 每個階段只跑對應的案例，由檢查點決定是否繼續 |
| 衛教內容不正確 | 高 | 只用權威來源、加上「注意」框、檢查沒有劑量，並由使用者判讀 |
| Codex 的行為與 Claude Code 不同 | 中 | T16 實測，依結果修正退路規則 |
| 以第三方材料產出的頁面誤入儲存庫 | 低 | 一律輸出到 `~/Documents/explainers/`，每個檢查點都檢查 `git status` |

## Open Questions
- EKF 是否做成公開範例（在檢查點 C 決定）。
- 忠實導讀約 6 個子頁是否足夠（由 T6 回答）。
- PG 長文、Harness Engineering 演進、LightGlue 是否要補驗（在檢查點 E 決定）。

## 探測結果

### T1（2026-10-03，Claude Code）

**1. 網頁全文**

| 材料 | `curl` 加上本機去除標籤 | WebFetch |
|---|---|---|
| PG〈How to Do Great Work〉 | 取得全文，11,738 個英文字，結尾為致謝段落 | 要求逐字回傳全文時，以著作權為由拒絕，只提供摘要與 125 字元以內的短引文 |
| Karpathy gist（`…/raw`） | 取得全文，1,921 個英文字，結尾與原文一致 | 9 個標題全部正確，順序也正確；各節字數只是估計值（加總約 2,170 字，實際為 1,921 字） |

結論：WebFetch 透過小模型回答提示，不能用來取得全文，只適合用來快速掌握大綱。

**2. PDF**

- Ronin PDF 共 39 頁，用 `pdftotext -layout` 抽出 11,456 個字。
- 少數特殊字形會變成 `�`，例如 `@DeRonin_` 的 `@`。這不影響理解，但引用時要對照原 PDF。
- Claude Code 的 Read 工具每次最多讀 20 頁 PDF，因此只作為退路。

**3. Claude Code 中可見的輔助 skill**

在代理上下文的 skill 清單中可以看到下列項目。這份清單只是本機現況，不得寫死進 `SKILL.md`。

| 能力 | 可見的項目 |
|---|---|
| 讀取網頁 | `anthropic-skills:chrome-browser`、`anthropic-skills:built-in-browser`、`claude-in-chrome`；工具：WebFetch、WebSearch |
| 讀取 PDF | `anthropic-skills:pdf` |
| 深度研究 | `anthropic-skills:deep-research` |

**4. Codex**

使用者選擇延後到 T16 實測。

**決定：網頁讀取的優先順序**（T2 寫入 `sources-and-research.md`）

1. 靜態頁面或原始文字（gist 加上 `/raw`、GitHub 的 raw 檔、一般 HTML 文章）：用 `curl -sL` 下載到暫存目錄，再用 Python 標準函式庫去除標籤，取得全文。用完即刪。
2. 需要 JS 或登入的頁面（例如 X）：經使用者同意後，使用讀取網頁類的輔助 skill。沒有這類 skill，或使用者拒絕時，請使用者把頁面存成 PDF。
3. WebFetch 只用來快速掌握大綱、確認標題，或在 `curl` 被擋時取得摘要。用了 WebFetch 時，要在回報中說明頁面只依據摘要。

### T16

（待填寫。）

### 檢查點 A 的發現（T2、T3，2026-10-03）

1. **候選疑問的數量與結構化提問的上限衝突。**
   - `AskUserQuestion` 每題最多 4 個選項，但規則要求列出 5–8 個候選疑問。
   - V1 只好把 7 個候選疑問拆成兩題多選，這樣就用掉 4 題上限中的 2 題，層級、語言與路徑只能擠在剩下的 2 題裡。
2. **長網址會撐開窄螢幕的版面。**
   - V1 的「來源」區有一個很長的網址連結，造成整頁出現水平捲軸。量測結果：scrollWidth 508 px，clientWidth 485 px。
   - 頁面上的處理方式是縮短連結文字。模板的 `a` 沒有 `overflow-wrap`，之後 document 與 topic 模式常會列出網址，所以同樣的問題會重複發生。
3. **headless Chrome 的窄版截圖並不是 390 px。**
   - 指定 `--window-size=390` 時，實際的視窗寬度是 500 px（Chrome 的最小視窗寬度），CSS 可用寬度是 485 px。
   - 也就是說，目前的「窄版檢查」等於在 485 px 下進行，並沒有真正驗證 390 px 的手機寬度。
4. 圖 2 的步進動畫中，第 3 步的說明文字在第 4 步與箭頭重疊。逐幀截圖時發現並已修正（改為只在第 3 幀顯示）。這屬於頁面本身的問題，不是規則的問題。
5. 用 `sed` 插入含有 `|` 的探測腳本時，又遇到分隔字元衝突；改用 Python 處理。這與 `CLAUDE.md` 中記錄的問題相同，但只發生在探測工具上，不影響 skill 本身。

**處理結果（使用者同意依建議處理）：**

- 第 1 點：候選疑問改為在訊息文字中編號列出。結構化提問只提供「建議組合」與替代組合，使用者也可以自填編號（`SKILL.md` 第 4 步第 1 項、`sources-and-research.md` §3）。
- 第 2 點：模板新增 `.content a { overflow-wrap: anywhere; }`。用含長網址的測試頁驗證：套用前是 OVERFLOW，套用後是 ok。
- 第 3 點：`SKILL.md` 第 6 步的窄版檢查改為在 390 px 的 iframe 中算繪，並以 `scrollWidth` 判定。指令原樣在 V1 頁面與模板上各執行一次，都回報 ok。`CLAUDE.md` 中的模板驗證指令仍使用 `--window-size=390`，留到 T18 一併更新。

6. **以變數組成路徑的 `rm` 會被 Claude Code 的安全檢查擋下。**（使用者以新模板重新產出 V1 時發現）
   - 我在迴圈中用 `rm $P` 刪除暫存的探測頁，`$P` 由 `$D/$n.src.html` 組成。安全檢查判定這個路徑在變數為空時可能指向根目錄，因此拒絕執行，整段指令都沒有跑。
   - `SKILL.md` 第 6 步的 `rm "$P"` 屬於同一種寫法。先前照原樣執行時沒有被擋，但其他代理在不同寫法下可能會被擋。
   - 使用者決定在 T18 處理，處理方向見 T18 的說明。

檢查點 A 判定通過（2026-10-03）。比較用的頁面 `~/Documents/explainers/llm-wiki/llm-wiki-new-template.html` 以新模板產出，在 390 px 下的溢出檢查為 ok。
