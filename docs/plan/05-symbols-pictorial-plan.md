# 實作計畫：符號對照圖與具象插圖品質（第五輪）

構想見 `docs/plan/05-symbols-pictorial-idea.md`，規格見 `docs/plan/05-symbols-pictorial-spec.md`。本文件同時是待辦清單：〈進度總覽〉每項一行，完成時勾選並補一句結果；各任務的驗收條件也逐項勾選；探測與驗收的細節記在〈結果〉。

## 進度總覽

### 第 0 階段：探測（不改產品檔案）
- [x] T1 Noto Emoji：授權、版本、物件清單、大小、id 前綴、兩種截圖 —— SVG 圖檔為 Apache 2.0；39 個候選轉成 symbol 後與原圖一致；共用隱藏 `<svg>` 在三種截圖中都能顯示漸層
- [x] T2 風格試畫：5 種物件各 3 次、助推器殘影草圖 —— 外形一致；發現模板的 `svg .x` 選擇器在 `<use>` 引用的物件中失效
- [x] T3 壓線檢查原型：V4 準確度 —— 7 個重建缺陷全部抓到；8 頁加上另外 23 個使用者頁面，在加入排除規則後 0 個回報；每頁約 0.6 秒
- [x] T4 Codex 觸發測試（使用者手動）—— 2026-10-12：5 個提示觸發 0 次；g3、g5 由 Codex 內建的 `imagegen` 產生點陣圖
- [x] T14 具象基準測試（使用者手動）—— 2026-10-13：(a)、(b) 畫成物件的節點都是 0 個；(a) 4 個方框加手繪圖示，(b) 4 個純方框

#### 檢查點 0
- [x] 使用者判讀 emoji 與自繪風格是否搭配、試畫結果、腳本準確度、Codex 結果 —— 2026-10-10 除 T4 外都已判讀；2026-10-12 T4 觸發 0 次，依外部 skill 調查修訂規格（R3、R6、R7）；2026-10-13 T14 結果已記錄

### 第 1 階段：符號對照規則（R1）
- [x] T5 `.sym`、圖說明單的 Symbols 欄、符號標註規則、`writing-rules.md` 引用 —— 2026-10-13：x̂ 在 SVG 與 HTML 中都正確顯示；`explainer-figure/SKILL.md` 112 行

#### 檢查點 A
- [x] 使用者確認 T5 的示範截圖；提供提交建議 —— 2026-10-13：使用者確認並提交（`72d22c9`）

### 第 2 階段：繪圖基礎（R2、R3、R6、R7）
- [x] T7 壓線檢查進入 `scripts/`，加入 Self-check 指令 —— 2026-10-13：7 個重建缺陷全部抓到；7 個範例頁與 24 個使用者頁面 0 個回報；`SKILL.md` 120 行
- [x] T8 風格規範與零件函式庫（人體、機器人、無人機、姿態計算、零件總覽圖）—— 2026-10-13：`parts.py` 9 個子指令；零件總覽圖 68 個形狀的外框都是 4px；`SKILL.md` 121 行
- ~~T9 Noto Emoji 子集、`emoji.md`、同步指令~~（2026-10-10 隨 R4 取消）
- ~~T10 若 T4 有觸發：改寫 explainer-figure 的 description 或隱藏方式~~（2026-10-12 取消：T4 觸發 0 次）
- [x] T15 節點外觀原則：`SKILL.md` 段落、`pictorial.md` 開頭、`icons.md` 禁令範圍、Recipe 3 片段 —— 2026-10-13：遮住文字後，瀏覽器與資料庫仍可辨認，API server 維持方框
- [x] T16 意圖檢查：遮住文字的截圖、與零件總覽圖並排、放大截圖 —— 2026-10-13：3 項指令在 Recipe 3 暫存頁與 Starship 範例頁都執行過；`SKILL.md` 124 行

#### 檢查點 B
- [x] 使用者判讀零件總覽圖與 Recipe 3 的片段截圖；提供提交建議 —— 2026-10-13：人體腿寬修正後通過

### 第 3 階段：驗證案例
- [x] T6 EKF 頁 v2（V1）—— 2026-10-13：圖 3 的機器人改用零件函式庫，5 個符號（μ、P、z、K、y）在圖、公式與符號表同色；自檢全部通過
- [x] T11 Starship 圖 4：發射到接回的 8 步姿態圖，外形依查得的資料（V2）—— 2026-10-13：暫存副本完成，自檢全部通過；等檢查點 C 決定是否取代範例
- [ ] T17 節點外觀重測（使用者手動，V8）
- [x] T18 P1–P4 改用物件風格（2026-10-13 檢查點 C 新增）—— 2026-10-13：5 個片段改用 `ink`；模板新增 `ink hollow`、`ink-level`，移除 4 個舊 class；受影響的範例圖只有 `llm-wiki` 圖 4、5 與 Starship 圖 2–5
- [ ] T19 Starship 範例全頁依新規則重畫，取代範例（2026-10-13 檢查點 C 新增）

#### 檢查點 C
- [ ] 使用者並排判讀 EKF 新舊版、Starship 圖 4 新舊版（決定是否取代範例）、T17 與 T14 的對照、T19 全頁；提供提交建議

### 第 4 階段：驗收與收尾
- [ ] T12 新主題頁（V7；使用者先指定主題）
- [ ] T13 版本 0.5.0、`CLAUDE.md`、README、構想文件的假設、索引狀態

#### 檢查點 D
- [ ] 規格〈成功條件〉全部達成；提供最終提交建議

## Overview

本輪讓 explainer-figure 能做三件事：

- 把公式符號標在圖上，並與公式使用相同的概念色。
- 以「粗外框＋平塗色」的風格畫出具象物件與它的姿態。不使用插圖庫，圖中的物件一律自繪（2026-10-10 決定）；幾何由零件函式庫 `scripts/parts.py` 產生（2026-10-12 決定）。
- 在任何圖型中，把代表具體東西的節點畫成那個東西，並在自檢中確認圖達到設計目的（2026-10-12 決定）。

另外加入壓線檢查腳本，並驗證 Codex 不會自動觸發 explainer-figure（2026-10-12 確認觸發 0 次）。頁面仍是單檔、離線，上限仍是 150 KB。

## Architecture Decisions

使用者已確認的決策列在規格〈0. 問題陳述與範圍〉。規劃時的補充：

1. **`SKILL.md` 的行數預算。** `skills/explainer-page/SKILL.md` 已有 130 行，本輪不修改。`skills/explainer-figure/SKILL.md` 有 111 行，新增內容以約 19 行為上限：Symbols 欄 1 行、圖型表具象插圖列的修改（不新增列）、壓線檢查指令約 6 行、節點外觀段落的改寫（淨增約 2 行）、零件函式庫指令約 3 行、意圖檢查約 3 行。其餘細節放進 references；超過時，意圖檢查的指令細節先移出。
2. **第一個腳本檔。** 兩個 skill 原本只在 markdown 中放 heredoc 指令。壓線檢查約 60–100 行 JavaScript，每次複製容易出錯，所以放成獨立檔 `scripts/check-overlap.js`。Claude Code 與 Codex 都從 skill 資料夾讀取這支檔案，不依賴平台功能。
3. **只看圖的截圖。** `explainer-figure/SKILL.md` § Self-check 的截圖指令會隱藏 `.content` 中不是 figure 的元素。共用的隱藏 `<svg>`（`template.html` 第 146 行）位於 `.content` 之外，但 `pictorial.md` 記錄過 `clipPath` 放在共用 `<svg>` 時，在只看圖截圖中失效。emoji 的漸層也可能遇到相同的問題，所以 T1 要在兩種截圖中都確認。（T1 結果：漸層在三種截圖中都正常；R4 已於 2026-10-10 取消。）
4. ~~**emoji 與圖示分開。**~~ 隨 R4 取消（2026-10-10）。
5. **最高風險先探測。** emoji 的風格與顯示、自繪風格的穩定性、腳本的誤報率，三項都在第 0 階段完成，先於任何產品檔案的修改。
6. **探測檔案。** 試畫與原型放在 session 的暫存目錄，不進儲存庫；結果與截圖路徑記在〈結果〉。
7. **提交方式。** 實作過程不自行 `git commit`；每個檢查點提供 `git add` 範圍與提交訊息。
8. **版本號。** 本輪新增功能，收尾時升為 0.5.0，四個 manifest 檔同步。
9. **P5 的 CSS 限制（T2 發現，2026-10-10 寫入規格 R3）。** `<use>` 引用的物件中，`svg .x` 選擇器與後代選擇器都不會套用，`vector-effect` 也不會繼承。所以 T8 新增的風格 class 不加 `svg ` 前綴，變化以 CSS 自訂屬性傳遞，物件不使用 `scale()`。
10. **探測程式的重建。** 第 0 階段的暫存目錄已在 session 結束後被清空。T7 依〈結果〉T3 的記錄重寫 `check-overlap.js`，並重跑 7 個重建缺陷與範例頁，確認結果與 T3 相同。
11. **第二個腳本檔：零件函式庫。** `scripts/parts.py` 只使用 Python 3 標準函式庫。圖示同步指令已要求 Python 3，壓線檢查在 Chrome 中執行，因此不新增 Node 這項依賴。函式庫以命令列子指令輸出 SVG 片段，產生器只在產頁時執行，頁面仍是單檔。
12. **外觀是獨立於圖型的維度。** 比照 diagram-design 的 ADR 0002：節點外觀（R6）不新增圖型，也不列元件清單，而是在既有的每一種圖型中判斷。調查見 `docs/plan/05-symbols-pictorial-skill-survey.md`。
13. **特定實物依資料繪製。** 函式庫不做火箭。T11 的 Starship 由代理查得的資料決定外形，以基本形組合（規格 R6 第 4 點）。
14. **基準先於修改。** T14 必須在 T15 修改規則前執行，T17 用同一個提示重測，兩者的差異才能歸因於 R6。

## Task List

### 第 0 階段：探測（不改產品檔案）

#### T1 Noto Emoji 探測

**說明：** 確認 Noto Emoji 的授權、版本與檔案格式，選出子集候選，並確認漸層在兩種截圖中都能顯示。

**驗收條件：**
- [x] 已讀 LICENSE 原文，記錄 SVG 圖檔的授權條款，以及內嵌與重新散布的條件
- [x] 選定一個發行版並記錄版本號
- [x] 統計 7 個範例頁、EKF 頁與候選主題需要的辨識型物件，列出約 30 個候選與 Noto 的覆蓋率
- [x] 記錄每個候選的檔案大小與總和；估算一頁放 5 個 emoji 的增量
- [x] 以一段程式替 emoji 內部的 id 加上 `e-<name>-` 前綴，同頁放 5 個 emoji 時沒有衝突
- [x] 把 emoji 放在共用的隱藏 `<svg>` 中，在整頁截圖與只看圖截圖中都正常顯示；不能顯示時，改測逐圖內嵌，並記錄結論
- [x] 把 emoji 與「粗外框＋平塗色」的自繪物件放在同一張圖中截圖，供檢查點 0 判讀

**驗證：** `git status` 只有本計畫檔有變動。

**相依：** 無　**檔案：** 本計畫檔、暫存檔　**規模：** M

#### T2 風格試畫

**說明：** 以「粗外框＋平塗色」試畫 5 種物件，每種畫 3 次，檢查穩定性；並畫一張助推器殘影草圖。

**驗收條件：**
- [x] 人、背包、俯視機器人、俯視車、火箭各畫 3 次，都在 720 寬的網格上
- [x] 記錄外框線寬、填色、陰影的參數（候選線寬 3px）
- [x] 助推器殘影草圖：物件定義一次，以 `<use>` 加上 `transform` 擺出至少 4 個姿態
- [x] 截圖交使用者判讀（檢查點 0；截圖路徑見〈結果〉T2）

**驗證：** 同一物件 3 次的外形一致，截圖中沒有歪掉、破損或溢出（V3）。

**相依：** 無　**檔案：** 本計畫檔、暫存檔　**規模：** M

#### T3 壓線檢查原型

**說明：** 依規格 R2 寫出原型腳本，量測漏報與誤報。

**驗收條件：**
- [x] 原型能逐幀檢查 stepper，輸出格式符合 R2 第 7 點（2026-10-10 修訂前為第 6 點），全部通過時不印出任何內容
- [x] 依規格 R2 表中 6 個已記錄的缺陷，在現有頁面的副本中重新放入，再加 1 個人工的文字重疊案例；7 個都抓到
- [x] 在 7 個範例頁與 EKF 頁上執行，逐一判讀每個回報是真缺陷或誤報，並記錄需要的排除規則
- [x] 記錄執行時間

**驗證：** V4 的兩個條件都成立。

**相依：** 無　**檔案：** 本計畫檔、暫存檔　**規模：** M

#### T4 Codex 觸發測試（使用者手動）

**說明：** 使用者在 Codex 中執行下列 5 個提示，每個提示開一個新 session。第 4 輪 T4 只記錄了提示的主題，沒有記錄原文，所以依主題重寫：

| # | 提示 |
|---|---|
| g1 | 幫我用 SVG 畫一張某公司 1–6 月銷售額的長條圖，數字自己假設。 |
| g2 | 用 SVG 畫一張 CPU 溫度在 10 分鐘內變化的折線圖。 |
| g3 | 畫一張 Web app 的架構圖：瀏覽器、API server、資料庫、快取。 |
| g4 | 做一個 KPI 儀表板的 HTML，包含營收、使用者數、轉換率三張卡片。 |
| g5 | 畫一張登入流程圖：輸入帳密、驗證、成功或失敗。 |

**判讀：** 檢查 session 紀錄中是否讀取 `explainer-figure/SKILL.md`，或回應中是否出現它的規則（例如 720 寬的網格、圖說明單）。

**驗收條件：**
- [x] 5 個提示的結果已記錄（〈結果〉T4）
- [x] 觸發 0 次；若有觸發，記錄情況並在 T10 一併改寫 explainer-figure 的 description 或隱藏方式，再請使用者重測

**相依：** 無　**檔案：** 本計畫檔　**規模：** S

#### T14 具象基準測試（使用者手動）

**說明：** 在 T15 修改規則前，記錄目前的 skill 與不用 skill 時，架構圖中有幾個節點畫成物件。使用與 T4 相同的模型，每個提示開一個新 session：

| # | 提示 |
|---|---|
| a | 用 SVG 畫一張 Web app 的架構圖：瀏覽器、API server、資料庫、快取。 |
| b | 用 explainer-page 做一頁說明一般 Web app 架構的頁面，包含一張架構圖：瀏覽器、API server、資料庫、快取。 |

**判讀：** 每張架構圖中，畫成物件的節點數、方框加圖示的節點數、純方框的節點數。

**驗收條件：**
- [x] (a)、(b) 的產物與 session 紀錄已記錄在〈結果〉
- [x] (b) 的產物保留，供 T17 並排比較（`temp/round-05/web-app-architecture-b.html`）

**相依：** 無　**檔案：** 本計畫檔　**規模：** S

#### 檢查點 0

- [x] 使用者判讀 T1 的 emoji 與自繪物件並排截圖 —— 2026-10-10：不採用彩色或單色 Noto Emoji，也不採用其他插圖庫；圖中的物件一律自繪（規格 R4 取消）
- [x] 使用者判讀 T2 的試畫結果與參數 —— 2026-10-10：外框 4px；人體採單一外輪廓；P5 改為每步一個姿態加淡色軌跡
- [x] T3 的準確度達到 V4；誤報需要的排除規則已確定（重畫文字、`<use>` 改用點擊測試）
- [x] T4 的結果已記錄 —— 2026-10-12：觸發 0 次，T10 取消
- [x] T14 的結果已記錄 —— 2026-10-13：見〈結果〉T14
- [x] 若任何一項不通過，先更新規格，再進入第 1 階段 —— 規格已於 2026-10-10 修訂（R2、R3、R4 與相關段落），2026-10-12 再依外部 skill 調查修訂（R3、R6、R7 與相關段落）

### 第 1 階段：符號對照規則（R1）

#### T5 符號對照規則

**說明：** 依規格 R1 加入公式符號的上色與圖上的符號標註。

**驗收條件：**
- [x] `template.html` 新增 `.sym`（或實作時確定的名稱），只使用 `--cc`
- [x] `explainer-figure/SKILL.md` 圖說明單加入 Symbols 欄
- [x] `svg-recipes.md` 加入符號標註的寫法：Unicode 下標、`<tspan>` 的退路、上色範圍（最多 5 個）
- [x] `writing-rules.md` § Ground the symbols 加一行，指向 explainer-figure
- [x] 在模板示範內容中放一個上色符號，截圖確認組合字元（x̂）在 SVG 與 HTML 中都正確顯示

**驗證：**
- [x] `CLAUDE.md` 的模板驗證指令全部通過（外部資源、兩種寬度）
- [x] 對比檢查不印出任何內容
- [x] `wc -l skills/explainer-figure/SKILL.md` 不超過約 130

**相依：** 檢查點 0　**檔案：** `template.html`、`explainer-figure/SKILL.md`、`svg-recipes.md`、`writing-rules.md`　**規模：** M

#### 檢查點 A

- [x] 使用者確認 T5 的示範截圖（組合字元 x̂ 在 SVG 與 HTML 中都正確顯示）
- [x] 提供 `git add` 範圍與提交訊息

### 第 2 階段：繪圖基礎（R2、R3、R6、R7）

#### T7 壓線檢查進入 skill

**說明：** 把 T3 的原型整理成 `scripts/check-overlap.js`，並在 Self-check 加入執行指令。

**驗收條件：**
- [x] `skills/explainer-figure/scripts/check-overlap.js` 支援 `data-touch` 排除
- [x] `explainer-figure/SKILL.md` § Self-check 加入執行指令，指令中的腳本路徑從 skill 根目錄寫起
- [x] 指令已實際執行一次

**驗證：**
- [x] V4 的兩個條件仍成立
- [x] `wc -l skills/explainer-figure/SKILL.md` 不超過約 130

**相依：** 檢查點 0　**檔案：** `scripts/check-overlap.js`（新增）、`explainer-figure/SKILL.md`　**規模：** S

#### T8 風格規範與零件函式庫

**說明：** 依規格 R3，把 T2 的結果寫成 `pictorial.md` 的規範，並建立零件函式庫。

**驗收條件：**
- [x] `skills/explainer-figure/scripts/parts.py`：只使用 Python 3 標準函式庫；以子指令輸出 SVG 片段；依尺寸參數直接輸出幾何，不使用 `scale()`
- [x] 基本形（清單實作時確定）與 3 個組合物件：人體（規格 R3 第 2 點的 4 條）、機器人（不限定俯視，能表示朝向）、無人機（四旋翼）
- [x] 姿態子指令：依軌跡計算每一步的位置與角度，輸出 P5 的 `<use>`
- [x] 零件總覽圖子指令
- [x] `pictorial.md` 加入「粗外框＋平塗色」的規範：線寬 4px、填色、陰影，只使用模板變數
- [x] `pictorial.md` 加入函式庫的用法、背包與車的基本形組合示範、新配方 P5（每步一個姿態、淡色軌跡、組合物件的分離寫法）
- [x] `pictorial.md` 寫明 P5 的 CSS 限制（不加 `svg ` 前綴、不用 `scale()`、P5 物件中不用 `box` 等既有 class）
- [x] `explainer-figure/SKILL.md` 圖型表的具象插圖列提到物件與姿態，指向 P5（不新增列）；加入函式庫的執行指令
- [x] `template.html` 新增需要的 class（不加 `svg ` 前綴）

**驗證：**
- [x] V3：零件總覽圖截圖，外形正確；人體的軀幹與腿之間沒有缺口（放大截圖）；不同尺寸的外框都是 4px
- [x] 同一組參數執行兩次，輸出相同（`diff` 無輸出）
- [x] `SKILL.md` 中的指令已實際執行一次
- [x] 壓線檢查與對比檢查都不印出任何內容
- [x] `CLAUDE.md` 的模板驗證指令全部通過

**相依：** T7　**檔案：** `scripts/parts.py`（新增）、`pictorial.md`、`template.html`、`explainer-figure/SKILL.md`　**規模：** L

#### ~~T9 Noto Emoji 子集~~（2026-10-10 取消）

隨規格 R4 取消。探測結果保留在〈結果〉T1。

#### ~~T10 依 T4 結果處理 explainer-figure 的觸發~~（2026-10-12 取消：T4 觸發 0 次）

**說明：** 原本的「emoji 接入既有規則」隨 R4 取消，只保留 T4 的後續處理。T4 觸發 0 次時，本任務取消。

**驗收條件：**
- [ ] 若 T4 有觸發：改寫 explainer-figure 的 description 或隱藏方式，並請使用者重測，直到觸發 0 次

**驗證：**
- [ ] `wc -l skills/explainer-figure/SKILL.md` 不超過約 130
- [ ] `claude plugin validate .` 通過

**相依：** T4　**檔案：** `explainer-figure/SKILL.md`　**規模：** S

#### T15 節點外觀原則

**說明：** 依規格 R6，把「畫成物件」從圖型層級移到節點層級，並刪改體現舊做法的句子。

**驗收條件：**
- [x] `explainer-figure/SKILL.md` 圖型表後的段落寫入規格 R6 第 1 點
- [x] `pictorial.md` 開頭：圖型依問題選擇、節點外觀依東西決定；風格規範適用於任何圖中的物件；P1–P5 是整張具象插圖的版面配方
- [x] `icons.md` 第 55 行的禁令限縮為「不要在標籤旁假造 Lucide 沒有的小圖示」，並指向 `pictorial.md`
- [x] `svg-recipes.md` Recipe 3：具體元件畫成物件、抽象元件保留方框；附一段可複製的片段，示範兩者並存與箭頭接在外接框的邊上
- [x] 外形依據的規則（規格 R6 第 4 點）寫進 `pictorial.md`
- [x] 不加入元件清單、連線配色、雙向平行箭頭

**驗證：**
- [x] Recipe 3 的片段貼進暫存頁截圖；壓線檢查與對比檢查都不印出任何內容
- [x] `wc -l skills/explainer-figure/SKILL.md` 不超過約 130

**相依：** T8　**檔案：** `explainer-figure/SKILL.md`、`pictorial.md`、`icons.md`、`svg-recipes.md`　**規模：** M

#### T16 意圖檢查

**說明：** 依規格 R7，在 Self-check 加入意圖檢查。

**驗收條件：**
- [x] Self-check 寫明順序：先對照圖說明單的 Message 欄確認意圖，再找缺陷；修正後重新截圖
- [x] 遮住文字的截圖指令（在只看圖的截圖中隱藏圖內的 SVG 文字）
- [x] 與零件總覽圖並排比較的指令
- [x] 放大截圖指令（`--force-device-scale-factor=4`，截取物件的交接處）

**驗證：**
- [x] V9：3 項指令都在 T15 的 Recipe 3 暫存頁與一個既有範例頁上實際執行一次
- [x] `wc -l skills/explainer-figure/SKILL.md` 不超過約 130；超過時把指令細節移到 references

**相依：** T8、T15　**檔案：** `explainer-figure/SKILL.md`（必要時 `svg-recipes.md` 或 `pictorial.md`）　**規模：** S

#### 檢查點 B

- [x] 使用者判讀零件總覽圖、Recipe 3 片段的截圖與它遮住文字的截圖 —— 2026-10-13：人體的腿外緣改為與軀幹切齊，其餘通過（〈結果〉檢查點 B）
- [x] 提供 `git add` 範圍與提交訊息

### 第 3 階段：驗證案例

#### T6 EKF 頁 v2（V1）

**說明：** 以 T5 的符號規則、T8 的零件函式庫與 T15 的節點外觀，改版 EKF 頁的圖 3 與公式段落。原頁不覆寫，新版另存為同目錄下的另一個檔案，只放在本機。

**驗收條件：**
- [x] 圖 3 每一幀都標出該步出現的符號（x̂ₖ、Pₖ、zₖ、Kₖ 等），關鍵概念的符號與公式同色（沿用原頁的記號 μ、P、z、K、y，見〈結果〉T6）
- [x] 機器人以零件函式庫畫成有朝向的物件，不再只是一個點
- [x] 公式段落中的符號使用 `.sym` 上色，與圖一致
- [x] 與原版並排截圖

**驗證：**
- [x] `explainer-page/SKILL.md` 第 6 步的自檢全部通過
- [x] 壓線檢查（T7）不印出任何內容；意圖檢查（T16）的 3 項都已執行

**相依：** T5、T8、T15、T16　**檔案：** 本機的 EKF 新版頁面、本計畫檔　**規模：** M

#### T11 Starship 圖 4：發射到接回的 8 步姿態圖（V2）

**說明：** 以 P5 與零件函式庫的姿態子指令重畫 `examples/starship-reusability/starship-reusability.html` 的圖 4，以檢查點 0 第二輪的 8 步草圖為底（使用者 2026-10-08 建議從發射畫起）。先在暫存副本中完成，等檢查點 C 由使用者決定是否取代範例。

**驗收條件：**
- [x] 飛船與助推器畫成物件；第 1–2 步兩者組合，第 3 步分離，之後只畫助推器
- [x] 飛船與助推器的外形依代理查得的資料畫出辨識特徵（例如高度與直徑的比例、格柵翼、襟翼、引擎），以基本形組合，不使用通用的火箭外形；回報列出依據與來源
- [x] L2 stepper ≤ 8 步，每一幀只顯示當下的姿態，軌跡以淡色虛線常駐；分離、「翻轉」與「折返」看得出來
- [x] 修正草圖的問題：姿態座標從軌跡算出、火焰不伸到地面以下、加上發射台
- [x] 範例頁的段落與圖說依新的 8 步改寫
- [x] 與原版並排截圖

**驗證：** 壓線檢查、意圖檢查與 `explainer-page/SKILL.md` 第 6 步的自檢都通過。（2026-10-13 通過）

**相依：** T8、T15、T16　**檔案：** 暫存副本、本計畫檔　**規模：** M

#### T17 節點外觀重測（使用者手動，V8）

**說明：** T15、T16 完成後，使用者在 Codex 中以 T14 (b) 的提示重測，模型與 T14 相同。

**驗收條件：**
- [ ] 架構圖中的具體元件畫成物件，抽象元件維持方框
- [ ] 產物通過全部自檢
- [ ] 與 T14 (b) 並排截圖，結果記錄在〈結果〉
- [ ] 範例頁中以抽象概念為主的機制圖（例如因果鏈）不受影響

**相依：** T14、T15、T16　**檔案：** 本計畫檔　**規模：** S

#### T18 P1–P4 改用物件風格

**說明：** `pictorial.md` § Drawn objects 規定圖中的每個物件都用 4px 的 `ink` 風格，但〈Rules for every pictorial figure〉與 P1–P4 的範例片段仍規定物件外框用 2px 的 `outline`、部件用 `box`。兩者矛盾，代理依 P1–P4 畫出的圖會與 P5 和節點物件不一致。本任務依規格 R3 第 5 點，讓 P1–P4 改用同一種風格。（2026-10-13 檢查點 C 新增）

**驗收條件：**
- [x] 決定剖開容器的寫法：外框、裁切後的分層、分層的概念色各用哪個 class；寫進〈Rules for every pictorial figure〉，取代 `outline` 那一條
- [x] P1、P1 變化、P2、P3、P4 的範例片段改用 `ink` 系列；組合物件（P2 的人）改用 `parts.py`，其餘以基本形組合
- [x] 決定模板中 `outline`、`edge`、`shape` 等舊 class 是否保留，並寫明理由（範例頁各自內嵌 CSS，移除不會影響它們）
- [x] 列出其他範例頁中受影響的圖（例如 `llm-wiki` 圖 4 中以方框表示的「You」），交使用者決定是否重畫；本任務不修改它們

**驗證：**
- [x] 每個片段貼進模板暫存頁截圖；壓線檢查、對比檢查都不印出任何內容；與零件總覽圖並排
- [x] 文件中新增或修改的指令都實際執行一次
- [x] `wc -l skills/explainer-figure/SKILL.md` 不超過約 130；`CLAUDE.md` 的模板驗證指令全部通過（若修改模板）

**相依：** T15　**檔案：** `pictorial.md`（必要時 `template.html`、`SKILL.md`）　**規模：** M

#### T19 Starship 範例全頁依新規則重畫

**說明：** 使用者同意以 T11 的圖 4 取代範例，條件是範例頁的所有圖都依新規則重畫，讓同一頁的圖風格一致。（2026-10-13 檢查點 C 新增）

**驗收條件：**
- [ ] 逐圖判斷並記錄：圖 1（因果鏈，節點是抽象概念）與圖 6（歸納卡）依 R6 保留，不重畫
- [ ] 圖 2（質量分布）依 T18 的 P1 寫法重畫
- [ ] 圖 3（兩節堆疊）重用圖 4 的飛船與助推器物件，以引線標註部位；高度維持按比例
- [ ] 圖 4 使用 T11 的版本
- [ ] 圖 5 下半（飛船回收 4 步）依使用者的決定：保留方框，或改為飛船的 P5 姿態圖
- [ ] 飛船與助推器在圖 2–5 中外形一致（同一組定義、同一個比例）
- [ ] 段落、圖說與來源行依新圖改寫
- [ ] 與原版並排截圖；使用者判讀後才寫回 `examples/`

**驗證：**
- [ ] `explainer-page/SKILL.md` 第 6 步的自檢、壓線檢查、意圖檢查、圖示同步都通過
- [ ] 寫回 `examples/` 後，7 個範例頁的壓線檢查仍不印出任何內容

**相依：** T11、T18　**檔案：** `examples/starship-reusability/starship-reusability.html`（寫回時）、暫存副本、本計畫檔　**規模：** M

#### 檢查點 C

- [x] 使用者並排判讀 EKF 新舊版，確認公式更容易對應到圖 —— 2026-10-13：圖 3 使用零件函式庫可以接受；另提出例子段落加圖的建議（〈結果〉檢查點 C）
- [ ] 使用者判讀 Starship 圖 4 新舊版，決定是否取代範例（取代時把暫存副本的圖 4 寫回範例，並重跑自檢）—— 2026-10-13：流程通過；軌跡改為隨步驟累積（P5 規則與 `pose` 一併修改）；同意取代，條件是範例頁的所有圖都依新規則重畫（新增 T18、T19）
- [ ] 使用者判讀 T17 與 T14 的對照
- [ ] 使用者判讀 T19 的全頁新舊版
- [ ] 提供 `git add` 範圍與提交訊息

### 第 4 階段：驗收與收尾

#### T12 新主題頁（V7）

**說明：** 使用者在本任務開始前指定主題。以新規則產出 1 頁，用到符號對照、自繪物件（含姿態）與節點外觀。

**驗收條件：**
- [ ] 使用者已指定主題
- [ ] 頁面用到 R1、R3、R6，並執行 R7 的意圖檢查
- [ ] 回報時列出每張圖用到的規則

**驗證：**
- [ ] `explainer-page/SKILL.md` 第 6 步的自檢、壓線檢查、意圖檢查、圖示同步指令都通過
- [ ] 使用者判讀

**相依：** T6、T11、T17　**檔案：** 本機頁面、本計畫檔　**規模：** M

#### T13 版本與文件

**說明：** 升版並更新說明文件。

**驗收條件：**
- [ ] 四個 manifest 檔升為 0.5.0
- [ ] `CLAUDE.md`〈架構〉加入 `scripts/check-overlap.js` 與 `scripts/parts.py`
- [ ] `README.md`、`README.zh-TW.md` 提到符號對照、物件姿態圖與節點外觀（只寫現況，不引用計畫文件）
- [ ] 構想文件〈Key Assumptions to Validate〉與規格〈待驗證的假設〉依結果勾選
- [ ] `docs/plan/README.md` 第 05 列的版本與狀態

**驗證：**
- [ ] `CLAUDE.md`〈驗證指令〉全部執行並通過
- [ ] `claude --plugin-dir . plugin details explain-as-webpage` 確認兩個 skill 都載入

**相依：** T12　**檔案：** manifest（4 個）、`CLAUDE.md`、README（2 個）、構想與規格文件、索引　**規模：** M

#### 檢查點 D

- [ ] 規格〈7. 成功條件〉全部達成
- [ ] 提供最終的 `git add` 範圍與提交訊息

## Risks and Mitigations

| 風險 | 影響 | 處理方式 |
|---|---|---|
| ~~emoji 的漸層放在共用的隱藏 `<svg>` 中時不顯示~~ | — | T1 確認不會發生；R4 已取消 |
| ~~Noto Emoji 的風格與粗外框不搭~~ | — | 檢查點 0 判讀後成立，R4 已取消 |
| 外形複雜的有機物件（器官、地球）沒有來源 | 中 | 不以手寫座標描繪；改用簡單形狀的示意、Lucide 圖示標在標籤旁，或留給下一輪的 explainer-cite |
| 探測程式隨暫存目錄消失 | 低 | T7 依〈結果〉T3 的記錄重寫，並重跑 V4 的兩個條件 |
| 壓線檢查誤報太多，代理不採信 | 中 | T3 以 V4 作為門檻；以 `data-touch` 排除本來就應接觸的元素 |
| SVG 文字中的組合字元（x̂）顯示錯位 | 低 | T5 截圖確認；錯位時改用 `<tspan>` 疊加符號 |
| `explainer-figure/SKILL.md` 超過約 130 行 | 中 | 細節放進 references；每個修改它的任務都量測行數；超過時先移出意圖檢查的指令細節 |
| 零件函式庫的輸出不夠好看或不夠彈性 | 中 | 零件總覽圖在檢查點 B 由使用者判讀；函式提供尺寸、角度與概念色參數 |
| 代理不用函式庫，仍手寫物件座標 | 中 | `SKILL.md` 放執行指令；T17 與 T12 的回報列出每張圖用到的規則，檢查是否使用函式庫 |
| R6 被過度套用，抽象概念也畫成裝飾性的物件 | 中 | R6 第 1 點規定抽象概念與同類節點用方框；V8 檢查範例頁中以抽象概念為主的機制圖 |
| 代理查不到 Starship 外形的可靠資料 | 低 | 依 `sources-and-research.md` 請使用者提供資料；回報列出依據與來源 |
| 一頁的上色符號超過 5 個 | 低 | R1 規定只有關鍵概念的符號上色，其餘只標註 |

## Open Questions

- 驗收用的新主題：使用者在 T12 開始前指定。
- Starship 圖 5 下半（飛船回收 4 步）保留方框，或改為 P5 姿態圖：T19 開始前由使用者決定。
- 其他範例頁（`llm-wiki`、`autoresearch`、`explain-as-webpage`）是否依新規則重畫：T18 列出受影響的圖後，由使用者決定放在第 4 階段或第 6 輪。
- ~~`.sym` 的正式名稱~~：T5 確定為 `.sym`（2026-10-13）。~~風格 class 的名稱~~：T8 確定為 `ink` 系列（2026-10-13）。
- ~~零件函式庫的子指令名稱、基本形清單，以及機器人與無人機的視角參數~~：T8 確定（見〈結果〉T8）。

## 結果

各任務完成後，在此依任務編號記錄探測數據、截圖路徑、判讀結果與規則的調整。

探測檔案都在當時 session 的暫存目錄（下稱 `$SCRATCH`），不進儲存庫。暫存目錄可能在 session 結束後被清除；T7 與 T9 要用到的兩支程式（`$SCRATCH/t3/check-overlap.js`、`$SCRATCH/tools/noto2symbol.py`）若已不存在，依下列記錄重寫。

### T1 Noto Emoji 探測（2026-10-08）

> 2026-10-10：檢查點 0 判讀後決定不採用 Noto Emoji（規格 R4 取消），本節保留作為技術記錄。

**結論：Noto Emoji 可以採用。SVG 圖檔的授權允許內嵌與重新散布；放在共用的隱藏 `<svg>` 中時，漸層在三種截圖中都正常顯示；一頁放 5 個 emoji 的增量為 15–49 KB。**

**授權。** 儲存庫有兩份授權，適用範圍不同：

| 檔案 | 授權 | 適用範圍 |
|---|---|---|
| 根目錄 `LICENSE` | SIL OFL 1.1（2024-07-29 由 Apache 2.0 改為 OFL，commit `254596e5`） | 字型 |
| `2D/svg/LICENSE` | Apache License 2.0（Copyright 2013 Google, Inc.） | 本輪使用的 SVG 圖檔 |

`README.md` 寫「圖檔採 Apache 2.0，見 ./LICENSE」，但根目錄的 `LICENSE` 已改為 OFL，兩者不一致；SVG 資料夾自己的 `LICENSE` 明確是 Apache 2.0，以它為準。Apache 2.0 的條件與本輪的對應做法：

- 重新散布時附上授權全文 → `assets/emoji/LICENSE` 放 Apache 2.0 全文。
- 修改過的檔案要明確標示已修改 → 本輪會移除 Illustrator 資料、縮短數字、改寫 id，所以 `noto.svg` 開頭的聲明要寫出「已轉換與修改」及修改內容。頁面的 emoji 區塊比照 Lucide，也複製這段聲明。
- 根目錄沒有 `NOTICE` 檔，不需要另外附 NOTICE。

**發行版。** 選定 `v2026-09-24-unicode18_0`（2026-09-24 發布，Unicode 18.0），圖檔路徑為 `2D/svg/emoji_u<碼位>.svg`，共 3,751 個檔案。前一版是 `v2.051`（2025-09-15）。

**候選物件與覆蓋率。** 依 7 個範例頁、EKF 頁、使用者其他頁面（避難包、甲狀腺、Unity）與構想文件的候選主題（Motion Planning、人體）列出 42 個「只需要辨識」的物件，Noto 有其中 39 個。大小為轉換後的位元組數（KB），`*` 表示內含漸層：

| 主題 | 物件 |
|---|---|
| starship | `rocket` U+1F680 9.3*、`satellite` U+1F6F0 4.7、`earth` U+1F30F 11.3*、`sun` U+2600 1.8、`moon` U+1F319 0.7、`fire` U+1F525 1.7*、`fuel-pump` U+26FD 2.6 |
| motion-planning | `car` U+1F697 2.8、`world-map` U+1F5FA 12.6、`mountain` U+26F0 5.3 |
| ekf | `robot` U+1F916 4.9*、`compass` U+1F9ED 3.0、`antenna` U+1F4E1 2.5、`pushpin` U+1F4CD 0.7、`camera` U+1F4F7 3.3 |
| body | `brain` U+1F9E0 8.5、`heart` U+1FAC0 4.0、`lungs` U+1FAC1 4.9*、`bone` U+1F9B4 2.7、`blood` U+1FA78 0.4、`microbe` U+1F9A0 6.1 |
| thyroid | `pill` U+1F48A 0.6 |
| go-bag | `backpack` U+1F392 5.1、`flashlight` U+1F526 2.0、`droplet` U+1F4A7 0.5、`radio` U+1F4FB 3.5、`battery` U+1F50B 2.0、`canned-food` U+1F96B 1.9、`bandage` U+1FA79 4.0、`house` U+1F3E0 2.9、`tent` U+26FA 1.4、`phone` U+1F4F1 3.6 |
| user-ref | `tree` U+1F333 1.4 |
| llm-wiki | `cloud` U+2601 0.8、`books` U+1F4DA 4.3、`laptop` U+1F4BB 6.2*、`light-bulb` U+1F4A1 3.5、`person` U+1F9D1 7.5* |
| unity | `bird` U+1F426 1.5 |

- Noto 沒有的 3 個：胃、甲狀腺、哨子。Unicode 18.0 的 `emoji-test.txt` 中也沒有這三個 emoji，所以任何 emoji 庫都不會有。它們留給 explainer-cite。
- 俯視機器人、俯視車與 Starship 助推器需要擺姿態，不屬於「只需要辨識」，由 T2 的自繪物件負責。Noto 的 `robot` 是機器人的臉，`car` 是側面，都不能代替俯視圖。
- 39 個中有 26 個與 Lucide 圖示同名或同義（例如 `rocket`、`backpack`、`heart`）。T9 的 `emoji.md` 要寫出兩者的分工：圖示標在標籤旁，emoji 代表圖中的物件本身。

**大小。** 原始 SVG 中有 6 個超過 45 KB（`rocket` 87 KB、`world-map` 99 KB），原因是 Illustrator 的私有資料 `<i:aipgf>`。轉換程式 `$SCRATCH/tools/noto2symbol.py` 做 5 件事：移除非 SVG 命名空間的元素與屬性、註解與沒有被引用的 id；把 `style` 屬性展開為屬性；數字四捨五入到小數 1 位；被引用的 id 依序改為 `e-<name>-g1`、`g2`…；每個 emoji 輸出成一行 `<symbol id="e-<name>" viewBox="0 0 128 128">`。轉換後 39 個合計 146,407 B，中位數 3.05 KB，最大是 `world-map` 12.6 KB。

- 一頁放 5 個中位數大小的 emoji 約增加 15 KB；放最大的 5 個（`person`、`brain`、`rocket`、`earth`、`world-map`）增加 49 KB。最大的範例頁 53 KB 加上 49 KB 為 102 KB，仍低於 150 KB。
- 候選的原始 SVG 中沒有 `<style>`、`class` 或 `href`，所以內嵌時不會把 CSS 規則帶進頁面。

**一致性與 id 衝突。** 39 個轉換後的 symbol 與原檔並排截圖（64px），外觀沒有可見差異：`$SCRATCH/work/t1-fidelity.png`。在模板副本中放入 5 個含漸層的 emoji（`rocket`、`earth`、`fire`、`robot`、`person`），頁面中沒有重複的 id。

**共用的隱藏 `<svg>`。** emoji 放在模板的共用隱藏 `<svg><defs>` 中（新增 `<!-- emoji:start -->`），在整頁截圖、只看圖截圖、單圖截圖三種情況下，漸層都正常顯示：`$SCRATCH/work/t1-shared-full-crop.png`、`t1-shared-figures.png`、`t1-shared-frame.png`。所以不需要改為逐圖內嵌，規格〈待驗證的假設〉第 2 項成立。`pictorial.md` 記錄的 `clipPath` 失效問題沒有在漸層上出現；三種截圖都沒有隱藏共用的 `<svg>`，因為它位於 `.content` 之外。

**與自繪物件並排。** 見 T2 的 `$SCRATCH/work/checkpoint0-emoji-vs-drawn.png`。

### T2 風格試畫（2026-10-08）

**結論：依參數畫出的 5 種物件，3 次的外形一致，沒有歪掉或破損；殘影草圖看得出「翻轉」與「折返」。但試畫發現模板的 CSS 寫法不能直接用於 P5：以 `<use>` 引用的物件中，`svg .x` 形式的規則全部失效。**

**試畫的參數（`$SCRATCH/t2/style.css`、`spec-draft.md`）：**

| 項目 | 參數 |
|---|---|
| 外框 | `stroke: var(--text)`、3px、圓角線端與轉角、`vector-effect: non-scaling-stroke` |
| 填色 | 概念色淺底 `--cb`，沒有概念色時為白色；深色部件（輪子、引擎噴嘴）用 `--text`；玻璃（車窗、光達）用 `--blue-bg` |
| 剪影 | 由多個形狀組成的物件（人）先畫 6px 的 `ink-edge`，再蓋上無外框的填色，只留外輪廓 |
| 陰影 | 主體形狀再畫一次，`--cc` 不透明度 18%，以圖自己 `<defs>` 中的 `clipPath` 裁到背光側（光源在左上；正面圖陰影在右側，朝 +x 的俯視圖與側視圖在 +y 側） |
| 朝向 | 有方向的物件朝 +x 畫，原點在中心，以 `translate()` 與 `rotate()` 擺放 |
| 殘影 | 目前姿態正常顯示，先前的姿態 `opacity: .3`；stepper 用 `data-step="k"` 顯示實色、`data-step="k+1+"` 顯示殘影 |

**每種物件的 3 次（`$SCRATCH/work/checkpoint0-objects.png`）：** run a 直接寫在圖中；run b 換概念色，機器人、車、火箭改以 `<use>` 引用；run c 再加上旋轉（背包 −12°、機器人 −35°、車 20°、火箭 −90°），人則縮小為 0.7 倍。3 次的外形一致。

**限制：** 3 次都由同一個代理在同一個 session 中依同一組數字畫出，所以這項結果證明的是「依配方的座標畫，外形穩定」，不證明「只依文字規則、沒有配方片段時也穩定」。T8 因此要為 5 種物件都附上可直接複製的片段。

**試畫中發現的問題與對 T8 的影響：**

1. **`svg .x` 選擇器在 `<use>` 引用的內容中失效。** 第一次截圖中，以 `<use>` 引用的機器人、車、火箭、助推器全部變成黑色，火焰的 `box warn` 也變成黑色。原因是 Chrome 在 `<use>` 的 shadow tree 中比對選擇器時，複製出來的元素沒有 `svg` 祖先，所以模板中所有 `svg .box`、`svg .line` 等規則都不會套用。把試畫的規則改為不加 `svg ` 前綴（`.ink`、`.shade`）後恢復正常。影響：P5 的物件定義只能使用不加前綴的 class；T8 在模板新增的風格 class 都不加 `svg ` 前綴，`pictorial.md` 要寫明「P5 物件中不可使用 `box`、`line` 等既有 class」。
2. **後代選擇器跨不進 `<use>`。** `.mid .ink` 這類規則同樣失效，只有可繼承的屬性與 CSS 自訂屬性能傳進去。變化（例如填色深淺）要以自訂屬性傳遞，並與概念色 class 放在同一個元素上；`--ink-fill: var(--cc)` 若放在外層，會在概念色設定前就被解析成預設值。
3. **`scale()` 會讓外框變細。** 人縮小為 0.7 倍時，3px 的外框變成 2.1px。加上 `vector-effect: non-scaling-stroke` 後線寬維持 3px。規則二選一：禁止 `scale()`，或在風格 class 上加 `vector-effect`；試畫採用後者。
4. **殘影的版面要避開路徑與其他姿態。** 草圖第一版中，姿態 4 疊在姿態 1 上，上升軌跡穿過姿態 4；調整座標後解決（`$SCRATCH/work/checkpoint0-booster-frame3.png`、`checkpoint0-booster-frame5.png`）。第五幀中，上升軌跡的起點仍從姿態 5 後方經過，留到 T11 修正。壓線檢查只檢查文字，抓不到「線穿過物件」與「物件疊在物件上」，這兩種要靠截圖判讀。

**填色深淺的比較（`$SCRATCH/work/checkpoint0-emoji-vs-drawn.png`）：** 淺底（`--cb`）與 emoji 的飽和色並排時對比明顯；中等填色（`--cc` 不透明度 45%）較接近 emoji 的色彩量。由檢查點 0 決定採用哪一種。

### T3 壓線檢查原型（2026-10-08）

**結論：原型符合 V4。7 個重建缺陷全部抓到；在 7 個範例頁與 EKF 頁上，加入 1 條排除規則後沒有任何回報。每頁執行約 0.6 秒。**

**原型（`$SCRATCH/t3/check-overlap.js`，128 行；執行器 `$SCRATCH/t3/run.sh`）：**

- 執行器把腳本插在頁面最後一個 `</body>` 前，存成暫存檔，以 `google-chrome --headless=new --window-size=1280,1000 --virtual-time-budget=5000 --dump-dom` 開啟，再從 `<pre id="overlap-report">` 取出報告。暫存檔路徑必須是絕對路徑：第一版用相對路徑組出 `file://./…`，Chrome 開不了頁面，報告顯示為空。
- 每個 `<figure>` 的 SVG 分別檢查；stepper 先退回第 1 幀，再逐幀按 ▶，每幀只檢查可見的元素。同一個問題在後續幀重複出現時只回報一次。
- 3 個類別：`text-overlap`（兩個文字框重疊，文字框各內縮 1px）、`line-through-text`（每隔 2 個螢幕像素沿外框取樣，取樣點落在文字框內）、`text-on-edge`（在文字框上取 5 × 3 個點，以 `isPointInFill` 判斷，部分在填色內、部分在外）。
- `<use>`（圖示、emoji、P5 物件）的內容在 shadow tree 中，無法逐一取得形狀，改用 `document.elementsFromPoint` 對同樣的 15 個點做點擊測試。第一版以 `<use>` 的外框判斷，在旋轉 −35° 的機器人與旋轉 20° 的車下方的標籤上各誤報 1 次（軸對齊的外框比物件大）；改為點擊測試後消失。
- 加上 `data-touch` 的元素（或它的祖先有 `data-touch`）不參與類別 2、3。
- 輸出格式：`fig-5 line-through-text: "bird.png" × path.line.dash M60 316 H480 …`；stepper 的問題在圖號後加 `[frame k]`。全部通過時不印出任何內容。

**重建缺陷。** 第 4 輪修正前的頁面沒有留存，所以從 `pictorial.md` 的 5 個配方片段（P1 背包、P1 變化、P2 人體、P3 罐子、P4 Unity 編輯器，前述缺陷所在的圖修正後的版本）建立乾淨頁面，再一次放入一個缺陷：

| # | 缺陷 | 放入方式 | 回報 |
|---|---|---|---|
| D1 | 「側袋」標籤壓到包身 | `pocket` 標籤移到包身左緣（x = 140） | 抓到：`line-through-text` 與 `text-on-edge` 共 5 行（側袋、底層、包身外框） |
| D2 | 虛線箭頭穿過標籤 | `split the 60%` 下移到虛線上 | 抓到：`line-through-text` |
| D3 | `sm` 標籤壓到長條左緣 | `≈ 40% of weight` 的中心移到 x = 450 | 抓到：`line-through-text`、`text-on-edge` |
| D4 | 拖曳箭頭穿過檔名 | 拖曳箭頭的起點上移到 y = 316 | 抓到：`bird.png` 與箭頭標籤各 1 行 |
| D5 | 箭頭穿過欄位名 | 箭頭終點延伸穿過 `Sprite: bird` | 抓到：`line-through-text` |
| D6 | 註解與引線重疊 | P3 的一則註解左移到引線上 | 抓到：`line-through-text` |
| D7 | 文字重疊（人工） | 在 P4 加一個與既有標籤重疊的文字 | 抓到：`text-overlap` |

乾淨頁面沒有任何回報。另外兩項正向測試：文字放在 `<use>` 機器人的邊緣時回報 `text-on-edge`；D6 的引線加上 `data-touch` 後不再回報。

**範例頁上的回報與排除規則。** 在 7 個範例頁、EKF 頁、預設輸出目錄中另外 23 個頁面與 T2 試畫頁上執行：

| 回報 | 判讀 | 處理 |
|---|---|---|
| `llm-wiki.html` 圖 2 第 3 幀：`"概念 X" × text "概念 X"`（使用者的 3 個 llm-wiki 版本也有） | 誤報：第 3 步把同一個框與文字在相同座標重畫一次，畫面上看不出差異 | 排除規則：內容相同、位置相差小於 1px 的兩個文字視為重畫，不回報 |
| T2 試畫頁圖 3、圖 4：旋轉物件下方的標籤 × `<use>` | 誤報：軸對齊外框比物件大 | 改用點擊測試（見上） |

加入上述兩項修改後，所有頁面都沒有回報。

**執行時間：** 每頁 0.54–0.68 秒（含啟動 Chrome）。

**規格 R2 的補充（T7 實作時寫進 skill）：**

- 排除規則除了 `data-touch`，再加上「重畫的相同文字」。
- 類別 3 對 `<use>` 改用點擊測試。
- 檢查範圍只有文字。線穿過物件、物件疊在物件上（T2 殘影草圖中的情況）仍要靠截圖判讀，與 R2 第 7 點的「不檢查」並列。

### 檢查點 0 第一次判讀與第二輪試畫（2026-10-08）

**使用者回饋（2026-10-08）：**

1. 使用者在 Google Fonts 看到的 Noto Emoji 是單色線框的字型版，以為本輪採用的是這種風格；第一輪對照圖用的是彩色版，兩者差很多。使用者偏好自繪的「粗外框＋平塗色」。
2. 外框可以再粗一點。人體要改進：手臂向外傾斜約 25°；下肢與軀幹的連接處不可出現兩段圓弧相交的缺口。使用者附上自己的草圖（`temp/round-05/Screenshot from 2026-10-08 15-53-19.png`）：頭是圓，軀幹是肩膀圓角的矩形，手臂與腿是藥丸形，全身高約 5 個頭徑。
3. 畫出助推器本身有幫助，但殘影會干擾。建議在姿態變化大的段落多加中間步驟；並評估能否從「飛船在助推器頂端」的發射開始，畫到飛船分離、助推器返回。
4. 詢問 T4 的提示詞為什麼都沒有指定 explainer-figure。
5. 請評估 Iconoir 與 Flaticon UIcons 兩個圖示庫。

**單色 Noto Emoji（字型版）。** 它不在 `googlefonts/noto-emoji` 儲存庫中，而是 `google/fonts` 的 `ofl/notoemoji/NotoEmoji[wght].ttf`（Version 3.002，可變字重 300–700，1,891 個字形，上游為 `googlefonts/emoji-bw`）。授權是 SIL OFL 1.1，沒有 Reserved Font Name。T1 的 39 個候選全部都有。以 fontTools 取出字形輪廓轉成 `<symbol>` 可行，每個約 1.3–13 KB。它是單色線稿：可以用文字色或概念色上色，但內部沒有獨立的填色區塊，無法做成「粗外框＋平塗色」。

**另外兩個圖示庫：**

| 圖示庫 | 授權 | 內容 | 結論 |
|---|---|---|---|
| Iconoir v7.12.1 | MIT | 1,383 個 regular（24×24、線寬 1.5）與 288 個 solid | 與 Lucide 同一類線條圖示。對本輪的候選物件，它沒有背包、手電筒、衛星、骨頭、帳篷、藥丸、肺、機器人，覆蓋率低於 Lucide。不採用：與 Lucide 混用違反 `icons.md`「只用一套」的規則，取代 Lucide 也沒有收益 |
| Flaticon UIcons | Flaticon License（非開放授權） | 4,000+ 個 | 不採用：授權為「不可轉讓、可撤銷」，免費使用必須在每個使用處標示出處；把圖檔放進本儲存庫再散布給其他使用者，不符合這些條件 |

**人體（`$SCRATCH/work/checkpoint0-r2-objects.png` 圖 1）。** 依使用者草圖重做，高 150 = 5 個頭徑：

- 頭：圓，r = 14，圓心 y = −61。頭與軀幹相距 11px。4px 外框在剪影外各占 4px，間距小於 8px 時，頭會與軀幹黏在一起。
- 軀幹：寬 40，上緣兩角為 r = 10 的圓角，下緣是直角，所以不會與腿形成圓弧缺口。
- 手臂：寬 12 的藥丸形，從肩點 (±15, −29) 向外傾斜 25°。
- 腿：寬 13，上緣平直並伸進軀幹 6px，只有下端是半圓。
- 兩種畫法：A 先畫 8px 的外框再蓋上填色，只留整體外輪廓；B 每個部件各有外框，手臂疊在軀幹上。A 的外形接近使用者草圖右側的剪影；B 在肩膀處出現手臂外框橫過軀幹的線。

**外框粗細（圖 2）。** 同一個背包以 3、4、5px 並排。5px 時，小部件（扣環、口袋縫線）開始擠在一起。建議採用 4px。

**`vector-effect` 不會傳進 `<use>`。** 圖 5 中縮小為 0.45 倍的人體，外框比其他物件細。原因是剪影的 class 加在 `<use>` 上，而 `vector-effect` 不是可繼承的屬性，`<use>` 內部的形狀仍隨 `scale()` 縮小線寬。結論：P5 規則改為「不使用 `scale()`，物件直接畫成需要的大小」；`vector-effect` 只能當作輔助。

**Starship 從發射到接回（`$SCRATCH/work/checkpoint0-r2-starship-8frames.png`）。** 不用殘影，每一幀只顯示當下的姿態，軌跡以淡色虛線表示。結論：可以畫，而且能放進 `writing-rules.md` 的上限（每個 stepper ≤ 8 步）。

| 步 | 內容 |
|---|---|
| 1 | 發射：飛船在助推器頂端，助推器點火 |
| 2 | 上升：整組向東傾斜 |
| 3 | 熱分離：飛船點火離開，助推器關機 |
| 4 | 翻轉：助推器轉向，飛船繼續飛離 |
| 5 | 返回點火：引擎朝東，推力讓助推器往西 |
| 6 | 滑行：沿弧線回到發射塔上方，轉成引擎朝下 |
| 7 | 下降：柵格翼修正方向 |
| 8 | 降落點火：發射塔機械臂在柵格翼下方接住 |

使用者提到的姿態變化大的段落（分離→翻轉→返回點火→下降），在這個版本分成第 3–7 步，每步只轉 50–90°。草圖的問題留到 T11 修正：第 2、3、4、6 步的物件沒有落在軌跡線上（姿態座標是估計值，要改為從軌跡算出）；第 1 步的火焰伸到地面以下；發射時沒有發射台。

**待使用者決定：** 辨識型物件的來源（彩色 Noto Emoji、單色 Noto Emoji 字型、或不使用插圖庫）；人體採 A 或 B；外框粗細；P5 是否把殘影改為「每步一個姿態＋淡色軌跡」。決定後先更新規格，再進入第 1 階段。

### 檢查點 0 的決定（2026-10-10）

使用者的決定：

1. 不使用插圖庫：圖中的物件一律自繪；標籤旁需要小圖示時，仍用 Lucide。
2. 人體採 A（單一外輪廓）。
3. 外框線寬 4px。
4. P5 不使用殘影，改為「每步一個姿態，加上淡色軌跡」。

依此修改的文件：

- 規格：§0 決策、R2（排除重畫文字、`<use>` 點擊測試、不檢查的項目）、R3（4px、人體做法、CSS 限制、不用 `scale()`、P5 改寫、既有「不用圖示」規則維持）、R4 取消、§3 檔案表、V2、V5 取消、V7、§6 邊界、§7 成功條件、§8 不做的事。
- 本計畫：進度總覽、Overview、架構決策第 1、3、4 點與新增第 9、10 點、T8、T9 取消、T10 縮減為 T4 的後續處理、T11 改為發射到接回的 8 步姿態圖、T12、T13、風險表、檢查點 0。

第 0 階段的暫存目錄在 session 結束後已被清空，`check-overlap.js` 與試畫檔案都不在了。T7 依〈結果〉T3 的記錄重寫腳本，並重跑 V4。檢查點 0 剩下 T4（Codex 觸發測試）待使用者執行。

### T4 Codex 觸發測試（2026-10-12）

使用者以 GPT-6.1-Sol（high）在 Codex 中執行 g1–g5，每個提示一個新 session，工作目錄是本儲存庫。產物與對話紀錄沒有保存（2026-10-13 整理參考檔時已不在本機）。

| # | 產物 | 作圖方式 | 讀取的 skill | explainer-figure |
|---|---|---|---|---|
| g1 | `company-sales-jan-jun.svg` | Python 產生 SVG，viewBox 1000×680 | 無 | 未觸發 |
| g2 | `cpu-temperature-10-minutes.svg` | Python 產生 SVG，viewBox 960×560 | 無 | 未觸發 |
| g3 | `web-app-architecture.png` | 內建 `image_gen` 工具，1536×1024 點陣圖，1.2 MB | `imagegen`（Codex 系統 skill） | 未觸發 |
| g4 | `kpi-dashboard.html` | 手寫 HTML，卡片圖示為手繪 24×24 線條 SVG | `frontend-ui-engineering`、`sites`、`git-workflow-and-versioning`、`browser-testing-with-devtools` | 未觸發 |
| g5 | `login-flowchart.png` | 內建 `image_gen` 工具，2149×732 點陣圖，1.1 MB | `imagegen` | 未觸發 |

判讀細節：

- 5 個 session 都沒有讀取 `skills/explainer-figure/SKILL.md`，產物也沒有 720 寬的網格、圖說明單或模板 class。
- g1 的 `rg --files -g '*.svg'` 列出了 `skills/explainer-figure/assets/icons/lucide.svg`。這是檔案搜尋的結果，session 沒有讀取這個檔案。
- g4 讀取了 Codex 自己的記憶檔 `~/.codex/memories/MEMORY.md`。檔中有先前 explainer-page session 的摘要，其中一條是「Explainer SVGs should use a fixed 720px viewBox」。g4 的產物沒有套用這條規則。這是 Codex 的記憶機制，不是本專案 skill 的觸發。
- g3、g5 的提示只說「畫一張」，沒有指定格式，所以 Codex 選擇 `imagegen`。g1、g2 的提示指定 SVG，Codex 就以程式寫出 SVG。

**imagegen 對照（使用者觀察）。** 使用者觀察到：不用本專案的 skill 時，Codex 能畫出具象的架構圖（g3）；指定本專案的 skill 後，這個能力不見了。對照結果：

- g3 的具象效果來自 `image_gen` 工具（點陣圖生成模型），不是 SVG 繪圖能力。`imagegen` 的 skill 內容主要是寫給生成模型的提示格式（Use case、Subject、Text verbatim、Constraints 等欄位）與單一變更的迭代方式，沒有可移植到 SVG 的繪圖規則。它的 description 也寫明圖表與示意圖較適合直接用 SVG 繪製時不要使用它。
- 本專案無法改用點陣圖生成：Claude Code 沒有圖片生成工具，而兩個平台共用同一份 `SKILL.md`；點陣圖的文字無法編輯、翻譯或搜尋，也無法做 stepper、深色模式與壓線檢查；g3、g5 各約 1.1–1.2 MB，超過 150 KB 上限。
- g3 與本專案規則的差距：g3 的每個元件畫成可辨識的物件（瀏覽器視窗、機櫃、資料庫圓柱、堆疊的快取層）；本專案的規則讓架構圖使用方框加上最多 24×24 的 Lucide 圖示，並且禁止以圖示風格手繪圖示（`icons.md`）。最初提議的 3 項個別規則（元件物件清單、連線使用目標元件的顏色、雙向平行箭頭）已撤回；以第一性原理分析的根本原因與外部 skill 調查，見 `docs/plan/05-symbols-pictorial-skill-survey.md`。

### 外部 skill 調查與併入決定（2026-10-12）

調查記錄見 `docs/plan/05-symbols-pictorial-skill-survey.md`。使用者的決定：

1. 吸收 3 項發現：外觀是獨立於圖型的維度、物件的幾何由程式產生、自檢包含意圖檢查；連同保留的「節點層級原則」一起併入本輪。
2. 零件函式庫使用 Python 3。
3. 內建的組合物件為人體、機器人（不限定俯視）、無人機。不做火箭：T11 的 Starship 要依代理能取得的資料畫出實際外形。
4. 同意階段與任務重排：T6 移到第 3 階段，新增 T14–T17。T17（節點外觀重測）是規劃時從 T14 拆出的任務，讓第 0 階段的基準與第 3 階段的重測分開記錄。

依此修改的文件：

- 規格：狀態行、§0 問題陳述與決策、範圍表、R3（零件函式庫）、R5 結果、新增 R6 與 R7、§2、§3、§4、§5（V2、V3、V6、新增 V8 與 V9、待驗證的假設）、§7、§8、§9。
- 本計畫：進度總覽、Overview、架構決策第 1 點與新增第 11–14 點、新增 T14–T17、T6、T8、T11、T12、T13、檢查點 A–D、風險表、待決問題、〈結果〉T4 的對照段落。

### T14 具象基準測試（2026-10-13）

**結論：兩張架構圖都沒有把任何節點畫成物件。不用 skill 的 (a) 是 4 個方框各加一個手繪的線條圖示；用 explainer-page 的 (b) 是 4 個純方框，沒有圖示。目前的規則讓 (b) 的視覺資訊比 (a) 少，這是 T15 要改變的基準。**

使用者以 GPT-6.1-Sol（high）在 Codex 中執行 (a)、(b)，模型與 T4 相同（使用者 2026-10-13 確認；紀錄檔沒有載明模型），每個提示一個新 session，工作目錄是本儲存庫。產物與對話紀錄存於 `temp/round-05/`：

| # | 產物 | 對話紀錄 | 物件 | 方框＋圖示 | 純方框 |
|---|---|---|---|---|---|
| a | `web-app-architecture-a.svg`（1440×800，4.7 KB） | `codex-session-web-app-architecture-a.md` | 0 | 4 | 0 |
| b | `web-app-architecture-b.html`（圖 1，viewBox 720×460；整頁 26 KB） | `codex-session-web-app-architecture-b.md` | 0 | 0 | 4 |

**(a) 不用 skill。** session 沒有讀取本專案的 skill。`rg --files -g '*svg*'` 列出 `svg-recipes.md` 與 `lucide.svg`，但 session 沒有讀取這兩個檔案。每個元件是一張 300×220 的白色圓角卡片，左上角有 64×64 的淡色底塊，底塊內是手繪的 24px 風格線條圖示：瀏覽器視窗、兩層伺服器、閃電（快取）、資料庫圓柱。4 個元件各用一種顏色。提示指定 SVG，所以 Codex 沒有使用 `imagegen`，這與 T4 的 g3 不同。

**(b) 使用 explainer-page。** 讀取順序：`explainer-page/SKILL.md` → `sources-and-research.md` → 一次性確認 → `writing-rules.md` → `explainer-figure/SKILL.md` → `template.html` → `svg-recipes.md`。session 沒有讀取 `pictorial.md` 與 `icons.md`。

- 圖 1 是 Recipe 3 形式的方框圖：4 個 `box` 方框，兩個 `box muted` 分組框（使用者端、伺服器端），沒有圖示，也沒有概念色。
- 確認訊息只寫「一張內嵌 SVG」，沒有寫 `SKILL.md` 第 4 步第 2 項要求的圖型。圖說明單是內部文件，紀錄中看不到。
- 依 `explainer-figure/SKILL.md` 的圖型表，「元件之間的關係」對應機制圖。具象插圖列的條件是「零件在實物、身體或容器中的位置」，不符合本題。所以代理沒有讀取 `pictorial.md`。圖說明單的 Icons 欄寫著「usually none」，所以代理也沒有讀取 `icons.md`。
- 這兩點符合外部 skill 調查的根本原因（`docs/plan/05-symbols-pictorial-skill-survey.md`）：規則把「畫成物件」綁在圖型層級，架構圖選成機制圖後，就不會再考慮節點外觀。
- 其他觀察：session 開始時讀取 Codex 記憶檔 `~/.codex/memories/MEMORY.md` 中先前 explainer-page 工作的摘要。T17 重測時，這份記憶仍會存在，兩次的條件相同。使用者在確認前問過一次「你好像卡住」，與本測試的判讀無關。

**截圖。** 以 Chrome 截取 (a) 全圖與 (b) 圖 1（隱藏圖以外的內容），存於本 session 暫存目錄 `t14/a.png`、`t14/b.png`。暫存目錄被清除後，可從 `temp/round-05/` 的產物重新截取。

### T5 符號對照規則（2026-10-13）

**結論：R1 已寫入 skill。組合字元 x̂（x 加 U+0302）在 SVG 與 HTML 中都正確顯示，所以不需要改用 `<tspan>` 疊加符號。實作時改了一個細節：沒有 Unicode 下標字時，退路 `<tspan>` 不能使用 `class="sm"`。**

修改的檔案：

| 檔案 | 修改 |
|---|---|
| `skills/explainer-page/assets/template.html` | 新增 `.sym { color: var(--cc); fill: var(--cc); }`，同一個 class 用在 HTML 的 `<span>` 與 SVG 的 `<tspan>`；概念色的 CSS 註解加上 `.sym`；示範內容：Q1 段落加入 `<span class="sym c1">x̂<sub>k</sub></span>`，圖 2 第 1 步的標籤改為 `<tspan class="sym c1">x̂ₖ</tspan> FILL: estimate`（14px，移除 `sm`） |
| `skills/explainer-figure/SKILL.md` | 圖說明單加入 Symbols 欄（111 → 112 行） |
| `skills/explainer-figure/references/svg-recipes.md` | § Colour meaning 下新增 § Symbols：標註位置、14px、Unicode 下標與退路、U+0302、上色範圍，以及 3 種寫法的對照表 |
| `skills/explainer-page/references/writing-rules.md` | § Ground the symbols 加一行，指向 svg-recipes.md § Symbols |

**`.sym` 同時設定 `color` 與 `fill` 的原因。** 模板的 `svg text` 規則把 `<text>` 的 `fill` 設為 `--text`，`<tspan>` 繼承的是這個已計算的顏色，所以只在 `<tspan>` 加上 `c1` 不會變色。`.sym` 直接設定 `fill`，在 `<tspan>` 上生效；在 HTML 中則由 `color` 生效。`.sym` 沒有搭配概念 class 時，`var(--cc)` 無效，兩個屬性都退回繼承值，文字維持原本的顏色。

**探測頁（`$SCRATCH` 為 T5 當時 session 的暫存目錄，`t5/t5-zoom.png`，2 倍解析度）：**

- HTML 中的 x̂ₖ、Pₖ、Kₖ（`<sub>`）與只有組合字元的 x̂、ŷ、P̂：帽子都在字母正上方。
- SVG 中的 x̂ₖ（Unicode 下標）、粗體的 x̂ₖ：正確，下標使用 `c1` 的顏色。
- 退路寫法 `P<tspan baseline-shift="sub" font-size="12">k|k−1</tspan>`：位置正確，內層 `<tspan>` 繼承外層的概念色。
- 放在 12px `sm` 標籤中時，Unicode 下標只剩約 7px，難以閱讀。所以規則要求符號標籤使用 14px，模板示範標籤也移除 `sm`。

**對規格 R1 第 2 點的修改。** 原寫法 `<tspan baseline-shift="sub" class="sm">` 中的 `sm` 會把下標設為灰色的 `--muted`，取代概念色。改為巢狀 `<tspan baseline-shift="sub" font-size="12">`。規格已同步修改。

**驗證：**

1. 外部資源：`grep` 沒有輸出。
2. 1280px 截圖：`$SCRATCH/t5/wide.png`。
3. 390px iframe：`<title>ok`，整頁沒有水平溢出；截圖 `$SCRATCH/t5/narrow.png`。
4. 對比檢查：沒有輸出。`.sym` 只使用 `--cc`，也就是 `c1`–`c5`。
5. `svg-recipes.md` 對照表的每一列都是 2 欄（`k|k−1` 中的 `|` 已跳脫）。
6. 模板圖 2 與 Q1 段落的截圖：`$SCRATCH/t5/template-demo.png`。

觀察：HTML 段落中的 `<sub>` 讓所在行的行高略增。這是瀏覽器的預設行為，本任務沒有修改。

### T7 壓線檢查進入 skill（2026-10-13）

**結論：依〈結果〉T3 的記錄重寫 `check-overlap.js`（128 行），結果與 T3 相同：7 個重建缺陷全部抓到；乾淨頁面、7 個範例頁、預設輸出目錄的 24 個頁面（含 EKF 頁）都沒有回報。**

**腳本與指令。**

- `skills/explainer-figure/scripts/check-overlap.js`：3 個類別、`data-touch` 排除、重畫文字的排除、`<use>` 的點擊測試，都依 T3 的設計。stepper 先按 ◀ 退回第 1 幀，再逐幀按 ▶；每幀檢查前把圖捲進視窗，因為 `elementsFromPoint` 只能測視窗內的點。字型載入後（`document.fonts.ready`）才量測。
- `SKILL.md` § Self-check 新增一段說明與 3 行指令：把腳本插在最後一個 `</body>` 前、存成 `mktemp` 暫存檔、以 Chrome `--dump-dom` 讀出報告。找不到報告元素時印出 `no report: the check did not run`，避免腳本沒有執行卻被當成通過。清單中「圖示同步指令不印出任何內容」一項改為同時包含壓線檢查。

**重寫時發現的問題。** 第一版腳本開頭的註解含有報告元素的完整標籤文字，`--dump-dom` 的輸出中，指令的正規表示式先比對到註解，把整支腳本當成報告印出。註解改寫後解決。

**驗證**（暫存檔在本 session 暫存目錄的 `t7/`）：

| 測試 | 結果 |
|---|---|
| 乾淨頁面（`pictorial.md` 的 5 個配方片段） | 沒有回報 |
| D1–D7（放入方式同 T3） | 7 個都抓到；回報的類別與 T3 相同 |
| D6 的引線加上 `data-touch` | 不再回報 |
| 文字放在旋轉 −35° 的 `<use>` 物件邊緣 | 回報 `text-on-edge` |
| 模板圖 2 第 3 幀加入一個與第 1 步標籤重疊的文字 | 回報 `fig-2 [frame 3] text-overlap` |
| 模板 | 沒有回報 |
| 7 個範例頁 | 沒有回報；每頁 0.58–1.35 秒（含啟動 Chrome） |
| 預設輸出目錄的 24 個頁面 | 沒有回報 |
| 從 `SKILL.md` 取出指令區塊原樣執行（只替換 skill 路徑） | 結果同上，`/tmp` 沒有留下暫存檔 |

### T8 風格規範與零件函式庫（2026-10-13）

**結論：`scripts/parts.py`（只用 Python 3 標準函式庫）以 9 個子指令印出 SVG 片段；模板新增 `ink` 系列 class；`pictorial.md` 新增 § Drawn objects 與 Recipe P5。零件總覽圖中 68 個 `ink` 形狀的外框都是 4px，同一組參數兩次輸出相同，輸出中沒有 `scale()`。**

**決定的名稱與清單（原為待決問題）：**

| 項目 | 決定 |
|---|---|
| 模板 class（不加 `svg ` 前綴） | `ink`（外框＋淺色填色：`--cb`，沒有概念色時為 `--bg`）、`ink dark`、`ink glass`、`ink-edge`＋`ink-fill`（單一外輪廓）、`ink-shade`（`--cc` 18%）、`ink-track`（P5 的淡色虛線軌跡） |
| 組合物件 | `person --height`（≥ 100）、`robot --size --view top\|side`、`drone --size --view top\|side` |
| 基本形 | `pill`、`rect --r "左上 右上 右下 左下"`、`cylinder`（資料庫、儲槽）、`ogive`（尖頭朝 +x 的長形，火箭級段等）；`--fill light\|dark\|glass` |
| 其他 | `pose`（依軌跡計算位置與角度，輸出 P5 的軌跡與 `<use data-step>`；路徑支援絕對座標的 M、L、H、V、Q、C；`--angles` 可為 `t`、`t+90`、`t-90` 或固定角度）、`sheet`（零件總覽圖，獨立 SVG 檔，內嵌模板的 CSS） |
| 共同參數 | `--id`、`--cls`（概念色）、`--at X,Y[,角度]`（直接輸出擺好位置的一份；不加時輸出放進 `<defs>` 的 `<g id>`） |

**與規格不同或規格沒有寫到的細節：**

1. **人體最小高度 100。** 外框固定 4px，頭與軀幹、兩腿之間必須保持 ≥ 11px（R3 第 1 點）。高度低於 100 時，腿的寬度與間距放不進軀幹的寬度，所以指令直接報錯。圖中需要更小的人時，改用 Lucide 的 `user` 圖示標在標籤旁。
2. **肩點改為 (±13, 軀幹頂 + 9)。** 規格沿用檢查點 0 的 (±15, −29)。實測時手臂的圓頭超出軀幹的肩角約 1px，形成小突起；內移 2px、下移 2px 後消失（放大截圖 `$SCRATCH/t8/zoom-person.png`）。
3. **陰影只畫在主體上。** 每個組合物件的陰影是主體再畫一次、以物件自己的 `clipPath`（id 為 `<物件 id>-shade`）裁到背光側：人體在 +x 側，朝 +x 的俯視與側視物件在 +y 側。基本形不畫陰影。
4. **`--at` 與 `--angles` 接受負值。** argparse 會把 `-32,-27` 當成選項名稱；`parts.py` 在解析前把這兩個參數與其後的負值合併。
5. **零件總覽圖的 `<style>` 包在 CDATA 中。** 模板 CSS 註解中的 `<span>`、`<tspan>` 範例會讓獨立 SVG 的 XML 解析失敗。

**驗證**（暫存檔在本 session 暫存目錄的 `t8/`）：

| 測試 | 結果 |
|---|---|
| V3：零件總覽圖（`sheet.png`） | 基本形、3 種尺寸的人體、俯視與側視的機器人和無人機（含旋轉）、4 步姿態都正確 |
| V3：人體放大 4 倍（`zoom-person.png`、`zoom-person100.png`） | 軀幹與腿之間沒有圓弧缺口；肩膀平順；150、120、100 的外框粗細相同 |
| V3：總覽圖中 `.ink` 形狀的計算後線寬 | 68 個全部是 4px |
| 同一組參數執行兩次（`sheet` 與文件中的全部指令） | `diff` 沒有輸出 |
| 輸出中的 `scale(` | 0 處 |
| `pictorial.md` 與 `SKILL.md` 中所有含 `parts.py` 的指令區塊原樣執行（只替換 skill 路徑） | 15 個指令都以 0 結束；`parts.py -h` 正常 |
| `person --height 90` | 印出錯誤訊息，結束碼 1 |
| 背包、車與 P5 範例的測試頁（`objects.html`、`p5.html`）與模板 | 壓線檢查、對比檢查都沒有輸出；P5 第 1、3、4 幀截圖中物件落在軌跡上 |
| `CLAUDE.md` 的模板驗證指令 | 外部資源無輸出；1280px 截圖正常；390px 為 `<title>ok` |

**觀察（留給檢查點 B 判讀）：** 無人機俯視圖中，旋翼大到幾乎碰到機身，機臂只露出很短一段。

### 檢查點 B（2026-10-13）

使用者判讀：

1. 人體的軀幹與腿交接處有段差：腿的外緣比軀幹內縮 1.5px。改為雙腿外緣與軀幹兩側切齊（`parts.py` 移除內縮），規格 R3 同步修改。修改後重新放大截圖（`t8/zoom-person.png`、`t8/zoom-person100.png`），150、120、100 三種尺寸的外側邊線都從軀幹直線延伸到腿，沒有段差。
2. 無人機維持現狀。
3. 陰影的分界維持現狀。
4. 其他截圖（零件總覽圖、Recipe 3 片段與它遮住文字的截圖、P5 第 3 幀）沒有問題。

修改後的驗證：3 種高度的腿外緣座標與軀幹側邊相同（±20、±16、±13.3）；文件中 20 個 `parts.py` 指令都以 0 結束；`sheet` 兩次輸出相同；總覽圖 68 個 `ink` 形狀的線寬都是 4px。

### T15 節點外觀原則（2026-10-13）

**結論：R6 已寫入 4 個檔案。Recipe 3 的新片段把瀏覽器與資料庫畫成物件、API server 保留方框；遮住所有文字後，兩個物件仍可辨認，結構仍表達「只有 API server 連到資料庫」。**

| 檔案 | 修改 |
|---|---|
| `explainer-figure/SKILL.md` | 圖型表後新增一段：圖型依問題選擇，節點外觀依它代表的東西決定；具體東西畫成物件，抽象概念與同類節點用方框；判準是遮住文字後的辨識（R6 第 1、2 點） |
| `pictorial.md` 開頭 | 改寫為兩部分：§ Drawn objects 適用於任何圖中的物件；P1–P5 是整張具象插圖的版面配方 |
| `pictorial.md` § Drawn objects | 新增「特定實物依資料繪製」的規則（R6 第 4 點） |
| `icons.md` 第 55 行 | 禁令限縮為「不要在標籤旁假造缺少的圖示」；需要在節點大小被認出的東西，畫成物件 |
| `svg-recipes.md` Recipe 3 | 標題加上「or a system」；新增 3 條規則（具體元件畫成物件、物件的標籤在下方、箭頭端點在物件外接矩形外 2px）；附 `parts.py` 指令與可複製的片段 |

沒有加入元件清單、連線配色、雙向平行箭頭（R6 第 6 點）。

**實作時的調整：** 瀏覽器標題列的 3 個圓點原本相距 12px。每個圓點含外框寬 10px，間距不足 § Drawn objects 的 11px 規則，所以改為相距 17px。

**驗證**（暫存檔在本 session 暫存目錄的 `t15/`、`t16/`）：Recipe 3 片段貼進模板暫存頁（`r3.html`），截圖 `t15/r3.png`；壓線檢查與對比檢查都沒有輸出；`svg-recipes.md` 中的片段與測試頁中的片段逐字相同；7 個範例頁的壓線檢查仍沒有輸出。

### T16 意圖檢查（2026-10-13）

**結論：Self-check 改為先比對意圖、再找缺陷。3 項指令都在 Recipe 3 暫存頁與 Starship 範例頁上實際執行過（V9）。`SKILL.md` 為 124 行；並排與放大兩段指令放在 `pictorial.md` § Check drawn objects，依架構決策第 1 點把細節移出。**

- **順序（`SKILL.md` § Self-check 開頭）：** 先截取遮住文字的圖，對照圖說明單的 Message 欄；不符合時先重畫。之後才逐項檢查缺陷。每次修正後重新截圖，直到兩者都通過。
- **遮住文字：** 既有的只看圖截圖指令新增變數 `H`。設為 `figure svg text,figure p,figcaption,.src{visibility:hidden}` 時，隱藏圖中所有文字、stepper 說明、圖說與來源行，版面不變。
- **與零件總覽圖並排：** `parts.py sheet` 輸出總覽圖，再與 `/tmp/figures.png` 並排截圖。
- **放大截圖：** 把指定圖的 `viewBox` 改為要檢查的區域，以 `--force-device-scale-factor=4` 截圖。第一次執行時，區域在頁寬下高約 548px，超過 500px 的視窗，下緣被切掉；改為固定 SVG 高度 440px 後，約 3:2 的區域都能完整放進視窗。

**V9 執行結果：**

| 頁面 | 遮住文字 | 並排 | 放大 |
|---|---|---|---|
| Recipe 3 暫存頁（`t15/r3.html`） | `t16/r3-hidden.png`：瀏覽器與資料庫可辨認，API server 是方框 | `t16/r3-side.png` | `t16/r3-zoom.png`（瀏覽器，3600 × 2000）：圓點分開，外框粗細一致 |
| `examples/starship-reusability/starship-reusability.html` | `t16/starship-hidden.png`：圖 1 的因果鏈維持方框；圖 2、3 的火箭是細線外框，遮住文字後只能勉強認出 | `t16/starship-side.png` | `t16/starship-zoom.png`（圖 4） |

Starship 範例頁的遮住文字截圖，可作為 T11 改版前的對照。

### T6 EKF 頁 v2（2026-10-13）

**結論：新版存於預設輸出目錄的 `extended-kalman-filter/extended-kalman-filter.v2.html`（55.6 KB），原頁未修改。圖 3 的機器人改由零件函式庫產生；5 個關鍵符號在圖 3、公式與符號表中使用相同的概念色。`explainer-page/SKILL.md` 第 6 步的自檢、壓線檢查、對比檢查都通過，意圖檢查的 3 項都已執行。**

暫存檔在 T6 當時 session 的暫存目錄（下稱 `$SCRATCH`）的 `t6/`，產生程式為 `t6/build.py`。

| 項目 | 內容 |
|---|---|
| CSS | 換成目前模板的 `<style>`（新增概念色、`ink`、`.sym`；`svg text.good` 改用 `--green-text`） |
| 符號與概念色 | `μ`（含 μ⁻）c1、`P`（含 P⁻）c2、`z` c3、`K` c4、`y` c5；其餘符號（u、f、Q、h、R、F、H、S）用一般文字色 |
| 圖 3 | viewBox 720 × 300 → 720 × 330；比例 80 px/m，地標 (4, 2) 位於 (420, 80)；機器人為 `robot --size 48 --view top --cls c1`；橢圓 P 改用 `box c2`，放大到能包住機器人；第 5 步以虛線保留 P⁻ 的外框，顯示範圍縮小；每一幀都標出該步的符號（μ、P、u、μ⁻、P⁻、h(μ⁻)、z、y、K y） |
| 公式段落 | 符號表、圖 3 後的段落（P⁻ = F P Fᵀ ＋ Q）、九步驟表、名詞表的 P 與 K 加上 `.sym` |
| 符號表 | 新增 y（創新）與 K（Kalman gain）兩列，因為兩者現在標在圖上（規格 R1 第 4 點：圖上標出的符號也列在對照表中） |

**與計畫寫法不同之處：** 驗收條件以 x̂ₖ、Pₖ、zₖ、Kₖ 為例；原頁全頁使用 μ、μ⁻ 與無下標的記號，v2 沿用原頁記號，不改寫全頁。

**取捨：** 原版以語意色表示橢圓的變化（第 2 步 `warn`、第 5 步 `good`）。R1 要求 P 在圖與公式同色，而概念色不能與語意色放在同一個元素上，所以 v2 的橢圓全部是 c2，變大與縮小只靠大小與 P⁻、P 的標籤表達。

**驗證**（截圖在 `t6/`）：

| 檢查 | 結果 |
|---|---|
| `FILL`、外部資源、大小、來源等級與日期 | 0、無輸出、55,641 B、無輸出 |
| 390px iframe、1280px 截圖 | `<title>ok`；`narrow.png`、`wide.png` |
| 對比檢查、壓線檢查 | 都沒有輸出 |
| 逐幀截圖 | `v2-all.png`；與原版並排 `compare-ekf.png`（第 1、2、4、5 幀） |
| 遮住文字 | `hidden.png`、逐幀 `hidden-all.png`：機器人可辨認；橢圓第 2 步變大、第 5 步縮小、第 6 步再變大，符合 Message |
| 與零件總覽圖並排 | `side.png`：外框、填色與總覽圖的機器人一致 |
| 放大 | `zoom.png`（圖 3 第 1 幀的機器人，3600 × 2000）：外框粗細一致，沒有缺口 |

**留給檢查點 C 判讀：** 俯視機器人在 48px 時，鏡頭狀的光達與三角形方向標記讓它有點像攝影機圖示；這是零件函式庫的既有外形（檢查點 B 已通過），本任務沒有修改。

### T11 Starship 圖 4（2026-10-13）

**結論：圖 4 改為從發射到接回的 8 步姿態圖，飛船與助推器依 V3 的比例與特徵以基本形組合。暫存副本 `t11/starship-v2.html`（54.4 KB）通過全部自檢；`examples/` 未修改，等檢查點 C 決定是否取代。**

暫存檔在本 session 暫存目錄的 `t11/`，產生程式為 `t11/build.py` 與 `t11/labels.html`。

**外形依據**（Wikipedia〈SpaceX Starship〉，與範例頁圖 3 使用的尺寸一致）：

| 特徵 | 資料 | 畫法 |
|---|---|---|
| 助推器比例 | 高 72.3 m、直徑 9 m（高徑比約 8） | `rect` 144 × 18 |
| 飛船比例 | 全高 124.4 m 減去助推器，約 52 m（高徑比約 5.8） | `ogive` 104 × 18，尖頭 30 |
| 柵格翼 | V3 為 3 片，比前兩代大約 1.5 倍、位置較低，兼作被接住的掛點 | 距頂端約 22px 的兩片深色短翼（側視只看到兩側的兩片） |
| 襟翼 | 前後各兩片，前襟翼在載荷艙附近 | 前端兩片小翼、尾端兩片大翼 |
| 隔熱瓦 | 迎風面覆蓋黑色六角形隔熱瓦 | 沿飛船一側的深色帶 |
| 引擎 | 助推器 33 具、飛船 6 具 Raptor | 尾端的深色短塊 |

Wikipedia 的 V3 數字有不一致：說明文字寫助推器 72.3 m，性能表寫 81 m；飛船寫 61 m，但全高為 124.4 m。本圖沿用範例頁圖 3 已採用的 72.3 m 與約 52 m，所以兩張圖的比例一致。

**8 步與姿態：** 軌跡由 `parts.py pose` 計算。上升軌跡 `M190 356 C190 180 335 188 410 118` 上取 0、0.25、1 三點（第 1–3 步）；返回軌跡從分離時助推器的中心開始，取 0、0.12、0.5、0.8、1 五點（第 4–8 步），角度依序為 −115°、180°、−125°、−80°、−90°；飛船分離後沿自己的軌跡在 0.55 處擺放（第 4 步）。分離前兩者放在同一個 `f4-stack` 中，第 3 步起各自擺放。

**修正草圖的問題：** 姿態都落在軌跡上；第 1 步的火焰在發射台的檯面下、兩腳之間，沒有伸到地面以下；加上發射台；發射塔畫得比整組火箭高（示意，沒有查證塔高）。

**實作時的調整：**

1. 物件寬度從 14px 改為 18px。14px 時 4px 外框占去大部分寬度，飛船幾乎全黑；高徑比維持不變。
2. viewBox 從 720 × 320 改為 720 × 560。按比例的整組火箭長約 258px，720 × 420 與 720 × 480 都放不下上升、分離與返回：第 2 步的火箭會穿過發射塔，第 3 步的飛船頭超出畫布。
3. 發射台向右移 15px，讓第 2 步的火焰離開發射塔。
4. 熱分離的火焰長度改為 12px。原本 18px 時，火焰尖端碰到助推器的頂端（放大截圖發現）。
5. 3 個步驟標籤原本壓到軌跡（壓線檢查回報 `line-through-text`），已移開。

**範例頁文字的修改：** 圖 4 前的段落改為「從發射畫起，用八步呈現……淡色虛線是兩者走過的軌跡」；8 步的 `data-caption` 依新的步驟改寫，內容取自原 5 步的說明；圖說改為八步的版本；來源行補上外形的依據。CSS 換成目前模板的 `<style>`。

**驗證**（截圖在 `t11/`）：

| 檢查 | 結果 |
|---|---|
| `FILL`、外部資源、大小、來源等級與日期 | 0、無輸出、54,449 B、無輸出 |
| 390px iframe、1280px 截圖 | `<title>ok`；`narrow.png`、`wide.png` |
| 對比檢查、壓線檢查、圖示同步 | 都沒有輸出；圖示同步後檔案不變 |
| 輸出中的 `scale(` | 0 處 |
| 逐幀截圖 | `compare-new.png`（8 幀）；原版 `compare-old.png`（5 幀） |
| 遮住文字 | `hidden-all.png`：發射、上升、分離、翻轉、折返、滑行、下降、接住都能從形狀與位置看出；飛船（深色、有襟翼）與助推器（淺色、有柵格翼）可區分 |
| 與零件總覽圖並排 | `side.png` |
| 放大 | `zoom-small.png`（第 3 幀分離處）；修正火焰長度後的 `sep.png` |

### 檢查點 C（2026-10-13，進行中）

**使用者判讀：**

1. EKF v2 圖 3 使用零件函式庫可以接受。俯視的差速機器人有點像攝影機，使用者認為可以在〈本頁的例子〉段落加一張機器人的圖來解決。這張圖可以從不同角度呈現機器人，以圖、引線與文字對應段落的敘述；也可以畫成運動學圖，把幾何符號與機器人的部位連起來。使用者提供的參考（存於儲存庫根目錄的 `temp/round-05/`，`temp/` 不加入版本控制）：
   - `temp/round-05/sensors-25-03553-g001-550.jpg`：機器人外觀與內部配置兩張照片，以箭頭標籤標出 LIDAR、CPU、ENCODERS、DRIVER、MCU、IMU。
   - `temp/round-05/Differential_Drive_Kinematics_of_a_Wheeled_Mobile_Robot.png`：Wikipedia 的差速運動學圖，標出 ICR、R、ω、v_L、v_R、V、φ、b、2r 與座標軸。
   - `temp/round-05/differential-3582cb59.png`：引線標註的參考（內容是汽車的差速齒輪剖面，與機器人無關）。標籤放在圖的外圍，每個標籤以一條細線指到對應的部位，十多個部位的標籤分布在四周而不互相交叉。
   - Wikipedia〈Differential wheeled robot〉的圖文搭配方式。
   這不屬於 T6，作為後續的構想記錄；是否納入 T12 或下一輪，由使用者決定。
2. Starship 圖 4 的流程整體通過。修改：軌跡虛線改為隨步驟出現，不再全程常駐。使用者選擇「累積顯示已走的路」，修改範圍包含 P5 規則與 `pose` 子指令。

**依第 2 點修改的檔案：**

| 檔案 | 修改 |
|---|---|
| 規格 | §0 新增決策；R3 第 3 點的軌跡規則改為隨步驟累積，姿態子指令輸出每一步的軌跡段，並可指定第一個姿態的步數 |
| `scripts/parts.py` | `pose` 不再輸出整條軌跡，改在每個 `<use>` 前輸出該步新增的軌跡段（`data-step="k+"`）。軌跡段以 de Casteljau 從原路徑精確切出，仍是 L、Q、C 指令。新增 `--first`：第一個姿態的步數，供 stepper 中途才出現的物件使用 |
| `pictorial.md` Recipe P5 | 開頭說明、`aria-label`、範例片段（以新的 `pose` 輸出重產）、`pose` 的說明與 `--first` 的用法 |
| T11 暫存副本 | 以新的 `pose` 重產：上升段第 2–3 步、飛船與返回段以 `--first 4` 從第 4 步起；圖 4 前的段落改為「淡色虛線隨步驟延伸，顯示已走過的軌跡」 |

**驗證：**

| 檢查 | 結果 |
|---|---|
| `pose` 的邊界情況 | 姿態剛好在指令交界時，不輸出零長度的片段；兩個姿態在同一點時，不輸出軌跡段；`--no-track` 只輸出 `<use>` |
| 文件中的 `parts.py` 指令（`SKILL.md` 與 references，共 21 個）與 `parts.py -h`、`pose -h` | 都以 0 結束 |
| `sheet` 執行兩次 | `diff` 沒有輸出；輸出中沒有 `scale(` |
| P5 範例片段貼進模板暫存頁（`p5/p5.html`） | 壓線檢查沒有輸出；第 1、2、3、5 幀截圖（`p5/p5-all.png`）中軌跡逐步延伸，各段相接 |
| T11 暫存副本 | `FILL` 0、外部資源無輸出、54,904 B、來源檢查無輸出、壓線檢查無輸出、390px 為 `<title>ok`；8 幀截圖 `t11/compare-new.png` |
| `claude plugin validate .` | 通過（只有根目錄 `CLAUDE.md` 的既有警告） |
| `wc -l skills/*/SKILL.md` | 124、130，沒有變動 |

**待辦：** Starship 圖 4 是否取代範例；T17 由使用者在 Codex 中執行。

### T18 P1–P4 改用物件風格（2026-10-13）

**結論：P1、P1 變化、P2、P3、P4 的範例片段都改用 `ink` 系列，幾何由 `parts.py` 產生；〈Rules for every pictorial figure〉的配色規則改為「物件與部件是 `ink`，物件內的抽象內容維持 `box`」。模板新增 2 個 class、移除 4 個舊 class。驗證全部通過。**

暫存檔在 T18 當時 session 的暫存目錄（下稱 `$SCRATCH`）的 `t18/`。

**決定：**

| 項目 | 決定 | 理由 |
|---|---|---|
| 剖開的容器（P1） | 分層畫成 `ink cN` 矩形，剛好蓋住容器的外接框，裁切到容器形狀內；最後以 `ink hollow` 畫外框 | 分層之間的界線也是 4px，與物件風格一致。第一版讓分層超出外框，壓線檢查回報分層邊緣壓到「git repo」標籤：檢查看不到裁切，所以改為剛好對齊外接框 |
| 填色區域（P2 的水位） | 第二份物件加上概念色與 `ink-level`（`--cb` 改為概念色 35% 混入背景色），放在裁切的 `<g>` 中 | 只用概念色淺底時，水位幾乎看不出來；變化以自訂屬性傳遞，符合 R3 |
| P1 變化的角色 | 「You」改用 `parts.py person --height 110`；「LLM」是抽象概念，保留方框 | R6 |
| P3、P4 | 罐子、瓶頸、蓋子、視窗與面板改用 `ink`；罐子中的元件列、面板中的欄位維持 `box` | 物件內不是實體部件的內容，與任何圖一樣用方框 |
| 舊 class | 從模板移除 `outline`、`edge`、`shape`、`area` | 配方已不使用；留著會讓代理畫出舊風格。範例頁各自內嵌 CSS，不受影響 |
| `parts.py` | `--fill` 新增 `hollow` | 讓容器外框也由函式庫產生 |

**實作時發現的陷阱：** 第一版 P2 把 `clip-path` 與 `transform` 放在同一個 `<use>` 上，裁切矩形跟著平移到畫面外，水位沒有出現。改為把裁切放在外層 `<g>`，並寫進〈Rules for every pictorial figure〉。

**受影響的範例圖（本任務不修改）：**

| 範例頁 | 圖 | 原因 |
|---|---|---|
| `llm-wiki` | 圖 4（git repo 資料夾與兩個角色） | P1 變化的舊寫法：2px 外框；「你」是方框，依 R6 應畫成人 |
| `llm-wiki` | 圖 5（`index.md`、`log.md` 兩份文件） | 文件畫成摺角的紙張，是物件，但用 2px 的舊外框 |
| `starship-reusability` | 圖 2–5 | 由 T19 處理 |
| `autoresearch`（3 頁）、`explain-as-webpage`（2 頁） | — | 節點是檔案、程式段落與步驟：抽象概念或同類節點，依 R6 保留方框 |

**驗證**（暫存檔在 `$SCRATCH/t18/`）：

| 檢查 | 結果 |
|---|---|
| 5 個新片段與 `pictorial.md` 中的片段逐字相同 | 是 |
| 6 張配方圖放進同一個模板暫存頁（`all.html`） | 壓線檢查、對比檢查、圖示同步都沒有輸出；id 沒有重複；`ink` 形狀的計算後線寬都是 4px |
| 遮住文字（`hidden.png`） | 背包、資料夾與人、人體水位、罐子、視窗都能從形狀辨認 |
| 與零件總覽圖並排（`side.png`）、放大（`zoom.png`：P1 分層與外框的交接、P2 的水位） | 線寬一致，交接處沒有缺口 |
| 文件中的 `parts.py` 指令（25 個）、`sheet` 兩次 | 都以 0 結束；輸出相同 |
| `CLAUDE.md` 的模板驗證指令 | 外部資源無輸出；390px 為 `<title>ok`；模板的壓線檢查沒有輸出 |
| `wc -l skills/*/SKILL.md` | 124、130，沒有變動 |
