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
  - [x] 專案模式的預設讀者為「工程師」
  - [x] 高風險主題的確認訊息中，沒有「只靠模型知識」的選項
  - [x] `SKILL.md` ≤ 約 130 行
- 驗證：通讀並交叉比對；確認行數
- 相依：檢查點 C
- 檔案：`references/writing-rules.md`、`references/sources-and-research.md`、`SKILL.md`

**T13（M）V4：甲狀腺衛教，繁中，一般大眾，深度研究（使用者選擇不用輔助 skill）**
- 說明：輸出到 `~/Documents/explainers/thyroid-health/`。原本要驗證 R8 的「使用研究類 skill」情況；使用者在確認時選擇不用輔助 skill，該情況已由 T10（deep-research）驗證，本題改為驗證內建做法的深度研究。
- 驗收：
  - [x] 頁面有「注意」框與「何時就醫」段落
  - [x] 來源都是權威來源，台灣讀者優先採用台灣資料
  - [x] 頁面中沒有劑量
- 驗證：
  - 用 `grep -nE '[0-9]+ ?(mg|mcg|µg|微克|毫克)'` 檢查劑量，應該沒有輸出
  - 執行自我檢查指令
  - 使用者判讀
- 相依：T12
- 檔案：無

**T14（M）V6：緊急避難包（台灣）**
- 說明：輸出到 `~/Documents/explainers/emergency-go-bag/`。
- 驗收：
  - [x] 使用實務指南主軸，即決策樹或檢查清單
  - [x] 頁面有「注意」框
  - [x] 引用台灣機關的來源
- 驗證：
  - 執行自我檢查指令
  - 截取兩種寬度的圖
  - 使用者判讀
- 相依：T12
- 檔案：無

**T15（M）V5：SpaceX Starship 與可復用火箭**
- 說明：讀者設定為非本科大學生，輸出到 `~/Documents/explainers/starship-reusability/`。
- 驗收：
  - [x] 結論寫明「截至 <日期>」
  - [x] 每個類比都說明在哪裡不成立
  - [x] 使用機制頁型，主軸為因果鏈
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
  - 檢查點 C 決定 EKF 不公開，所以範例段落不變。
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

### 第 2 階段的發現（T4–T6，2026-10-03）

1. **輔助 skill 可能依賴尚未安裝的工具。**（R8，V2）
   - 使用者選擇使用 PDF skill，但它建議的 Python 函式庫（`pdfplumber`、`pypdfium2`、`pymupdf`）本機都沒有安裝。它列出的命令列做法就是 `pdftotext`，和內建做法相同。
   - 安裝套件屬於「先問再做」的項目；使用者選擇不安裝。結論：在這個環境中，PDF skill 沒有帶來額外效益。
   - 建議：`sources-and-research.md` §5 補上一條規則，在提議輔助 skill 之前，先確認它需要的工具已經安裝；若需要安裝，在確認訊息中說明。
2. **忠實導讀的頁面樹可行。**（V2）
   - 約 11,500 字的原文產出「主頁＋6 個子頁」。各頁正文約 1,300–2,100 個中文字，都在 3,500 字的預算內。
   - 對照表共 35 列：33 列對應到實際存在的 `h2`，2 列是有理由的略過。
   - 回答了待決問題「約 6 個子頁是否足夠」：對這份材料足夠。
3. **路線圖的子頁沒有明確的骨架。**
   - `page-types.md` 只定義路線圖的主頁。這次每個月份子頁自行採用「本月路線（圖 1：該月的單元與練習任務）→ 疑問 → 里程碑 → 資源」的結構。
   - 建議：把這個結構補進 `page-types.md` 的路線圖頁型。
4. **對照表的核對沒有現成指令。**
   - 這次是用臨時的 shell 迴圈，逐列確認目標 `h2` 是否存在。
   - 可以考慮把這個迴圈補進 `extending-pages.md` §6。
5. **為了讓 7 頁的頁面樹一致，產出時用了暫存的組裝腳本。**
   - 腳本放在 scratchpad，沒有放在輸出目錄，因此不違反「不在頁面旁留下腳本」。
   - 檢查點 B 結束後刪除。

6. **確認訊息中的清單，使用者可能看不到。**（V8）
   - 候選疑問寫在結構化提問之前的訊息文字中，但這次提問被中斷，使用者回覆「沒有看到清單」。
   - 建議：`SKILL.md` 第 4 步與 `sources-and-research.md` §3 改為把編號清單直接放進提問本身，例如題目文字或選項說明，不要只放在提問前的訊息中。
7. **短材料也可能需要頁面樹。**（V8）
   - 學習計畫約 3,300 個中文字，低於長文門檻；但使用者要求「每個階段一個子頁」，以說明每一步怎麼做。
   - 目前的規則只在長文時才提供「忠實導讀（頁面樹）」。建議：材料有自然的階段或章節時（例如路線圖、計畫），不論長短都提供「依階段分頁」的選項。
8. **使用者期待的內容超出材料本身。**（V8）
   - 計畫只寫了「做什麼」與驗收項目，使用者要的是「具體怎麼做、驗收在檢查什麼、預期成果」。
   - 這次補上的指令與程式片段依一般做法撰寫，每頁都以「說明」框標示為「一般做法（非計畫原文）」，指令沒有上網查證。
   - 建議：document 模式加入「依材料展開成操作說明」的選項，並說明補充內容的來源與查證方式；這和 T9 的 topic 模式查證規則有關，可以在 T9 一併處理。
9. **雙欄的「項目／內容」表格在中文頁面中，第一欄會被擠成每行一兩個字。**（V8）
   - 這次在各列的第一個儲存格加上 `white-space:nowrap` 解決，並把「具體步驟」改成編號清單。
   - 建議：在模板中提供一個鍵值表的樣式，例如 `table.kv td:first-child { white-space: nowrap; }`，並在 `writing-rules.md` 說明何時使用。
10. **子頁第一版只有圖 1，不符合 L0 每頁 2–5 張圖的規則。**（V8）
    - 事後為每個子頁補上一張說明機制的圖。
    - 建議：路線圖子頁的骨架（見第 3 點）要寫明「除了本階段路線圖，至少再加一張說明機制的圖」。
11. **暫存目錄在工作階段中途失效。**
    - V2 的組裝腳本與內容檔留在已失效的 scratchpad 中，無法再使用或清理。
    - V8 改用儲存庫外的 `~/Documents/explainers/.work-cpp/`，檢查點 B 結束後以字面路徑刪除。

**檢查點 B 的處理結果（2026-10-03）：**使用者判讀 V2、V8 可讀。同意第 1、3、4、6、9、10 點，均已實作。第 7、8 點經回顧兩個「計畫類」頁面的實際做法後，整理成規則 A–D，使用者全部同意並已實作：

- 第 1 點：`sources-and-research.md` §5，提議輔助 skill 前先確認工具已安裝。
- 第 3、10 點：`page-types.md` 的路線圖子頁骨架，要求除了本階段路線圖，至少再加一張說明機制的圖。
- 第 4 點：`extending-pages.md` §6 加入對照表的核對迴圈，並實際測試過：錯誤列會回報 MISSING，略過的列會印出 skipped。
- 第 6 點：`SKILL.md` 第 4 步與 `sources-and-research.md` §3，候選疑問清單改放在提問本身。
- 第 9 點：模板新增 `table.kv`，`writing-rules.md` 新增「Label tables」一節。
- A：`page-types.md` 改為「Roadmap and plan pages」，內容包括：計畫類不論長短都預設建立頁面樹、主頁固定要回答的問題、單元四欄卡片、檢查點兩欄表，以及「Explain every check」原則。
- B：`sources-and-research.md` 新增 §6「Expanding material into steps」，固定標籤表新增「Note／說明」；確認步驟會詢問是否展開成操作說明。
- C：`svg-recipes.md` 的配方 7 新增蛇形排列，以及可點選的主頁圖 1。
- D：`extending-pages.md` §6 新增暫存組裝腳本的規則；`svg-recipes.md` 新增「只顯示圖」的截圖方法，兩段範例都實際執行過。


### 第 3 階段的發現（T9、T10，2026-10-03）

1. **T10 沒有驗證內建退路。**
   - 使用者在 V3 的確認中選擇「深度研究＋deep-research skill」，所以計畫中「拒絕輔助 skill、驗證內建退路」這一項沒有做。
   - 改由 T11 在確認時提供選項，由使用者決定。
2. **deep-research skill 的設計與本 skill 的規則衝突。**
   - 它會把研究筆記與報告寫進目前的工作目錄（也就是儲存庫），會派出多個子代理，子代理也會在 `/tmp` 留下下載的原始資料。
   - 這次的處理：把工作目錄改到儲存庫外的 `~/Documents/explainers/.work-ekf/`；頁面完成後，刪除該資料夾與子代理在 `/tmp` 留下的 `ekfr*` 資料夾（刪除前已確認是本次研究期間建立的）。
   - 建議：`sources-and-research.md` §5／§7 補上兩條規則。一是研究類輔助 skill 的工作目錄要指向暫存資料夾，結束後連同下載檔一併刪除；二是在確認訊息中預告它會派出子代理、需要較長時間（這次約 13 分鐘）。
3. **輔助 skill 的輸出中有數字前後不一致。**
   - 研究者回報手寫骨架的模擬誤差是 0.052 m，彙整報告卻寫 0.023 m。頁面沒有引用這個數字。
   - 建議：使用輔助 skill 的數字之前，先和它的原始筆記交叉核對。
4. **固定標籤的英文名稱與規格不同。**
   - 規格 R6 的高風險「注意」框，英文原本是 Note；但 Note 已用於「說明」框（§6），所以改為 Caution／注意。T12 依此實作。

5. **內建退路在 T11（V7）驗證可行。**
   - 使用者選擇「輕量查證、不用輔助 skill」。
   - WebFetch 讀不到 TED 逐字稿（由 JavaScript 載入），也被 Wired 擋下。依 §2 改用 `curl` 下載原始 HTML 後在本機搜尋，兩份原始訪談的原文都順利取得。
6. **影片類的原始出處只能靠二手轉述。**
   - Kevin Rose 訪談只有影片；依「不支援影片」的規則，改用兩份二手摘錄，標為「二手整理」並註明未查證原影片。
   - 其中一份摘錄的頁面在查證期間已回傳 404，可見記錄存取日期的必要。
7. **自己寫的案例句子，要逐句對回來源。**
   - 初稿把「SpaceX 改用新技術、減少外包」寫成案例，但 Wired 原文只列出成本偏高的原因，沒有這句話。對照原文後已修正。
   - 建議：在 §7 補一條規則：每個「實際案例」都要能指到來源中的對應句子。


**檢查點 C 的回饋與處理（2026-10-03）：**

- V7（first principles）：使用者判讀沒有問題。
- V3（EKF）有三點回饋，已修正：
  1. P̄、μ̄ 使用組合橫線（U+0304），在網頁上位置歪斜、不易辨識。已全部改為上標減號：HTML 用 `<sup>−</sup>`，依 Welch & Bishop 的事前估計記號，並在頁面上說明它的意思。
  2. 「估計、預測、共變異數」沒有說明是「什麼」的估計，太抽象。第 1 題新增「本頁的例子：一台在室內行走的機器人」與符號對照表；第 3 題的動畫說明與九步計算表全部改用機器人的語言，並附上以 numpy 實際算出的示意數字（出發 (0, 0) → 預測 (3.0, 0) → 地標 (4, 2) 的距離與方位 → 更新 (2.89, 0.01)）；「F P Fᵀ ＋ Q 讓範圍變大」改用「走 3 m、方向差 2° → 側向偏約 10 cm」的幾何直覺解釋。
  3. 頁面像演算法說明，看不出和機器人的關聯。由上一點的貫穿全頁例子與對照表處理，結論框也加上「EKF 回答的是：我在哪裡、有多確定」。
  - 修改後正文 3,501 個中文字（預算約 3,500），390 px 檢查為 ok；兩張表的前兩欄設為不換行，避免公式斷行。
- 同意的規則補強（第 2、3、7 點）已寫入 `sources-and-research.md` §5、§7。
- 由這次回饋衍生、待使用者決定的規則：
  - (a) 不使用組合附加符號（x̄、μ̄、x̂），改用 `<sup>`、下標或文字（`writing-rules.md` § Formulas）。
  - (b) 從某個領域角度解釋一項技術時，前段要有貫穿全頁的具體例子、符號與領域物件的對照表；過程類說明要用這個例子的實際計算數字（`writing-rules.md` 或 `page-types.md` 的機制頁）。
  - (c) 多欄表格中較短的名稱或公式欄也要不換行（把 `table.kv` 的規則擴大到前幾欄）。
- 使用者決定（2026-10-03）：EKF 維持不公開，作為本機驗證產物；EKF 頁面仍有改善空間，等本計畫完成後再檢討。三條衍生規則 (a)(b)(c) 同意並已寫入 `writing-rules.md`（Formulas、Ground the symbols in one running example、Label tables），`SKILL.md` 的內容檢查清單同步加註。檢查點 C 通過。


### T13 結果（2026-10-04）

- 確認結果：疑問 1、2、3、5、6、8；L0；繁中、一般大眾；深度研究，不用輔助 skill。輸出路徑 `~/Documents/explainers/thyroid-health/thyroid-health.html`。
- 自我檢查：FILL 0、外部資源 0、約 32 KB、來源等級與存取日期 awk 無輸出、劑量 grep 無輸出、正文 2,517 個 CJK 字（預算 3,500）、390px 為 ok；3 張圖。截圖發現原因表第一欄（每列標籤）斷成每行兩字，已加 `nowrap` 修正，這是 `writing-rules.md` § Label tables 已有的規則，屬執行疏漏而非規則缺口。
- 查證：每個關鍵主張至少兩個權威來源。原始檔暫存於 `~/Documents/explainers/.work-thy/`，頁面完成後已刪除（先列出內容再以字面路徑刪除）。國健署在頁面上標為 g2（政府機關屬「權威」，依 §8 表格）。
  - 美國 NIDDK：亢進、低下、葛瑞夫茲病、橋本氏病（g2）。
  - 英國 NHS：亢進、低下、亢進併發症（甲狀腺風暴警訊）、亢進治療（服用抗甲狀腺藥物期間出現發燒、喉嚨痛要立即就醫）（g2）。
  - 國健署〈碘攝取不足只跟甲狀腺腫大有關？〉2020/03/19：認明碘鹽、孕婦需碘量大增（g1）。
  - 雙和醫院〈認識甲狀腺機能亢進〉2019-06-25：多為免疫疾病、約 5% 為毒性結節、不可隨便停藥（g2）。
  - 臺大醫院健康電子報 2013-11（邱偉益）：低下的原因、症狀、補充甲狀腺素、不可自行調整劑量；台灣鼻咽癌放療後的甲狀腺低下（g2）。
- 頁面要寫明的來源差異：國健署建議一般民眾使用碘鹽；NIDDK 提醒自體免疫甲狀腺疾病患者避免大量海藻與碘補充劑，兩者適用對象不同。
- 新發現（檢查點 D 要討論）：
  - 國健署主站的憑證鏈不完整，`curl` 與 WebFetch 都失敗。改依 AIA 下載 TWCA 中繼憑證，和系統根憑證合併後以 `--cacert` 完整驗證連線，沒有使用 `-k`。建議把這個做法補進 `sources-and-research.md` §2。
  - 馬偕醫院擋下 `curl`，健康九九＋的文章已經 404，雙和醫院的內容是動態載入，改以 WebFetch 摘錄。

### T14 結果（2026-10-04）

- 確認結果：主頁回答疑問 1、2、3、4、6；疑問 7（地震、颱風、空襲的差別）依使用者要求做成子頁；L0；繁中、一般大眾；輕量查證，不用輔助 skill。這是第一次在確認時由使用者指定「某題做子頁」，流程不需要新規則：照 `extending-pages.md` §6 第一次產出就建立頁面樹即可。
- 輸出：`~/Documents/explainers/emergency-go-bag/emergency-go-bag.html`（主頁，2 張圖、4 張表）與 `emergency-go-bag--scenarios.html`（子頁，1 張圖、3 張表）。
- 自我檢查：兩頁 FILL 0、外部資源 0、約 31 KB 與 27 KB、來源等級 awk 無輸出、正文 2,103 與 2,171 個 CJK 字、390px 皆為 ok；頁面樹三項檢查（一致、標示目前頁、連結存在）皆無錯誤。
- 來源：消防署〈緊急避難包準備清單〉（2025-06-26，含 1、2、3 天版）、國防部《臺灣全民安全指引》PDF（2025-11）、消防防災館 6 篇、臺北市與高雄市消防局，共 10 個，全為 g2。研究暫存檔放在工作階段暫存目錄，完成後已刪除。
- 逐句核對來源時修正 5 處超出來源的敘述：電子支付失效（來源只寫提款機）、哨子用途、以「箱」換算瓶裝水（改為瓶數）、颱風「數天預報」、表格「為什麼」欄的推論。後兩類改為標示「一般背景說明／依官方建議推論」。實務指南的「為什麼」欄與「常見錯誤」表天生含推論，`page-types.md` 可考慮規定在表下標示（檢查點 D 討論）。
- 消防署主站（www.nfa.gov.tw）與國健署同樣缺 TWCA 中繼憑證；同一個 AIA 做法有效。這是第二個政府網站出現同樣問題，支持把做法補進 `sources-and-research.md` §2。
- 兩份官方文件對避難包飲水量的寫法不同（消防署：體重 × 15 毫升／天；《指引》：兩瓶 600 毫升），頁面以 60 公斤的範例實際計算並說明差異來自天數。

### T15 結果（2026-10-04）

- 確認結果：疑問 1、2、3、4、5；使用者選 L2（第 3 題「助推器怎麼回來」用 stepper，其餘 L0）；繁中、非本科大學生；輕量查證，不用輔助 skill。
- 輸出：`~/Documents/explainers/starship-reusability/starship-reusability.html`。4 張圖：圖 1 因果鏈（兩列蛇形）、圖 2 兩節結構、圖 3 助推器返回 stepper（5 步）、圖 4 每公斤動能比較＋飛船回收四步。
- 自我檢查：FILL 0、外部資源 0、約 37 KB、來源等級 awk 無輸出、無組合附加符號、正文 2,760 個 CJK 字＋247 個英文詞、390px 為 ok。stepper 逐格截圖發現第 4、5 步的標籤離助推器太遠且隔著上升軌跡，已把發射塔右移、標籤移到塔左側。
- 貫穿例子：用 NASA Glenn 頁面的數字實算火箭方程式（比衝 350 秒、7,600 m/s → MR ≈ 9.1、推進劑約 89%），再對照 Starship 的載荷比例（約 2–3%）；第 4 題用 ½v² 算出飛船每公斤能量約為助推器的 10 倍。
- 來源（8 筆）：SpaceX 試飛報告第 5、7–14 次（g1）、NASA Glenn 與 NASA Ames 的 Jones（2018）（g2）、Wikipedia 兩篇（g3）。成本的個人說法（Musk）放入「新興說法」框；Jones「可復用不保證便宜」與 Starship 的目標並列，放入「推論」框。
- 新發現（檢查點 D 討論）：
  - SpaceX 官網是 JavaScript 頁面，`curl` 與 WebFetch 都只拿到空殼；改從官網背後的內容服務（content.spacex.com 的 JSON）取得試飛報告全文。`sources-and-research.md` §2 對「需要 JavaScript 的頁面」只建議瀏覽器類輔助 skill 或請使用者存成 PDF，可補一句：先找頁面背後的公開資料端點。
  - 新聞網站（NASASpaceFlight）回 403，第 15 次試飛的日期與目標無法找到原句，因此頁面不寫（遵守 §7 第 8 點）。
  - Wikipedia 的一般網頁回傳的是內嵌 wikitext 的 HTML，改用 MediaWiki API 的 `prop=extracts&explaintext=1` 取得純文字。

### 檢查點 D 的決定（2026-10-04）

- 使用者同意三條新規則，已寫入並實際執行新增的指令：
  - `sources-and-research.md` §2：伺服器缺中繼憑證時，依 AIA 補上中繼憑證後以 `--cacert` 連線，不用 `-k`（以 www.nfa.gov.tw 實測：未補時 `curl` 錯誤 60，補上後 200）。
  - `sources-and-research.md` §2：需要 JavaScript 的頁面，先從 HTML 與它載入的小型腳本找公開資料端點（spacex.com 的 `environment.js` 寫有 `cmsBaseUrl`）；Wikipedia 改用 MediaWiki API 取得純文字（已實測）。
  - `page-types.md` 實務指南：「為什麼」欄與常見錯誤表若是推論，要在表下標明。
- 使用者決定把 LLM Wiki（以新模板產出的版本）與 Starship 收進 `examples/llm-wiki/`、`examples/starship-reusability/` 作為繁中範例。規格 §0「第三方頁面不公開」已加註這個例外；README 兩個語言版本的範例段落與目錄結構已加入兩個範例。EKF 仍不公開。
- 使用者調整了 README 的「靈感來源」段落（改放貼文截圖）。調整後，下一段開頭的「This skill implements the first three.／本 skill 實作前三項」失去指涉對象，留給使用者決定，T17 一併處理。
- 使用者要求以最新版 skill 重做儲存庫說明頁，且不參考 `examples/explain-as-webpage/`：
  - 確認結果：疑問 1、2、3、4、5、7，安裝方式以小表放在頁尾；L0 單頁（套件頁型）；繁中、工程師；輸出 `~/Documents/explainers/sphinx-style-notes-maker/explain-as-webpage.html`。
  - 貫穿例子用 Starship 請求走完 7 步；反事實用 T1 的「WebFetch 與 `curl` 讀同一篇文章」實測；圖 3 以 `wc -c` 與 `claude plugin details` 的數字畫出各檔案的載入時機。
  - 自我檢查：FILL 0（正文原本提到這個標記本身，造成計數 1，已改寫）、外部資源 0、約 37 KB、390px 為 ok。截圖發現兩個問題並修正：決策樹中間分支的標籤壓在線上、安裝表的指令在字中間斷行（改為程式碼區塊）。
  - 使用者回饋：圖 3 原本以位元組數畫長條，只有前兩列標 token 數，單位混用且會誤導（`writing-rules.md` 9.8 KB 與 `SKILL.md` 11.8 KB 的 token 估計值同為約 3.7k）。改為全部用 token 估計值：把每個參考檔與模板各包成測試用 skill，以 `claude plugin details` 估得，頁面標明是估計值。使用者決定這條規則屬於 skill 而非本儲存庫：已寫入 `writing-rules.md` § Figures and text（依問題選圖表單位、一張圖一種單位、代理指標要說明、在圖說或來源行與回報中說明單位與理由、估計值要標明），並在 `SKILL.md` 第 7 步的回報項目加上「每張數值圖的單位與理由」。

### 圖中數值的意義（2026-10-04）

- 使用者認為上一輪的「依問題選單位」太侷限，要涵蓋各種圖表。以 idea-refine 整理成 `docs/ideas/figure-values.md`，使用者選定方向 A＋B＋C＋E＋G：
  - `writing-rules.md` § Figures and text：「讀圖四問」（量什麼、單位或無單位時的定義與範圍、怎麼讀、從哪來），取代「選單位」規則；「每個數字給單位」從 English 小節移到適用所有語言的 § Sentences。
  - `svg-recipes.md`：新增 § Axes and scales（軸名附單位、刻度、參考線、圖例、示意圖不放刻度），附位移、溫度、ROC 三個例子；「只顯示圖」的截圖改為保留來源行（已實際執行）。
  - `SKILL.md` 第 6 步清單合併成「每個數字有來源與單位，每張數值圖說明量什麼、怎麼讀、從哪來」，第 7 步回報列出單位與理由；仍為 130 行。
- 四個範例的 21 張含數字的圖（含行號、步驟編號這類標籤）逐一檢查，修正 6 處：autoresearch `prepare.py` 子頁圖 3（token 單位、補來源行）、`train.py` 子頁圖 2（參數量、補來源行說明 × 1.22 與 LR 無單位）、主頁圖 3（val_bpb 的單位與方向）、LLM Wiki 圖 1（「約」10–15 頁、標明是作者的估計）、Starship 圖 1（「占起飛質量」）、圖 4（MJ → MJ/kg）。英文的 explain-as-webpage 範例符合四問，但內容停在 v2（只有專案模式），是否以新產出的繁中說明頁取代，留給使用者決定。

### 儲存庫說明頁收為雙語範例（2026-10-04）

- 依繁中說明頁產出英文版，取代舊的英文範例 `examples/explain-as-webpage/explain-as-webpage.html`；繁中版存為同目錄的 `explain-as-webpage.zh-TW.html`。英文版正文 1,616 字（預算 1,800），FILL 0、外部資源 0、390px 為 ok；英文標籤較長，圖 2、圖 4 的結果框右移，圖 3 的註記拆成三行，截圖確認無重疊。
- README 封面圖改用兩版的圖 1：`docs/images/cover-process.png`（英文）與新增的 `cover-process.zh-TW.png`（繁中）。
- `README.md` 的範例段落只列英文範例（explain-as-webpage、autoresearch），`README.zh-TW.md` 只列繁中範例（explain-as-webpage、llm-wiki、starship-reusability）；繁中版的層級截圖說明改為「取自英文範例 `examples/autoresearch/`」。兩份的目錄結構仍列出全部範例資料夾。`CLAUDE.md` 的範例說明同步更新。
- 使用者修正了「Inspiration／靈感來源」；英文版的拼字錯誤（seggestions）與介系詞（of → in the post）已修正。

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
