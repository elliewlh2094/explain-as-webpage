# 符號對照圖與具象插圖品質（symbols and pictorial）

## Problem Statement

我們如何讓頁面上的圖直接連結公式符號與實際物件（機器人、感測器、量測值），並穩定畫出可辨識、可切開標註的具象物件，同時維持單一 HTML 檔與現有的配色規則？

起因（使用者 2026-10-07 提出）：

1. **頁面大小上限是否限制表現力。** 使用者認為 `SKILL.md` 第 6 步的 150 KB 上限可能影響頁面品質，並提議依需求分級（動畫用高規格、流程圖用低規格）。量測結果（2026-10-07）：7 個範例頁為 28–53 KB，最大的一頁只用到上限的 35%；stepper 最多的 `llm-wiki.html`（43 KB）與 `autoresearch.html`（36 KB）也遠低於上限。150 KB 沒有限制住任何一頁。真正限制表現力的是篇幅預算（`writing-rules.md` § Length budget：2–6 張圖、最多 2 個 stepper、每個 ≤ 8 步）、「選最低層級」的規則、不可使用外部資源，以及繪圖品質。
2. **具象物件。** 使用者提供 5 張參考圖：人體（實心剪影）、背包（線條）、樹與地球（粗外框加平塗色）、胃（無外框的平塗色）。問題不是畫不出人體，而是畫不出有一定具象程度的物件；使用者可能問任何主題。`pictorial.md` 為了避免外形歪掉，刻意只允許用簡單形狀組合，所以這是能力上限，不是缺陷。
3. **使用者認為需要動畫的 4 個例子。** 逐一檢查後，只有兩個主要缺連續運動：

| 例子 | 現況的問題 | 主要缺少的能力 | 連續動畫的必要性 |
|---|---|---|---|
| `examples/starship-reusability/` 圖 4（助推器返回） | 只畫軌跡線，沒有畫助推器本身，看不到「翻轉、折返」的姿態變化 | 物件與姿態 | 高：沿路徑移動並旋轉 |
| 使用者的 EKF 頁（`~/Documents/explainers/extended-kalman-filter/`）圖 3 | stepper 結構正確，但機器人只是一個點，圖上沒有 x̂、P、z、K | 符號對照 | 中：不確定性橢圓隨行走連續變大 |
| 機器人導航課程的 Motion Planning 單元（使用者的課程影片截圖） | 投影片有圖，但 Path Planning → Curve Interpolation → Trajectory Planning → Feedback Control 四個階段的圖彼此沒有連結 | 同一個場景（同一張地圖、同一台車）貫穿各階段 | 中到高：Feedback Control 的偏差修正是連續運動 |
| 教科書與課程的公式（例如 Kalman Filter 的預測與更新式） | 符號只出現在公式裡，圖上找不到它對應的部位 | 符號對照 | 低 |

`writing-rules.md` § Ground the symbols in one running example 已要求一張「符號 → 例子中的意義」對照表，但那是文字；圖本身仍然沒有符號。

## Recommended Direction

第 5 輪做兩個方向：D（符號對照圖）與 A（具象插圖品質）。

**D：符號對照圖。** 圖上的部位直接標出符號（機器人位置標 x̂ₖ、不確定性橢圓標 Pₖ、光達量測線標 zₖ）；公式中的同一個符號使用與圖上部位相同的概念色（`c1`–`c5`，與「關鍵概念最多 5 個」一一對應）。讀者看到公式中的 Pₖ，就能在圖上找到同色的橢圓。規則放在 `explainer-figure`，`writing-rules.md` 的符號段落加一行引用。

**A：具象插圖品質。** 分成 3 部分：

1. **壓線檢查腳本**：在 headless Chrome 中取得文字框與線段、箭頭的邊界，報告相交位置。引線（`lead`、`pin`）等本來就應接觸文字的元素以 class 排除。來源是 backlog 原有項目（第 4 輪 T12 回饋第 9 項）。
2. **插圖風格規範**：採用「粗外框＋平塗色」一種風格，與現有 `outline` class 最接近。規範包含線寬、填色、比例、標籤與引線位置、品質檢查清單；外形規則的物件（人、背包、俯視機器人、俯視車、火箭）用基本形組合，並畫出姿態（朝向）。規範也收錄「殘影」：在路徑上畫多個淡色姿態，表示物件隨時間的位置與朝向。殘影是靜態圖，L3 完成前就能改善 Starship 圖 4 這類問題。原 backlog 的「更自然的人體剪影」併入這裡。
3. **插圖庫子集**：外形複雜、只需辨識的物件（地球、樹、器官）從 Noto Emoji 取用，做法同 Lucide 圖示：子集放進儲存庫，產頁時只複製用到的圖，不從網路下載。基本形負責「結構」（切開、分層、標註部位），插圖庫負責「辨識」。

第 5 輪另外處理一項跨輪驗證：Codex 是否會自動觸發 explainer-figure（原 backlog 第 11 項）。第 5 輪會修改 explainer-figure，順便處理的成本低。

使用者已確認（2026-10-07）：

- 範圍：第 5 輪做 D 與 A；之後先做 C（explainer-cite），再做 B（規格表＋L3）。見〈後續輪次〉。
- 具象物件來源：混合。插圖庫負責辨識，基本形加風格規範負責結構。
- 插圖風格：粗外框＋平塗色（使用者參考圖中樹與地球的風格）。
- 插圖庫：Noto Emoji，使用者認為與粗外框風格還算接近。
- `<slug>.assets/` 的使用條件：頁面引用點陣圖時才允許，不以規格高低決定。
- 不放寬 150 KB 上限。

## Key Assumptions to Validate

- [ ] 符號對照能讓公式更容易理解 —— 用 D 的規則改版 EKF 頁的圖 3 與公式段落，與原版並排，由使用者判讀。
- [ ] 風格規範能讓代理穩定畫出外形規則的物件 —— 人、背包、俯視機器人、俯視車、火箭各畫 3 次，檢查外形是否一致、是否歪掉。
- [ ] 殘影能在沒有動畫的情況下表現姿態變化 —— 用殘影重畫 Starship 圖 4，確認讀者看得出「翻轉」與「折返」。
- [ ] Noto Emoji 子集的授權、大小與風格可以接受 —— 查閱 LICENSE 原文確認圖檔的授權條款；選 30 個常用物件量測大小；放進範例頁，與粗外框的自繪插圖並排，確認風格不突兀（Noto Emoji 大多沒有深色外框）。
- [ ] 壓線檢查腳本的誤報少到代理會採信結果 —— 以第 4 輪記錄的壓線案例重建測試資料（見 Open Questions），計算漏報與誤報數量。
- [ ] Codex 不會在一般繪圖提示中自動觸發 explainer-figure —— 在 Codex 中重跑第 4 輪 T4 的 5 個圖表提示；若會觸發，改寫 description 或改用其他隱藏方式。

## MVP Scope

**做：**

- D：`explainer-figure` 加入符號標註與公式上色規則；`writing-rules.md` § Ground the symbols in one running example 加一行引用。是否需要在 `template.html` 新增 HTML 文字用的概念色 class，實作時確認。
- A1：壓線檢查腳本，並寫進 `explainer-figure/SKILL.md` § Self-check。
- A2：插圖風格規範（含姿態與殘影），寫進 `pictorial.md` 或新的 reference。
- A3：Noto Emoji 子集、LICENSE 與同步指令，做法比照 `icons.md`。
- Codex 自動觸發 explainer-figure 的實測。
- 驗收：
  - 改版 EKF 頁的圖 3 與公式段落，與原版並排比較。
  - 以殘影重畫 Starship 圖 4，與原版並排比較。
  - 以一個需要辨識型物件的主題產出 1 頁，用到插圖庫與自繪插圖。
  - 其餘範例重新截圖，確認沒有退化。
  - 兩個 `SKILL.md` 各自維持約 130 行以內；`CLAUDE.md` 的驗證指令全部通過。

**不做：** 公式與圖的滑鼠連動、L3 動畫、引用點陣圖。

## Not Doing (and Why)

- **放寬 150 KB 上限** —— 範例頁最大只用到上限的 35%，上限沒有限制住任何一頁。
- **規格表與 L3** —— 延到 C 之後。殘影先處理一部分姿態問題。
- **explainer-cite** —— 涉及授權、截圖與 assets 資料夾，獨立成一輪。
- **公式與圖的滑鼠連動（指到公式項目時圖上部位亮起）** —— 先驗證靜態的標註與上色是否足夠，不夠才加。
- **多種插圖風格** —— 同一頁的圖會不一致；只定一種。
- **用手寫座標描繪有機形狀（胃、大陸輪廓）** —— 外形不穩定；改由插圖庫提供，插圖庫沒有的物件留給 explainer-cite。
- **C 類計算圖** —— 每張圖都要寫程式，排在 cite 之後。

## Open Questions

- 壓線檢查的測試資料從哪裡來？第 4 輪的壓線問題都已修正，修正前的頁面沒有留存。已知案例記錄在 `docs/plan/04-visual-forms-plan.md`：T2 結果表（「側袋」標籤壓到包身、虛線箭頭穿過標籤、`sm` 標籤壓到長條左緣）與 T12 延伸的逐圖截圖列（Unity 頁 Step 1、2 的箭頭穿過檔名與欄位名、Step 4、5 的註解與引線重疊）。建議依這些描述在現有頁面的副本中重新放入缺陷。
- 公式中的符號上色，是否需要在 `template.html` 新增 HTML 文字用的概念色 class？實作時確認。
- Noto Emoji 子集要收哪些物件、多少個？建議比照第 4 輪圖示的做法，先統計範例與新主題實際需要的物件。
- 版本號是否升為 0.5.0？

## 後續輪次（原第 5 輪 backlog）

以下項目來自 2026-10-07 的 backlog 暫存清單，依使用者決定的順序排列。原清單引用的 `docs/ideas/`、`docs/specs/`、`tasks/` 路徑已改為 `docs/plan/` 中的現行檔名。

### 第 6 輪候選：explainer-cite（引用既有圖片）

- 內容：查詢開放授權圖庫、以 headless Chrome 截取公開網頁、PIL 裁切壓縮、寫入 `<slug>.assets/`、圖說附作者與授權；受版權保護的圖在確認步驟逐張列出。需要登入的頁面由使用者自己截圖。
- 已決定：只有引用點陣圖的頁面才允許 `<slug>.assets/`。
- 待決：`<slug>.assets/` 每頁一個資料夾，或整個主題共用一個。
- 影響：打破「單檔、沒有額外資料夾」的規則，需要改 `SKILL.md` 第 5、6 步與 Red Flags。
- 出處：`docs/plan/04-visual-forms-idea.md`（A 類、第二階段）。

### 第 7 輪候選：規格表＋L3

- 規格表：把 `SKILL.md` 第 3 步的層級表與 `writing-rules.md` 的篇幅預算合併。每個層級一列，寫出回答哪一類問題、圖數上限、stepper 數與步數上限、檔案大小上限、產頁成本。只在較高的層級放寬圖數與步數上限。
- 第 4 步的確認改為逐圖描述預期效果：圖的形式（例如「stepper 6 步」或「連續動畫約 4 秒」）、讀者會看到什麼、降一級會失去什麼。使用者希望維持「代理建議、使用者修改」，但代理要描述得更清楚，讓使用者能判斷是否調整。
- L3：使用者決定直接使用 anime.js（MIT，v4 完整版約 24.5 KB，可內嵌 UMD 單檔），仍是單一 HTML 檔。24.5 KB 加上目前最大的範例頁（53 KB）仍在 150 KB 上限內。動工前要定義 L3 回答哪一類核心問題（例如沿路徑的運動與姿態變化、連續變形）。
- 自檢：連續動畫無法只看單一畫面，要讓動畫停在多個時間點分別截圖。
- 驗證案例：Starship 助推器返回、Motion Planning 的 Feedback Control。
- 出處：`docs/plan/04-visual-forms-idea.md` Open Questions；本文件〈Problem Statement〉。

### 之後：C 類計算圖

- 內容：以假設範例在頁面內實際運算後畫出的圖（例如 Welch Labs 的雜訊到影像），不用方框代替。
- 成本：每張圖都要寫程式；排在 explainer-cite 之後。
- 出處：`docs/plan/04-visual-forms-idea.md`（C 類）。

### 跨輪驗證（下次產頁時順便觀察）

- Codex 不指定 skill 名稱時能否觸發 explainer-page。出處：`docs/plan/03-material-modes-plan.md` T16。
- 代理在第 7 步是否主動列出每張數值圖的單位與理由（讀圖四問）。出處：`docs/plan/03-material-modes-figure-values.md`。
- 第 3 輪未驗證的情境：Paul Graham 長文、Harness Engineering 的演進、LightGlue。出處：`docs/plan/03-material-modes-spec.md` §10。
- 輔助 skill 自帶的提問或輸出檔是否破壞「只確認一次、只輸出一個檔案」。出處：`docs/plan/03-material-modes-spec.md` §6。
- 沒有網路工具時的退路（使用者在第 3 輪決定不測，列出備查）。出處：`docs/plan/03-material-modes-plan.md` T16。
