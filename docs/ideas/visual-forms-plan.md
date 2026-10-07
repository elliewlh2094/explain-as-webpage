# 實作計畫：擴充視覺表現形式（第四輪）

構想見 `docs/ideas/visual-forms.md`，待辦清單見 `docs/ideas/visual-forms-todo.md`。

## Overview

目前 explain-as-webpage 的圖只有方框、圓點、箭頭組成的流程圖與簡易數值圖。本輪把 skill 拆成編排者 `explain-as-webpage` 與繪圖 skill `explainer-figure`，並加入 B 類具象插圖、D 類歸納卡、圖示與概念色。頁面仍是單檔、離線、不違反授權；L0–L2 判準與既有機制圖、stepper 不退化。

## Architecture Decisions

使用者在 2026-10-06 決定：

- 繪圖 skill 名稱為 `explainer-figure`；第二階段的引用 skill 對應命名為 `explainer-cite`。
- `explainer-figure` 只由編排者呼叫。description 寫明不處理一般圖表；樣式一律取自 `explain-as-webpage/assets/template.html`。
- 重做 starship-reusability 與 llm-wiki 兩個範例，與舊版並排比較。
- 新主題由使用者在 T12 之前指定。

規劃時對構想的調整與補充：

1. **`SKILL.md` 已經是 130 行。** 加入圖說明單與 explainer-figure 指引時，必須同時移出等量內容。第 6 步的「單圖／單幀截圖」說明與 ASCII 那條 rationalization 移到 explainer-figure。
2. **圖示不整包放進模板。** 模板會被複製到每一頁。100 個圖示約 30–50 KB，會占用 150 KB 上限的三成。`assets/icons/` 放子集，頁面只複製實際用到的 `<symbol>`。新增一條檢查指令：每個 `<use href="#i-…">` 都有對應 symbol，而且沒有未使用的 symbol。
3. **歸納卡是 HTML，不是 SVG。** 卡片用 CSS grid，窄版自動變單欄；SVG 有 540px 最小寬度，無法變單欄。歸納卡放在 `<figure id="fig-N" class="cards">` 內，所以有圖號與圖說，計入篇幅預算的圖數（2–5 張），也會出現在既有的「只看圖」截圖中。
4. **回歸檢查改寫。** 每個範例都內嵌自己的 CSS 副本，修改模板不影響範例，所以重新截圖既有範例驗證不到任何東西。真正的回歸風險是新 skill 產出的頁面是否仍保有機制圖與 stepper。驗收改為：模板示範內容在兩種寬度通過檢查，重做的 starship 頁保留 L2 stepper 並正常運作。
5. **跨 skill 相對路徑的安裝風險。** 如果使用者只複製 `skills/explain-as-webpage/`，`../explainer-figure/` 會失效。編排者 `SKILL.md` 與 README 寫明兩個 skill 必須並列安裝。
6. **最高風險的假設先探測。** 具象外形是否畫得穩、圖示庫授權與覆蓋率、拆分前的 token 基準，放在第 0 階段，先於任何搬移。
7. **概念色避開語意色。** 語意色已用紅 `#c0392b`、綠 `#16a085`、橘 `#e67e22`、藍 `#2980b9` 與灰。概念色候選中，靛色接近藍色，橄欖色接近綠色，要以對比與色相差篩選。
8. **提交方式。** build 過程不自行 `git commit`；每個檢查點提供 `git add` 範圍與提交訊息建議。
9. **版本號。** 新增 skill 屬於功能增加，預設升為 0.4.0，三個 manifest 同步。
10. **計畫檔位置。** 本輪的計畫與待辦放在 `docs/ideas/visual-forms-plan.md`、`visual-forms-todo.md`。`tasks/` 保留第三輪內容，不修改。

## Task List

### 第 0 階段：風險探測（不改產品檔案）

#### T1 基準與圖示庫

**說明：** 記錄拆分前的 token 成本，比較 Lucide 與 Tabler 的授權與覆蓋率，建議一套。

**驗收條件：**
- [x] `claude --plugin-dir . plugin details sphinx-style-notes-maker` 的輸出記錄在「探測結果」
- [x] 兩套圖示庫的 LICENSE 原文已讀，內嵌與重新散布的條件已記錄
- [x] 列出 4 個範例與候選新主題需要的圖示概念（實際 101 個），記錄兩套各自的覆蓋率，並建議一套

**驗證：** 套件下載到 `$CLAUDE_JOB_DIR/tmp`，儲存庫沒有新增檔案（`git status` 只有本計畫檔）。

**相依：** 無　**檔案：** 本計畫檔　**規模：** S

#### T2 具象外形試畫

**說明：** 依現有網格規則，在暫存目錄試畫三張 SVG：背包分層容器、人體剪影加引線標註、罐子內部組成。

**驗收條件：**
- [x] 三張 SVG 都在 720 寬的網格上，文字 ≥ 12px
- [x] 截圖交使用者判讀（檢查點 0）
- [x] 如果外形變形，記錄限縮方案：「圖示組合＋簡單幾何容器」（未變形，不需要限縮）

**驗證：** 截圖沒有溢出、重疊或外形破損。

**相依：** 無　**檔案：** 暫存檔、本計畫檔　**規模：** S

### 檢查點 0
- [x] 使用者選定圖示庫與具象插圖的範圍（2026-10-06：Lucide；MVP 採用分層容器、剪影＋引線、物件內部組成三種配方）

### 第 1 階段：拆分（行為不變）

#### T3 建立 `skills/explainer-figure/`

**說明：** 用 `git mv` 把 `svg-recipes.md` 移到新 skill，寫新 `SKILL.md`，更新所有引用。編排者的行為不變。

**驗收條件：**
- [x] 新 `SKILL.md` 含 description（限定由編排者呼叫）、圖型選擇判準、圖說明單格式、單圖自檢（移入「只看圖」與「單幀」截圖指令）
- [x] 所有引用已更新：編排者 `SKILL.md`、`page-types.md`、`writing-rules.md`、`template.html` 註解、兩份 README 的目錄樹、`CLAUDE.md` 架構段；`svg-recipes.md` 內對模板的引用改為 `../explain-as-webpage/assets/template.html`（依既有慣例從 skill 根目錄寫起，不是從 references 資料夾）
- [x] 兩個 `SKILL.md` 各 ≤ 約 130 行（129 行、90 行）

**驗證：** `grep -rn 'svg-recipes'` 沒有失效路徑；`claude plugin validate .` 通過；`plugin details` 顯示兩個 skill，token 與 T1 基準比較並記錄。

**相依：** 檢查點 0　**檔案：** 約 8 個（多為一行引用）　**規模：** M

#### T4 觸發測試

**說明：** 檢查 explainer-figure 的 description 不會搶走一般繪圖需求。

**驗收條件：**
- [x] 5 個一般圖表提示（長條圖、折線圖、架構圖等）都沒有觸發 explainer-figure
- [x] 2 個說明頁提示觸發 explain-as-webpage

**驗證：** `claude --plugin-dir . -p "<提示>" --output-format stream-json --verbose`，檢查輸出中的 Skill 呼叫。

**相依：** T3　**檔案：** 本計畫檔　**規模：** XS

### 檢查點 A
- [x] 使用者檢視拆分 diff；提供提交建議（2026-10-06 使用者表示來不及檢視，先繼續 T6；diff 未經使用者檢視，T3–T4 後來以分組提交收錄）

### 第 2 階段：視覺詞彙

#### T5 概念色

**說明：** 加入最多 5 個概念色，與語意色分開，並提供 WCAG 對比檢查指令。

**驗收條件：**
- [x] `template.html` 的 `:root` 有 `--c1`…`--c5` 與淺底色；SVG class `.c1`…`.c5` 與 HTML `.chip.c1`…
- [x] `svg-recipes.md` § Colour meaning 拆成語意色與概念色；`writing-rules.md` 加概念色規則（與關鍵概念一一對應，不用語意色表示概念）
- [x] explainer-figure 自檢加入對比檢查指令（Python 讀 `:root` 變數，文字與底色對比 ≥ 4.5:1）

**驗證：** 對比指令實際執行，全部 ≥ 4.5:1；模板兩種寬度截圖正常。

**相依：** 檢查點 A　**檔案：** 4　**規模：** M

#### T6 歸納卡

**說明：** 加入卡片網格的 CSS、配方與觸發條件。

**驗收條件：**
- [x] 模板有 `.cards`、`.card` CSS（grid，≤ 768px 單欄，內文 ≥ 13px）與一組示範卡；`.chip` 已在 T5 加入
- [x] `references/cards.md`：結構、每頁 ≤ 2 張、每張 ≤ 6 格、圖例、計入圖數；參考 component.gallery 的 Card 與 Badge
- [x] `writing-rules.md` 加觸發條件：4 個以上平行項目且欄位相同時，用卡片取代文字

**驗證：** 390px iframe 檢查輸出 `<title>ok`；寬版截圖卡片不溢出。

**相依：** T5　**檔案：** 3　**規模：** M

#### T7 圖示

**說明：** 放入檢查點 0 選定圖示庫的子集，說明如何把 symbol 複製進頁面。

**驗收條件：**
- [x] `assets/icons/` 有子集、LICENSE 與版本記錄
- [x] `references/icons.md`：名稱索引、複製 `<symbol>` 的方法、顏色用 `currentColor`、檢查指令
- [x] 模板頂部的 `<defs>` 預留 symbol 區塊

**驗證：** 檢查指令在示範頁實際執行一次：符合時沒有輸出，有缺漏時列出；記錄子集大小。

**相依：** 檢查點 0、T5　**檔案：** 3＋圖示子集　**規模：** M

#### T8 具象插圖

**說明：** 寫具象插圖配方：分層容器、剪影加引線標註、物件內部組成（範圍依檢查點 0）。

**驗收條件：**
- [x] `references/pictorial.md` 的每個配方都有符合網格規則的 SVG 片段
- [x] 配方使用概念色與圖示的方式與 T5、T7 一致

**驗證：** 三個片段截圖沒有溢出或重疊。

**相依：** T5、T7　**檔案：** 1　**規模：** S

### 檢查點 B
- [x] 使用者檢視模板截圖（卡片、chip、圖示、概念色）與配方片段；提供提交建議（2026-10-06：語意色與概念色、chip 容易分辨；歸納卡與圖示「目前還行」，需要實際案例才能判斷效果，留待 T10–T12 與檢查點 C；三個具象插圖配方「還算不錯」）

### 第 3 階段：編排者整合

#### T9 圖說明單接入流程

**說明：** 讓編排者在學習摘要中為每張圖寫圖說明單，並在產出步驟交給 explainer-figure。

**驗收條件：**
- [x] 編排者第 2 步加入圖說明單（格式在 explainer-figure）；第 5 步指向 `../explainer-figure/SKILL.md`；寫明兩個 skill 需並列安裝
- [x] `page-types.md` 標出各頁型可用的新圖型
- [x] 讀圖四問由兩邊互相引用，不重複

**驗證：** 編排者 `SKILL.md` ≤ 約 130 行；逐條比對新舊規則，沒有矛盾。

**相依：** T5–T8　**檔案：** 3　**規模：** S

### 第 4 階段：驗收頁面

#### T10 重做 starship-reusability

**說明：** 以新 skill 重做 topic 模式範例，沿用原頁的來源。

**驗收條件：**
- [x] 輸出到 `~/Documents/explainers/`，保留 L2 stepper 且正常運作
- [x] 與原頁兩種寬度並排截圖
- [x] 記錄散文字數與圖數的前後比較

**驗證：** 編排者第 6 步的全部自檢通過。

**相依：** T9　**規模：** M

#### T11 重做 llm-wiki

**說明：** 以新 skill 重做 document 模式範例。驗收條件與驗證同 T10（沒有 stepper 要求）。

**相依：** T9　**規模：** M

#### T11a 依驗收結果補兩條繪圖規則（2026-10-06 新增）

**說明：** T11 發現兩個規則缺口，使用者同意在本輪修正：圖上已有的文字不在段落中重述；分層容器加上兩側角色與資訊流向箭頭的變化。

**驗收條件：**
- [x] `writing-rules.md` § Figures and text 有「Do not repeat the figure in the text」；`cards.md`、`pictorial.md` 都引用它
- [x] `pictorial.md` 有「P1 with actors and flow arrows」小節與一個 SVG 片段

**驗證：** 片段檢查腳本（預期 4 個片段）、新片段截圖、引用檢查。

**相依：** T11　**檔案：** 3　**規模：** S

#### T12 新主題一頁

**說明：** 以使用者指定的新主題產出一頁，至少一張具象插圖。

**驗收條件：**
- [x] 至少一張具象插圖，通過自檢
- [x] 統計 T10–T12 實際用到的圖示；子集缺少超過 2 成時，改為從 npm 鎖定版本取用

**相依：** T9、使用者指定主題　**規模：** M

### 檢查點 C
- [x] 使用者判讀新舊並排截圖，以及概念色與語意色是否混淆（2026-10-06：三個主題的新版「效果很不錯」）
- [x] 使用者決定是否以新版取代 `examples/` 中的兩頁（同意；已複製 v2 並更新 `README.zh-TW.md` 的兩段說明）

### 第 5 階段：Codex 與打包

#### T13a 材料與整理方式的規則（2026-10-06 新增，來自 T12 的經驗）

**說明：** 代理讀不到的材料（影片、需權限的論文、需登入的頁面）改為依保真度提出取得管道；document 模式的確認固定詢問「依原材料順序或問題導向」，大綱用原材料的結構；事後要求改順序時視為重新規劃。

**驗收條件：**
- [x] `sources-and-research.md` §1 不再「遇到影片就停止」；§2 新增「Material you cannot read」：三種管道、給使用者的提問範例、AI 整理稿的處理規則、不繞過權限
- [x] §3 固定詢問整理方式（原材料順序：單頁或頁面樹；問題導向），大綱取自原材料而非中介文件
- [x] `SKILL.md` When NOT to use 與第 4 步第 1 項同步；≤ 約 130 行
- [x] `extending-pages.md` §2 新增「改成依原材料順序」→ 依 §6 重新規劃，允許搬移並重新編號圖、互動圖的 id 一起改名

**驗證：** 測試腳本 `$CLAUDE_JOB_DIR/tmp/t13a.sh`、引用檢查、`claude plugin validate .`。

**相依：** T12　**檔案：** 4　**規模：** M

#### T13b 頁面與圖的規則（2026-10-06 新增，來自 T12 的經驗）

**說明：** T12 回饋清單的第 3–8、10、11 項：子頁骨架、文件查不到時的寫法、介面示意圖 P4、程式片段標示、讀者例外、卡片連結、篇幅量測範圍、多頁檢查寫成腳本檔。第 9 項（瀏覽器量測的壓線檢查）排入插圖繪製規範。

**驗收條件：**
- [x] `extending-pages.md` §6：子頁圖 1 依原材料順序列出各節並連到段落；主頁圖 1 的子頁節點連到子頁、可用歸納卡取代短節；材料中每段都有的部分（如 Recap）在每個子頁用同一個 `h2`，缺少時照實說明
- [x] `extending-pages.md` §5：篇幅量測只算 `<main>`、不含來源行；多頁檢查寫成腳本檔，不用 `bash -c`
- [x] `sources-and-research.md` §4：一手來源查不到某個名稱時，寫出來源列了什麼，不斷言它不存在
- [x] `pictorial.md` 新增 P4 介面示意圖（附片段，註明「版面為示意，不是實際截圖」）
- [x] `writing-rules.md`：程式片段標示「引用」或「依描述重建」；程式教學可讓非本科讀者選擇看短片段
- [x] `cards.md`：主頁上的卡片標題可以連到子頁

**驗證：** 測試腳本 `$CLAUDE_JOB_DIR/tmp/t13b.sh`、片段檢查（預期 5 個）、P4 截圖、引用檢查、`claude plugin validate .`。

**相依：** T13a　**檔案：** 5　**規模：** M

#### T13c 讓代理真的用上新圖型、保住讀者的問題（2026-10-06 新增，來自 Codex 實測）

**說明：** 使用者在 Codex（GPT-6.1-Sol high）以 Ronin 的機器人工程師路線圖 PDF 實測，新版沒有卡片、具象插圖或圖示，標題變成「本月的學習單元如何連接？」這類模板，舊版的實務問題（職缺要求、沒有硬體或 GPU、作品集）消失。原因：T13a 的「每節一個 `h2`」把標題換成原文結構；路線圖頁型仍寫「表格」、未連到卡片與具象插圖，且「unit card」與歸納卡同名；確認訊息不列圖型；圖型選擇沒有逐項對照。

**驗收條件：**
- [x] 依原材料順序時，原材料只決定順序與範圍，每個 `h2` 仍是讀者的問題；主頁另有 2–4 個貫穿全文的實務問題
- [x] 候選問題附好壞範例；`SKILL.md` 第 2 步要求從讀者處境出發
- [x] 路線圖頁型：各階段成果用連到子頁的卡片，貫穿各階段的成品用具象插圖 P3，「unit card」改為「unit table」，主頁與子頁都問讀者的實務問題
- [x] 確認訊息第 2 項列出每頁預計的圖與圖型；L0 改為「文字＋靜態圖（SVG 或卡片）」；explainer-figure 對每份圖說明單逐列對照圖型表
- [x] 以同一份 PDF 重跑（Codex 與 Claude Code 各一次），比較標題與圖型（T13d）

**驗證：** 測試腳本 `$CLAUDE_JOB_DIR/tmp/t13c.sh`、引用檢查、片段檢查、`claude plugin validate .`。

**相依：** T13b　**檔案：** 5　**規模：** M

#### T13e 候選問題編號與路線圖子頁的固定標題（2026-10-07 新增，來自 T13d）

**驗收條件：**
- [x] 候選問題用 (1)、(2)、(3) 編號，並說明圓圈數字在部分終端機中會擠在一起
- [x] 路線圖子頁：圖 1 與里程碑用固定的短標題（除名詞與來源外只有這兩個）；其餘 `h2` 都是具體問題；資源不獨立成節，放在用到它的問題下或頁尾的 `<details>`

**驗證：** 測試腳本 `$CLAUDE_JOB_DIR/tmp/t13e.sh`、引用檢查、`claude plugin validate .`。

**相依：** T13d　**檔案：** 2　**規模：** XS

#### T13 Codex 實測（使用者手動）

**驗收條件：**
- [x] 在 Codex 產出一頁時，編排者讀取了 explainer-figure（兩次 Codex 實測都讀了 `explainer-figure/SKILL.md`；Codex 的 skill 清單是否顯示 explainer-figure，使用者決定不測）

**相依：** T9

#### T14 打包

**驗收條件：**
- [x] 四個 manifest 檔升為 0.4.0
- [x] 兩份 README：新 skill、並列安裝說明、目錄樹；`CLAUDE.md` 同步
- [x] `docs/ideas/visual-forms.md` 的 Open Questions 標註已決定的事項

**驗證：** `CLAUDE.md` 的驗證指令全部通過。

**相依：** 檢查點 C、T13　**規模：** M

### 檢查點 D
- [x] 全部驗收條件達成；提供最終提交建議（2026-10-07；未完成項目見 T14 結果）

### 第 6 階段：收尾（2026-10-07 新增）

**說明：** T14 結果列出的未完成項目中，下列 3 項屬於本輪交付物的同步或驗證，在本輪收尾。在 Codex 上重跑 T13e 經使用者判斷不做（2026-10-07）。新功能與跨輪的驗證（explainer-cite、插圖繪製規範、C 類計算圖、L3 等）移到第五輪，不在本階段處理。

#### T15 構想文件的假設勾選框

**說明：** `docs/ideas/visual-forms.md` 的 Key Assumptions 有 8 項，都沒有打勾，但多數已在本檔的探測結果中驗證。

**驗收條件：**
- [x] 已驗證的項目打勾，並在同一行附上結果與出處（例如「T4：explainer-figure 0 次觸發」）
- [x] 沒有驗證或只部分驗證的項目維持不勾，並寫明原因（例如 Codex 的 skill 清單：使用者決定不測）
- [x] 前幾輪的構想文件（`explain-as-webpage.md`、`explain-as-webpage-v2.md`、`figure-values.md`）不改，它們是當時的紀錄

**驗證：** 逐項對照本檔「探測結果」中的出處。

**相依：** 無　**檔案：** 1　**規模：** XS

#### T16 Codex marketplace 改回 GitHub 來源（使用者手動）

**說明：** `main` 已推送到 `origin`（`elliewlh2094/explain-as-webpage`）。使用者本機的 Codex marketplace 仍指向本機路徑。

**驗收條件：**
- [x] `codex plugin marketplace add elliewlh2094/explain-as-webpage` 取代本機路徑來源
- [x] Codex 的 plugin 快取資料夾是 0.4.0，skill 清單中有 `explain-as-webpage:explainer-page`

**相依：** 無

#### T17 重做儲存庫說明頁與 README 封面圖

**說明：** `examples/explain-as-webpage/` 的英文與繁中兩頁仍是第三輪的內容：模板寫「254 行」、manifest 寫「0.2.0」，沒有 explainer-figure、歸納卡、具象插圖與圖示。這兩頁的開頭畫面是 README 的封面圖。

**驗收條件：**
- [x] 以 0.4.0 的 skill 重做兩頁，涵蓋兩個 skill 的分工、各檔案的讀取時機與 token 估計值（取自 `plugin details`）、新的圖型
- [x] 兩頁都通過 `SKILL.md` 第 6 步的檢查；390px iframe 為 `<title>ok`
- [x] 依 `CLAUDE.md` 的截圖參數重截 `docs/images/cover-process.png` 與 `cover-process.zh-TW.png`
- [x] 兩份 README 刪除「這一頁描述的是第三輪時的 skill」那一句，並依新內容更新範例說明

**驗證：** 第 6 步檢查、兩種寬度截圖、README 連結檢查、使用者判讀。

**相依：** 無（與 T15、T16 互不相依）　**檔案：** 6　**規模：** L

### 檢查點 E
- [ ] T15–T17 的驗收條件達成；提供提交建議

## Risks and Mitigations

| 風險 | 影響 | 對策 |
|---|---|---|
| 代理畫不穩具象外形 | 高 | T2 先試畫；變形就限縮為圖示組合＋幾何容器 |
| explainer-figure 搶走一般繪圖需求 | 中 | description 限定由編排者呼叫；T4 觸發測試 |
| 圖示占用頁面大小 | 中 | 只複製用到的 symbol；檢查指令列出未使用的 symbol |
| 只安裝其中一個 skill，相對路徑失效 | 中 | `SKILL.md` 與 README 寫明並列安裝 |
| 編排者 `SKILL.md` 超出行數上限 | 低 | T3、T9 移出等量內容到 explainer-figure |
| 概念色與語意色混淆 | 中 | 色相篩選與對比檢查；檢查點 C 由使用者判讀 |

## Open Questions

- ~~T12 的新主題~~：使用者指定 Unity 新手教學影片，材料是 NotebookLM 整理稿（見 T12 結果）。
- **插圖繪製規範（後續工作，使用者 2026-10-06 提出）**：MVP 的三種配方可以接受，但需要一套繪製規範，讓 skill 產出的插圖維持一定品質。本輪 T8 的 `pictorial.md` 先收錄 T2 的發現作為基本規則；完整規範（線寬、填色、比例、標籤與引線位置、品質檢查清單等）建議在檢查點 C 之後，根據 T10–T12 實際產出的插圖歸納，再決定是否排入本輪。
- （第二階段）頁面樹的 `<slug>.assets/` 每頁一個資料夾，或整個主題共用一個。

## 探測結果

### T1（2026-10-06）

**結論：兩套圖示庫的授權都允許內嵌與重新散布，覆蓋率相同（101 個概念各缺 3 個）。建議採用 Lucide，理由是單一圖示較小、線條規格一致；最後由使用者在檢查點 0 決定。**

**token 基準（拆分前，0.3.0）。** `claude --plugin-dir . plugin details sphinx-style-notes-maker` 的輸出：

| 元件 | always-on | on-invoke |
|---|---|---|
| explain-as-webpage | ~400 tok | ~3.8k tok |

產頁時另外讀取的 reference 大小（位元組）：`svg-recipes.md` 18,023、`sources-and-research.md` 14,836、`writing-rules.md` 11,091、`page-types.md` 8,138、`extending-pages.md` 7,342、`template.html` 15,726。`plugin details` 只計算 `SKILL.md`，不計算 references；拆分後要同時比較這兩組數字。

**授權（已讀 LICENSE 原文）。**

| 項目 | Lucide `lucide-static@1.52.0` | Tabler `@tabler/icons@3.49.0` |
|---|---|---|
| 授權 | ISC；其中約 110 個衍生自 Feather 的圖示另受 MIT（Cole Bemis）約束 | MIT（Paweł Kuna） |
| 條件 | 所有副本須附著作權聲明與許可聲明 | 所有副本或實質部分須附著作權聲明與許可聲明 |
| 圖示數（outline） | 2,130 | 5,184 |
| 單一 symbol 大小（去除空白後，中位數／p90） | 約 232／369 B | 約 249／428 B |
| 規格 | 24×24、`stroke="currentColor"`、`stroke-width="2"` | 同左，另多一條透明的 `<path d="M0 0h24v24H0z">` |

兩套都可以內嵌與重新散布。處理方式：儲存庫的 `assets/icons/` 附 LICENSE 原文；頁面只要用到圖示，就在 symbol 區塊前加一段 HTML 註解，內含授權名稱、著作權行與許可聲明（約 0.8–1.1 KB）。Lucide 若用到 Feather 衍生的圖示，註解要再加 MIT 聲明，這是選 Lucide 的額外成本。

**覆蓋率。** 依 4 個範例與候選新主題（Unity GameObject、人體體液、避難包）列出 101 個圖示概念，逐一比對兩套的檔名（腳本在 `$CLAUDE_JOB_DIR/tmp/icons/coverage.py`，不進儲存庫）：

- Lucide 缺 3 個：降落傘（parachute）、腎臟（kidney）、細胞（cell）。
- Tabler 缺 3 個：3D 移動軸（move-3d，可用 `axis-x`／`arrows-move` 替代）、腎臟、手電筒（flashlight）。
- 缺少比例約 3%，遠低於構想文件的 2 成門檻，不需要改為從 npm 取用。
- 腎臟、細胞這類器官與構造，本來就屬於具象插圖（T2、T8）的工作，不靠圖示。

**大小估計。** 子集約 100 個圖示時，儲存庫內的子集檔約 25 KB。一頁用 5–10 個圖示，加上授權註解，約增加 2–4 KB，在 150 KB 上限內影響很小。

### T2（2026-10-06）

**結論：三種具象外形都能用基本圖形（圓角矩形、圓、二次曲線路徑）穩定畫出，沒有變形，不需要限縮。第一版的問題都是標籤與線條的版面衝突，靠截圖找到，修正一次即可。** 試畫檔在 `$CLAUDE_JOB_DIR/tmp/t2/`（`probe.html`、`figures.png`），不進儲存庫。

| 圖 | 配方 | 用到的技法 | 第一版的問題 |
|---|---|---|---|
| A 避難包 | 分層容器 | 圓角矩形包身＋`clipPath` 裁切三層＋引線標註 | 「側袋」標籤壓到包身 |
| B 人體體液 | 剪影＋引線 | 6 個圓角矩形與圓組成剪影；先畫粗外框再蓋填色，得到聯集外輪廓；水位用 `clipPath` 裁切；右側分段長條 | 虛線箭頭穿過標籤；`sm` 標籤壓到長條左緣 |
| C GameObject 罐子 | 物件內部組成 | 罐身路徑＋蓋子＋4 個元件框（各含 1 個 Lucide 圖示）＋引線 | 無 |

寫進 T8 配方的發現：

1. **`clipPath` 要放在該圖自己的 `<svg><defs>` 內。** 放在頁面共用的隱藏 `<svg>` 時，正常頁面顯示正確；但「只看圖」與「單幀」截圖指令會把共用區塊設成 `display:none`，Chrome 就不套用裁切，剪影整個消失。箭頭 marker 與圖示 `<symbol>` 不受影響。
2. **剪影的聯集外輪廓**：同一組圖形先以 `stroke-width:4` 深色畫一次，再以無外框的填色畫一次，重疊處的內部線條就被蓋掉。
3. **圖示用 `<use href="#i-…" width="20" height="20">`**，顏色用 `color` 加 `stroke: currentColor`；20px 的 Lucide 圖示放在 44px 高的元件框內清楚可辨。
4. **文字邊界檢查抓不到「文字壓到圖形」**。試畫用的檢查腳本只估算文字是否超出畫布（故意放一個超出的標籤時，腳本會報錯）；文字與圖形重疊仍要靠截圖判讀。
5. 剪影由圓角矩形組成，外觀接近人台模型。對說明頁足夠；更自然的人體輪廓要用手寫曲線，穩定性未測，不列入 MVP。

### T3（2026-10-06）

**結論：拆分完成，編排者的行為不變。** `svg-recipes.md` 以 `git mv` 移到 `skills/explainer-figure/references/`，所有引用都能解析。

與原計畫不同的四處：

1. **跨 skill 路徑從 skill 根目錄寫起**（`../explain-as-webpage/assets/template.html`），不是原計畫寫的 `../../`。既有 references 都以 skill 根目錄為基準（例如 `extending-pages.md` 寫 `assets/template.html`），維持同一慣例。
2. **圖說明單的「圖型」欄目前只列既有圖型**（9 個配方、stepper、滑桿）。歸納卡與具象插圖在 T6、T8 加入，避免 skill 引用尚不存在的檔案。
3. **explainer-figure 的 frontmatter 設 `disable-model-invocation: true` 與 `user-invocable: false`。** 這直接實作「只由編排者呼叫」：Claude Code 不把它列入可呼叫的 skill，也不出現在斜線選單；編排者用讀檔的方式讀取 `../explainer-figure/SKILL.md`，不經過 Skill 工具。Codex 是否忽略這兩個欄位，由 T13 確認。
4. 安裝說明（兩份 README）的 `cp -r` 改為同時複製兩個資料夾，並說明必須並列。原計畫排在 T14，但不改會讓複製安裝立刻失效，所以提前到本任務。

驗證：

| 項目 | 結果 |
|---|---|
| 引用檢查腳本（`$CLAUDE_JOB_DIR/tmp/t3/refs.py`：skill 內每個反引號中的 `.md`／`.html` 路徑，都要能從 skill 根目錄、`references/` 或所在資料夾解析） | 搬移前 `ok`；搬移後未改引用時列出 8 處失效；改完 `ok` |
| `grep -rn 'svg-recipes' skills` | 只剩新路徑 |
| 三個 manifest 的 `json.tool` | 全部 ok |
| `claude plugin validate .` | 通過（只有根目錄 `CLAUDE.md` 的預期警告） |
| 模板外部資源 grep | 無輸出 |
| 模板 390px iframe | `<title>ok` |
| 移入的兩個截圖指令（對 starship 範例執行） | 只看圖截圖正常；圖 3 停在 3／5 幀 |

**token 比較（`plugin details`）：**

| | 拆分前 | 拆分後 |
|---|---|---|
| always-on | ~403 tok | ~549 tok（explainer-figure ~150；實際 session 不載入，見 T4） |
| explain-as-webpage on-invoke | ~3.8k | ~3.9k |
| explainer-figure on-invoke | — | ~1.8k |
| 產一頁時讀取的「SKILL.md＋繪圖規則」位元組 | 12,064＋18,023＝30,087 | 12,014＋5,412＋16,656＝34,082（+3,995 B，約 +1k tok） |

`plugin details` 把 explainer-figure 的 description 算進 always-on，但 T4 的 session 初始化資訊顯示它沒有被載入，所以實際 always-on 仍約 400 tok。每頁的成本增加約 1k tok，來自新 `SKILL.md` 的圖說明單與圖型表。

### T4（2026-10-06）

**結論：explainer-figure 在 Claude Code 中不會被自動觸發，一般繪圖需求仍交給 dataviz 或直接回答；說明頁需求仍觸發 explain-as-webpage。**

以 `claude --plugin-dir . -p "<提示>" --output-format stream-json --verbose --max-turns 2`（禁用寫檔與網路工具）執行 7 個提示，共花費約 1.4 美元：

| 提示 | Skill 呼叫 |
|---|---|
| g1 月銷售長條圖（SVG） | dataviz |
| g2 CPU 溫度折線圖（SVG） | dataviz |
| g3 Web app 架構圖 | 無 |
| g4 KPI 儀表板 | dataviz |
| g5 登入流程圖（中文） | 無 |
| e1 RANSAC 知識網頁 | `sphinx-style-notes-maker:explain-as-webpage` |
| e2 卡爾曼濾波知識網頁（中文） | `sphinx-style-notes-maker:explain-as-webpage` |

每個 session 的 init 事件中，`skills` 與 `slash_commands` 都只有 `sphinx-style-notes-maker:explain-as-webpage`，沒有 explainer-figure。部分執行以 `error_max_turns` 結束，這是刻意設定的回合上限，不影響判讀。e1、e2 在 2 回合內還沒走到產出步驟，所以「編排者在產出時讀取 explainer-figure」要在 T10 實際產頁時確認。

### T5（2026-10-06）

**結論：模板加入 5 個概念色與 `.chip`，所有圖內文字色在所有底色上的對比都 ≥ 4.5:1。** 檢查過程發現既有的綠色圖內文字未達標，依使用者決定只把文字改深。

**既有的綠色文字。** `svg text.good` 原本用 `--green`（#16a085），在頁面底色上只有 3.20:1。新增 `--green-text`，只用於 `svg text.good`；框線、箭頭、圓點仍用 #16a085，既有範例不受影響。使用者選的方案寫的是 #117a65，但它在概念色淺底上只有 4.43:1（c3）與 4.49:1（c5），所以改用再深一點的 #107360，最低對比 4.86:1。

**概念色的選法。** 語意色在 OKLCH 色相上占了紅 30°、橘 56°、綠 175°、藍 242°。概念色放在剩下的色相區間，而且要夠深，文字才能達到 4.5:1。篩選條件（腳本在 `$CLAUDE_JOB_DIR/tmp/t5pick.py`，不進儲存庫）：

- 文字在頁面底色與自己的 10% 淺底上都 ≥ 4.5:1。
- 與每個語意色的 OKLab 距離 ≥ 0.12。
- 概念色兩兩之間的 OKLab 距離 ≥ 0.08。5 個深色在剩下的色相中很難再拉開；目前最近的一對是紫 c1 與靛 c5（0.094），截圖中仍可分辨。

| class | 顏色 | 淺底 | 頁面底色上的對比 | 與語意色的最小距離 |
|---|---|---|---|---|
| c1 紫 | #7d3c98 | #f2ecf5 | 6.89 | 0.189（藍） |
| c2 橄欖 | #56661a | #eef0e8 | 6.18 | 0.180（綠） |
| c3 洋紅 | #a61e6e | #f6e8f0 | 6.75 | 0.131（紅） |
| c4 棕 | #7a5230 | #f2eeea | 6.65 | 0.136（紅） |
| c5 靛 | #4a3fa0 | #edecf6 | 8.16 | 0.172（藍） |

順序依彼此的區別度排列：頁面只有 2 個概念時用 c1、c2，兩色差異最大。

**CSS 寫法。** `.c1`–`.c5` 各自設定 `--cc`（主色）與 `--cb`（淺底），再由 `svg .box:is(.c1,…)`、`.line`、`.dot`、`text` 與 `.chip` 共用。如此 SVG 與 HTML 用同一組 class，不必重複寫 5 次。`.chip` 原本排在 T6，改在本任務加入，因為概念色的圖例就是文字中的 chip。

驗證：

| 項目 | 結果 |
|---|---|
| 對比檢查（實作前，對原模板） | 缺少 `--green-text`、`--c1`…`--c5`；把綠色列入時 3.20:1 |
| 對比檢查（實作後，`SKILL.md` 中的指令原文） | 無輸出 |
| 對比檢查（把 `--green-text` 改回 #16a085 的副本） | 列出 11 組未達標，最低 2.77:1（在 c3 淺底上） |
| 色票截圖（上排語意色、下排概念色、chip） | 兩排可分辨；棕 c4 與橘色 warn 不相混 |
| 模板外部資源 grep、390px iframe | 無輸出；`<title>ok` |
| 引用檢查腳本 | `ok` |
| `SKILL.md` 行數 | 編排者 129、explainer-figure 107 |

舊範例的 `:root` 沒有 `--green-text` 與 `--c1`…`--c5`，對它們執行檢查指令會出現 `KeyError`。這是預期的結果：檢查指令只用在以新模板產出的頁面。

### T6（2026-10-06）

**結論：模板加入歸納卡（HTML 的 CSS grid），寬版 2 或 3 欄、窄版 1 欄，卡內最小字級 13px。** 規則寫在 `explainer-figure/references/cards.md`，觸發條件寫在 `writing-rules.md`，圖型表加了一列。

設計決定：

- **結構**：`<figure id="fig-N" class="cards">` 內放 `.card-grid`，每張 `.card` 有標題 `.card-title` 與 2–4 組 `<dt>`／`<dd>` 欄位。用 `<dl>` 是因為每張卡的欄位相同，讀者逐欄比較。
- **欄數**：4 張不加 class（2×2），5–6 張用 `cols-3`。不排成一列 4 張以上，因為卡片會窄到中文換行過多。768px 以下一律 1 欄。
- **顏色**：卡片頂邊與標題使用概念色（`c1`–`c5`，沿用 T5 的 `--cc`）；沒有 class 時是中性藍。不在卡片上使用 `bad`／`good`。
- **卡片、表格與機制圖的分工**：以文字描述的 4–6 個平行項目用卡片；以數字比較，或欄位超過 4 個時用表格；有流程、因果或時間關係時用機制圖；3 個以下用文字。
- **component.gallery**：該網站只是各設計系統 Card 元件的索引，可直接採用的只有定義「一張卡代表一個實體」，已引用在 `cards.md`。其餘樣式維持 Sphinx／RTD 的白底細框。
- 模板示範先寫成 3 張 `cols-3` 的彩色卡，與「4–6 張」的規則不符；改為 4 張中性卡，以免代理照抄。

驗證（測試腳本 `$CLAUDE_JOB_DIR/tmp/t6/cardtest.sh`：在 1280px 與 390px 的 iframe 中讀取第一個 `.card-grid` 的欄數、`.card` 內最小字級與頁面是否溢出）：

| 項目 | 結果 |
|---|---|
| 測試（實作前） | 兩種寬度都回報 `no card-grid` |
| 測試（3 張 `cols-3`） | 1280px：3 欄、13px、ok；390px：1 欄、13px、ok |
| 測試（最終 4 張） | 1280px：2 欄、13px、ok；390px：1 欄、13px、ok |
| 單圖截圖指令（`SKILL.md` 原文，`#fig-3`） | 只顯示卡片；非 stepper 圖沒有按鈕，腳本中的點擊不影響截圖 |
| 整頁寬版截圖 | 卡片在 stepper 與反事實表之間，未溢出 |
| 對比檢查、模板外部資源 grep、390px iframe、引用檢查 | 無輸出；無輸出；`<title>ok`；`ok` |
| 模板大小 | 15,726 B → 18,903 B（T5＋T6） |
| `SKILL.md` 行數 | 編排者 129、explainer-figure 108 |

### T7（2026-10-06）

**結論：`skills/explainer-figure/assets/icons/` 收錄 106 個 Lucide 圖示與授權全文；頁面只放實際用到的圖示，由一條同步指令複製。** 用 2 個圖示的測試頁比沒有圖示時多 2,647 B，其中約 2.1 KB 是授權聲明。

檔案：

- `assets/icons/lucide.svg`（25,867 B）：開頭是授權聲明註解（ISC 全文與 Feather 的 MIT 全文，去掉 `--` 以便放進 HTML 註解），之後每行一個 `<symbol id="i-<name>" viewBox="0 0 24 24">`。T1 的 98 個概念圖示，加上 8 個通用圖示（`file-code`、`square-dashed`、`circle-check`、`circle-x`、`gauge`、`scale`、`key`、`hourglass`）。
- `assets/icons/LICENSE`：lucide-static 1.52.0 的 LICENSE 原文。
- `references/icons.md`：分組名稱表、兩種用法（SVG 內的 `<use>`、HTML 內的 `<svg class="icon">`）、同步指令、新增圖示的方法。

設計決定：

- **同步指令取代「只檢查」**：計畫原本寫的是檢查指令（列出缺漏與未使用的 symbol）。改為一條同步指令：讀取頁面中所有 `href="#i-…"`，把對應的 symbol 與授權聲明寫進模板的 `<!-- icons:start -->…<!-- icons:end -->` 區塊，移除不再使用的 symbol，並列出子集沒有的名稱。代理不必手動複製，也就不會漏掉或留下多餘的 symbol；重跑時沒有輸出就代表通過。
- **授權聲明只在用到圖示時寫入頁面**：沒有圖示的頁面不增加任何位元組。
- **顏色**：`.icon` 的 `stroke` 是 `var(--cc, currentColor)`，所以加上 `c1`–`c5` 時是概念色，在卡片標題旁則跟著標題的顏色。
- **大小**：`svg.icon`（HTML 內）設成 1.15em，並以 `min-width: 0` 覆蓋 `figure svg` 的 540px 最小寬度；歸納卡在 `<figure>` 內，不覆蓋的話圖示會被撐到 540px。

驗證（測試腳本 `$CLAUDE_JOB_DIR/tmp/t7/test.sh`：從 `icons.md` 取出指令原文，對一份放了 `#i-rocket`（卡片標題）、`#i-droplet`（stepper，`c1`）與不存在的 `#i-no-such-icon` 的模板副本執行）：

| 項目 | 結果 |
|---|---|
| 測試（實作前） | `FAIL: no icons.md command` |
| 第一次執行 | 第一次列出 `missing: name`：模板 CSS 註解中有字面的 `href="#i-name"`，被指令當成用到的圖示。改寫註解後只列出 `missing: no-such-icon` |
| 寫入的 symbol | 只有 `i-droplet`、`i-rocket`；授權聲明存在 |
| 重跑 | 檔案不變 |
| 移除所有 `<use>` 後再跑 | symbol 0 個，授權聲明一併移除 |
| 截圖 | stepper 中的水滴是紫色（`c1`），火箭在卡片標題前，大小與文字相當 |
| 390px iframe、外部資源 grep（測試頁與模板） | `<title>ok`；無輸出（授權聲明中的網址在註解內，不觸發） |
| 對比檢查、歸納卡測試、引用檢查 | 無輸出；2 欄／1 欄、13px；`ok` |
| 模板大小、`SKILL.md` 行數 | 19,426 B；編排者 129、explainer-figure 110 |

### T8（2026-10-06）

**結論：`explainer-figure/references/pictorial.md` 收錄 3 個具象插圖配方（P1 分層容器、P2 剪影＋引線、P3 物件內部組成），每個都附可直接使用的 SVG 片段，並把 T2 的發現寫成 7 條共同規則。** 三個片段通過自動檢查，截圖沒有溢出或重疊。

共同規則（每條都對應 T2 實際看到的失敗）：用簡單圖形組成物件、左圖右註、`id` 留在該圖自己的 `<defs>` 並加圖號前綴、顏色分工、比例說明、圖示只標部件、文字壓到圖形只能靠截圖發現。

模板新增 6 個 class，讓配方不必寫任何顏色或 `style`：

| class | 用途 |
|---|---|
| `outline` | 容器外框（文字色、2px、無填色） |
| `lead`、`pin` | 引線與引線端點（灰色、1px） |
| `edge`、`shape` | 剪影的兩次繪製：先畫粗外框，再蓋上無外框的填色，只留整體外輪廓 |
| `area` | 填色區域（水位、範圍），主色 25% 不透明度；加 `c1`–`c5` 時用概念色 |

與 T2 試畫不同的地方：

- **剪影只定義一次**：圖形放在 `<defs><g id="f2-person">`，用三次 `<use>`（`edge`、`shape`、`area`）。水位改用矩形 `clipPath` 裁切 `area` 那一次，不再用剪影本身當 `clipPath`。原因是 `clipPath` 內的 `<use>` 不能引用 `<g>`，剪影必須重複寫三次；新寫法只寫一次。
- **`area` 用整體不透明度**：第一版用 `fill-opacity`，腿與軀幹重疊的地方顏色變深（截圖可見）。改為 `opacity: .25`，整組圖形一起合成，重疊處不會變深。10% 淺底色沒有外框時太淡，所以不用淺底色。
- 片段標籤改為英文，與其他 reference 一致；中文頁面的字寬預算仍依 `svg-recipes.md` 的規則。

驗證（測試腳本 `$CLAUDE_JOB_DIR/tmp/t8/check.py`：取出 `pictorial.md` 中的每個 `html` 片段，檢查數量、viewBox、只用模板中存在的 class、`id` 前綴、沒有寫死顏色、`role` 與 `aria-label`、文字邊界，再組成測試頁）：

| 項目 | 結果 |
|---|---|
| 測試（實作前） | `FAIL: no pictorial.md` |
| 測試（實作後） | `ok` |
| 圖示同步指令（對測試頁） | 寫入 4 個 symbol，無輸出 |
| 只看圖截圖 | 三張圖無溢出或重疊；圖 2 第一版重疊處變深，已修正 |
| 390px iframe | `<title>ok` |
| 回歸：引用檢查、對比檢查、歸納卡測試、圖示測試、模板外部資源 grep | 全部通過 |
| 模板大小、`SKILL.md` 行數 | 20,083 B；編排者 129、explainer-figure 111 |

**觀察到的風險：** 測試頁重建後忘了重跑圖示同步指令，圖 3 的圖示就直接消失，畫面上沒有任何錯誤提示。`SKILL.md` 的自檢已要求同步指令必須沒有輸出；T10–T12 實際產頁時，要確認代理有執行這一步。

### T9（2026-10-06）

**結論：編排者第 2 步加入「圖說明單」，`page-types.md` 寫明歸納卡與具象插圖可用於任何頁型的單一問題。** 第 5 步指向 explainer-figure 與「兩個 skill 需並列安裝」已在 T3 完成，本任務不再修改。

- `SKILL.md` 第 2 步新增一條：每張預計的圖寫一份圖說明單，格式見 `../explainer-figure/SKILL.md` § Figure brief，並列出圖型（機制、數值、歸納卡、具象）與概念色。行數 129 → 130，仍在約 130 行的上限內。
- `page-types.md`：頁型表下方加一段。歸納卡與具象插圖不綁定頁型，各用於一個問題；具象插圖也可以當機制頁或實務指南頁的圖 1，條件是主要問題在問位置或容納關係。頁型表與各頁型的圖 1 不變。
- 讀圖四問只定義在 `writing-rules.md` § Figures and text；`svg-recipes.md`、`cards.md` 與 explainer-figure `SKILL.md` 都引用它，沒有重寫（`grep` 確認）。

驗證（測試腳本 `$CLAUDE_JOB_DIR/tmp/t9/test.sh`）：

| 項目 | 結果 |
|---|---|
| 測試（實作前） | 第 2 步沒有圖說明單；`page-types.md` 沒有提到新圖型 |
| 測試（實作後）：第 2 步引用 § Figure brief、並列安裝說明、`page-types.md` 提到 `cards.md` 與 `pictorial.md`、行數 ≤ 131、引用檢查 | `ok` |
| `claude plugin validate .` | 通過（預期的 `CLAUDE.md` 警告） |
| `plugin details` on-invoke | explain-as-webpage ~4.1k、explainer-figure ~2.4k（T3 時為 ~3.9k、~1.8k） |

### T10（2026-10-06）

**結論：以新 skill 重做的 Starship 頁在 `~/Documents/explainers/starship-reusability/starship-reusability-v2.html`（49,511 B），通過編排者第 6 步的全部檢查。新頁用了 2 張具象插圖、1 組歸納卡、3 個概念色與 4 個圖示；散文少了約 5%，圖從 4 張增為 6 張。** 新舊並排截圖在 `~/Documents/explainers/visual-forms-review/`。

確認訊息（第 4 步）的回覆：沿用 5 個核心問題；L2，6 張圖；繁中、非專業大學生；沿用舊頁 8 筆來源（存取日期 2026-10-04），不重新查證。

| 圖 | 舊頁 | 新頁 |
|---|---|---|
| 1 | 因果鏈 | 沿用（語意色） |
| 2 | — | 具象 P1：火箭剖面，層高等於占起飛質量的比例（推進劑 89%、結構與引擎 10%、載荷 1%），左側有 0–100% 刻度 |
| 3 | 兩欄文字框（助推器、飛船） | 具象：兩節堆疊，高度按比例（V3：72.3 m＋約 52 m），引線標註 |
| 4 | 助推器返回 stepper | 沿用 5 步；助推器軌跡改紫色 `c1`、飛船改橄欖色 `c2` |
| 5 | 動能長條（飛船用紅色 `bad`） | 改為 `c1`／`c2`：飛船不是「問題」，舊頁用紅色是語意誤用 |
| 6 | 9 列試飛表 | 歸納卡：6 項能力的狀態、首次、備註，各有圖示；試飛表移入 `<details>` |

概念色：助推器 `c1`、飛船 `c2`、載荷 `c3`，用在圖 2–6、內文 chip 與名詞表。確認訊息中寫「貫穿圖 1–6」，實際上圖 1 是因果鏈，維持語意色，沒有加概念色。

數字比較（散文只計 `<p>`、`<li>` 中的漢字，不含表格、圖、圖說、來源行、`<details>`、名詞與來源兩節）：

| | 舊頁 | 新頁 |
|---|---|---|
| 散文漢字 | 2,244 | 2,129（−5%） |
| 圖 | 4 | 6（L2 上限） |
| 檔案大小 | 37,472 B | 49,511 B（含 4 個圖示與約 2.1 KB 授權聲明） |

驗證：

| 項目 | 結果 |
|---|---|
| `grep -c FILL`、外部資源 grep、來源等級與日期 | 0；無輸出；無輸出 |
| 對比檢查 | 無輸出 |
| 圖示同步指令 | 無輸出；頁面有 `fuel`、`recycle`、`satellite`、`tower-control` 4 個 symbol |
| 390px iframe | `<title>ok` |
| stepper | 第 5／5 幀正常，助推器為紫色 |
| 單圖截圖（圖 2、3、6） | 第一版有 3 個問題，已修正（見下） |

產頁過程中發現的問題：

1. **載荷那一層看不見**：3px 高的 `c3` 層被 2px 的外框蓋住。把它移到外框之後繪製。
2. **圖 3 的比例尺與火箭頂端不一致**：比例尺從 y = 20 開始，鼻錐頂端在 y = 35。改為兩者都從 y = 40 開始（310px = 124 m）。
3. **「上排／下排」在窄版不成立**：歸納卡在 768px 以下會疊成一欄。內文改為「前三張／後三張」，並在 `cards.md` § Limits 加一條規則：以順序或標題指稱卡片，不用列或欄。這是本任務唯一改到 skill 的地方。

尚未驗證：這一頁由我依 skill 檔案產出，所以「編排者在產出步驟會自行讀取 explainer-figure」沒有得到獨立驗證。這要在 T13（Codex）或另一個沒有本對話脈絡的 session 中確認。

### T11（2026-10-06）

**結論：以新 skill 重做的 LLM Wiki 頁在 `~/Documents/explainers/llm-wiki/llm-wiki-v2.html`（42,689 B），通過第 6 步的檢查。新頁用了 2 張具象插圖、1 組歸納卡、3 個概念色與 5 個圖示。散文多了約 10%，原因是依使用者選擇新增了「適用情境」歸納卡與它的引導段落；不計新增內容時，散文與舊頁相當。** 並排截圖在 `~/Documents/explainers/visual-forms-review/llm-wiki-side-by-side-*.png`。

確認訊息的回覆：沿用 5 個核心問題；圖 1–4，**加上**適用情境歸納卡（我原本建議不加，因為 5 個問題中沒有 4–6 個欄位相同的平行項目）；繁中、非專業大學生。document 模式依規則重讀 gist 全文（`curl` 取得 raw，11,985 B），內容與舊頁依據的版本一致，存取日期更新為 2026-10-06。

| 圖 | 舊頁 | 新頁 |
|---|---|---|
| 1 | 因果鏈 | 沿用 |
| 2 | RAG 對 wiki 的 stepper；概念頁用橘色 `warn`、新頁面用綠色 `good` | 沿用 5 步；原始來源 `c2`、wiki 頁面 `c1`；矛盾改用 `bad` 文字標註在概念頁上 |
| 3 | — | 歸納卡：原文 § The core idea 的 5 種適用情境 × 2 個欄位（放進什麼來源、wiki 會長出什麼），各有圖示 |
| 4 | 方框箭頭的三層架構；schema 用 `warn`、wiki 用 `good` | 具象 P1 加資訊流向：git repo 資料夾分成 schema（`c3`）、wiki（`c1`）、raw/（`c2`）三層，LLM 在左、你在右，箭頭表示資訊流向（使用者回饋後修改，見下） |
| 5 | `index.md`／`log.md` 對照表 | 具象 P3：兩份檔案的內容示意（依類別對依時間），取代對照表 |

數字比較（計算方式同 T10）：

| | 舊頁 | 新頁 |
|---|---|---|
| 散文漢字 | 1,474 | 1,628（+10%） |
| 圖、表 | 3 圖、5 表 | 5 圖、4 表 |
| 檔案大小 | 31,661 B | 42,689 B |

散文增加的部分：歸納卡的引導段落（約 90 字）、圖 5 的引導句（約 45 字）、git repo 一句（約 30 字）。第一版問題 2 的段落把圖 4 引線上的「誰寫、誰讀」又寫了一遍（1,681 字），刪除重複後降為 1,628 字。

驗證：

| 項目 | 結果 |
|---|---|
| `grep -c FILL`、外部資源 grep | 0；無輸出 |
| 來源等級檢查 | 列出 gist 那一行沒有等級。document 模式不要求等級（只有 topic 模式要求），屬預期 |
| 對比檢查、圖示同步 | 無輸出；5 個 symbol |
| 390px iframe | `<title>ok` |
| stepper | 第 5／5 幀正常 |
| 單圖截圖（圖 3、4、5） | 無溢出或重疊 |

產頁過程中發現的問題：

1. **重複說明**：見上。這也是規則的缺口。`cards.md` 寫了「卡片取代文字，不在內文重述」，但具象插圖沒有對應的規則；圖 4 的引線已經寫出內容時，段落只需要告訴讀者該看哪裡。建議在 T14 或繪製規範中補上：具象插圖的引線文字不在內文重述。
2. **卡片引導句寫了「第二欄」**：它違反 T10 剛加入的規則（不用列或欄指稱）。改為以欄位名稱「wiki 會長出什麼」指稱。這表示規則有用，但我第一次撰寫時沒有遵守。
3. 歸納卡只有 5 張，`cols-3` 的第二列留一個空位。規則允許，看起來可以接受。

**使用者回饋（2026-10-06）：** 舊頁圖 3 用箭頭表達資訊流向，新版圖 4 第一版只強調三層的意象，流向消失了。改為：資料夾留在中間，LLM 放左邊、你放右邊，6 條箭頭表示資訊流向（LLM 依 schema、讀 raw、寫 wiki；你讀 wiki、挑選來源、與 LLM 一起修訂 schema）。原本右側引線的「誰寫、誰讀」改由箭頭表達，各層的說明放進層內。截圖確認箭頭都停在層的邊緣、標籤沒有壓線；390px 檢查 `<title>ok`；頁面 43,493 B。其餘圖使用者判讀可以。

這個組合（分層容器＋兩側角色＋流向箭頭）是 `pictorial.md` 目前沒有的變化。建議在插圖繪製規範中加入：問題同時問「放在哪裡」與「誰讀寫」時，角色畫在容器外，用箭頭連到各層，不用引線。

### T11a（2026-10-06）

**結論：兩條規則已補上。編排者的 `writing-rules.md` 規定圖上已有的文字不在段落中重述；`pictorial.md` 新增「P1 with actors and flow arrows」，附 LLM Wiki 圖 4 的英文版片段。**

- `writing-rules.md` § Figures and text 新增一條：引線註解、卡片欄位、層內說明留在圖上；段落只說該看哪裡、比較什麼，需要時指向圖的某一部分，不重述。放在編排者這一側，因為段落由編排者撰寫，而且規則適用於所有圖。
- `cards.md` 原本的「段落說要比較什麼」改為引用這一條；`pictorial.md` 的共同規則加一條「Notes stay in the figure」，同樣引用它。
- `pictorial.md` 新增 P1 的變化：容器放中間（x = 240–480），角色各放一側，每側最多 3 條箭頭且不交叉，每條箭頭停在層的邊緣、標一個動詞；層的說明放在層內，不用引線；段落只說要比較哪些箭頭。

驗證（測試腳本 `$CLAUDE_JOB_DIR/tmp/t11a.sh`）：

| 項目 | 結果 |
|---|---|
| 測試（實作前） | 4 項規則檢查都失敗；片段數為 3，預期 4 |
| 測試（實作後）：規則與引用、P1 變化小節、4 個片段的網格／class／`id` 前綴／顏色／文字邊界、引用檢查 | `ok` |
| 新片段截圖 | 箭頭停在層的邊緣，標籤沒有壓線；圖說第一版寫「your arrows reach only the top and bottom layers」，但 wiki → You 的箭頭也連到 wiki，改為「the only arrow into the wiki comes from the LLM」 |
| 390px iframe（4 個片段的測試頁） | `<title>ok` |
| `SKILL.md` 行數 | 編排者 130、explainer-figure 111（未改動） |

### T12（2026-10-06）

**結論：新主題頁在 `~/Documents/explainers/unity-beginner/unity-beginner.html`（42,355 B），通過第 6 步的全部檢查。頁面用了 1 張具象插圖（GameObject 罐子）、1 組歸納卡、1 個滑桿（L1）、3 個概念色與 10 個圖示。**

材料與確認：

- 使用者指定 YouTube 影片〈The Unity Tutorial For Complete Beginners〉，提供用 NotebookLM 整理的 `~/Downloads/Unity 新手指南.md`（30,354 B，約 5,860 個漢字，5 段從不同角度整理同一部影片）。以 document 模式處理。
- 確認回覆：問題 1–5（三步學習法、GameObject 與 Component、五個步驟、引用、Time.deltaTime）；問題導向單頁、L1；非本科大學生，允許短程式片段；**加上**輕量核對 Unity 官方文件。
- 核對了 12 個 API 與 2 篇 Manual（Unity 2021.3，影片使用的版本）。11 個的官方說明與整理稿一致。`FindGameObjectWithTag` 在 2021.3、2022.3、6000.0 的個別頁面都回傳 404，GameObject 類別的方法清單中只有 `FindWithTag`（「回傳一個帶有該 Tag、啟用中的 GameObject」）。頁面照實寫出，並建議找不到時改用 `FindWithTag`；沒有斷言舊名稱不能用。

| 圖 | 形式 | 內容 |
|---|---|---|
| 1 | 路線圖（Recipe 7，主軸） | 三步學習法，每一步的成果對應本頁的圖 |
| 2 | 具象 P3 | Bird 這個 GameObject（`c1`）的罐子，裝 5 個 Component（`c2`），各有圖示與引線 |
| 3 | 歸納卡（5 張） | Flappy Bird 的 5 個步驟：做出什麼、學到什麼 |
| 4 | 對照圖（Recipe 2） | 編輯時拖拽 對 執行時用 Tag 尋找；Prefab 生成的管道用 `c3` |
| 5 | 滑桿（L1） | 調整 FPS（30–120），比較「每幀移 0.1」與「乘上 deltaTime」的每秒距離；示意數字 |

散文 1,499 個漢字（預算約 3,500），5 張圖（L1 上限 5）。

驗證：

| 項目 | 結果 |
|---|---|
| `grep -c FILL`、外部資源 grep | 0；無輸出 |
| 來源等級與日期（整理稿列為 g3，Unity 文件 g1） | 無輸出 |
| 對比檢查、圖示同步 | 無輸出；10 個 symbol |
| 390px iframe | `<title>ok` |
| 滑桿：依序點 30／60／120 FPS 按鈕 | 0.50／1.00／2.00 倍；長條寬 120／240／480 px |
| 單圖截圖（圖 2–5） | 無溢出；圖 4 的兩條箭頭原本沒有對應到 ①②，補上編號 |

**圖示覆蓋率（T10–T12）：** 三頁共用到 19 個不同的圖示，全部在子集中，缺少 0%，低於 2 成的門檻，不需要改為從 npm 取用。

**發現的規則缺口：** skill 規定「影片不接受為材料」與「只用全文、不用摘要」。這次的材料是 AI 工具整理的影片摘要，由使用者主動提供。我依 document 模式處理，並做了 4 件事：
1. 頁首加「說明」框，寫明材料是 NotebookLM 整理稿，不是影片本身。
2. 來源列為 g3。
3. 把 NotebookLM 自己的評價（「非常值得觀看」、大型專案改用 Singleton）放進「限制與整理稿的補充」，不當成影片的主張。
4. 整理稿的「證據位置」欄大多是空的，因此無法回溯到逐字稿，頁面也寫明了這一點。

這些做法目前不在 `sources-and-research.md` 中，建議在 T14 或下一輪補成規則。

### T12 延伸：依影片順序改寫成頁面樹（2026-10-06）

**結論：使用者追問「五個步驟各做成獨立頁面，主頁順著影片的話題順序」，並補充了 NotebookLM 整理稿（新增 7 段，檔案 54,181 B）。依 `extending-pages.md` §6 改成主頁＋5 個子頁，六頁都通過第 6 步與 §5 的檢查。**

確認回覆：主頁＋5 個子頁（Step 4、5 雖在整理稿同一段，仍依影片拆成兩頁）；各頁層級與圖依提案（只有 Step 3 是 L1）；新 API 繼續輕量核對。

| 頁面 | 內容 | 圖 | 散文漢字 | 大小 |
|---|---|---|---|---|
| `unity-beginner.html`（主頁，改寫） | 影片怎麼鋪陳 → 三步學習法 → 準備 → 五個步驟 → 下一步 | 影片結構圖（步驟框連到子頁、標出 Recap）、三步學習法、五步歸納卡（標題連到子頁） | 1,625 | 32,867 B |
| `--step1-interface` | 四個面板、GameObject 與 Component、讓鳥出現 | 子頁圖 1、Unity 編輯器四面板的具象圖（新）、罐子（從主頁移來，註解加上各組件在第幾步加入） | 910 | 29,821 B |
| `--step2-physics-input` | Rigidbody 2D、Start 與 Update、引用、按鍵跳躍、public 變數 | 子頁圖 1、Start／Update／GetKeyDown 的 8 幀時間軸（新）、Inspector 中拖入引用的具象圖（新） | 1,109 | 29,205 B |
| `--step3-pipes` | 父子物件、deltaTime、Prefab 與生成、Destroy | 子頁圖 1、父子管道具象圖（新）、deltaTime 滑桿（從主頁移來）、管道生命週期流程（新） | 1,384 | 33,742 B |
| `--step4-score` | Logic Manager 與 UI、計分與 ContextMenu、Trigger 與 Tag、Layer 與參數化 | 子頁圖 1、管道中間 Trigger 的具象圖（新）、拖拽對 Tag 尋找（從主頁移來） | 1,367 | 30,625 B |
| `--step5-game-over` | Game Over 與重來、Collision 判定失敗、birdIsAlive、打包 | 子頁圖 1、Collision 對 Trigger（新）、birdIsAlive 的前後對照（新） | 947 | 27,025 B |

做法：

- 依 §6，六頁的共用部分（側欄頁面樹、麵包屑、每頁的圖 1、從主頁移來的圖的重新編號、圖示同步）由一支暫存腳本 `$CLAUDE_JOB_DIR/tmp/t12b/gen.py` 從同一份清單產生；各頁內容分別寫在 `*.content.html`。腳本暫時保留，方便使用者要求修改時重建；job 刪除時一併清除。
- 子頁圖 1 用 Recipe 7 的「三個一列、蛇形」排列整理稿各小節的順序，每個方框連到對應的段落；主頁圖 1 用同一個函式，步驟框連到子頁。
- 每個子頁最後一節是「作者怎麼總結這一步？」，對應影片的 Recap。整理稿說 Step 1–4 都有 Recap，但沒有記下 Step 4 的內容；Step 4 子頁照實說明，並依本頁四節整理重點。
- 新增 API 核對：`Random.Range`（float 版包含兩端）、`Debug.Log`、`SetActive`、`GetActiveScene`、`ContextMenu`、`Vector2.up`、`Vector3.left`、`transform.position`、`GameObject.layer`、`KeyCode.Space` 與 uGUI 的 Canvas Scaler、Rect Transform（調整大小改寬高、不改縮放）都與整理稿一致。uGUI 的頁面在 Scripting API 中是 404，改查 uGUI 1.0 套件文件。

驗證：

| 項目 | 結果 |
|---|---|
| 每頁 `FILL`、外部資源、來源等級與日期、對比 | 全部為 0 |
| 每頁 390px iframe | 6 頁都是 `ok` |
| 頁面樹一致（`extending-pages.md` §5） | 6 頁的區塊雜湊相同（`6 9b06…`）；每頁都標記自己；所有連結的頁面都存在 |
| 對照表：整理稿 37 個小節 → 頁面與 `h2` | 只印出 1 行 skipped：「快速判斷」一段是 NotebookLM 的評價，未採用（其中「可能無用處」的事實已併入主頁的限制） |
| Step 3 滑桿（移到子頁、編號改為 f3-） | 30／60／120 FPS 為 0.50／1.00／2.00 倍 |
| 逐圖截圖（6 頁共 19 張） | 修正 4 處：Step 1 編輯器圖的拖曳箭頭穿過檔名；Step 2 Inspector 圖的箭頭穿過欄位名、兩條註解太近；Step 3 流程圖「timer 歸零」標錯箭頭；Step 4、5 的 Trigger 註解與引線重疊或過擠 |

**過程中的工具問題：** 檢查腳本第一版用 `F=… bash -c "$(cat 對比檢查)"` 執行對比檢查，被 Claude Code 的刪除安全檢查擋下（它無法檢查 `bash -c` 內的腳本）。改成把對比檢查存成 Python 檔、整個檢查寫成一般腳本檔執行。skill 中的指令都是直接的 heredoc，不受影響。

### T13a（2026-10-06）

**結論：skill 不再把「影片」一律視為範圍外。代理讀不到材料時，改為依保真度提出三種取得管道；document 模式的確認固定詢問整理方式；頁面寫好後才要求改順序時，視為重新規劃。**

使用者對 T12 回饋的決定：第 1 點從「影片」放寬到所有代理讀不到、但使用者能透過其他工具取得的材料；第 2 點的主修正放在確認步驟，延伸頁面只做退路。

修改：

| 檔案 | 內容 |
|---|---|
| `sources-and-research.md` §1 | 「影片網址一律停止」改為「提出取得管道；不下載字幕、不自行繞過權限」 |
| `sources-and-research.md` §2 | 新增「Material you cannot read」：1 使用者自己取得全文、2 逐字稿或匯出、3 AI 工具的筆記（如 NotebookLM，g3）；給使用者的提問範例（依原順序、附時間點、保留原話與程式碼）；以 AI 筆記建頁時的 5 條規則（說明框、來源分級、引用位置、分開工具自己的評價、技術事實對照一手來源） |
| `sources-and-research.md` §3 | 大綱用原材料的結構，不用中介文件自己的標題；整理方式改為固定問題（原材料順序：短的單頁、長的頁面樹；問題導向），並與候選問題合併成同一題；原本長篇材料的兩欄選擇表併入這一段 |
| `SKILL.md` | When NOT to use 只排除「以影片為輸出」；第 4 步第 1 項改為詢問整理方式。行數維持 130 |
| `extending-pages.md` §2 | 新增一列與一條規則：改成依原材料順序視為重新規劃，依 §6 重建；先備份；允許搬移並重新編號圖，互動圖的元素 id 與 script 中的 `f<n>-` 一起改名 |
| `writing-rules.md` 固定標籤 | Note／說明框的用途加上「AI 筆記材料」 |

驗證：

| 項目 | 結果 |
|---|---|
| 測試（實作前） | 14 項失敗 |
| 測試（實作後）：舊的停止規則已移除、新小節與 5 條規則、§3 的整理方式與大綱來源、`SKILL.md` 兩處與行數、`extending-pages.md` 的重新規劃規則、引用檢查 | `ok` |
| `claude plugin validate .` | 通過（預期的 `CLAUDE.md` 警告） |
| `plugin details` on-invoke | explain-as-webpage ~4.1k（未變）、explainer-figure ~2.4k |

README 中「影片不接受為材料」的說法（`README.md` 第 154 行、`README.zh-TW.md` 第 149 行）留到 T14 同步修改。

### T13b（2026-10-06）

**結論：T12 回饋清單的第 3–8、10、11 項都寫進 skill；第 9 項（瀏覽器量測的壓線檢查）依使用者同意的安排，留給插圖繪製規範。**

| 項目 | 檔案 | 內容 |
|---|---|---|
| 3 子頁骨架 | `extending-pages.md` §6 | 子頁圖 1 依原材料順序列出各節（Recipe 7，三個一列），每格連到對應 `h2`；主頁圖 1 的子頁節點連到子頁，短節可用一組連到子頁的歸納卡取代；材料中每段都有的部分在每個子頁用同一個 `h2`，缺少時保留標題並照實說明 |
| 4 文件查不到 | `sources-and-research.md` §4 | 一手來源沒有某個名稱的條目時，寫出它列了什麼，不斷言名稱不存在 |
| 5 介面示意圖 | `pictorial.md` | 新增 Recipe P4（英文版的 Unity 編輯器四面板圖）：面板名稱寫在面板內、一張圖一個動作、圖說註明「版面為示意，不是實際截圖」、需要找真實按鈕時請使用者提供截圖 |
| 6 程式片段標示 | `writing-rules.md` § Code excerpts | 來源行寫明「引用」或「依材料描述重建」；不可把重建的程式當成原文 |
| 7 讀者例外 | `writing-rules.md` § Reader | 程式教學時，非本科讀者可在確認時選擇看程式：每頁 1–2 段、每段最多 5 行 |
| 8 卡片連結 | `cards.md` | 主頁上的卡片標題可連到子頁，卡片同時是導覽 |
| 10 篇幅量測 | `extending-pages.md` §5 | 只量 `<main class="content">`，並去掉來源行 |
| 11 腳本檔 | `extending-pages.md` §5 | 多頁檢查寫成腳本檔執行；`bash -c "$(…)"` 會被 Claude Code 的安全檢查拒絕 |

驗證：

| 項目 | 結果 |
|---|---|
| 測試（實作前） | 10 項規則檢查失敗；片段數 4，預期 5 |
| 測試（實作後）：10 項規則、5 個片段的網格／class／`id` 前綴／顏色／文字邊界、引用檢查、`SKILL.md` 行數 | `ok` |
| P4 片段截圖 | 拖曳箭頭沒有穿過文字，面板標籤都在框內 |
| 新的篇幅量測指令（從 `extending-pages.md` 原文取出執行） | Unity 主頁 1,380 字（舊指令把側欄與來源行算進去，為 1,625 字）；Step 3 子頁 1,151 字 |
| `claude plugin validate .` | 通過（預期的 `CLAUDE.md` 警告） |

### T13c（2026-10-06）

**結論：五項規則修正都已寫入。依原材料順序整理時，標題仍是讀者的問題；路線圖頁型改用卡片與具象插圖；確認訊息會列出每頁的圖型；圖型選擇改為逐列對照。是否真的改善，要由 T13d 以同一份 PDF 重跑判斷。**

Codex 實測（使用者，GPT-6.1-Sol high，材料：Ronin〈How to become a Robotics Engineer in 6 months〉PDF，對話紀錄 `~/Downloads/codex-session-01a11140-…md`，產出 `~/Documents/explainers/robotics-engineer-6-months/`，舊版移到 `~/Downloads/robotics-engineer-6-months/`）的發現：

| 觀察 | 證據 |
|---|---|
| 本機路徑重新安裝成功，編排者會讀 explainer-figure | 對話紀錄讀了 `explainer-figure/SKILL.md`、`svg-recipes.md`，回報「圖解依 explainer-figure 規則製作」 |
| 沒讀卡片、具象插圖與圖示的規則 | `cards.md`、`pictorial.md`、`icons.md` 都沒有被讀取；7 頁 16 張圖全是方框箭頭，沒有卡片、概念色、圖示 |
| 確認訊息詢問了整理方式（T13a 生效） | 提供「依原文順序：總覽＋6 個月份頁」與「問題導向：單頁」兩個選項 |
| 標題變成結構模板 | 每個月份頁都有「本月的學習單元如何連接？」「本月里程碑如何證明你已理解？」「本月資源應該如何使用？」；舊版的「要買哪些東西？要花多少錢？」「沒有硬體也沒有 GPU，這個月要怎麼學？」與主頁的職缺、作品集問題都沒有出現 |
| 第 5 個月圖 2 箭頭歪掉 | 使用者指出後由 Codex 修正；再次說明需要壓線檢查工具 |

修改：

| 檔案 | 內容 |
|---|---|
| `sources-and-research.md` §3 | 「原材料順序」改為：原文各節決定各頁涵蓋什麼與順序，每個 `h2` 仍是讀者會問的問題；新增「Good candidate questions」：從讀者處境出發（要買什麼、花多少、沒有設備怎麼辦、會出什麼錯、怎麼展示成果），避免「本月的單元如何連接」這類只重述結構的問題 |
| `extending-pages.md` §6 | 主頁除了全文結構的問題，另有 2–4 個貫穿全文的實務問題 |
| `page-types.md` 路線圖 | 主頁的「各階段成果」改用連到子頁的卡片；「什麼貫穿各階段」改用具象插圖 P3；新增「讀者帶來的實務問題」；子頁標題要問讀者的問題並舉反例；「unit card」改名為「unit table」；第二張圖可以是本階段成品的具象插圖 |
| `SKILL.md` | 第 2 步的核心問題從讀者處境出發；L0 改為「文字＋靜態圖（SVG 或卡片）」；第 4 步第 2 項列出每頁預計的圖與圖型。行數維持 130 |
| `explainer-figure/SKILL.md` | 每份圖說明單逐列對照圖型表；卡片或具象插圖適用時優先使用，機制圖仍是因果與流程的預設 |

驗證：

| 項目 | 結果 |
|---|---|
| 測試（實作前，含路線圖段落的範圍檢查） | 12 項失敗 |
| 測試（實作後）：13 項規則、`SKILL.md` 行數、引用檢查、5 個片段檢查 | `ok` |
| 殘留的「unit card」 | `skills`、構想文件、README、`CLAUDE.md` 都沒有 |
| `claude plugin validate .` | 通過（預期的 `CLAUDE.md` 警告） |
| `plugin details` on-invoke | explain-as-webpage ~4.2k（+0.1k）、explainer-figure ~2.5k（+0.1k） |

### T13d（2026-10-07，使用者重跑）

**結論：T13c 有效，但效果因代理而異。Claude（Opus 5.5 high）這版標題全是讀者的具體問題，並用了卡片、具象插圖與滑桿；Codex（GPT-6.1-Sol high）的主頁明顯改善，月份頁仍有三個模板標題，也沒有具象插圖。** 兩者都在 Plan mode 執行，提示詞與材料相同。

注意：使用者提供的 `~/Downloads/robotics-engineer-6-months-codex-t13/` 是第一次 Codex 實測的產出（檔案時間 2026-10-06 21:40）。這次 Codex 改用 slug `robotics-engineer-six-months`，實際產出在 `~/Downloads/robotics-engineer-six-months-codex-t13c/`，以下比較用的是後者。

| | 第一次 Codex | Codex（T13c 後） | Claude（T13c 後） |
|---|---|---|---|
| 確認：讀者／展開步驟 | 具基本程式概念的學習者／展開 | 工程師／不展開（「不是逐步安裝教學」） | 非本科大學生／展開 |
| 確認是否列出每頁的圖與圖型 | 否 | 只寫「L0 靜態圖解」 | 是，逐頁列出（因果鏈、卡片、零件圖 P3、L1 滑桿等） |
| 讀了哪些圖型規則 | 未讀 cards／pictorial | 讀了 `cards.md`，未讀 `pictorial.md` | 讀了 `cards.md`、`pictorial.md`、`icons.md` |
| 主頁標題 | 結構導向（「如何連成一條學習路線」「如何讀就業說法」） | 「哪些部分不買硬體也能學，預算怎麼看？」「作品集要保留哪些證據？」等實務問題 | 「沒有硬體或 GPU，哪些可以先做？」「雇主實際看什麼？作品集怎麼寫才可信？」等 |
| 月份頁標題 | 6 頁都是「本月的學習單元如何連接？」「本月里程碑如何證明…」「本月資源應該如何使用？」＋抽象問題 | 6 頁都有「本月如何從基礎走到實作成果？」「如何確認本月能力已達標？」「本月原文有哪些資源？」，中間的問題較具體（「Arduino 與 ESP32 如何選用？」「控制器為何振盪？」） | 只有「這個月學哪些單元？」「月底要能做到什麼？」兩個固定標題，其餘全是具體問題（「為什麼不要用 L298N？」「要不要買 3D 印表機？」「沒有 GPU 怎麼練強化學習？」） |
| 卡片／具象插圖／stepper | 0／0／0 | 主頁 1 組卡片／0／0 | 主頁與第 1 月卡片、第 2、3、5 月具象插圖、每頁 stepper |
| 官方文件查核 | 有 | 有（gazebosim、control.ros.org、OpenCV、Hugging Face 等 6 處） | 有（docs.ros.org、Nav2、Espressif 等 6 處） |

觀察：

- 使用者覺得 Claude「額外找了其他資源」。兩版查核官方文件的數量相近；差別主要來自確認時的選擇：Claude 那次選了「展開成步驟」，`sources-and-research.md` §6 規定展開時要對版本相關指令做輕度查核，所以內容多了安裝與操作的說明。這已在 skill 中，不需要新規則。
- 兩個代理的候選問題都用 ①②③ 編號，在使用者的終端機中擠在一起。skill 沒有規定編號格式；`writing-rules.md` 只在頁面表格中提到 ①②③。
- Codex 月份頁剩下的三個模板標題，對應路線圖子頁骨架的固定部分（圖 1、里程碑、資源）。目前骨架沒有說這些部分該用什麼標題，代理就各自寫成「本月…如何…？」。

### T13e（2026-10-07）

**結論：兩個小缺口已補上。候選問題改用 (1)、(2)、(3) 編號；路線圖子頁除了名詞與來源，只有圖 1 與里程碑兩個固定標題，其餘標題都必須是具體問題，資源不再獨立成節。**

| 檔案 | 修改 |
|---|---|
| `sources-and-research.md` §3 | 候選問題用 (1)、(2)、(3) 編號；圓圈數字在部分終端機與字型中會擠在一起 |
| `page-types.md` 路線圖子頁 | 第 2 項：圖 1 放在固定標題下（「這個月學哪些單元？」）；第 3 項：其餘每個 `h2` 都是具體問題；第 5 項：里程碑放在固定標題下（「月底要能做到什麼？」），並寫明除名詞與來源外只有這兩個固定標題；第 6 項：資源不獨立成節，最推薦的一兩個放在用到它的問題下，其餘收進頁尾的 `<details>` |

固定標題的寫法取自 T13d 中 Claude 那一版；Codex 那一版的「本月原文有哪些資源？」正是第 6 項要避免的寫法。

驗證：

| 項目 | 結果 |
|---|---|
| 測試（實作前） | 5 項失敗 |
| 測試（實作後，路線圖檢查限定在子頁段落）＋引用檢查 | `ok` |
| `claude plugin validate .` | 通過（預期的 `CLAUDE.md` 警告） |

### T14 與檢查點 D（2026-10-07）

**結論：第四輪打包完成，版本 0.4.0。兩份 README、`CLAUDE.md` 與構想文件都已同步；`CLAUDE.md` 列出的驗證指令全部通過。**

| 檔案 | 修改 |
|---|---|
| 四個 manifest 檔 | `.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json`、`.codex-plugin/plugin.json`、`.agents/plugins/marketplace.json` 的版本號 0.3.0 → 0.4.0 |
| `README.md`、`README.zh-TW.md` | 說明兩個 skill；圖片改為「內嵌 SVG 與 HTML 卡片」；L0 改為「文字＋靜態圖（SVG 或卡片）」；新增「不只方框與箭頭」一項（歸納卡、具象插圖、概念色、Lucide 圖示，舉兩個繁中範例；英文版以路徑指出，因為英文 README 只列英文範例）；確認訊息會列出每頁的圖與整理方式；新增 NotebookLM 筆記的使用範例；目錄樹補上 `cards.md`、`pictorial.md`、`icons.md`、`assets/icons/`；「刻意不做的事」拆成「不產出影片」與「不直接讀取讀不到的材料」；授權段落註明內附的 Lucide 圖示 |
| `CLAUDE.md` | 專案現況改為兩個 skill、0.4.0、讀不到的材料的取得管道；架構段補上模板的新 class 與圖示區塊、`cards.md`、`pictorial.md`、`icons.md`、`assets/icons/`；兩個繁中範例的說明 |
| `docs/ideas/visual-forms.md` | Open Questions 中已決定的 4 項（圖示庫、skill 名稱、單獨呼叫、版本號）標註結果；`<slug>.assets/` 與 L3 仍留待以後 |

驗證（測試腳本 `$CLAUDE_JOB_DIR/tmp/t14.sh` 與 `CLAUDE.md` 的驗證指令，寫成腳本檔執行）：

| 項目 | 結果 |
|---|---|
| T14 測試（實作前） | 25 項失敗 |
| T14 測試（實作後）：版本號、README 目錄樹、材料管道、L0、授權、`CLAUDE.md` 架構、Open Questions、引用檢查 | `ok` |
| manifest `json.tool` | 4 檔都 ok |
| `claude plugin validate .` | 通過（預期的 `CLAUDE.md` 警告） |
| `plugin details` | 0.4.0；Skills (2)；always-on ~549 tok；on-invoke 4.2k／2.5k |
| 模板外部資源 grep、寬版截圖、390px iframe | 無輸出；正常；`<title>ok` |
| 7 個範例頁的外部資源 grep | 都是 0 |

**本輪沒有完成、留待以後的項目：**

- Codex 的 skill 清單是否顯示 explainer-figure（`disable-model-invocation` 在 Codex 是否有效）：使用者決定不測。
- 插圖繪製規範，以及其中的瀏覽器量測壓線檢查腳本（T12 回饋第 9 項）。T10–T12 與兩次 Codex 實測都出現箭頭穿過文字或歪掉的情況。
- 第二階段：cite-figure（引用圖片、`<slug>.assets/`）；未來的 L3（anime.js）。
- 推送到 GitHub 後，把 Codex 的 marketplace 改回 GitHub 來源，並確認快取資料夾是 0.4.0。

### 改名：plugin 名稱改為 explain-as-webpage（2026-10-07，併入 T14）

**結論：plugin 名稱、marketplace 名稱、GitHub 網址與 Codex 的顯示名稱，都從 `sphinx-style-notes-maker`／「Sphinx-style Notes Maker」改為 `explain-as-webpage`／「Explain As Webpage」。** 使用者已先把 GitHub 儲存庫改名為 `elliewlh2094/explain-as-webpage`，本機 `origin` 也已指向新網址。安裝後的 skill 名稱變成 `explain-as-webpage:explain-as-webpage`。

| 檔案 | 修改處數 |
|---|---|
| 四個 manifest 檔（`name`、`homepage`、`repository`、`displayName`） | 12 |
| `README.md`、`README.zh-TW.md`（安裝指令、呼叫名稱） | 16 |
| `CLAUDE.md`（`plugin details` 指令） | 1 |
| `examples/explain-as-webpage/` 兩頁（麵包屑、安裝指令、呼叫名稱、來源行） | 22 |

保留舊名稱的地方：`tasks/plan.md`、`docs/specs/explain-as-webpage-v3.md` 與本檔先前的結果記錄，這些是當時的歷史紀錄。本機的儲存庫資料夾仍叫 `sphinx-style-notes-maker`；改資料夾名稱會讓 Claude Code 的專案記憶路徑失效，沒有改。

驗證：4 個 manifest 的 `json.tool` 都 ok；`claude plugin validate .` 通過；`claude --plugin-dir . plugin details explain-as-webpage` 顯示 `explain-as-webpage 0.4.0`、Skills (2)；模板與 7 個範例頁沒有外部資源；`examples/explain-as-webpage/` 兩頁的 390px 檢查都是 `ok`；T14 測試仍為 `ok`。

### 改名：主 skill 改為 explainer-page（2026-10-07，併入 T14）

**結論：plugin 維持 `explain-as-webpage`，主 skill 改名為 `explainer-page`，與 `explainer-figure`、第二階段的 `explainer-cite` 一致。安裝後的呼叫方式是 `/explain-as-webpage:explainer-page`。**

- 資料夾 `skills/explain-as-webpage/` 以 `git mv` 改為 `skills/explainer-page/`；frontmatter `name`、標題（Explainer Page）與模板開頭的註解同步。
- explainer-figure 的 4 個檔案共 18 處：相對路徑改為 `../explainer-page/…`，說明文字中的 skill 名稱一併改。
- 兩份 README、`CLAUDE.md`、`examples/explain-as-webpage/` 兩頁：逐處判斷字串指的是 plugin 還是 skill，只改 skill 的部分（呼叫名稱、`cp -r` 安裝指令、檔案路徑、說明文字）；plugin 名稱、marketplace、GitHub 網址與範例資料夾名稱不變。
- 順便修正：`examples/explain-as-webpage/` 兩頁的 `cp -r` 指令原本只複製一個資料夾，是 T3 拆分時漏改的；現在同時複製兩個 skill。這兩頁其餘內容仍停在 0.2 版的描述（例如「一個 skill」、模板 254 行），而它的開頭畫面是 README 的封面圖，所以沒有改寫。
- 未改：歷史紀錄、`docs/ideas/visual-forms.md` 與 `figure-values.md` 中當時的名稱。

驗證：引用檢查 `ok`；5 個具象插圖片段檢查 `ok`；4 個 manifest 的 `json.tool` ok；`claude plugin validate .` 通過；`plugin details` 顯示 `explain-as-webpage 0.4.0`、Skills (2) `explainer-figure, explainer-page`、always-on ~529 tok；模板無外部資源、390px `<title>ok`；兩個 `SKILL.md` 為 130、111 行。以 `claude --plugin-dir . -p "/explain-as-webpage:explainer-page …"` 實際呼叫：session 的 skill 清單與斜線指令都只有 `explain-as-webpage:explainer-page`（explainer-figure 仍隱藏），代理回覆正在使用該 skill，花費約 0.18 美元。

### T15（2026-10-07）

**結論：`docs/ideas/visual-forms.md` 的 8 項假設都已驗證，全部打勾，每項附上結果與出處。** 前幾輪的構想文件沒有改。

兩項需要說明的判斷：

- 「description 不會搶走一般繪圖需求」：假設寫的驗證方式（5 個一般圖表提示）在 Claude Code 完整執行並通過，因此打勾；Codex 的 skill 清單未測，寫在同一行。
- 「token 成本沒有明顯增加」：每頁約 +1k tok（+13%），增加的部分是新功能（圖說明單與圖型表），拆分本身沒有增加成本，因此打勾；數字寫在同一行，供使用者重新判斷。

驗證：逐項對照本檔 T1、T2、T3、T4、T10、T11、T12、T13、T13d 與檢查點 B、C 的紀錄；`grep` 計數為 8 個 `[x]`、0 個 `[ ]`。

### T16（2026-10-07）

**結論：Codex 已改用 GitHub 來源的 0.4.0。新發現：Codex 的 `$` 自動補全清單同時列出 `explain-as-webpage:explainer-page` 與 `explain-as-webpage:explainer-figure`，表示 explainer-figure 的 `user-invocable: false` 在 Codex 中沒有讓它從清單隱藏。** Claude Code 中 explainer-figure 仍隱藏（T4、T14）。Codex 是否會在一般繪圖需求中自動觸發 explainer-figure 沒有測；這一項移到第五輪的候選清單。

| 檢查 | 結果 |
|---|---|
| `~/.codex/config.toml` | `source_type = "git"`，`source = "https://github.com/elliewlh2094/explain-as-webpage.git"` |
| `codex plugin marketplace list` | ROOT 為 `~/.codex/.tmp/marketplaces/explain-as-webpage` |
| marketplace 快照 | `8bdd0e8`，與當時的 `origin/main` 相同 |
| `codex plugin list` | installed、enabled、0.4.0 |
| plugin 快取資料夾 | 只有 `0.4.0` |
| 新 Codex session 輸入 `$explain`（使用者手動） | 列出 explainer-figure 與 explainer-page |

之後推送新的 commit 時，以 `codex plugin marketplace upgrade explain-as-webpage` 更新快照。

### T17（2026-10-07）

**結論：`examples/explain-as-webpage/` 的繁中與英文兩頁以 0.4.0 的規則重做（project 模式、套件頁型、L0、工程師讀者），兩張 README 封面圖已重截，兩份 README 的範例說明已更新並刪除暫時說明句。** 兩頁都改從目前的 `template.html` 開始，舊頁用的是第三輪的模板（沒有概念色、卡片與圖示的樣式）。

確認回覆：照建議的 (1)–(4) 進行。

| 圖 | 舊頁 | 新頁 |
|---|---|---|
| 1 | 7 步主流程，每格一行檔案 | 每格最多兩行：紫色 `c1` 是 explainer-page 的檔案，橄欖色 `c2` 是 explainer-figure 的規則；第 4 步改用 `user` 圖示標出，不再用 `warn` 色（`warn` 代表後果，語意不符） |
| 2 | 層級選法 | 沿用；L0 改為「文字＋靜態圖」，並註明 SVG 或卡片 |
| 3 | — | 新增歸納卡：機制圖、數值圖、歸納卡、具象插圖，欄位為「適用的問題」與「本儲存庫的例子」，各有圖示 |
| 4 | 8 個檔案的 token 長條 | 13 個長條，依 skill 上色；explainer-figure 的描述以虛線表示（Claude Code 不載入，Codex 會列出） |
| 5 | 追問落點 | 沿用 |

token 估計值（`plugin details`，參考檔與模板逐一包成測試用 skill，2026-10-07）：explainer-page 描述約 390、`SKILL.md` 約 4.2k；explainer-figure `SKILL.md` 約 2.5k；`sources-and-research.md` 7.5k、`page-types.md` 3.9k、`writing-rules.md` 4.9k、`extending-pages.md` 3.6k、`template.html` 7.9k、`svg-recipes.md` 7.0k、`cards.md` 1.6k、`pictorial.md` 7.3k、`icons.md` 1.8k。專案模式不用新圖型的首次產出約 30.4k，三種新圖型都用到約 41.1k，全部約 52.2k。

驗證：

| 項目 | 繁中 | 英文 |
|---|---|---|
| `grep -c FILL`、外部資源 grep | 0；無輸出 | 0；無輸出 |
| 檔案大小 | 51,059 B | 53,166 B |
| 正文（`<p>`、`<li>`，不含表格、圖、來源行、名詞與來源） | 1,808 個漢字＋101 個英文字（舊頁 1,484 漢字；預算約 3,500） | 1,497 字（舊頁同法計 1,210；預算約 1,800） |
| 圖示同步、對比檢查、頁內錨點 | 無輸出；5 個 symbol（`user`、`network`、`chart-column`、`files`、`image`）；全部錨點存在 | 同左 |
| 390px iframe | `<title>ok` | `<title>ok` |
| 只顯示圖的截圖 | 無溢出或壓線 | 同左；英文標籤較長，圖 1 第 4 步的標題右移 10px 避開圖示 |

封面圖：在 1247px 寬視窗量測圖 1 圖說底端（英文 1,108 px、繁中 1,002 px），各加 16 px 後以 `--force-device-scale-factor=1.5` 截取：`cover-process.png` 1871×1686、`cover-process.zh-TW.png` 1871×1527。README 的連結檢查無缺漏。

**使用者回饋（2026-10-07）：** 範例頁只說明專案現狀，不提開發歷程與重做經過。兩頁各改 6 處：Starship 實例表的引言與第 ①、④ 列改寫成單一請求；「解決什麼問題」一節刪除第三、四輪的句子，改為「沒有軟體專案也能用」；「現況與限制」第一項改為「0.4.0，可在 Claude Code 與 Codex 上使用」，來源行改指 `plugin.json` 與 T13d。來源行仍保留指向計畫檔章節的出處，因為每個事實都要有來源。修改後：繁中 50,776 B、正文 1,755 個漢字；英文 52,810 B、正文 1,441 字；兩頁 FILL 0、無外部資源、390px `<title>ok`。修改都在圖 1 之後，封面圖不需要重截。

**使用者回饋（2026-10-07，來源）：** 範例頁不引用 `docs/ideas/` 與 `tasks/`。可改出處的條目改指 README、skill 檔案或 `CLAUDE.md`：拆分理由改依 `explainer-figure/SKILL.md` 的 frontmatter 與 § Overview 描述分工，「現況與限制」改指 README 三節並刪除引用圖片構想的指引。另外 3 處由使用者決定：Starship 實例表第 3 欄第 ①–⑤ 列只寫範例頁上看得到的事實（第 ④ 列改為頁面上的結果），第 ⑥、⑦ 列標為作者實測；WebFetch 實測表保留，段落補上 `sources-and-research.md` §2 的規則，數字標為作者實測；圖 4 的 Codex 虛線長條保留，標為作者實測。兩頁已無 `docs/ideas/`、`tasks/` 字串；繁中 50,635 B、正文 1,767 個漢字；英文 52,824 B、正文 1,453 字；FILL 0、無外部資源、390px `<title>ok`、頁內錨點都存在。
