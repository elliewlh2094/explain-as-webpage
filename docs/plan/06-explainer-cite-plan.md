# 實作計畫：引用既有圖片（explainer-cite）與第 5 輪留下的修正（第六輪）

構想見 `docs/plan/05-symbols-pictorial-idea.md`〈後續輪次〉，規格見 `docs/plan/06-explainer-cite-spec.md`。本文件同時是待辦清單：〈進度總覽〉每項一行，完成時勾選並補一句結果；各任務的驗收條件也逐項勾選；探測與驗收的細節記在〈結果〉。

## 進度總覽

### 第 0 階段：探測（不改產品檔案）
- [x] T1 授權欄位：Commons、Openverse、NASA、MDPI 文章頁、arXiv LightGlue 摘要頁 —— 2026-10-16：5 個來源都能以 `curl` 取得授權；MDPI 網頁擋 `curl`（403），改由 Crossref 確認 CC BY 4.0；LightGlue 為 arXiv 預設授權（受限）
- [x] T2 圖片處理：WebP 大小與畫質、`pdftoppm` 裁切、Chrome 區域截圖、`<svg><image>` 在各種截圖中的顯示、壓線檢查對 `<image>` 的誤報 —— 2026-10-16：1440px WebP q80 為 37–91 KB；`<svg><image>` 在 4 種截圖中都正常，壓線檢查 0 誤報；發現 3 個規則缺口（見〈結果〉T2）
- [x] T3 層級示意圖的重製方式：以舊頁重產，與現有檔比對 —— 2026-10-16：裁切規則與幀設定可以重現；L0 尺寸相同，L1、L2 高度差 −7、+18px，來自 Chrome 版本的控制項外觀

#### 檢查點 0
- [x] 使用者確認授權分類、大小上限、層級示意圖的重製方式 —— 2026-10-16：單張 200 KB、資料夾 1 MB；程式庫的圖算自由；壓線檢查新增「文字落在 `<image>` 範圍內」；層級示意圖高度隨版面

### 第 1 階段：第 5 輪留下的修正（R7、R8）
- [x] T4 `ink-shade` 不再染到外框：`parts.py`、`pictorial.md`、Starship 與 llm-wiki 範例 —— 2026-10-16：改為只修改 CSS（`.ink-shade` 重畫它蓋住的外框）；背光側外框只剩 `--text` 色，人體逐像素不變，`parts.py` 不需修改
- [x] T5 autoresearch 3 頁改用目前模板的 CSS，重截層級示意圖 —— 2026-10-16：對比掃描兩種寬度都是 `none`；三張層級示意圖重截，寬度與幀設定不變，L1、L2 高 970、921px

#### 檢查點 A
- [x] 使用者判讀放大截圖與新舊層級示意圖；提供提交建議 —— 2026-11-02：判讀通過並提交（`8f524c0`）；L1 滑桿改為藍色，是 Chrome 的預設外觀，新舊 CSS 都沒有滑桿規則，接受

### 第 2 階段：explainer-cite 規則（R1–R5）
- [x] T6a `skills/explainer-cite/`：`SKILL.md`、references、scripts —— 2026-11-02：`SKILL.md` 114 行、2 個 references、`cite.py`（`license`、`prepare`、`check`），壓線檢查新增 `text-on-image`；Openverse 的搜尋端點逾時，尚未實際連線驗證（〈結果〉T6a）
- [x] T6b explainer-page 與 explainer-figure 的整合、模板的 `figure img` 樣式、示範截圖 —— 2026-11-02：`explainer-page/SKILL.md` 131 行；示範主題（主頁＋子頁，CC BY-SA 4.0 的 Commons 照片）通過資產、壓線與 390px 檢查

#### 檢查點 B
- [x] 使用者確認規則與示範截圖；提供提交建議 —— 2026-11-02：判讀通過；always-on 的驗收條件改為比對 frontmatter 與安裝後的 skill 清單

### 第 3 階段：驗收案例
- [x] T7 EKF 頁 v3：論文照片加引線、差速運動學圖（V1、V5）—— 2026-11-02：v3 完成，共同檢查與意圖檢查通過；待檢查點 C 由使用者判讀（〈結果〉T7）
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
- [x] Wikimedia Commons：`prop=imageinfo&iiprop=url|size|extmetadata&iiurlwidth=1440` 回傳的作者（`Artist`）、授權（`LicenseShortName`、`LicenseUrl`）、縮圖網址欄位記錄完成，各附一個範例值。
- [x] Openverse：查詢 API 回傳的 `license`、`license_version`、`creator`、`foreign_landing_url` 記錄完成；確認不需要 API 金鑰時的速率限制。
- [x] NASA Image and Video Library API：回傳欄位與公有領域聲明的位置記錄完成。
- [x] MDPI *Sensors* 25(11):3553 文章頁：確認授權為 CC BY 4.0，取得作者、標題、DOI 與圖 1 的圖說。
- [x] arXiv LightGlue 摘要頁：記錄授權欄位（arXiv 的預設授權不允許改作時，V2 的圖屬於受限）。

**驗證：** 每個來源的 `curl` 指令與輸出摘錄記在〈結果〉T1。

**相依：** 無。**可能動到的檔案：** 無（暫存目錄）。**規模：** S。

#### T2 圖片處理

**說明：** 量測圖片處理的大小與畫質，並確認 `<svg><image>` 在既有檢查中的行為。

**驗收條件：**
- [x] 照片（MDPI 圖）、截圖（一個公開網頁）、PDF 圖（LightGlue 圖 1）各以 1440px 與 720px 寬、WebP 有損（品質 70、80、90）與無損、PNG 輸出，記錄大小並並排截圖判讀畫質；提出單張與資料夾大小上限的數值與依據。
- [x] `pdftoppm -x -y -W -H` 與 headless Chrome 的區域截圖都能在沒有 Pillow 的情況下輸出 PNG。
- [x] 一個暫存頁中放入 `<img>` 與 `<svg><image>` 各一張：寬版截圖、390px iframe（`<title>ok`）、只看圖截圖、遮住文字截圖中都能顯示。
- [x] 同一個暫存頁加上引線與外側標籤，壓線檢查沒有誤報；故意讓一個標籤壓在引線上時能抓到。
- [x] 既有的外部資源檢查（`grep -nE '(src=|url\()…'`）是否涵蓋 `<image href="https://…">`；不涵蓋時，記下 T6a 要補的寫法。

**驗證：** 大小表與截圖路徑（`temp/round-06/t2/`）記在〈結果〉T2。

**相依：** T1（取得 MDPI 圖的授權後才放進並排截圖）。**可能動到的檔案：** 無。**規模：** M。

#### T3 層級示意圖的重製方式

**說明：** 找出 `docs/images/tier-l0-figure.png`、`tier-l1-slider.gif`、`tier-l2-stepper.gif` 的產生方式（commit `9e5e754` 與當時的記錄），並以舊頁重產一次。

**驗收條件：**
- [x] 記錄三個檔案的像素尺寸、GIF 的幀數、每幀時間與循環設定。
- [ ] 以本機工具（headless Chrome 截圖，PIL 組 GIF；本機沒有 ImageMagick）從目前的 autoresearch 頁重產三個檔案，尺寸與幀數和現有檔案相同；PNG 與現有檔案逐位元組相同，或差異只來自字型算圖並記錄原因。—— 未完全達成：L0 尺寸相同；L1、L2 高度差 −7、+18px，原因是 Chrome 版本的控制項外觀（〈結果〉T3），待檢查點 0 決定

**驗證：** 指令與比對結果記在〈結果〉T3。

**相依：** 無。**可能動到的檔案：** 無。**規模：** S。

#### 檢查點 0

- [x] 使用者確認 T1 的授權欄位、T2 的大小上限、T3 的重製方式。arXiv 預設授權的處理已在規劃時確認（規格〈0〉，2026-10-16）。—— 2026-10-16：4 項決定寫入規格〈0〉與 R2、R3、R4、R7

## 第 1 階段：第 5 輪留下的修正

#### T4 `ink-shade` 不再染到外框（R8、V6）

**說明：** 修改 `parts.py` 的 `group()`，讓陰影不蓋住外框，並重新產生所有由 `parts.py` 產生的片段。（2026-10-16：比較後改為只修改 CSS，見〈結果〉T4 與規格 R8。）

**驗收條件：**
- [x] 比較至少兩種做法（例如陰影畫在外框之前、陰影之後重畫只有外框的形狀），以 4 倍放大截圖選出背光側外框只有 `--text` 色、且輸出最短的做法。—— 比較 B（`parts.py` 加只有外框的重畫層）與 D（只改 CSS），選 D
- [x] 零件總覽圖（`parts.py sheet`）在正常大小下與修改前並排，外觀相同。—— 人體與基本形逐像素相同；機器人與無人機只有背光側外框改變
- [x] `pictorial.md` 中由 `parts.py` 產生的片段，與對應指令的輸出逐字相同；文件中的 `parts.py` 指令都以 0 結束。—— `parts.py` 未修改；18 個指令都以 0 結束
- [x] `examples/starship-reusability/` 與 `examples/llm-wiki/` 中的物件改用新輸出；llm-wiki 圖 5 手寫的摺角陰影一併檢查。—— 改為同步內嵌 CSS 的一條規則；摺角陰影也由新規則修正

**驗證：**
- [x] 7 個範例頁的壓線檢查沒有輸出。
- [x] 修改的範例頁（因改為只改 CSS，實際是 4 頁，見〈結果〉T4）：`FILL` 為 0、沒有外部資源、390px 為 `<title>ok`、DOM 對比掃描兩種寬度都是 `<title>none`。
- [x] 放大截圖與並排截圖存於 `temp/round-06/t4/`。

**相依：** 檢查點 0。**可能動到的檔案：** `skills/explainer-figure/scripts/parts.py`、`skills/explainer-figure/references/pictorial.md`、`examples/starship-reusability/starship-reusability.html`、`examples/llm-wiki/llm-wiki.html`。**規模：** M。

#### T5 autoresearch 改用目前模板的 CSS（R7、V7）

**說明：** 3 頁的 `<style>` 換成目前模板的版本，再以 T3 的做法重截三張層級示意圖。

**驗收條件：**
- [x] 3 頁的 `<style>` 與目前模板相同；文字、圖與圖說不變（`diff` 只出現在 `<style>` 內）。
- [x] DOM 對比掃描在 1280px 與 700px 都是 `<title>none`（原本有 6 組低於 4.5:1）。
- [x] 三張層級示意圖以 T3 的做法重截：寬度 1239px、幀數、每幀時間、滑桿值與裁切規則和舊檔相同，高度隨版面（檢查點 0 決定）；新舊並排截圖存於 `temp/round-06/t5/`。

**驗證：**
- [x] 3 頁：`FILL` 為 0、沒有外部資源、390px 為 `<title>ok`、壓線檢查沒有輸出。
- [x] 頁面樹檢查（`extending-pages.md` §5）沒有輸出。

**相依：** T3、檢查點 0。**可能動到的檔案：** `examples/autoresearch/*.html`（3 個）、`docs/images/tier-*`（3 個）。**規模：** M。

#### 檢查點 A

- [x] 使用者判讀 T4 的放大截圖與 T5 的新舊層級示意圖；提供 `git add` 範圍與提交訊息。—— 2026-11-02：提交 `8f524c0`

## 第 2 階段：explainer-cite 規則

#### T6a `skills/explainer-cite/`（R1–R4）

**說明：** 新增 skill 的 `SKILL.md`、references 與 scripts。

**驗收條件：**
- [x] `SKILL.md`：frontmatter（隱藏設定與 description）、輸入輸出、引用與自繪的判準、3 種來源、授權分類與受限圖的處理、資產資料夾規則、資產檢查指令。約 130 行以內。—— 114 行
- [x] references：來源與授權的細節（各 API 的指令與欄位、PDF 與網頁的取得方式、CC BY-SA 的圖說寫法），以及標註引用圖的配方（附一段可直接複製的片段）。—— `sources-and-licenses.md`、`annotated-image.md`
- [x] scripts：授權查詢（Commons 檔名或 Openverse 查詢字串 → 作者、授權、連結）與裁切壓縮（原圖、裁切範圍、寬度 → 圖檔與大小）；只用 Python 標準函式庫，裁切壓縮在沒有 Pillow 時印出退路指令。—— `cite.py`；另涵蓋 NASA、Crossref、arXiv 與資產檢查
- [x] `check-overlap.js` 新增一類「文字落在 `<image>` 範圍內」（檢查點 0 決定）：T2 的示範頁中，壓在照片上的標籤被回報，外側標籤與引線沒有誤報；7 個範例頁仍沒有輸出。—— T2 的示範頁已不在，依相同內容重建
- [ ] 文件中的每個指令都實際執行一次並以 0 結束；資產檢查在乾淨的暫存主題上沒有輸出，故意刪掉一個圖檔或留下一個未引用的圖檔時各印出一行。—— 未完全達成：`license openverse` 逾時，解析邏輯只以樣本測試；其餘指令與資產檢查都達成。T9 使用前再測一次

**驗證：**
- [x] `wc -l skills/explainer-cite/SKILL.md` 約 130 行以內。—— 114 行
- [ ] `claude plugin validate .` 通過；`claude --plugin-dir . plugin details explain-as-webpage` 顯示 3 個 skill；explainer-cite 的 frontmatter 隱藏設定與 explainer-figure 相同，且安裝後的 skill 清單不列出 explainer-cite（檢查點 B 改寫，原條件為「不在 always-on 的 token 成本中」）。—— validate 通過、3 個 skill、隱藏設定相同；skill 清單要等安裝 0.6.0 才能確認，移到 T11

**相依：** 檢查點 0、檢查點 A。**可能動到的檔案：** `skills/explainer-cite/SKILL.md`、`skills/explainer-cite/references/*.md`（2 個）、`skills/explainer-cite/scripts/*`（1–2 個）、`skills/explainer-figure/scripts/check-overlap.js`。**規模：** M。

#### T6b explainer-page 與 explainer-figure 的整合（R1 第 4 點、R5）

**說明：** 修改 explainer-page 的 6 處、兩個 references、模板，以及 explainer-figure 的圖型表。

**驗收條件：**
- [x] `skills/explainer-page/SKILL.md` 依規格 R5 第 1 點修改 6 處，總行數 ≤ 132。—— 131 行；另在第 5 步加入 explainer-cite 的引用，並把 skill 數改為 3
- [x] `extending-pages.md`、`writing-rules.md` 依 R5 第 3、4 點修改；`explainer-figure/SKILL.md` 圖型表新增一列。
- [x] `template.html` 新增 `figure img` 樣式；不新增顏色。
- [x] 以一張自由授權圖（T1 取得的 Commons 圖）做一個暫存示範頁：一張 `<img>`、一張標註的 `<svg><image>`，截圖存於 `temp/round-06/t6b/`。—— 改用 `File:TurtleBot3 Burger.jpg`：它是直式 CC BY-SA 4.0 照片，可同時測試裁切、高度上限與相同方式分享的寫法

**驗證：**
- [x] `CLAUDE.md`〈驗證指令〉的模板檢查全部通過（外部資源、兩種寬度、DOM 對比掃描）。
- [x] 示範頁通過資產檢查、壓線檢查與 390px 檢查。
- [x] `wc -l skills/*/SKILL.md` 三個都約 130 行以內。—— 114、125、131 行

**相依：** T6a。**可能動到的檔案：** `skills/explainer-page/SKILL.md`、`skills/explainer-page/references/extending-pages.md`、`skills/explainer-page/references/writing-rules.md`、`skills/explainer-page/assets/template.html`、`skills/explainer-figure/SKILL.md`。**規模：** M。

#### 檢查點 B

- [x] 使用者確認 T6a、T6b 的規則與示範截圖；提供 `git add` 範圍與提交訊息。—— 2026-11-02：判讀通過；窄版標註圖的橫向捲動維持現狀

## 第 3 階段：驗收案例

V1–V4 共同的檢查（規格 §5）：資產檢查沒有輸出、`FILL` 為 0、沒有外部資源、390px 不溢出、壓線檢查沒有輸出、HTML ≤ ~150 KB、資產資料夾符合大小上限。每個案例都依 explainer-page 的 7 步流程進行，包含第 4 步的確認；確認訊息與回報的內容記在〈結果〉，用來檢查受限圖是否逐張列出。

#### T7 EKF 頁 v3（R6、V1、V5）

**驗收條件：**
- [x] 以 v2 為基礎另存 v3（本機，不覆寫 v2）。
- [x] 〈本頁的例子〉引用 MDPI 照片：圖說有作者、標題、CC BY 4.0、連結與「標註為本頁加上」；引線標出 LIDAR、IMU、編碼器，並連到頁面的符號。—— 依檢查點 0 的觀察，沿用原圖的標籤，引線只加符號
- [x] 差速運動學圖：`parts.py robot` 俯視機器人，標出 x、y、θ、v、ω 與輪距，與公式、符號對照表同色；遮住文字的截圖中可辨認機器人與朝向。—— x、y、θ 屬於 μ，用 c1；v、ω 屬於沒有概念色的 u，在圖、公式與表中都維持文字色
- [ ] 通過共同檢查與意圖檢查；v2、v3 並排截圖存於 `temp/round-06/t7/`；由使用者判讀。—— 檢查都通過、截圖已存；待檢查點 C 判讀

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
- [ ] 安裝 0.6.0 後，session 的 skill 清單列出 explainer-page，不列出 explainer-cite 與 explainer-figure。

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
| `<image>` 在只看圖截圖中被隱藏，或壓線檢查誤報 | 中 | T2 確認不會發生；新增的「文字落在 `<image>` 範圍內」一類以 7 個範例頁確認沒有誤報 |
| 驗收頁含受版權保護的圖 | 低 | 驗收頁只放本機，不進版本控制 |

## Open Questions

- V3、V4 的主題（使用者在 T9、T10 開始前指定）。
- ~~explainer-cite 的 references 檔名、scripts 的檔名與子指令~~：T6a 決定（規格第 3 節）。
- ~~`ink-shade` 的修正做法~~：T4 決定（規格 R8）。

## 結果

### T1 授權欄位（2026-10-16）

**結論：5 個來源都能在本機以 `curl` 取得作者與授權。MDPI 文章頁擋 `curl`，改由 Crossref 與 Europe PMC 取得授權與圖說。LightGlue 的 arXiv 授權為預設授權，屬於受限。**

| 來源 | 指令重點 | 作者 | 授權 | 連結與其他 |
|---|---|---|---|---|
| Wikimedia Commons | `api.php?action=query&prop=imageinfo&iiprop=url\|size\|mime\|extmetadata&iiurlwidth=1440`；可用 `generator=search&gsrnamespace=6` 搜尋 | `extmetadata.Artist`（HTML，需去掉標籤） | `LicenseShortName`（例：`CC BY-SA 4.0`）、`LicenseUrl`、`AttributionRequired`、`Copyrighted` | `descriptionurl`；`thumburl` |
| Openverse | `api.openverse.org/v1/images/?q=…&license=cc0,pdm,by,by-sa` | `creator`、`creator_url` | `license`（例：`by`）、`license_version`、`license_url` | `foreign_landing_url`、`url`、`attribution`（現成的完整署名句） |
| NASA Image and Video Library | `images-api.nasa.gov/search?q=…&media_type=image`；圖檔清單在 `collection.json` | `photographer`（35 筆中只有 12 筆有）；`description` 結尾的 `Credits:` | 沒有授權欄位 | `nasa_id`、`center`；`~orig`、`~large`、`~medium` 等尺寸 |
| MDPI *Sensors* 25(11):3553 | 文章頁 `curl` 回 403；改用 `api.crossref.org/works/10.3390/s25113553` | Crossref `author`（7 位，第一作者 Diego Guffanti） | Crossref `license[].URL` = `https://creativecommons.org/licenses/by/4.0/` | 標題 *Comparison of Two System Identification Approaches for a Four-Wheel Differential Robot Based on Velocity Command Execution*；Europe PMC（PMC12158320）全文 XML 的圖 1 圖說：“Real robot overview and instrumentation.” |
| arXiv LightGlue（2306.13643） | 摘要頁的授權連結；或 OAI-PMH `GetRecord&metadataPrefix=arXiv` 的 `<license>` | — | `http://arxiv.org/licenses/nonexclusive-distrib/1.0/`（預設授權，受限） | 程式庫 `cvg/LightGlue` 為 Apache-2.0，`assets/` 有 `architecture.svg`、`teaser.svg`、`benchmark.png` 等圖 |

**影響 T6a 的發現：**

1. **Commons 的縮圖只接受標準寬度。** 自己組 1440px 的縮圖網址會回 HTTP 400。要用 API 回傳的 `thumburl`；它可能比要求的寬（要求 1440，回傳 1920），下載後再縮小。
2. **Wikimedia 要求 User-Agent。** 腳本送出固定的工具名稱。依 Wikimedia 的政策，User-Agent 可以附聯絡方式，但腳本不寫入任何個人資料。（探測時第一次對 Commons 的請求誤用了使用者的 email 作為 User-Agent 的聯絡方式，之後的請求都已改正。）
3. **NASA 沒有授權欄位。** NASA 的圖一般不受著作權保護，但 `description` 的 `Credits:` 可能標出非 NASA 的作者。規則：`Credits:` 不是 NASA 時，視為授權不明。
4. **期刊網頁常擋 `curl`。** 有 DOI 的論文先查 Crossref 的 `license`；圖說從 Europe PMC 全文 XML 取得（只限 PMC 收錄的論文）。
5. **程式庫中的圖。** 程式庫的授權（Apache-2.0、MIT、BSD）是否算「自由」，規格 R2 沒有寫。LightGlue 的論文圖受限，但程式庫的 `assets/` 有同類的圖。需在檢查點 0 決定。

### T2 圖片處理（2026-10-16）

**結論：1440px 寬的 WebP q80 落在 37–91 KB。`<svg><image>` 在寬版、390px、只看圖與遮住文字的截圖中都正常，壓線檢查對它沒有誤報。另外發現 3 個規則缺口：`<img>` 需要 `max-width`、外部資源檢查漏掉 `<image href>`、壓線檢查看不到壓在照片上的文字。**

**大小（KB）：**

| 圖 | 尺寸 | WebP q70 | WebP q80 | WebP q90 | WebP 無損 | JPEG q85 | PNG |
|---|---|---|---|---|---|---|---|
| 照片（NASA 音震艙，直式） | 1440 × 2168 | 64 | 91 | 214 | 2182 | 289 | 2996 |
| 照片（同上，裁成橫式） | 1440 × 961 | 28 | 39 | 82 | 848 | 117 | 1210 |
| 線條圖（Commons 差速運動學圖） | 1440 × 1440 | 41 | 47 | 60 | 93 | 117 | 272 |
| PDF 圖（LightGlue 圖 1，300 dpi） | 1125 × 690 | 31 | 37 | 47 | 18 | 75 | 58 |
| 網頁截圖（Wikipedia，2 倍） | 1440 × 900 | 60 | 69 | 86 | 72 | 137 | 197 |
| MDPI 照片（使用者提供的 550px 版） | 550 × 251 | 13 | 15 | 23 | 76 | 30 | 124 |

- 畫質：以原尺寸裁出文字、牆面紋理與細線並排（`temp/round-06/t2/quality-sheet.png`）。q70 的牆面紋理稍糊，q80 與無損看不出差別；文字與線條在 q70 也清楚。
- 格式規則的建議：照片用 WebP q80；截圖、線條圖、PDF 圖同時輸出 q80 與無損，留較小的一個（PDF 圖無損 18 KB 比 q80 小；線條圖 q80 47 KB 比無損小）。
- **建議上限：單張 ≤ 200 KB、顯示高度 ≤ 540 CSS px（像素 1080，以裁切達成）、每個主題的資產資料夾 ≤ 1 MB。** 依據：q80 的最大值 91 KB 來自一張 1440 × 2168 的直式照片，200 KB 保留給細節更多的照片；直式照片在 720px 寬時高 1084 CSS px，超過一個畫面，所以限制顯示高度；1 MB 約可放 10 張以上，足夠主頁加 6 個子頁的頁面樹。

**工具：**

- `pdftoppm -f 1 -l 1 -r 300 -x 1275 -y 840 -W 1125 -H 690 -png` 直接裁出 LightGlue 圖 1。座標 = 點數 × dpi ÷ 72，先以低解析度（`-r 60`）算圖找出位置。
- 沒有 Pillow 時，以一個暫存頁（`<img>` 加負的 margin、視窗大小等於裁切範圍）讓 Chrome 截圖。與 Pillow 的裁切結果逐像素相同，但只能輸出 PNG。
- headless Chrome 以 `--force-device-scale-factor=2 --window-size=720,900` 截取公開網頁，得到 1440px 寬的截圖。

**暫存示範頁（模板＋一張 `<img>`＋一張 `<svg><image>` 加引線）：**

| 檢查 | 結果 |
|---|---|
| 寬版截圖（`temp/round-06/t2/demo-wide.png`） | 兩張圖都正常 |
| 390px iframe | `<title>ok`，但 `<img>` 在 figure 內被裁掉並出現捲軸（`demo-narrow.png`）：模板沒有 `figure img` 的寬度規則，R5 第 5 點需要 |
| 只看圖、遮住文字的截圖（`figs-cmp.png`） | 兩張圖都顯示；遮住文字時只隱藏本頁加的標籤，照片本身的文字（MDPI 圖的 LIDAR、CPU 標籤）仍在 |
| 壓線檢查 | 只回報故意放入的缺陷（引線穿過「z measured」），`<image>` 沒有誤報 |

**發現的規則缺口：**

1. **外部資源檢查漏掉 `<image href>`。** 現行的 `grep -nE '(src=|url\()…https?://'` 不比對 `href`，`<image href="https://…">` 會通過。T6a 的資產檢查加上 `grep -nE '<image\b[^>]*href=["'\'']?https?://'`（已測試，可抓到 `href` 與 `xlink:href`，不會抓到 Sources 的 `<a href>`）。
2. **壓線檢查看不到壓在照片上的文字。** 示範頁中故意放在照片上的「BAD over photo」沒有被回報，因為照片不是填色形狀。可以在 `check-overlap.js` 加一類「文字落在 `<image>` 範圍內」；這是規格第 3 節以外的修改，需在檢查點 0 決定。
3. **照片上的引線不清楚。** 1px 的 `--muted` 引線在深色機身上幾乎看不見。標註規則需要加白色底線（同一條線先以較粗的 `--bg` 畫一次），T6a 的配方寫入這一點。

**給 T7 的觀察：** 使用者提供的 MDPI 圖本身已經有 LIDAR、CPU、ENCODERS、DRIVER、MCU、IMU 標籤。再加本頁的引線會重複，T7 應改為沿用原圖的標籤，只加符號（例如 LIDAR → z）。這張圖只有 550px 寬；Europe PMC 的原圖網址回 403，需要時請使用者提供原圖，或接受 550px（顯示寬 480 CSS px 時約 1.1 倍）。

### T3 層級示意圖的重製方式（2026-10-16）

**結論：裁切規則與 GIF 設定可以重現；L0 的尺寸與框線逐像素相同，只有文字的反鋸齒不同。L1、L2 的高度差 −7 與 +18px，原因是本機 Chrome 的控制項外觀與當時不同，不是做法不同。**

- 現有檔案：L0 為 1239 × 799 PNG；L1 為 1239 × 976、L2 為 1239 × 866 的 GIF，各 8 幀，每幀 800 ms、最後一幀 1600 ms、無限循環（commit `9e5e754` 的說明與檔案一致）。L1 的 8 幀滑桿值為 1、2、3、5、8、13、19、28 分鐘；L2 為步驟 1–8。
- 來源頁：`examples/autoresearch/autoresearch.html` 在 `9e5e754` 的版本（之後 `3a9c515` 改過內容）。
- 重製做法（腳本存於 `temp/round-06/t3/tiers.py`）：`--force-device-scale-factor=1.5 --window-size=1247,4400` 截整頁；裁切為 x 從 `.content` 左緣 + 2px、寬 1239，y 從該節 `h2` 上緣 + 3px 到 figure 下緣 + 20px（以 L0 逐像素比對找出）；GIF 的 8 幀取各幀範圍的聯集，使用一份共用的 256 色調色盤、不抖色。
- 比對（`temp/round-06/t3/`）：

| 檔案 | 原檔 | 重製 | 差異 |
|---|---|---|---|
| L0 | 1239 × 799，137 KB | 1239 × 799，115 KB | 框線與箭頭逐像素相同；文字的反鋸齒不同（`l0-diff.png`） |
| L1 | 1239 × 976，157 KB | 1239 × 969，168 KB | 滑桿圓鈕在原檔為灰色，本機 Chrome 為藍色（`cmp-l1.png`） |
| L2 | 1239 × 866，275 KB | 1239 × 884，321 KB | stepper 按鈕的 ◀ ▶ 字形大小不同（`cmp-l2.png`） |

- 第一次重製時 GIF 達 0.8–1.2 MB：Pillow 把 RGB 幀轉成 GIF 時預設使用網頁調色盤並抖色，背景 `#fcfcfc` 變成斜紋，每一幀都整張不同。改用共用調色盤、不抖色後恢復正常大小。
- **對 T5 驗收條件的影響：** 「尺寸與舊檔相同」無法達成，因為控制項外觀隨 Chrome 版本改變，而且 T5 換 CSS 後版面也會變。建議改為：寬度 1239、幀數、每幀時間與裁切規則相同，高度由裁切規則決定。需在檢查點 0 確認。

### T4 `ink-shade` 不再染到外框（2026-10-16）

**結論：只修改 CSS 就能讓背光側的外框只剩 `--text` 色。`parts.py` 不需要修改；人體等單一外輪廓的物件逐像素不變；範例中手寫的陰影（Starship 助推器、llm-wiki 摺角）也一併修好。**

- **影響範圍**：只有以 `ink`（外框畫在形狀邊界上）繪製的物件會被染色，包括機器人、無人機、Starship 助推器與 llm-wiki 的摺角。人體以 `ink-edge`＋`ink-fill` 繪製，可見的外框在形狀外側，陰影只落在填色範圍內，所以本來就沒有問題。
- **比較的兩種做法**（暫存測試頁，4 倍截圖，取背光側外框的像素）：

| 做法 | 內容 | 背光側外框的顏色 | 人體 | 手寫的陰影 | 增加的輸出 |
|---|---|---|---|---|---|
| 修改前 | — | `#404040` 加上混色 (67,68,58)、(68,70,57)；摺角 (79,58,71)、(82,57,72) | — | — | — |
| B | `parts.py` 在陰影之後加一層只有外框的形狀 | 只有 `#404040` | 不變 | 修不到 | 每個物件多一個 `<g>` |
| D | CSS：`.ink-shade` 改用 `fill-opacity` 並畫 3px 的 `--text` 外框 | 只有 `#404040`；摺角只剩灰階的反鋸齒 | 第一版的手臂與軀幹重疊處變成兩倍深 | 修好 | 無 |

- **D 的修正**：重疊處變深，是因為 `fill-opacity` 逐形狀套用，原本的 `opacity` 套在整個群組上。新增 `.ink-fill ~ .ink-shade { opacity: .18; fill-opacity: 1; stroke: none; }`，讓 `ink-edge`＋`ink-fill` 之後的陰影維持原本的畫法。兄弟選擇器在 `<use>` 的 shadow tree 中有效，修正後人體區域與修改前逐像素相同。
- **限制**：`ink` 物件的陰影若由多個重疊的形狀組成，重疊處會染兩次色。`pictorial.md` 的 class 表寫明「`ink` 物件的陰影只用一個形狀」；零件函式庫的機器人與無人機都只用一個形狀。
- **修改的檔案**：`template.html` 一條規則改成兩條；4 個內嵌模板 CSS 的範例頁同步（4 頁原本與模板的 `<style>` 完全相同）；`pictorial.md` class 表的 `ink-shade` 一列。
- **驗證**：
  - 放大截圖（`temp/round-06/t4/zoom-old-new.png`）：Starship 圖 3 助推器背光側的外框，修改前內側一半帶紫色，修改後只剩 `--text` 色。llm-wiki 圖 5 的紙張沒有概念色，陰影為灰色，看不出差別。
  - 零件總覽圖（`sheet-old-new.png`）：人體與基本形逐像素相同；機器人與無人機只有背光側的外框改變（1,500 個像素，最大差值 48）。
  - `pictorial.md` 中 18 個 `parts.py` 指令都以 0 結束。
  - 7 個範例頁的壓線檢查都沒有輸出；修改的 4 頁 `FILL` 為 0、沒有外部資源、390px 為 `<title>ok`、DOM 對比掃描兩種寬度都是 `<title>none`。
  - 模板：外部資源檢查沒有輸出、390px 為 `<title>ok`、DOM 對比掃描兩種寬度都是 `<title>none`。
- **未修改**：預設輸出目錄中的本機頁面（EKF v2、差速路徑追蹤 4 頁）仍是舊規則，它們不在版本控制中。

### T5 autoresearch 改用目前模板的 CSS（2026-10-16）

**結論：3 頁換成目前模板的 `<style>` 後，DOM 對比掃描在兩種寬度都沒有低於 4.5:1 的組合。三張層級示意圖以 T3 的腳本重截並寫回 `docs/images/`。**

- **CSS 的差異**：模板是舊 CSS 的超集。差異只有顏色調整（連結、側欄標題、`code`、提示框標題、`text.good`）與新增的規則（概念色、`ink` 系列、圖示、卡片、來源等級），沒有刪除的規則。替換後，3 頁在 `<style>` 以外的內容與修改前完全相同。
- **驗證**：3 頁的 `FILL` 為 0、沒有外部資源、390px 為 `<title>ok`、DOM 對比掃描兩種寬度都是 `<title>none`（修改前有提示框標題 1.83、2.41、2.37，側欄頁面樹標籤 3.73，`code` 3.82，連結 4.19，側欄標題 4.30）、壓線檢查沒有輸出；頁面樹檢查 3 項都沒有輸出。
- **層級示意圖**（新舊並排：`temp/round-06/t5/l0-old-new.png`、`l1-old-new.png`、`l2-old-new.png`）：

| 檔案 | 舊 | 新 |
|---|---|---|
| `tier-l0-figure.png` | 1239 × 799，137 KB | 1239 × 799，115 KB |
| `tier-l1-slider.gif` | 1239 × 976，8 幀，157 KB | 1239 × 970，8 幀，168 KB |
| `tier-l2-stepper.gif` | 1239 × 866，8 幀，275 KB | 1239 × 921，8 幀，334 KB |

  每幀時間（800 ms，最後一幀 1600 ms）、無限循環與 L1 的滑桿值都與舊檔相同。L2 變高，是因為圖 3 的圖說在 `3a9c515` 加了 val_bpb 的說明，變成兩行。README 以 `width="640"` 顯示，高度的差異不影響版面。

### T6a `skills/explainer-cite/`（2026-11-02）

**結論：explainer-cite 的 `SKILL.md`、2 個 references 與 `cite.py` 完成，壓線檢查新增 `text-on-image`。兩項驗收條件未完全達成：Openverse 尚未實際連線驗證；`plugin details` 的估算表仍列出隱藏 skill 的 token。**

- **檔案**：`SKILL.md` 114 行；`references/sources-and-licenses.md` 83 行；`references/annotated-image.md` 43 行；`scripts/cite.py` 262 行（T6b 修正後）。腳本放在一個檔案中，有 3 個子指令，只用 Python 標準函式庫，`prepare` 的 Pillow 為選用。
- **與規格不同的決定**（已寫回規格）：
  - arXiv 讀摘要頁。OAI-PMH 端點連續 25 秒沒有回應，摘要頁約 1 秒回應，而且規格的授權依據本來就是摘要頁。
  - 不解析 XML。只取 3 個欄位，以正規表示式讀 HTML 即可，避免 XML 解析器的外部實體與展開風險。
  - 資產檢查做成 `cite.py check`，不用規格原寫的 `grep`；另外檢查圖是否在 `<figure>` 中、在資料夾內，以及 R3 的 3 個上限。
- **實作時發現的缺陷**：
  - Commons 的 `thumbwidth` 在原圖比要求窄時仍回報要求的寬度（回報 1440，實際 596）。`image_size` 改取兩者較小值。這個修法不完整，T6b 改為從網址讀真實寬度。
  - 配方片段第一版的引線穿過照片上的 “ASSEMBLED ROBOT”，底線切斷了文字。壓線檢查讀不到照片中的文字，所以改了片段，並在 `annotated-image.md` 寫明要看截圖。
- **驗證**：

| 項目 | 結果 |
|---|---|
| `license commons`（檔名、搜尋）、`nasa`、`crossref`、`arxiv` | 欄位正確；MDPI 為 CC BY 4.0、LightGlue 為 arXiv 預設授權（`restricted`），與 T1 一致；查無資料時以 1 結束 |
| 授權分類 13 個名稱 | CC0、公有領域、CC BY、CC BY-SA 為 `free`；NC、ND、GFDL、未知、arXiv 預設授權為 `restricted` |
| `license openverse` | **3 次都逾時**（30–40 秒）；`/v1/` 根路徑回 200，換 User-Agent 無效，問題在服務端。解析邏輯以 T1 記錄的欄位組成樣本測試，輸出正確 |
| `prepare` | 照片、`--kind flat`、裁切、超過上限時以 1 結束並印出原因；LightGlue 圖 1 為 18 KB，與 T2 相同 |
| 沒有 Pillow（`python3 -S`） | 印出退路指令；實際執行 Chrome 指令，輸出 520 × 240 的 PNG |
| 文件中的其他指令 | Commons 下載、NASA 尺寸清單、`pdftoppm` 兩段、`pdfimages` 兩段、網頁截圖、Europe PMC 全文 XML 都以 0 結束 |
| 壓線檢查 | 配方片段沒有輸出；壓在照片上與跨過照片邊緣的標籤回報 `text-on-image`，外側標籤與 `data-touch` 不回報；引線穿過標籤照常回報；7 個範例頁與模板沒有輸出 |
| 資產檢查 | 乾淨的主題沒有輸出；刪掉圖檔、未引用的檔案、缺少作者與授權、外部網址、資料夾外、`<figure>` 外、過高、過大各印出對應的行，以 1 結束 |
| `claude plugin validate .` | 通過；1 個警告是根目錄的 `CLAUDE.md`，屬預期 |
| `plugin details` | `Skills (3)`；估算表的 always-on 為 explainer-cite ~160、explainer-page ~370、explainer-figure ~130 |

- **`plugin details` 的估算**：`explainer-figure` 的 frontmatter 與 explainer-cite 相同，估算表一樣把它算進 always-on，所以這張表不反映 `disable-model-invocation`。實際上，session 的 skill 清單只列出 `explainer-page`，沒有 `explainer-figure`。這項驗收條件無法用這個指令證明，檢查點 B 已改寫（見 T6a 的驗證項目）。
- **截圖**：`temp/round-06/t6a/demo-wide.png`。示範頁的 `<img>` 寬版正常；390px 的 `<img>` 規則在 T6b 加入。

### T6b explainer-page 與 explainer-figure 的整合（2026-11-02）

**結論：explainer-page 的 6 處、2 個 references、explainer-figure 的圖型表與模板都已修改。依 skill 的步驟從查授權走到資產檢查，示範主題全部通過。**

- **修改**：
  - `explainer-page/SKILL.md`：Overview、第 2 步圖型、第 4 步第 2 項、第 5 步、第 6 步資產檢查、第 7 步、Red Flags。第 2 步寫明引用圖要在第 4 步之前讀 explainer-cite，否則確認時還沒有授權資訊。
  - `extending-pages.md`：子頁共用資料夾；§5 加入資產檢查。
  - `writing-rules.md`：引用圖來源行的規則；固定標籤兩列。
  - `explainer-figure/SKILL.md`：圖型表一列；「三個 skill 並列」。
  - `template.html`：`figure img` 一條規則。
- **實作時發現的缺陷**：
  - Commons 會把縮圖對齊到標準寬度：`thumbwidth` 回報 1440，實際檔案 1920。`--crop` 使用來源像素，這個差異會裁錯位置。`cite.py` 改從 `thumburl` 的 `1920px-` 讀寬度。
  - 寬版的 `<img>` 顯示 748 × 561，超過 540 CSS px：內容欄實際寬 748px，不是規格假設的 720px。`figure img` 的 `max-width` 改為 `min(100%, 720px)`，修正後量得 720 × 540。
  - `cite.py check` 在主頁不存在時（單頁名為 `a--b.html`）會丟出 traceback。第 6 步現在對每一頁執行，所以改為略過不存在的主頁。
- **驗證**：

| 項目 | 結果 |
|---|---|
| 模板：外部資源、390px、DOM 對比掃描 | 沒有輸出、`<title>ok`、兩種寬度都是 `<title>none` |
| 示範流程 | `license commons` → `curl` → `prepare`：整張照片顯示高 983 CSS px，回報並以 1 結束；裁切後 1440 × 1080、59 KB |
| 示範主題 2 頁（英文主頁、繁中子頁共用同一圖檔） | `FILL` 為 0、沒有外部資源、資產檢查與壓線檢查沒有輸出 |
| 390px | 兩頁 `<title>ok`；`<img>` 為 343/343，`figure` 沒有內部捲軸（T2 時會被裁切） |
| 文件中的 shell 範例 | 第 6 步、`extending-pages.md` §5 依原文執行，沒有輸出、以 0 結束 |
| 沒有引用圖的頁面 | 7 個範例頁的資產檢查沒有輸出、以 0 結束 |
| 外觀 | 寬版、窄版與遮住文字的截圖都看過：`temp/round-06/t6b/` |
| `claude plugin validate .`、manifest | 通過；警告是根目錄 `CLAUDE.md`、沒有 icon 與 marketplace 同目錄，都與本輪無關 |

- **窄版的標註圖**：`figure svg` 的 `min-width: 540px` 讓它在 390px 時橫向捲動，右側標籤要捲動才看得到。所有 SVG 圖都是這樣，本輪不改。
- **範例頁的 CSS**：7 頁都沒有 `<img>`，所以不同步 `figure img` 這條規則。規格〈6. 邊界〉也把修改 R7、R8 以外的範例列為要先詢問的項目。
- **Openverse**：第 4 次仍然逾時。

### T7 EKF 頁 v3（2026-11-02）

**結論：v3 新增論文照片（圖 2）與差速運動學圖（圖 3），共同檢查與意圖檢查都通過，等待檢查點 C 判讀。論文全文解決了規劃時沒有注意到的兩個問題：四輪照片與頁面的差速例子是否相符，以及輪距公式的來源。**

- **第 4 步的確認**（2026-11-02，核心問題、L2、繁中與讀者不變）：
  - 新增的圖：兩張都加；原圖 2–4 改為圖 4–6。較便宜的選項是只加照片，損失是讀者看不到 v·cos θ 的非線性來源。
  - 照片：用使用者提供的 550 × 251 版本。Europe PMC 的原圖網址回 403。
  - IMU：標為 ω 的另一來源。頁面的例子不用 IMU，所以標「ω（本例改由輪子換算）」，段落連到〈融合輪式里程計與 IMU〉。
  - 授權：照片為 CC BY 4.0（自由），`cite.py license crossref` 與 T1 的結果一致，不需要逐張列為受限圖。
- **從論文全文（Europe PMC）查到的事實**：
  - 平台有四個輪子，但式 (6) 把同側兩輪平均成左、右各一輪，所以仍用差速模型。頁面的段落寫明這一點，否則讀者會質疑照片與「左右兩輪」的例子不符。
  - 式 (8) 為 v = (v_r + v_l)/2、ω = (v_r − v_l)/L，是圖 3 上半部公式的來源。
  - 論文的簡化模型以編碼器算 v、以 IMU 量 ω；里程計由整合編碼器、IMU 與光達的 SLAM 系統估計。
- **修改**：
  - `<style>` 換成目前的模板（含 `ink-shade` 修正與 `figure img`）；側欄日期改為 2026-11-02。
  - 符號表 μ 那一列的 x、y、θ 上 c1。
  - 新增 2 個名詞（差速驅動、輪距）與 1 筆來源（g2）。
  - 圖 3 的算例沿用頁面既有的數字（1.5 m/s 直行 2 秒），沒有新增假設值。
- **驗證**：

| 項目 | 結果 |
|---|---|
| `FILL`、外部資源、`topic` 來源檢查 | 0、沒有輸出、沒有輸出 |
| 資產檢查 | 沒有輸出，以 0 結束 |
| HTML 大小；資產資料夾 | 63.7 KB；1 個檔案，16 KB |
| 壓線檢查（含 stepper 每一幀） | 沒有輸出。第一版回報 `vr` 壓在 θ 弧線上，放大弧線與 v 箭頭後解決 |
| 390px；DOM 對比掃描 | `<title>ok`；兩種寬度都是 `<title>none` |
| 意圖檢查（`v3-new-figures-words-hidden.png`） | 機器人與朝向可辨認；照片本身的文字保留，3 條引線都在 |
| 圖號 | `fig-1`–`fig-6` 依序，`href` 都有對應 |

- **篇幅**：本文 3,596 個中文字，略高於預算約 3,500（v2 為 3,349）；圖 6 張，在 L2 的上限內。新增的 2 段都有圖要說明，所以不刪。
- **截圖**：`temp/round-06/t7/v2-v3.png`、`v3-new-figures.png`、`v3-new-figures-words-hidden.png`。
- **Skill 的使用情況**：`license`、`prepare`、`check` 與標註配方都不需要另外補規則。檔名含版本（`.v3`）時，`<hub>` 取到 `extended-kalman-filter.v3`，資料夾與頁面對應正確。
