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
- [ ] 使用者檢視拆分 diff；提供提交建議（2026-10-06 使用者表示來不及檢視，先繼續 T6；T3–T6 的變更尚未提交）

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

#### T12 新主題一頁

**說明：** 以使用者指定的新主題產出一頁，至少一張具象插圖。

**驗收條件：**
- [ ] 至少一張具象插圖，通過自檢
- [ ] 統計 T10–T12 實際用到的圖示；子集缺少超過 2 成時，改為從 npm 鎖定版本取用

**相依：** T9、使用者指定主題　**規模：** M

### 檢查點 C
- [ ] 使用者判讀新舊並排截圖，以及概念色與語意色是否混淆
- [ ] 使用者決定是否以新版取代 `examples/` 中的兩頁

### 第 5 階段：Codex 與打包

#### T13 Codex 實測（使用者手動）

**驗收條件：**
- [ ] 在 Codex 產出一頁時，編排者讀取了 explainer-figure

**相依：** T9

#### T14 打包

**驗收條件：**
- [ ] 三個 manifest 升為 0.4.0
- [ ] 兩份 README：新 skill、並列安裝說明、目錄樹；`CLAUDE.md` 同步
- [ ] `docs/ideas/visual-forms.md` 的 Open Questions 標註已決定的事項

**驗證：** `CLAUDE.md` 的驗證指令全部通過。

**相依：** 檢查點 C、T13　**規模：** M

### 檢查點 D
- [ ] 全部驗收條件達成；提供最終提交建議

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

- T12 的新主題（使用者在 T12 之前指定）。
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

