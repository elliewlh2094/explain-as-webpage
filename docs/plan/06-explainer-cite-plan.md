# 實作計畫：引用既有圖片（explainer-cite）與第 5 輪留下的修正（第六輪）

構想見 `docs/plan/05-symbols-pictorial-idea.md`〈後續輪次〉，規格見 `docs/plan/06-explainer-cite-spec.md`。本文件同時是待辦清單：〈進度總覽〉每項一行，完成時勾選並補一句結果；各任務的驗收條件也逐項勾選；探測與驗收的細節記在〈結果〉。

## 進度總覽

### 第 0 階段：探測（不改產品檔案）
- [ ] T1 授權欄位：Commons、Openverse、NASA、MDPI 文章頁、arXiv LightGlue 摘要頁
- [ ] T2 圖片處理：WebP 大小與畫質、`pdftoppm` 裁切、Chrome 區域截圖、`<svg><image>` 在各種截圖中的顯示、壓線檢查對 `<image>` 的誤報
- [ ] T3 層級示意圖的重製方式：以舊頁重產，與現有檔比對

#### 檢查點 0
- [ ] 使用者確認授權分類、大小上限、層級示意圖的重製方式

### 第 1 階段：第 5 輪留下的修正（R7、R8）
- [ ] T4 `ink-shade` 不再染到外框：`parts.py`、`pictorial.md`、Starship 與 llm-wiki 範例
- [ ] T5 autoresearch 3 頁改用目前模板的 CSS，重截層級示意圖

#### 檢查點 A
- [ ] 使用者判讀放大截圖與新舊層級示意圖；提供提交建議

### 第 2 階段：explainer-cite 規則（R1–R5）
- [ ] T6a `skills/explainer-cite/`：`SKILL.md`、references、scripts
- [ ] T6b explainer-page 與 explainer-figure 的整合、模板的 `figure img` 樣式、示範截圖

#### 檢查點 B
- [ ] 使用者確認規則與示範截圖；提供提交建議

### 第 3 階段：驗收案例
- [ ] T7 EKF 頁 v3：論文照片加引線、差速運動學圖（V1、V5）
- [ ] T8 LightGlue 論文的 document 模式頁（V2）
- [ ] T9 Wikimedia 主題頁（V3；使用者先指定主題）
- [ ] T10 公開網頁截圖（V4；使用者先指定主題，可與 T9 同頁）

#### 檢查點 C
- [ ] 使用者判讀 4 個案例；提供提交建議

### 第 4 階段：收尾
- [ ] T11 版本 0.6.0、`CLAUDE.md`、README、構想文件的後續輪次、索引狀態

#### 檢查點 D
- [ ] 規格〈7. 成功條件〉全部達成；提供最終提交建議

## Overview

本輪讓 explainer-page 能在讀者需要看到真實物件、介面或原文圖表時，引用既有的點陣圖：

- 新增第三個 skill `explainer-cite`，負責取得圖片、查證授權、裁切壓縮、放進 `<hub>.assets/`、需要時加上引線與符號標籤。
- 頁面仍是一個 HTML 檔，只在引用點陣圖時多一個由整個主題共用的資產資料夾。
- 自由授權的圖直接使用；受限的圖在確認步驟逐張列出，由使用者決定。

另外處理第 5 輪檢查點 D 留下的 3 項：`ink-shade` 染到外框、autoresearch 範例的舊 CSS，以及 EKF 頁的機器人圖（兼作 explainer-cite 的第一個驗收案例）。

## Architecture Decisions

使用者已確認的決策列在規格〈0. 問題陳述與範圍〉。規劃時的補充：

1. **第三個隱藏 skill。** explainer-cite 比照 explainer-figure：frontmatter 設 `disable-model-invocation: true`、`user-invocable: false`，只由 explainer-page 以相對路徑讀取。取得與授權屬於「圖從哪裡來」，與 explainer-figure 的「圖怎麼畫」分開；兩個 `SKILL.md` 也都沒有空間放這些規則。
2. **標註沿用 explainer-figure。** 標註引用圖時，`<svg>` 中的引線、符號與概念色都用 explainer-figure 的既有規則。explainer-cite 只寫 `<image>` 的放法與「標籤放在圖片外側」這一條，不另寫一套標註規則。
3. **`explainer-page/SKILL.md` 的行數預算。** 它已有 130 行，本輪必須修改 6 處（規格 R5 第 1 點）。修改以改寫既有句子為主，淨增以 2 行為上限；資產檢查的指令放在 explainer-cite，第 6 步只寫一行引用。超過時，把第 6 步既有的部分說明移到 references。
4. **腳本只用 Python 標準函式庫加選用的 Pillow。** 授權查詢只需要 `urllib` 與 `json`。裁切壓縮優先用 Pillow，缺少時退回 `pdftoppm` 與 Chrome 輸出 PNG。不新增 Node 這項依賴。
5. **最高風險先探測。** API 是否能存取、`<image>` 在既有檢查中的行為、層級示意圖能否重現，三項都在第 0 階段完成，先於任何產品檔案的修改。
6. **第 5 輪的修正先做。** R7、R8 與 explainer-cite 沒有共用的介面，風險低，先做可以讓範例在 explainer-cite 的修改之前就處於乾淨的狀態。R8 必須在 T7 之前完成，因為 T7 的差速圖會用到 `parts.py robot`。
7. **探測檔案。** 探測與試作放在 session 的暫存目錄，不進儲存庫；需要保留的截圖放 `temp/round-06/`（gitignored），結果與路徑記在〈結果〉。文件不記 session 暫存路徑。
8. **驗收頁不進版本控制。** V1–V4 的頁面與資產資料夾放在預設輸出目錄，只在本機。
9. **提交方式。** 實作過程不自行 `git commit`；每個檢查點提供 `git add` 範圍與提交訊息。下一個任務會改到未提交的同一批檔案時，先提醒使用者提交。
10. **版本號。** 本輪新增 skill，收尾時升為 0.6.0，四個 manifest 檔同步。

### 相依圖

```
T1 授權欄位 ─┐
T2 圖片處理 ─┼─ 檢查點 0 ─┬─ T6a explainer-cite ── T6b 整合 ── 檢查點 B ─┬─ T7 EKF v3 ─┐
T3 層級示意圖 ┘           │                                           ├─ T8 LightGlue ├─ 檢查點 C ── T11 ── 檢查點 D
                          ├─ T4 ink-shade ─────────────────────────────┘（T7 需要 T4） │
                          └─ T5 autoresearch ── 檢查點 A               ├─ T9 Wikimedia ─┤
                                                                      └─ T10 網頁截圖 ┘
```

- T4、T5 與 T6a、T6b 互不相依，可以交錯進行；但 T4 會改 `examples/`，T5 會改 `examples/` 與 `docs/images/`，兩者完成後先過檢查點 A 再開始 T6a，避免同一批未提交的檔案混在一起。
- T7–T10 彼此獨立，順序依使用者指定主題的時間決定。

## 第 0 階段：探測

#### T1 授權欄位

**說明：** 以 `curl` 取回每個來源的授權資訊，確認欄位名稱與格式，作為 T6a 腳本的依據。

**驗收條件：**
- [ ] Wikimedia Commons：`prop=imageinfo&iiprop=url|size|extmetadata&iiurlwidth=1440` 回傳的作者（`Artist`）、授權（`LicenseShortName`、`LicenseUrl`）、縮圖網址欄位記錄完成，各附一個範例值。
- [ ] Openverse：查詢 API 回傳的 `license`、`license_version`、`creator`、`foreign_landing_url` 記錄完成；確認不需要 API 金鑰時的速率限制。
- [ ] NASA Image and Video Library API：回傳欄位與公有領域聲明的位置記錄完成。
- [ ] MDPI *Sensors* 25(11):3553 文章頁：確認授權為 CC BY 4.0，取得作者、標題、DOI 與圖 1 的圖說。
- [ ] arXiv LightGlue 摘要頁：記錄授權欄位（arXiv 的預設授權不允許改作時，V2 的圖屬於受限）。

**驗證：** 每個來源的 `curl` 指令與輸出摘錄記在〈結果〉T1。

**相依：** 無。**可能動到的檔案：** 無（暫存目錄）。**規模：** S。

#### T2 圖片處理

**說明：** 量測圖片處理的大小與畫質，並確認 `<svg><image>` 在既有檢查中的行為。

**驗收條件：**
- [ ] 照片（MDPI 圖）、截圖（一個公開網頁）、PDF 圖（LightGlue 圖 1）各以 1440px 與 720px 寬、WebP 有損（品質 70、80、90）與無損、PNG 輸出，記錄大小並並排截圖判讀畫質；提出單張與資料夾大小上限的數值與依據。
- [ ] `pdftoppm -x -y -W -H` 與 headless Chrome 的區域截圖都能在沒有 Pillow 的情況下輸出 PNG。
- [ ] 一個暫存頁中放入 `<img>` 與 `<svg><image>` 各一張：寬版截圖、390px iframe（`<title>ok`）、只看圖截圖、遮住文字截圖中都能顯示。
- [ ] 同一個暫存頁加上引線與外側標籤，壓線檢查沒有誤報；故意讓一個標籤壓在引線上時能抓到。
- [ ] 既有的外部資源檢查（`grep -nE '(src=|url\()…'`）是否涵蓋 `<image href="https://…">`；不涵蓋時，記下 T6a 要補的寫法。

**驗證：** 大小表與截圖路徑（`temp/round-06/t2/`）記在〈結果〉T2。

**相依：** T1（取得 MDPI 圖的授權後才放進並排截圖）。**可能動到的檔案：** 無。**規模：** M。

#### T3 層級示意圖的重製方式

**說明：** 找出 `docs/images/tier-l0-figure.png`、`tier-l1-slider.gif`、`tier-l2-stepper.gif` 的產生方式（commit `9e5e754` 與當時的記錄），並以舊頁重產一次。

**驗收條件：**
- [ ] 記錄三個檔案的像素尺寸、GIF 的幀數、每幀時間與循環設定。
- [ ] 以本機工具（headless Chrome 截圖，PIL 組 GIF；本機沒有 ImageMagick）從目前的 autoresearch 頁重產三個檔案，尺寸與幀數和現有檔案相同；PNG 與現有檔案逐位元組相同，或差異只來自字型算圖並記錄原因。

**驗證：** 指令與比對結果記在〈結果〉T3。

**相依：** 無。**可能動到的檔案：** 無。**規模：** S。

#### 檢查點 0

- [ ] 使用者確認 T1 的授權欄位、T2 的大小上限、T3 的重製方式。arXiv 預設授權的處理已在規劃時確認（規格〈0〉，2026-10-16）。

## 第 1 階段：第 5 輪留下的修正

#### T4 `ink-shade` 不再染到外框（R8、V6）

**說明：** 修改 `parts.py` 的 `group()`，讓陰影不蓋住外框，並重新產生所有由 `parts.py` 產生的片段。

**驗收條件：**
- [ ] 比較至少兩種做法（例如陰影畫在外框之前、陰影之後重畫只有外框的形狀），以 4 倍放大截圖選出背光側外框只有 `--text` 色、且輸出最短的做法。
- [ ] 零件總覽圖（`parts.py sheet`）在正常大小下與修改前並排，外觀相同。
- [ ] `pictorial.md` 中由 `parts.py` 產生的片段，與對應指令的輸出逐字相同；文件中的 `parts.py` 指令都以 0 結束。
- [ ] `examples/starship-reusability/` 與 `examples/llm-wiki/` 中的物件改用新輸出；llm-wiki 圖 5 手寫的摺角陰影一併檢查。

**驗證：**
- [ ] 7 個範例頁的壓線檢查沒有輸出。
- [ ] 2 個修改的範例頁：`FILL` 為 0、沒有外部資源、390px 為 `<title>ok`、DOM 對比掃描兩種寬度都是 `<title>none`。
- [ ] 放大截圖與並排截圖存於 `temp/round-06/t4/`。

**相依：** 檢查點 0。**可能動到的檔案：** `skills/explainer-figure/scripts/parts.py`、`skills/explainer-figure/references/pictorial.md`、`examples/starship-reusability/starship-reusability.html`、`examples/llm-wiki/llm-wiki.html`。**規模：** M。

#### T5 autoresearch 改用目前模板的 CSS（R7、V7）

**說明：** 3 頁的 `<style>` 換成目前模板的版本，再以 T3 的做法重截三張層級示意圖。

**驗收條件：**
- [ ] 3 頁的 `<style>` 與目前模板相同；文字、圖與圖說不變（`diff` 只出現在 `<style>` 內）。
- [ ] DOM 對比掃描在 1280px 與 700px 都是 `<title>none`（原本有 6 組低於 4.5:1）。
- [ ] 三張層級示意圖以 T3 的參數重截，尺寸與幀數和舊檔相同；新舊並排截圖存於 `temp/round-06/t5/`。

**驗證：**
- [ ] 3 頁：`FILL` 為 0、沒有外部資源、390px 為 `<title>ok`、壓線檢查沒有輸出。
- [ ] 頁面樹檢查（`extending-pages.md` §5）沒有輸出。

**相依：** T3、檢查點 0。**可能動到的檔案：** `examples/autoresearch/*.html`（3 個）、`docs/images/tier-*`（3 個）。**規模：** M。

#### 檢查點 A

- [ ] 使用者判讀 T4 的放大截圖與 T5 的新舊層級示意圖；提供 `git add` 範圍與提交訊息。

## 第 2 階段：explainer-cite 規則

#### T6a `skills/explainer-cite/`（R1–R4）

**說明：** 新增 skill 的 `SKILL.md`、references 與 scripts。

**驗收條件：**
- [ ] `SKILL.md`：frontmatter（隱藏設定與 description）、輸入輸出、引用與自繪的判準、3 種來源、授權分類與受限圖的處理、資產資料夾規則、資產檢查指令。約 130 行以內。
- [ ] references：來源與授權的細節（各 API 的指令與欄位、PDF 與網頁的取得方式、CC BY-SA 的圖說寫法），以及標註引用圖的配方（附一段可直接複製的片段）。
- [ ] scripts：授權查詢（Commons 檔名或 Openverse 查詢字串 → 作者、授權、連結）與裁切壓縮（原圖、裁切範圍、寬度 → 圖檔與大小）；只用 Python 標準函式庫，裁切壓縮在沒有 Pillow 時印出退路指令。
- [ ] 文件中的每個指令都實際執行一次並以 0 結束；資產檢查在乾淨的暫存主題上沒有輸出，故意刪掉一個圖檔或留下一個未引用的圖檔時各印出一行。

**驗證：**
- [ ] `wc -l skills/explainer-cite/SKILL.md` 約 130 行以內。
- [ ] `claude plugin validate .` 通過；`claude --plugin-dir . plugin details explain-as-webpage` 顯示 3 個 skill，explainer-cite 不在 always-on 的 token 成本中。

**相依：** 檢查點 0、檢查點 A。**可能動到的檔案：** `skills/explainer-cite/SKILL.md`、`skills/explainer-cite/references/*.md`（2 個）、`skills/explainer-cite/scripts/*`（1–2 個）。**規模：** M。

#### T6b explainer-page 與 explainer-figure 的整合（R1 第 4 點、R5）

**說明：** 修改 explainer-page 的 6 處、兩個 references、模板，以及 explainer-figure 的圖型表。

**驗收條件：**
- [ ] `skills/explainer-page/SKILL.md` 依規格 R5 第 1 點修改 6 處，總行數 ≤ 132。
- [ ] `extending-pages.md`、`writing-rules.md` 依 R5 第 3、4 點修改；`explainer-figure/SKILL.md` 圖型表新增一列。
- [ ] `template.html` 新增 `figure img` 樣式；不新增顏色。
- [ ] 以一張自由授權圖（T1 取得的 Commons 圖）做一個暫存示範頁：一張 `<img>`、一張標註的 `<svg><image>`，截圖存於 `temp/round-06/t6b/`。

**驗證：**
- [ ] `CLAUDE.md`〈驗證指令〉的模板檢查全部通過（外部資源、兩種寬度、DOM 對比掃描）。
- [ ] 示範頁通過資產檢查、壓線檢查與 390px 檢查。
- [ ] `wc -l skills/*/SKILL.md` 三個都約 130 行以內。

**相依：** T6a。**可能動到的檔案：** `skills/explainer-page/SKILL.md`、`skills/explainer-page/references/extending-pages.md`、`skills/explainer-page/references/writing-rules.md`、`skills/explainer-page/assets/template.html`、`skills/explainer-figure/SKILL.md`。**規模：** M。

#### 檢查點 B

- [ ] 使用者確認 T6a、T6b 的規則與示範截圖；提供 `git add` 範圍與提交訊息。

## 第 3 階段：驗收案例

V1–V4 共同的檢查（規格 §5）：資產檢查沒有輸出、`FILL` 為 0、沒有外部資源、390px 不溢出、壓線檢查沒有輸出、HTML ≤ ~150 KB、資產資料夾符合大小上限。每個案例都依 explainer-page 的 7 步流程進行，包含第 4 步的確認；確認訊息與回報的內容記在〈結果〉，用來檢查受限圖是否逐張列出。

#### T7 EKF 頁 v3（R6、V1、V5）

**驗收條件：**
- [ ] 以 v2 為基礎另存 v3（本機，不覆寫 v2）。
- [ ] 〈本頁的例子〉引用 MDPI 照片：圖說有作者、標題、CC BY 4.0、連結與「標註為本頁加上」；引線標出 LIDAR、IMU、編碼器，並連到頁面的符號。
- [ ] 差速運動學圖：`parts.py robot` 俯視機器人，標出 x、y、θ、v、ω 與輪距，與公式、符號對照表同色；遮住文字的截圖中可辨認機器人與朝向。
- [ ] 通過共同檢查與意圖檢查；v2、v3 並排截圖存於 `temp/round-06/t7/`；由使用者判讀。

**相依：** T4、檢查點 B。**規模：** M。

#### T8 LightGlue 論文的 document 模式頁（V2）

**驗收條件：**
- [ ] 從 arXiv PDF 以 `pdftoppm` 裁出頁面討論的圖；授權依 T1 的結果分類，受限時逐張列在確認中。
- [ ] 圖說與 Sources 有作者、標題、授權與連結。
- [ ] 通過共同檢查；由使用者判讀。同時記錄第 3 輪未驗證的 LightGlue 情境（`docs/plan/03-material-modes-spec.md` §10）的觀察結果。

**相依：** 檢查點 B。**規模：** M。

#### T9 Wikimedia 主題頁（V3）

**驗收條件：**
- [ ] 使用者在任務開始前指定主題。
- [ ] 以 Commons 或 Openverse API 查得候選圖，授權欄位來自 API；確認訊息列出候選圖與授權。
- [ ] 圖說與 Sources 一致；通過共同檢查；由使用者判讀。

**相依：** 檢查點 B。**規模：** M。

#### T10 公開網頁截圖（V4）

**驗收條件：**
- [ ] 使用者在任務開始前指定主題；可與 T9 同頁。
- [ ] 只截公開頁；遇到登入牆或 cookie 同意牆時停止並回報。
- [ ] 截圖逐張列在確認中（出處、授權、用途、修改）；通過共同檢查；由使用者判讀。

**相依：** 檢查點 B。**規模：** S–M。

#### 檢查點 C

- [ ] 使用者判讀 T7–T10；提供 `git add` 範圍與提交訊息（驗收頁不進版本控制，只提交文件與修正）。

## 第 4 階段：收尾

#### T11 版本與文件

**驗收條件：**
- [ ] 4 個 manifest 檔升為 0.6.0。
- [ ] `CLAUDE.md`：〈專案現況〉的「兩個 agent skill」改為三個；〈架構〉加入 `skills/explainer-cite/` 與 `<hub>.assets/` 的例外。
- [ ] `README.md`、`README.zh-TW.md`：skill 清單與「單一 HTML 檔」的說明加入資產資料夾的例外。
- [ ] `docs/plan/05-symbols-pictorial-idea.md`〈後續輪次〉的第 6 輪候選與第 5 輪留下的項目標為已完成；〈跨輪驗證〉加入「Codex 是否依相對路徑讀取 explainer-cite」。
- [ ] 規格〈待驗證的假設〉逐項勾選並附結果；`docs/plan/README.md` 第 06 列的狀態改為已完成。

**驗證：**
- [ ] `CLAUDE.md`〈驗證指令〉全部通過；`plugin details` 顯示 3 個 skill。

**相依：** 檢查點 C。**可能動到的檔案：** 4 個 manifest、`CLAUDE.md`、2 個 README、2 個 `docs/plan/` 文件。**規模：** M。

#### 檢查點 D

- [ ] 規格〈7. 成功條件〉全部達成；提供最終的 `git add` 範圍與提交訊息。

## Risks and Mitigations

| 風險 | 影響 | 對策 |
|---|---|---|
| Pillow 不一定安裝在使用者的機器上 | 中 | 裁切壓縮退回 `pdftoppm` 與 Chrome 輸出 PNG；確認訊息說明檔案會較大，安裝由使用者決定 |
| 圖庫 API 在 sandbox 或網路環境中被擋 | 中 | T1 先確認；被擋時請使用者核准網路存取，或改用使用者材料中的圖 |
| `explainer-page/SKILL.md` 超過約 130 行 | 中 | 以改寫取代新增，指令細節放 explainer-cite；仍超過時把第 6 步的部分說明移到 references |
| arXiv 預設授權不允許改作，V2 無法裁切 | 中 | T1 先確認；受限時依 R2 逐張列出，由使用者決定，或改用作者以 CC BY 釋出的版本（處理方式已確認，2026-10-16） |
| CC BY-SA 的相同方式分享義務 | 低 | 圖說寫明標註後的圖依 CC BY-SA 釋出（R2 第 4 點） |
| 層級示意圖無法重現 | 中 | T3 先以舊頁重產比對；無法重現時，記錄差異並由使用者決定是否接受新的尺寸或幀數 |
| `<image>` 在只看圖截圖中被隱藏，或壓線檢查誤報 | 中 | T2 先確認；需要時修改截圖指令或 `check-overlap.js` 的排除規則（屬於第 3 節以外的修改，先問使用者） |
| 驗收頁含受版權保護的圖 | 低 | 驗收頁只放本機，不進版本控制 |

## Open Questions

- V3、V4 的主題（使用者在 T9、T10 開始前指定）。
- 單張圖與資產資料夾的大小上限（T2 提出，檢查點 0 確認）。
- explainer-cite 的 references 檔名、scripts 的檔名與子指令（T6a 決定）。
- `ink-shade` 的修正做法（T4 比較後決定）。

## 結果

（各任務完成時補上。）
