# 規格：引用既有圖片（explainer-cite）與第 5 輪留下的修正（第六輪）

> 狀態：規格（2026-10-16）。構想見 `docs/plan/05-symbols-pictorial-idea.md`〈後續輪次〉的「第 6 輪候選：explainer-cite」與「第 5 輪留下的項目」；實作計畫與待辦見 `docs/plan/06-explainer-cite-plan.md`。需求有變動時，先更新本文件再實作。

## 0. 問題陳述與範圍

**問題陳述（How Might We）**：我們如何讓頁面在讀者需要看到真實物件、介面或原文圖表時，引用既有的點陣圖，並正確標示作者與授權，同時讓頁面在只多一個資產資料夾的情況下維持離線、可攜與現有的自檢流程？

**起因**：第 4 輪把使用者收集的圖分成 A–D 四類（`docs/plan/04-visual-forms-idea.md`〈Problem Statement〉）。B 類（具象插圖）與 D 類（歸納卡）已在第 4、5 輪完成。A 類「引用既有圖片」的例子（ASU 體液分布圖、ESA 音震艙照片、NotebookLM 介面截圖）需要讀者看到真實的東西，自繪物件無法取代。第 5 輪的 EKF 頁也遇到同樣的情況：使用者提供的參考圖（MDPI 論文中的機器人照片）比任何自繪物件都更能說明「感測器裝在哪裡」。

**已與使用者確認的決策**：

- 只有引用點陣圖的頁面才允許資產資料夾（2026-10-07）。
- 不放寬 150 KB 上限；這個上限只計算 HTML 檔本身（2026-10-07）。
- 授權以開放授權為主，受版權保護的圖在確認步驟逐張列出；headless Chrome 只截公開網頁（2026-10-04）。
- 第 6 輪範圍：explainer-cite，加上第 5 輪檢查點 D 留下的全部 3 項（EKF 機器人圖、autoresearch 舊 CSS、`ink-shade`）（2026-10-16）。
- 資產資料夾由整個主題共用，命名為 `<hub>.assets/`，主頁與子頁都引用它（2026-10-16）。
- 圖片來源支援 3 種：開放授權圖庫、公開網頁截圖、使用者材料中的圖（2026-10-16）。使用者這次沒有選「使用者自行提供的截圖」，本輪列入〈8. 不做的事〉。
- 架構：新建隱藏 skill `skills/explainer-cite/`，比照 explainer-figure，只由 explainer-page 以相對路徑讀取（2026-10-16）。
- EKF 機器人圖：引用 MDPI 論文照片並加引線，另以零件函式庫自繪差速運動學圖（2026-10-16）。
- 驗收案例 4 個：EKF 論文照片、LightGlue 論文 PDF 的圖、Wikimedia 主題頁、公開網頁截圖；後兩者的主題由使用者在任務開始前指定（2026-10-16）。
- 不在 `examples/` 新增範例。驗收頁放預設輸出目錄，截圖放 `temp/round-06/`（2026-10-16）。
- 引用的點陣圖允許加上引線與符號標籤，做法是以 `<svg>` 包住 `<image>`（2026-10-16）。
- 需要登入的頁面維持現行做法，請使用者存成 PDF，不另外支援使用者提供的截圖（2026-10-16）。
- arXiv 論文的圖依摘要頁標示的授權分類；預設授權（arXiv non-exclusive license）不允許改作，屬於受限，在確認步驟逐張列出，由使用者決定（2026-10-16）。

**範圍檢查**：R1–R5 都屬於「引用一張圖」這一個流程：取得、查授權、處理、放進資產資料夾、標註、列入確認與自檢。它們不能分開出貨，所以採用單一規格加上需求編號。R6–R8 是第 5 輪留下的修正，與 R1–R5 沒有共用的介面，可以獨立出貨；放進同一份規格是為了共用驗證流程與版本號。各需求的相依如下：

| 需求 | 內容 | 相依 |
|---|---|---|
| R1 | explainer-cite skill 與圖型選擇 | — |
| R2 | 來源與授權 | R1 |
| R3 | 資產資料夾 `<hub>.assets/` 與圖片處理 | R1 |
| R4 | 標註引用圖 | R1、R3 |
| R5 | explainer-page 的規則整合 | R1–R4 |
| R6 | EKF 頁的機器人圖 | R4、R8 |
| R7 | autoresearch 範例改用目前模板的 CSS | — |
| R8 | `ink-shade` 不再染到外框 | — |

## 1. 需求

### R1 explainer-cite skill 與圖型選擇

1. **檔案**：新增 `skills/explainer-cite/SKILL.md`。frontmatter 設 `disable-model-invocation: true`、`user-invocable: false`，description 寫明「只由 explainer-page 使用，不處理一般的圖片搜尋或下載」，寫法比照 `skills/explainer-figure/SKILL.md`。
2. **讀取方式**：explainer-page 以 `../explainer-cite/SKILL.md` 讀取，不依賴平台的自動觸發。三個 skill 資料夾必須並列。
3. **輸入與輸出**：輸入是圖說明單（`explainer-figure/SKILL.md` § Figure brief）中圖型為「引用圖」的一列；輸出是 `<hub>.assets/` 中的圖檔、一個 `<figure id="fig-N">` 元素，以及一筆來源記錄（作者、標題、授權、連結、本頁做過的修改）。
4. **圖型選擇**：`explainer-figure/SKILL.md` § Choosing the figure type 的圖型表新增一列「引用圖」，指向 `../explainer-cite/SKILL.md`。判準如下：
   - 讀者需要認出一個真實東西的外觀（特定的機器、地點、器官、產品），而自繪物件只能畫出通用外形時，引用。
   - 讀者需要在真實介面上找到位置（要點哪個按鈕、哪個欄位）時，引用。
   - 頁面討論的就是材料中的那張圖（論文的結果圖、架構圖）時，引用。
   - 要表達結構、機制、因果或符號對應時，自繪。引用圖可以補充自繪圖，不取代機制圖。
5. **行數**：`skills/explainer-cite/SKILL.md` 約 130 行以內，細節放進 `references/`。

### R2 來源與授權

1. **3 種來源與取得方式**：

| 來源 | 取得方式 | 授權資訊從哪裡來 |
|---|---|---|
| 開放授權圖庫 | Wikimedia Commons API（`prop=imageinfo`、`iiprop=url|size|extmetadata`、`iiurlwidth`）；Openverse API；公有領域機構（例如 NASA Image and Video Library API） | API 回傳的作者、授權名稱與授權連結欄位 |
| 公開網頁截圖 | headless Chrome 截取指定的視窗大小與區域 | 網站的著作權聲明；沒有開放授權時視為受限 |
| 使用者材料中的圖 | PDF：`pdftoppm -f N -l N -r <dpi> -x -y -W -H` 裁切，或 `pdfimages` 取出內嵌圖；專案：直接複製儲存庫中的圖檔 | PDF：材料本身或其出版頁面標示的授權（例如 arXiv 摘要頁、期刊文章頁）；專案：使用者自己的專案視為使用者擁有 |

2. **授權分兩類**：
   - **自由**：CC0、公有領域、CC BY、CC BY-SA。可以裁切、縮放與標註。圖說與 Sources 寫出作者、授權與連結。
   - **受限**：CC BY-NC 系列、CC BY-ND 系列、保留所有權利、授權不明。只在使用者於第 4 步確認中同意後使用。
3. **受限圖的處理**：
   - 第 4 步的確認逐張列出受限圖：出處、授權、用途、本頁會做的修改。
   - ND（禁止改作）的圖不可裁切與標註，只能整張縮放後放上頁面。
   - 授權不明的圖視為保留所有權利。
4. **CC BY-SA 的標註**：裁切或標註後的圖仍是 BY-SA，圖說寫明「本頁裁切／標註，依 CC BY-SA 4.0 釋出」。
5. **不繞過存取限制**：遇到登入牆、付費牆或 cookie 同意牆時停止，改用其他來源，或請使用者提供材料。這條規則延續 `sources-and-research.md` §2〈Material you cannot read〉。
6. **記錄**：每張圖的來源記錄在取得時就寫下，不在產頁後回想。

### R3 資產資料夾 `<hub>.assets/` 與圖片處理

1. **位置與命名**：資產資料夾放在主頁旁，命名為 `<hub>.assets/`，`<hub>` 是主頁的檔名主幹。頁面樹的子頁也引用同一個資料夾（`<hub>--<child>.html` 中寫 `src="<hub>.assets/…"`）。單頁主題的 `<hub>` 就是頁面本身的檔名主幹。
2. **只在需要時建立**：頁面沒有引用點陣圖時不建立資料夾。
3. **圖檔命名**：小寫 kebab-case，描述圖的內容，例如 `robot-sensors.webp`。不使用圖號，因為圖號會隨頁面修訂而改變。
4. **格式與尺寸**：
   - 照片：WebP 有損壓縮。
   - 截圖、線條圖、含文字的圖：WebP 無損壓縮或 PNG，以較小者為準。
   - 寬度最大 1440px（內容寬 720px 的 2 倍，對應高解析度螢幕）。
   - 單張圖與整個資料夾的大小上限由 T2 探測決定，寫進 explainer-cite。
5. **HTML 大小**：150 KB 上限只計算 HTML 檔本身。圖不以 base64 內嵌。
6. **處理工具**：Pillow（`PIL`）為選用。缺少 Pillow 時，PDF 用 `pdftoppm` 的裁切參數、網頁用 Chrome 的視窗大小輸出 PNG，並在確認中說明檔案會較大。安裝 Pillow 由使用者決定，比照 `sources-and-research.md` §5 的輔助 skill 規則。
7. **暫存檔**：下載的原圖與中間檔放在輸出目錄以外的暫存目錄，產頁後刪除。資產資料夾只留頁面引用的檔案。

### R4 標註引用圖

1. **不標註時**：`<figure>` 中放 `<img src="<hub>.assets/…" alt="…" width="…" height="…">`，加上圖說與來源行。`alt` 描述圖的內容，不重複圖說。
2. **標註時**：`<figure>` 中放一個 `<svg viewBox="0 0 720 H">`，以 `<image href="<hub>.assets/…">` 放圖，再以 explainer-figure 既有的 `lead`、`pin`、概念色與符號標註規則（`svg-recipes.md` § Symbols）畫引線與標籤。
3. **標籤位置**：標籤放在圖片範圍外，引線從標籤指到圖上的部位。原因：照片的底色不固定，標籤放在圖上無法保證 4.5:1 的對比。
4. **圖說**：寫明「標註為本頁加上」／「Annotations added by this page」。
5. **檢查**：壓線檢查（`check-overlap.js`）與只看圖、遮住文字的截圖照常適用。T2 確認 `<image>` 在這些檢查中能正常顯示，且不產生誤報。

### R5 explainer-page 的規則整合

1. **`skills/explainer-page/SKILL.md`**（目前 130 行，修改後仍約 130 行，以改寫取代新增；指令細節放在 explainer-cite）：
   - Overview 第 12 行：「no extra figure or script folders」改為允許 `<hub>.assets/`，只用於引用的點陣圖。
   - 第 2 步的圖說明單：圖型加入「cited image」。
   - 第 4 步第 2 項：計畫的圖列出引用圖的出處與授權類別；受限圖逐張列出（R2 第 3 點）。
   - 第 6 步：加入資產檢查（指令放在 explainer-cite，第 6 步只寫一行引用）。
   - 第 7 步：回報每張引用圖的出處與授權。
   - Red Flags 第 121 行：「Leaving helper scripts, image files, or extra folders next to the page」改為排除 `<hub>.assets/` 中被引用的圖檔。
2. **資產檢查**（全部通過時不印出任何內容）：
   - 頁面中每個 `<img src>` 與 `<image href>` 指向的檔案都存在。
   - `<hub>.assets/` 中每個檔案都被主題中的某一頁引用。
   - 頁面中沒有指向外部 URL 的 `src` 或 `href`（既有的外部資源檢查，需確認也涵蓋 `<image href>`）。
   - 每張引用圖的圖說或來源行都有作者與授權。
3. **`references/extending-pages.md`**：頁面樹的子頁共用 `<hub>.assets/`；§5 的頁面樹檢查加入資產檢查。
4. **`references/writing-rules.md`**：圖片來源行的格式（作者、標題、授權、連結、本頁的修改），以及固定標籤的中英對照（例如 Image source／圖片來源、License／授權）。
5. **`assets/template.html`**：新增 `figure img` 的樣式（`display: block; max-width: 100%; height: auto`），讓圖在 390px 寬時不溢出。不新增顏色。

### R6 EKF 頁的機器人圖

1. **頁面**：在本機的 EKF 頁（預設輸出目錄的 `extended-kalman-filter/`）以 v2 為基礎另存 v3，不覆寫 v2。頁面不加入版本控制。
2. **引用照片**：使用者提供的 MDPI *Sensors* 論文圖（`temp/round-05/sensors-25-03553-g001-550.jpg`）。T1 先確認授權為 CC BY 4.0，並取得作者與連結。放在〈本頁的例子〉段落，以引線標出 LIDAR、IMU、編碼器，並把它們連到頁面的符號（例如 LIDAR 對應量測 z）。這張圖同時是 V1。
3. **自繪差速運動學圖**：以 `parts.py robot` 畫俯視的差速機器人，標出位置 x、y、朝向 θ、線速度 v、角速度 ω 與輪距。符號與公式、符號對照表同色（第 5 輪 R1）。參考圖 `temp/round-05/Differential_Drive_Kinematics_of_a_Wheeled_Mobile_Robot.png`、`temp/round-05/differential-3582cb59.png` 只作構圖參考，不引用。
4. **順序**：R8 完成後才畫，讓機器人物件使用修正後的畫法。

### R7 autoresearch 範例改用目前模板的 CSS

1. `examples/autoresearch/` 的 3 頁把 `<style>` 換成目前模板的版本，做法比照第 5 輪檢查點 D 的 explain-as-webpage 兩頁（`docs/plan/05-symbols-pictorial-plan.md`〈結果〉檢查點 D）。文字、圖與圖說不變。
2. 換 CSS 後，DOM 對比掃描（`CLAUDE.md`〈驗證指令〉）在 1280px 與 700px 都沒有低於 4.5:1 的組合。
3. 重截 README 的三張層級示意圖：`docs/images/tier-l0-figure.png`、`docs/images/tier-l1-slider.gif`、`docs/images/tier-l2-stepper.gif`。尺寸、幀數與裁切範圍沿用現有檔案。重截前先以舊頁重產一次，確認做法能重現現有檔案（比照封面圖的做法）。

### R8 `ink-shade` 不再染到外框

1. **問題**：`ink-shade` 是不加外框的同一形狀，畫在物件之後，會蓋住外框內側的一半。放大時，背光側的外框帶有概念色（`docs/plan/05-symbols-pictorial-plan.md`〈結果〉T19）。
2. **修改**：`skills/explainer-figure/scripts/parts.py` 的 `group()` 改變陰影的畫法，讓陰影只落在外框以內。實際做法（例如陰影畫在外框之前、陰影之後重畫只有外框的形狀，或縮小陰影的裁切範圍）在 T4 實作時比較後決定。
3. **同步**：`pictorial.md` 中由 `parts.py` 產生的片段重新產生，並與輸出逐字相同；`examples/starship-reusability/` 與 `examples/llm-wiki/` 中的物件重新產生。llm-wiki 圖 5 手寫的摺角陰影（`ink-shade` 加 `ink hollow`）一併檢查。
4. **不變**：正常大小下的外觀、物件的尺寸與位置。

## 2. 技術組成與指令

本儲存庫沒有建置系統或測試套件。下列指令都是驗證用。

```bash
# 既有：manifest、plugin、模板外部資源、兩種寬度截圖、DOM 對比掃描（見 CLAUDE.md〈驗證指令〉）
for f in .claude-plugin/*.json .codex-plugin/plugin.json .agents/plugins/marketplace.json; do python3 -m json.tool "$f" >/dev/null && echo "ok $f"; done
claude plugin validate .
claude --plugin-dir . plugin details explain-as-webpage   # 應顯示 Skills (3)
wc -l skills/*/SKILL.md                                   # 各約 130 行以內

# 既有：自檢指令（explainer-page/SKILL.md 第 6 步；explainer-figure/SKILL.md § Self-check 的對比、壓線、意圖檢查）
python3 -c "import PIL; print(PIL.__version__)"           # 選用：裁切壓縮
command -v pdftoppm pdfimages google-chrome               # 必要：PDF 裁切、網頁截圖
```

本輪新增的指令要在實作後寫進 skill，並實際執行一次：

- 授權查詢（R2）：輸入 Commons 檔名或 Openverse 查詢字串，印出作者、授權與連結。
- 裁切壓縮（R3）：輸入原圖、裁切範圍與寬度，輸出圖檔並印出大小。
- 資產檢查（R5）：輸入主題的頁面，全部通過時不印出任何內容。

## 3. 會動到的檔案

| 檔案 | 需求 | 變更 |
|---|---|---|
| `skills/explainer-cite/SKILL.md`（新增） | R1–R5 | 流程、輸入輸出、授權分類、資產檢查指令 |
| `skills/explainer-cite/references/`（新增） | R2、R4 | 來源與授權的細節；標註引用圖的配方。檔名在 T6a 確定 |
| `skills/explainer-cite/scripts/`（新增） | R2、R3 | 授權查詢與裁切壓縮。檔名與子指令在 T6a 確定 |
| `skills/explainer-figure/SKILL.md` | R1 | 圖型表新增「引用圖」一列 |
| `skills/explainer-page/SKILL.md` | R5 | 見 R5 第 1 點 |
| `skills/explainer-page/references/extending-pages.md` | R5 | 共用資產與頁面樹檢查 |
| `skills/explainer-page/references/writing-rules.md` | R5 | 圖片來源行、固定標籤 |
| `skills/explainer-page/assets/template.html` | R5 | `figure img` 樣式 |
| `skills/explainer-figure/scripts/parts.py` | R8 | `group()` 的陰影畫法 |
| `skills/explainer-figure/references/pictorial.md` | R8 | 重新產生的片段 |
| `examples/starship-reusability/starship-reusability.html`、`examples/llm-wiki/llm-wiki.html` | R8 | 重新產生的物件 |
| `examples/autoresearch/*.html` | R7 | `<style>` 換成目前模板的版本 |
| `docs/images/tier-l0-figure.png`、`tier-l1-slider.gif`、`tier-l2-stepper.gif` | R7 | 重截 |
| `.claude-plugin/*.json`、`.codex-plugin/plugin.json`、`.agents/plugins/marketplace.json` | — | 版本升為 0.6.0 |
| `CLAUDE.md`、`README.md`、`README.zh-TW.md` | — | 「兩個 skill」改為三個；架構段落加入 explainer-cite 與 `<hub>.assets/` |

`skills/explainer-page/SKILL.md` 已有 130 行，本輪必須修改它（R5）。修改以改寫既有句子為主，淨增以 2 行為上限；超過時，把第 6 步既有的部分說明移到 references。`skills/explainer-figure/SKILL.md` 目前 124 行，本輪只新增圖型表的一列。

## 4. 寫作風格

- skill 的檔案用英文，句型比照現有 references：短句、一句一個動作、規則後面附上它要防止的失敗。
- 規格與計畫文件用繁體中文與台灣用語，並遵守 `writing-rules.md`。
- 新的配方附一段可以直接複製的片段，格式比照 `pictorial.md` 的 P1；使用腳本的配方附上指令與它的輸出。

## 5. 驗證策略

| # | 驗證項目 | 需求 | 判定方式 |
|---|---|---|---|
| V1 | EKF 頁 v3 的論文照片（本機） | R2–R4、R6 | 授權確認為 CC BY 4.0；圖說有作者、授權、連結與「標註為本頁加上」；引線標出 LIDAR、IMU、編碼器並連到符號；由使用者判讀 |
| V2 | LightGlue 論文 PDF 的圖（document 模式） | R2–R5 | 從 PDF 裁出的圖清晰，授權依 arXiv 摘要頁標示；授權受限時逐張列在確認中；由使用者判讀 |
| V3 | Wikimedia 主題頁（topic 模式；使用者在任務開始前指定主題） | R2–R5 | 授權欄位來自 API；圖說與 Sources 一致；由使用者判讀 |
| V4 | 公開網頁截圖（使用者在任務開始前指定主題；可與 V3 同頁） | R2–R5 | 截圖逐張列在確認中；只截公開頁；由使用者判讀 |
| V5 | EKF 差速運動學圖 | R6 | 遮住文字的截圖中可辨認機器人與它的朝向；x、y、θ、v、ω 與公式同色；通過壓線檢查 |
| V6 | `ink-shade` 修正 | R8 | 4 倍放大截圖中，背光側的外框只有 `--text` 色；零件總覽圖中所有物件的外觀在正常大小下不變；`pictorial.md` 的片段與 `parts.py` 的輸出逐字相同；7 個範例頁的壓線檢查沒有輸出 |
| V7 | autoresearch 的 CSS | R7 | DOM 對比掃描兩種寬度都是 `<title>none`；新舊層級示意圖並排，由使用者判讀 |

V1–V4 共同的檢查：資產檢查沒有輸出、`FILL` 為 0、沒有外部資源、390px 不溢出、壓線檢查沒有輸出、HTML ≤ ~150 KB、資產資料夾符合 R3 的大小上限。

**回歸檢查**：

- 模板的示範內容在 1280px 與 390px 兩種寬度都通過檢查，DOM 對比掃描通過。
- 7 個範例頁的壓線檢查沒有輸出。
- 3 個 `SKILL.md` 都在約 130 行以內。

### 待驗證的假設

- [ ] Wikimedia Commons、Openverse 與 NASA 的 API 在本機可以用 `curl` 存取，且回傳可用的作者與授權欄位（T1）。
- [ ] `<svg>` 中的 `<image href="<hub>.assets/…">` 在 `file://` 開啟、390px iframe、只看圖與遮住文字的截圖中都能顯示（T2）。
- [ ] 壓線檢查對 `<image>` 沒有誤報（T2）。
- [ ] 一張 1440px 寬的照片以 WebP 壓縮後，在可接受的畫質下小於 200 KB（T2 決定實際上限）。
- [ ] 現有的層級示意圖可以用本機的工具重現（T3）。
- [ ] Codex 會依相對路徑讀取 `explainer-cite/SKILL.md`（列入〈跨輪驗證〉，下次在 Codex 產頁時觀察）。

## 6. 邊界

- **Always**
  - 頁面維持單一 HTML 檔，唯一的例外是放引用點陣圖的 `<hub>.assets/`。
  - HTML 檔維持 ≤ ~150 KB。
  - 每張引用圖都有作者、授權與連結。
  - 三個 `SKILL.md` 各在約 130 行以內。
  - 四個 manifest 檔的版本號同步。
  - 新的指令寫進 skill 後實際執行一次。
  - 每個檢查點提供 `git add` 範圍與提交訊息，由使用者提交。
- **Ask first**
  - 新增第 3 節以外的 reference、腳本或資產。
  - 改變 L0–L2 的判準或篇幅預算。
  - 把驗收頁、點陣圖或資產資料夾加入版本控制。
  - 取代 `examples/` 中除 R7、R8 以外的頁面或圖。
- **Never**
  - 繞過登入牆、付費牆或 cookie 同意牆。
  - 沒有使用者同意就使用受限圖，或把受限圖標示為自由授權。
  - 以 base64 把點陣圖內嵌進 HTML。
  - 把私人路徑或 session 暫存路徑寫進文件。
  - 代替使用者 commit。

## 7. 成功條件

- V1–V7 都完成，使用者判讀 V1–V4 與 V7 後認為可以接受。
- V1–V4 的頁面都通過共同檢查（§5）。
- 三個 `SKILL.md` 各在約 130 行以內，`claude plugin validate .` 通過，`plugin details` 顯示 3 個 skill，四個 manifest 檔都是 0.6.0。

## 8. 不做的事（及理由）

- **使用者自行提供的截圖**（2026-10-16 使用者確認）：需要登入的頁面維持現行做法，請使用者存成 PDF（`sources-and-research.md` §2）。
- **在 `examples/` 新增引用圖的範例**（2026-10-16）：儲存庫不增加點陣圖；第 7 輪的公開案例庫可以收這類頁面。
- **以 base64 內嵌點陣圖**：2–3 張照片就會超過 150 KB 上限。
- **每頁一個資產資料夾**（2026-10-16）：子頁引用同一張圖時要複製多份。
- **AI 生圖**：沿用第 4 輪的決定（`docs/plan/04-visual-forms-idea.md`〈Not Doing〉）：兩個平台不一定都能用，細節可能是捏造的，授權也不明。
- **自動搜尋並選圖**：代理提出候選圖，由確認步驟決定；不在沒有確認的情況下大量下載。
- **影片與動畫 GIF 的引用**：頁面只引用靜態圖。
- **規格表＋L3、程式關係視覺化、C 類計算圖**：分別排在第 8 輪、第 7 輪與之後（`docs/plan/05-symbols-pictorial-idea.md`〈後續輪次〉）。

## 9. 待決問題

- V3、V4 的主題（使用者在 T9、T10 開始前指定）。
- 單張圖與資產資料夾的大小上限（T2 決定）。
- explainer-cite 的 references 檔名、scripts 的檔名與子指令（T6a 決定）。
- `ink-shade` 的修正做法（T4 比較後決定）。
- 層級示意圖的重製工具與參數（T3 決定）。
