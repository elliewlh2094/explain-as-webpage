# 規格：explain-as-webpage 第三輪（材料模式）

> 狀態：已實作（2026-10-04，plugin 版本 0.3.0；實作與驗證紀錄見 `docs/plan/03-material-modes-plan.md`）。前兩輪的構想見 `docs/plan/01-initial-skill-idea.md`、`docs/plan/02-english-page-tree-idea.md`。實作時先依本規格以 `planning-and-task-breakdown` 拆成 `docs/plan/03-material-modes-plan.md` 與 `docs/plan/03-material-modes-todo.md`；需求有變動時，先更新本文件再實作。

## 0. 問題陳述與範圍

**問題陳述（How Might We）**：我們如何讓使用者在沒有軟體專案的情況下，只提供材料（網址、PDF、Markdown）或只提供一個主題，再加上想問的問題，就能得到與專案模式同樣好讀、來源清楚的 HTML 知識頁？

**現況的限制**：
- 第 1 步只讀專案。
- 事實只能來自專案檔案，而且明文禁止借用網路數字。
- 預設輸出路徑以 git 儲存庫命名。
- 頁面主軸固定為因果鏈。
- `description` 的觸發條件綁定 "their own project's code"。

**範圍檢查**：下列 R1–R8 都是同一個 7 步流程中的規則，彼此交織，無法各自獨立交付。因此採用單一規格加上需求編號，不另外拆成 capability map。

**已與使用者確認的決策**：
- 維持同一個 skill，在第 1 步依材料類型分流。
- 長篇材料要用「疑問驅動」或「忠實導讀」，每次由使用者選擇。
- 沒有材料時，查證深度（輕量／深度）每次由使用者選擇。深度研究的筆記是否另存也每次詢問，以不另存為優先。
- 不支援影片。
- 第三方材料產出的頁面預設只在本機驗證，不公開。例外：使用者在檢查點 D 判讀後，決定把 LLM Wiki（document 模式）與 Starship（topic 模式）兩頁收進 `examples/`，作為繁體中文範例（2026-10-04）。

## 1. 情境評估

| 情境 | 目前 | 本輪之後 | 依據 |
|---|---|---|---|
| 1. 網路長文網址（Karpathy gist、Paul Graham 長文） | 部分可以：沒有讀取網頁的流程；超過一頁的篇幅預算時，只能在追問時才延伸成頁面樹 | 支援 | R1、R2、R5、R8 |
| 2. PDF 長文（Ronin 的機器人學路線圖） | 部分可以：同上；Claude Code 每次最多讀 20 頁 PDF | 支援 | R1、R2、R4、R8 |
| 3. 技術主題、沒有材料（Harness Engineering 演進、EKF、LightGlue） | 弱：沒有查證流程，也無法區分定論與新興說法 | 支援。主題模式先找原始文件（論文、官方儲存庫），再依文件模式讀取 | R1、R3、R5、R8 |
| 4. 非軟體知識（甲狀腺衛教、Starship、緊急避難包、first principle） | 弱：同 3；沒有讀者設定與高風險主題規則；因果鏈不適合清單或規劃型內容 | 支援 | R3、R4、R5、R6 |
| 5. 先做學習計畫，再轉成網頁（C++） | 可以：Markdown 計畫就是材料；缺少路線圖頁型 | 支援。skill 只負責「Markdown 轉網頁」，前面的計畫步驟由使用者自行完成 | R1、R4 |
| 6. YouTube 教學影片 | 做不到：代理無法觀看影片，web fetch 也取不到字幕 | **不支援**，寫進 When NOT to use | — |

## 2. 需求

### R1 材料模式分流（第 1 步）

| 模式 | 輸入 | 讀取方式 | 事實出處的寫法 |
|---|---|---|---|
| `project` | 專案的程式碼、資料、報告 | 維持現狀 | 路徑＋行號或章節 |
| `document` | 網址、本機 PDF、Markdown 或文字檔、貼上的文字 | 網頁：用 web fetch 工具，或經同意後使用的輔助 skill（R8）。內容不完整或取得失敗時，請使用者把網頁存成 PDF 或文字檔。PDF：先用 `pdftotext -layout`，沒有這個工具時才分段讀取，每次 ≤ 20 頁。文字檔：直接讀取 | 章節標題或頁碼 |
| `topic` | 只有主題與疑問 | 先找原始文件（論文、官方文件、權威機構的資料），找到後依 `document` 模式讀取；其餘部分依 R3 查證 | 網址＋存取日期＋來源等級（R5） |

- **混合輸入**：例如提供論文，但疑問超出論文範圍。材料依 `document` 模式處理，超出範圍的疑問依 R3 查證。
- **影片網址**：說明不支援後停止，不嘗試下載字幕。
- **非專案模式的輸出路徑**：`~/Documents/explainers/<topic-slug>/<topic-slug>.html`，與代理目前所在的目錄無關。專案模式維持 `~/Documents/explainers/<repo-name>/<topic-slug>.html`。

### R2 長篇材料（`document` 模式）

- 確認訊息一律列出以下內容，供使用者勾選與決定：
  - 材料大綱：各章節與其字數。
  - 5–8 個候選疑問：使用者常只說「做得更好懂」，不會主動提出疑問。
  - 兩種做法，由使用者選擇其一：
    - **疑問驅動**：主頁回答 3–5 個疑問，其餘內容以連結指回原文。單頁的篇幅預算不變。
    - **忠實導讀**：第一次產出就建立頁面樹（主頁＋最多約 6 個子頁），沿用 `extending-pages.md` 的命名與側欄規則。主頁放「材料結構圖」，以及連到各章摘要的連結。
- 選擇忠實導讀時，內部摘要要列出「原文章節 → 頁面章節」的對照表，自我檢查時用它確認沒有漏掉的章節。
- 內容以改寫與說明為主。直接引用要短（≤ 2 句）、明確標示，並附上原文連結。

### R3 主題模式的查證（`topic` 模式）

- **確認之前**：先做少量搜尋，只用來擬出大綱與候選疑問。
- **確認時**：讓使用者選擇查證深度。

  | 深度 | 來源數量 | 規則 |
  |---|---|---|
  | 輕量 | 約 5–10 個 | 優先採用原始或權威來源 |
  | 深度 | 較多 | 每個關鍵主張至少要有 2 個獨立來源；來源之間有衝突時，寫在頁面上。另外詢問是否在頁面旁另存 `<slug>.research.md`，預設不另存 |

- **平台沒有網路工具時**：告知使用者，並請使用者提供材料。不得在沒有說明的情況下，改用模型自身的知識撰寫。
- **模型自身的知識**：只能用來寫銜接說明，並標示為「一般背景」。

### R4 頁型與主軸圖

依內容類型選擇主軸圖，取代「每頁都用因果鏈」。

| 頁型 | 適用內容 | 主軸圖（圖 1） |
|---|---|---|
| 機制（現有） | 技術、演算法、物理或生理機制（EKF、可復用火箭、甲狀腺激素） | 因果鏈 |
| 論述 | 論述文、思考方法（Paul Graham 長文、first principle） | 論點地圖：主張 → 理由 → 例子 → 限制 |
| 路線圖 | 學習計畫、路線圖（Ronin 的文章、C++ 學習計畫） | 時間軸：階段、先備條件、產出物 |
| 實務指南 | 準備與決策類（緊急避難包） | 決策樹或分類檢查清單 |
| 演進 | 概念的演變（Prompt → Context → Harness → … Engineering） | 演進圖：每一階段要解決的問題，以及是什麼促成下一階段 |
| 套件、程式導讀（現有） | 程式碼 | 維持現狀 |

- 「反事實對照」只在專案模式中必備。其他模式只在材料支持時，才放「對照」（A 與 B 的比較，或之前與之後的比較）。
- 各章節的標題仍然寫成讀者會問的疑問句。

### R5 共識程度標示

- 來源分為 4 個等級：
  - 原始材料
  - 權威機構或同儕審查
  - 二手整理
  - 新興或個人說法
- 「來源」區的每一筆來源，都要標上等級與存取日期。
- 若某個主張只有「新興或個人說法」等級的來源支撐，就把它放進「新興說法」提示框。例如 Loop Engineering 或 Graph Engineering 若只出自少數人的貼文，就不能寫成定論。
- 內容會快速變動的主題（例如 Starship 的試飛進度），結論要寫明「截至 <日期>」。

### R6 讀者設定與高風險主題

- **讀者設定**分為三種：
  - 一般大眾
  - 非本科大學生
  - 工程師或本科背景

  這項設定決定術語的數量、是否放公式與程式碼，以及是否使用類比。使用類比時，要說明類比在哪裡不成立。專案模式預設為「工程師或本科背景」。
- **高風險主題**包括醫療健康、緊急避難與人身安全、法律、財務。這類主題適用以下規則：
  - 只採用權威來源。頁面面向台灣讀者時，優先採用台灣主管機關或專業學會的資料。
  - 頁首放「注意」框，說明本頁是一般資訊，不能取代專業人員的建議。
  - 不寫劑量，也不寫個人化的治療建議。
  - 醫療主題必須有「何時就醫」段落。
  - 至少要做輕量查證，不提供「只靠模型知識」的選項。

### R7 確認步驟與觸發條件

- 確認訊息仍然只發一次。使用結構化提問時最多 4 題：
  1. 疑問清單與涵蓋方式（R2）
  2. 層級與頁數
  3. 讀者設定與頁面語言
  4. 查證深度、輔助 skill（R8）與輸出路徑

  已有明確預設值的項目，寫在說明文字中即可。
- 重寫 `description`，加入文件模式與主題模式的觸發語，例如「整理成網頁」「這篇文章」「這份 PDF」「知識文件」。長度維持在 1024 字元以內；目前已有 881 字元，需要精簡既有內容。

### R8 選用的輔助 skill 與工具

依能力判斷是否使用，不把任何 skill 設為相依。

- **偵測方式**：Claude Code 會把已安裝 skill 的名稱與描述放進代理的上下文；Codex 預期也是如此，但尚待實測。因此「調查」只是比對代理已經看得到的清單，不掃描檔案系統，也不安裝任何東西。
- **比對的能力**：只比對下列三種。表中列出的是常見例子，不是固定的名稱清單。

  | 能力 | 常見例子 | 帶來的效益 |
  |---|---|---|
  | 讀取網頁 | 瀏覽器類 skill 或工具（例如 `chrome-browser`、`built-in-browser`、fetch 類 MCP） | 讀取需要 JS 或登入的頁面（例如 X 貼文），並取得全文，而不是摘要 |
  | 讀取 PDF | PDF 類 skill（例如 `pdf`） | 處理表格、掃描檔與版面複雜的 PDF |
  | 深度研究 | 研究類 skill（例如 `deep-research`） | 讓 R3 的深度研究有較完整的搜尋與交叉比對 |

- **取得同意**：在第 4 步的單次確認中，列出偵測到的輔助 skill，以及打算用在哪一步，使用者可以拒絕。沒有偵測到，或使用者拒絕時，退回內建做法（web fetch、`pdftotext`、R3 的研究流程）。
- **使用限制**：
  - 輔助 skill 只負責取得材料與查證，產出的內容併入內部摘要。頁面結構、寫作規則與自我檢查仍以本 skill 為準。
  - 輔助 skill 產生的中間檔案放在暫存目錄，並在回報時說明。若輔助 skill 會另外向使用者提問，要在確認訊息中先預告。
  - `SKILL.md` 不把任何其他 skill 的名稱寫成必要條件。例子只放在 reference 中。
- **回報**：第 7 步的回報要寫明實際用了哪些輔助 skill，或退回了哪一種內建做法。

## 3. 技術組成與指令

skill 由 Markdown、單檔 HTML 與 inline SVG 組成，沒有建置系統。執行時會用到 web fetch／search 工具、`pdftotext`、`google-chrome --headless`，以及經同意後使用的輔助 skill。

驗證指令沿用 `CLAUDE.md` 中的 manifest 檢查、`claude plugin validate .`、外部資源 grep 與雙寬度截圖，另外新增下列指令：

```bash
wc -l skills/explain-as-webpage/SKILL.md          # 應 ≤ ~130
python3 -c "import re;t=open('skills/explain-as-webpage/SKILL.md').read();print(len(re.search(r'^description: (.*)$',t,re.M).group(1)))"   # 應 ≤ 1024
pdftotext -layout "<pdf>" - | wc -w               # 估計材料長度
```

## 4. 後續實作會動到的檔案

| 檔案 | 變更 |
|---|---|
| `skills/explain-as-webpage/SKILL.md` | 修改 `description`、Overview、When to Use（加入影片排除），以及第 1、2、4、6、7 步與 Red Flags。目前已有 128 行，必須把細節移到 references |
| `references/sources-and-research.md`（新增） | R1、R2 的讀取規則，R3 的查證流程，R5 的來源等級，R6 的高風險主題規則，R8 的輔助 skill 例子與限制 |
| `references/page-types.md`（新增） | 從 `writing-rules.md` 移入現有的套件與程式導讀頁型，再加入 R4 的 4 種新頁型 |
| `references/writing-rules.md` | 把頁面骨架通用化為「主軸圖」；加入讀者設定；事實與來源規則改為依模式區分；固定標籤表新增「新興說法／Emerging view」「注意／Note」「存取日期／Accessed」 |
| `references/svg-recipes.md` | 新增論點地圖、時間軸、決策樹或檢查清單、演進圖 4 種配方 |
| `references/extending-pages.md` | 新增「第一次產出就建立頁面樹」一節（R2 的忠實導讀） |
| `assets/template.html` | 新增來源等級標籤與「注意」框的樣式，仍然不使用外部資源 |
| `README.md`、`README.zh-TW.md` | 說明三種材料模式與不支援影片 |
| `.claude-plugin/`、`.codex-plugin/`、`.agents/plugins/` | 版本號同步升為 `0.3.0` |
| `CLAUDE.md` | 更新架構段落 |

## 5. 寫作風格

`SKILL.md` 與 references 維持英文、短句、表格，再加上指向 reference 的連結。第 1 步的改寫方向如下：

```markdown
### 1. Identify the material and gather context

| Mode | The user gives | Read it with | Cite as |
|---|---|---|---|
| project | a repo, report, or code path | file reads | `path` + line or heading |
| document | a URL, PDF, Markdown or text file | web fetch / `pdftotext -layout` | heading or page |
| topic | only a topic and questions | primary sources first, then search | URL + access date + grade |

Read `references/sources-and-research.md` for document and topic modes.
Video URLs are out of scope: say so and stop.
```

規格與計畫文件使用繁體中文與台灣用語，並遵守 `writing-rules.md`。

## 6. 驗證策略

以下 8 個驗證案例都要在實作後實際執行一次 skill。

| # | 案例 | 模式與設定 | 主要驗證點 |
|---|---|---|---|
| V1 | Karpathy LLM Wiki gist（https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f） | `document`／網址／短文 | 取得全文、候選疑問、疑問驅動 |
| V2 | Ronin 的機器人學路線圖 PDF（39 頁，約 1.15 萬字） | `document`／PDF／長文 | `pdftotext`、忠實導讀頁面樹、路線圖主軸、章節涵蓋對照 |
| V3 | Extended Kalman Filter（以機器人學的角度） | `topic`／輕量 | 原始來源優先、L2 stepper 呈現預測與更新迴圈 |
| V4 | 甲狀腺亢進與低下衛教 | `topic`／高風險／一般大眾／繁體中文 | 「注意」框、「何時就醫」段落、權威來源、沒有劑量 |
| V5 | SpaceX Starship 與可復用火箭 | `topic`／非本科大學生 | 「截至日期」、類比的限制 |
| V6 | 緊急避難包（台灣常見天災） | `topic`／高風險（人身安全）／實務指南 | 決策樹或檢查清單主軸、台灣機關的來源 |
| V7 | first principle 與其應用 | `topic`／論述 | 論點地圖、每句引述 Musk 的話都有出處、共識程度標示 |
| V8 | C++ 學習計畫 | `document`／Markdown | 路線圖主軸、計畫的每個階段都有對應內容 |

**V8 的前提**：學習計畫的 Markdown 由使用者事先用 `idea-refine` 與 `planning-and-task-breakdown` 產出。這只是本次驗證的準備步驟，不是本 skill 的相依。

**R8 的驗證**：至少讓一個案例使用輔助 skill，例如 V2 使用 PDF 類 skill，或 V3、V4 選擇深度研究時使用研究類 skill。另外至少讓一個案例在使用者拒絕輔助 skill 後走內建做法，再比較兩者產出的完整度。

**每個案例都要通過的檢查**：
- `SKILL.md` 第 6 步的自我檢查指令。
- 1280 px 與 390 px 兩種寬度的截圖檢查。
- 確認訊息只發一次。
- 由使用者判讀可讀性。

**專案模式的回歸檢查**：逐段比對 diff，確認專案模式的規則語意不變；並重新截圖 `examples/` 中的現有頁面。

**頁面的存放位置**：V1、V2 等以第三方材料產出的頁面只放在本機，不加入版本控制。

### 待驗證的假設

- [ ] web fetch 能取得長文的全文。Claude Code 的 WebFetch 可能只回傳摘要。實作時用 Paul Graham 長文做一次只抓取、不產頁的測試；若失敗，改用 `curl` 抓取後在本機轉成文字，或改用 R8 的讀取網頁輔助 skill。
- [ ] 新增 4 種主軸圖後，手繪的 SVG 不會錯位。以截圖檢查。
- [ ] 確認步驟最多 4 題時，使用者仍可以接受。以 V1、V2 的實際互動判讀。
- [ ] 輕量查證足以支撐衛教內容的正確性。以 V4 的來源清單與使用者判讀確認。
- [x] Codex 有可用的網路工具，或「沒有網路工具」的退路可以運作。在 Codex 上實測一次。（T16，2026-10-04：預設就有 `web__run`；唯讀 sandbox 內 `curl` 因 DNS 失敗，Codex 請求在 sandbox 外執行，經使用者核准後取得全文。完全沒有網路工具時的退路未實測，使用者決定不再測。）
- [x] Codex 也會把已安裝 skill 的清單放進上下文，使 R8 的偵測在兩個平台上行為一致。在 Codex 上實測一次。（T16，2026-10-04：清單中有 `sphinx-style-notes-maker:explain-as-webpage`，名稱帶 plugin 前綴。）
- [ ] 輔助 skill 自帶的提問或輸出檔，不會破壞「單次確認、單檔輸出」。以 R8 的驗證案例確認。

## 7. 邊界

- **Always**
  - 維持單檔 HTML，不使用外部資源。
  - 每個事實都附上出處。
  - 執行自我檢查。
  - `SKILL.md` 維持約 130 行以內。
  - 三份 manifest 的版本號同步。
  - 中文使用台灣用語。
- **Ask first**
  - 新增第 4 節以外的 reference。
  - 新增腳本或相依套件，例如 `yt-dlp`、`pypdf`。
  - 改變專案模式的行為。
  - 把 skill 拆成多個。
  - 把任何頁面放進 `examples/`。
- **Never**
  - 支援影片，或下載字幕。
  - 使用外部 CDN。
  - 捏造來源或數字。
  - 高風險主題只靠模型知識撰寫。
  - 把第三方材料產出的頁面加入版本控制。
  - 代替使用者 commit。
  - 把任何其他 skill 設為必要相依。
  - 未經同意就使用輔助 skill。
  - 為了尋找 skill 而掃描檔案系統，或安裝 skill。

## 8. 成功條件

- 8 個驗證案例都產出頁面，並通過自我檢查與截圖檢查；使用者判讀後，認為頁面「比原材料好懂」。
- 每個案例的確認訊息都包含 R7 規定的內容，而且最多 4 題。
- `topic` 模式頁面的每一筆來源，都有等級與存取日期；V4、V6 都有「注意」框。
- 只要用到輔助 skill，確認訊息都事先列出；回報時寫明實際用了哪些輔助 skill，或退回了哪一種內建做法。
- `SKILL.md` 沒有把任何其他 skill 寫成必要條件。
- `SKILL.md` 維持約 130 行以內，`description` 在 1024 字元以內，並通過 `claude plugin validate .`。

## 9. 不做的事（及理由）

- **影片或字幕抓取**：使用者明確排除。
- **跨主題索引或知識庫、三層以上的頁面樹**：延續前兩輪的決定，避免增加管理負擔。
- **自動研究或爬取腳本**：違反「不附產生器腳本」的原則。
- **把其他 skill 設為必要相依**（例如 `deep-research`、`idea-refine`、`planning-and-task-breakdown`）：這些 skill 不一定在兩個平台上都有。改用 R8 的做法：偵測到就提議，經同意才使用，沒有就退回內建做法。
- **掃描檔案系統來尋找 skill**：已安裝 skill 的清單本來就在代理的上下文中，不需要額外存取。
- **公開以第三方材料產出的頁面**：有著作權疑慮。

## 10. 待決問題

- 是否把 EKF（或其他 `topic` 模式的頁面）做成公開範例，放進 `examples/`。
- 使用者貼上的純文字逐字稿是否視為一般文字材料。目前假設會視為一般文字材料，但 skill 不主動索取逐字稿。
- 約 1.2 萬字的材料採用忠實導讀時，約 6 個子頁是否足夠。
- 未列為驗證案例的情境（Paul Graham 長文、Harness Engineering 演進、LightGlue）是否要在後續補驗。
