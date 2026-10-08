# 實作計畫：符號對照圖與具象插圖品質（第五輪）

構想見 `docs/plan/05-symbols-pictorial-idea.md`，規格見 `docs/plan/05-symbols-pictorial-spec.md`。本文件同時是待辦清單：〈進度總覽〉每項一行，完成時勾選並補一句結果；各任務的驗收條件也逐項勾選；探測與驗收的細節記在〈結果〉。

## 進度總覽

### 第 0 階段：探測（不改產品檔案）
- [ ] T1 Noto Emoji：授權、版本、物件清單、大小、id 前綴、兩種截圖
- [ ] T2 風格試畫：5 種物件各 3 次、助推器殘影草圖
- [ ] T3 壓線檢查原型：V4 準確度
- [ ] T4 Codex 觸發測試（使用者手動）

#### 檢查點 0
- [ ] 使用者判讀 emoji 與自繪風格是否搭配、試畫結果、腳本準確度、Codex 結果

### 第 1 階段：符號對照（R1）
- [ ] T5 `.sym`、圖說明單的 Symbols 欄、符號標註規則、`writing-rules.md` 引用
- [ ] T6 EKF 頁 v2（V1）

#### 檢查點 A
- [ ] 使用者並排判讀 EKF 新舊版；提供提交建議

### 第 2 階段：具象插圖品質（R2–R4）
- [ ] T7 壓線檢查進入 `scripts/`，加入 Self-check 指令
- [ ] T8 風格規範、5 種物件配方、P5 物件與姿態
- [ ] T9 Noto Emoji 子集、`emoji.md`、同步指令
- [ ] T10 emoji 接入既有規則：圖型表、`pictorial.md`、`icons.md`
- [ ] T11 Starship 圖 4 殘影版（V2）

#### 檢查點 B
- [ ] 使用者判讀 Starship 圖 4，決定是否取代範例；提供提交建議

### 第 3 階段：驗收與收尾
- [ ] T12 新主題頁（V7；使用者先指定主題）
- [ ] T13 版本 0.5.0、`CLAUDE.md`、README、構想文件的假設、索引狀態

#### 檢查點 C
- [ ] 規格〈成功條件〉全部達成；提供最終提交建議

## Overview

本輪讓 explainer-figure 能做兩件事：

- 把公式符號標在圖上，並與公式使用相同的概念色。
- 以「粗外框＋平塗色」的風格畫出具象物件與它的姿態；只需要辨識的物件，改用 Noto Emoji 子集。

另外加入壓線檢查腳本，並驗證 Codex 不會自動觸發 explainer-figure。頁面仍是單檔、離線，上限仍是 150 KB。

## Architecture Decisions

使用者已確認的決策列在規格〈0. 問題陳述與範圍〉。規劃時的補充：

1. **`SKILL.md` 的行數預算。** `skills/explainer-page/SKILL.md` 已有 130 行，本輪不修改。`skills/explainer-figure/SKILL.md` 有 111 行，新增內容以約 19 行為上限：Symbols 欄 1 行、圖型表 1 列、壓線檢查指令約 6 行。其餘細節放進 references。
2. **第一個腳本檔。** 兩個 skill 原本只在 markdown 中放 heredoc 指令。壓線檢查約 60–100 行 JavaScript，每次複製容易出錯，所以放成獨立檔 `scripts/check-overlap.js`。Claude Code 與 Codex 都從 skill 資料夾讀取這支檔案，不依賴平台功能。
3. **只看圖的截圖。** `explainer-figure/SKILL.md` § Self-check 的截圖指令會隱藏 `.content` 中不是 figure 的元素。共用的隱藏 `<svg>`（`template.html` 第 146 行）位於 `.content` 之外，但 `pictorial.md` 記錄過 `clipPath` 放在共用 `<svg>` 時，在只看圖截圖中失效。emoji 的漸層也可能遇到相同的問題，所以 T1 要在兩種截圖中都確認。
4. **emoji 與圖示分開。** Lucide 圖示是單色線條，以 CSS 上色；Noto Emoji 自帶顏色與漸層，不受概念色影響。兩者的使用規則不同，所以分成 `icons.md` 與 `emoji.md`，區塊標記也分開（`icons:start`、`emoji:start`）。
5. **最高風險先探測。** emoji 的風格與顯示、自繪風格的穩定性、腳本的誤報率，三項都在第 0 階段完成，先於任何產品檔案的修改。
6. **探測檔案。** 試畫與原型放在 session 的暫存目錄，不進儲存庫；結果與截圖路徑記在〈結果〉。
7. **提交方式。** 實作過程不自行 `git commit`；每個檢查點提供 `git add` 範圍與提交訊息。
8. **版本號。** 本輪新增功能，收尾時升為 0.5.0，四個 manifest 檔同步。

## Task List

### 第 0 階段：探測（不改產品檔案）

#### T1 Noto Emoji 探測

**說明：** 確認 Noto Emoji 的授權、版本與檔案格式，選出子集候選，並確認漸層在兩種截圖中都能顯示。

**驗收條件：**
- [ ] 已讀 LICENSE 原文，記錄 SVG 圖檔的授權條款，以及內嵌與重新散布的條件
- [ ] 選定一個發行版並記錄版本號
- [ ] 統計 7 個範例頁、EKF 頁與候選主題需要的辨識型物件，列出約 30 個候選與 Noto 的覆蓋率
- [ ] 記錄每個候選的檔案大小與總和；估算一頁放 5 個 emoji 的增量
- [ ] 以一段程式替 emoji 內部的 id 加上 `e-<name>-` 前綴，同頁放 5 個 emoji 時沒有衝突
- [ ] 把 emoji 放在共用的隱藏 `<svg>` 中，在整頁截圖與只看圖截圖中都正常顯示；不能顯示時，改測逐圖內嵌，並記錄結論
- [ ] 把 emoji 與「粗外框＋平塗色」的自繪物件放在同一張圖中截圖，供檢查點 0 判讀

**驗證：** `git status` 只有本計畫檔有變動。

**相依：** 無　**檔案：** 本計畫檔、暫存檔　**規模：** M

#### T2 風格試畫

**說明：** 以「粗外框＋平塗色」試畫 5 種物件，每種畫 3 次，檢查穩定性；並畫一張助推器殘影草圖。

**驗收條件：**
- [ ] 人、背包、俯視機器人、俯視車、火箭各畫 3 次，都在 720 寬的網格上
- [ ] 記錄外框線寬、填色、陰影的參數（候選線寬 3px）
- [ ] 助推器殘影草圖：物件定義一次，以 `<use>` 加上 `transform` 擺出至少 4 個姿態
- [ ] 截圖交使用者判讀（檢查點 0）

**驗證：** 同一物件 3 次的外形一致，截圖中沒有歪掉、破損或溢出（V3）。

**相依：** 無　**檔案：** 本計畫檔、暫存檔　**規模：** M

#### T3 壓線檢查原型

**說明：** 依規格 R2 寫出原型腳本，量測漏報與誤報。

**驗收條件：**
- [ ] 原型能逐幀檢查 stepper，輸出格式符合 R2 第 6 點，全部通過時不印出任何內容
- [ ] 依規格 R2 表中 6 個已記錄的缺陷，在現有頁面的副本中重新放入，再加 1 個人工的文字重疊案例；7 個都抓到
- [ ] 在 7 個範例頁與 EKF 頁上執行，逐一判讀每個回報是真缺陷或誤報，並記錄需要的排除規則
- [ ] 記錄執行時間

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
- [ ] 5 個提示的結果已記錄
- [ ] 觸發 0 次；若有觸發，記錄情況並在 T10 一併改寫 explainer-figure 的 description 或隱藏方式，再請使用者重測

**相依：** 無　**檔案：** 本計畫檔　**規模：** S

#### 檢查點 0

- [ ] 使用者判讀 T1 的 emoji 與自繪物件並排截圖，確認 Noto Emoji 的風格可接受
- [ ] 使用者判讀 T2 的試畫結果與參數
- [ ] T3 的準確度達到 V4；誤報需要的排除規則已確定
- [ ] T4 的結果已記錄
- [ ] 若任何一項不通過，先更新規格，再進入第 1 階段

### 第 1 階段：符號對照（R1）

#### T5 符號對照規則

**說明：** 依規格 R1 加入公式符號的上色與圖上的符號標註。

**驗收條件：**
- [ ] `template.html` 新增 `.sym`（或實作時確定的名稱），只使用 `--cc`
- [ ] `explainer-figure/SKILL.md` 圖說明單加入 Symbols 欄
- [ ] `svg-recipes.md` 加入符號標註的寫法：Unicode 下標、`<tspan>` 的退路、上色範圍（最多 5 個）
- [ ] `writing-rules.md` § Ground the symbols 加一行，指向 explainer-figure
- [ ] 在模板示範內容中放一個上色符號，截圖確認組合字元（x̂）在 SVG 與 HTML 中都正確顯示

**驗證：**
- [ ] `CLAUDE.md` 的模板驗證指令全部通過（外部資源、兩種寬度）
- [ ] 對比檢查不印出任何內容
- [ ] `wc -l skills/explainer-figure/SKILL.md` 不超過約 130

**相依：** 檢查點 0　**檔案：** `template.html`、`explainer-figure/SKILL.md`、`svg-recipes.md`、`writing-rules.md`　**規模：** M

#### T6 EKF 頁 v2（V1）

**說明：** 以 T5 的規則改版 EKF 頁的圖 3 與公式段落。原頁不覆寫，新版另存為同目錄下的另一個檔案，只放在本機。

**驗收條件：**
- [ ] 圖 3 每一幀都標出該步出現的符號（x̂ₖ、Pₖ、zₖ、Kₖ 等），關鍵概念的符號與公式同色
- [ ] 機器人畫成有朝向的物件，不再只是一個點
- [ ] 公式段落中的符號使用 `.sym` 上色，與圖一致
- [ ] 與原版並排截圖

**驗證：**
- [ ] `explainer-page/SKILL.md` 第 6 步的自檢全部通過
- [ ] T3 的壓線原型在新頁上沒有回報

**相依：** T5　**檔案：** 本機的 EKF 新版頁面、本計畫檔　**規模：** M

#### 檢查點 A

- [ ] 使用者並排判讀 EKF 新舊版，確認公式更容易對應到圖
- [ ] 提供 `git add` 範圍與提交訊息

### 第 2 階段：具象插圖品質（R2–R4）

#### T7 壓線檢查進入 skill

**說明：** 把 T3 的原型整理成 `scripts/check-overlap.js`，並在 Self-check 加入執行指令。

**驗收條件：**
- [ ] `skills/explainer-figure/scripts/check-overlap.js` 支援 `data-touch` 排除
- [ ] `explainer-figure/SKILL.md` § Self-check 加入執行指令，指令中的腳本路徑從 skill 根目錄寫起
- [ ] 指令已實際執行一次

**驗證：**
- [ ] V4 的兩個條件仍成立
- [ ] `wc -l skills/explainer-figure/SKILL.md` 不超過約 130

**相依：** 檢查點 0　**檔案：** `scripts/check-overlap.js`（新增）、`explainer-figure/SKILL.md`　**規模：** S

#### T8 風格規範與 P5

**說明：** 依規格 R3，把 T2 的結果寫成 `pictorial.md` 的規範與配方。

**驗收條件：**
- [ ] `pictorial.md` 加入「粗外框＋平塗色」的規範：線寬、填色、陰影，只使用模板變數
- [ ] 5 種物件的配方片段；人體剪影改用新風格
- [ ] 新配方 P5「物件與姿態」，含殘影與 stepper 並用的寫法
- [ ] `template.html` 新增需要的 class

**驗證：**
- [ ] 每個配方片段都貼進暫存頁截圖，外形與 T2 一致
- [ ] 壓線檢查與對比檢查都不印出任何內容
- [ ] `CLAUDE.md` 的模板驗證指令全部通過

**相依：** T7　**檔案：** `pictorial.md`、`template.html`　**規模：** M

#### T9 Noto Emoji 子集

**說明：** 依規格 R4 與 T1 的結論，把子集、授權與使用規則放進 skill。

**驗收條件：**
- [ ] `assets/emoji/noto.svg`（開頭有授權聲明，內部 id 已加前綴）與 `assets/emoji/LICENSE`
- [ ] `references/emoji.md`：名稱表、使用時機、尺寸、與自繪物件並用的規則、同步指令、新增 emoji 的方法
- [ ] `template.html` 加入 `<!-- emoji:start -->`／`<!-- emoji:end -->`

**驗證：**
- [ ] 同步指令已實際執行一次；在放 5 個 emoji 的暫存頁上不印出任何內容，頁面 ≤ 150 KB
- [ ] 兩種截圖中 emoji 都正常顯示
- [ ] `CLAUDE.md` 的模板驗證指令全部通過

**相依：** T8　**檔案：** `assets/emoji/`（新增 2 個）、`emoji.md`（新增）、`template.html`　**規模：** M

#### T10 emoji 接入既有規則

**說明：** 讓代理在選圖型時找得到 emoji，並修改與它衝突的既有規則。

**驗收條件：**
- [ ] `explainer-figure/SKILL.md` § Choosing the figure type 加入一列「只需要辨識的物件」，指向 `references/emoji.md`
- [ ] `pictorial.md` 的「物件要自己畫，不用圖示」改為允許 emoji 的例外（規格 R3 第 4 點）
- [ ] `icons.md` 中「器官等不在子集中的物件改畫具象插圖」一句，改為先查 `emoji.md`
- [ ] 若 T4 有觸發，一併改寫 explainer-figure 的 description 或隱藏方式，並請使用者重測

**驗證：**
- [ ] `wc -l skills/explainer-figure/SKILL.md` 不超過約 130
- [ ] `claude plugin validate .` 通過

**相依：** T9　**檔案：** `explainer-figure/SKILL.md`、`pictorial.md`、`icons.md`　**規模：** S

#### T11 Starship 圖 4 殘影版（V2）

**說明：** 以 P5 重畫 `examples/starship-reusability/starship-reusability.html` 的圖 4。先在暫存副本中完成，等檢查點 B 由使用者決定是否取代範例。

**驗收條件：**
- [ ] 助推器畫成物件，每一步顯示它的姿態；「翻轉」與「折返」看得出來
- [ ] 保留 L2 stepper，每一幀多顯示一個姿態
- [ ] 與原版並排截圖

**驗證：** 壓線檢查與 `explainer-page/SKILL.md` 第 6 步的自檢都通過。

**相依：** T8　**檔案：** 暫存副本、本計畫檔　**規模：** S

#### 檢查點 B

- [ ] 使用者判讀 Starship 圖 4 新舊版，決定是否取代範例（取代時把暫存副本的圖 4 寫回範例，並重跑自檢）
- [ ] 提供 `git add` 範圍與提交訊息

### 第 3 階段：驗收與收尾

#### T12 新主題頁（V7）

**說明：** 使用者在本任務開始前指定主題。以新規則產出 1 頁，用到符號對照、自繪物件（含姿態或殘影）與 emoji。

**驗收條件：**
- [ ] 使用者已指定主題
- [ ] 頁面用到 R1、R3、R4 三項
- [ ] 回報時列出每張圖用到的規則

**驗證：**
- [ ] `explainer-page/SKILL.md` 第 6 步的自檢、壓線檢查、emoji 與圖示同步指令都通過
- [ ] 使用者判讀

**相依：** T10、T11　**檔案：** 本機頁面、本計畫檔　**規模：** M

#### T13 版本與文件

**說明：** 升版並更新說明文件。

**驗收條件：**
- [ ] 四個 manifest 檔升為 0.5.0
- [ ] `CLAUDE.md`〈架構〉加入 `scripts/check-overlap.js`、`assets/emoji/`、`references/emoji.md`
- [ ] `README.md`、`README.zh-TW.md` 提到符號對照與 emoji（只寫現況，不引用計畫文件）
- [ ] 構想文件〈Key Assumptions to Validate〉與規格〈待驗證的假設〉依結果勾選
- [ ] `docs/plan/README.md` 第 05 列的版本與狀態

**驗證：**
- [ ] `CLAUDE.md`〈驗證指令〉全部執行並通過
- [ ] `claude --plugin-dir . plugin details explain-as-webpage` 確認兩個 skill 都載入

**相依：** T12　**檔案：** manifest（4 個）、`CLAUDE.md`、README（2 個）、構想與規格文件、索引　**規模：** M

#### 檢查點 C

- [ ] 規格〈7. 成功條件〉全部達成
- [ ] 提供最終的 `git add` 範圍與提交訊息

## Risks and Mitigations

| 風險 | 影響 | 處理方式 |
|---|---|---|
| emoji 的漸層放在共用的隱藏 `<svg>` 中時不顯示 | 高 | T1 在兩種截圖中探測；不行時改為逐圖內嵌，並在 id 加上圖號前綴 |
| Noto Emoji 的風格與粗外框不搭 | 中 | 檢查點 0 由使用者判讀並排截圖；不行時回到規格，重新評估插圖庫 |
| 壓線檢查誤報太多，代理不採信 | 中 | T3 以 V4 作為門檻；以 `data-touch` 排除本來就應接觸的元素 |
| SVG 文字中的組合字元（x̂）顯示錯位 | 低 | T5 截圖確認；錯位時改用 `<tspan>` 疊加符號 |
| `explainer-figure/SKILL.md` 超過約 130 行 | 低 | 細節放進 references；每個修改它的任務都量測行數 |
| 一頁的上色符號超過 5 個 | 低 | R1 規定只有關鍵概念的符號上色，其餘只標註 |

## Open Questions

- 驗收用的新主題：使用者在 T12 開始前指定。
- `.sym` 與風格 class 的正式名稱：T5、T8 實作時確定。
- Noto Emoji 的發行版與子集內容：T1 決定。

## 結果

各任務完成後，在此依任務編號記錄探測數據、截圖路徑、判讀結果與規則的調整。
