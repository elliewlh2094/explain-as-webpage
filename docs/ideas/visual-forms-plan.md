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
- [ ] 新 `SKILL.md` 含 description（限定由編排者呼叫）、圖型選擇判準、圖說明單格式、單圖自檢（移入「只看圖」與「單幀」截圖指令）
- [ ] 所有引用已更新：編排者 `SKILL.md`、`page-types.md`、`writing-rules.md`、`template.html` 註解、兩份 README 的目錄樹、`CLAUDE.md` 架構段；`svg-recipes.md` 內對模板的引用改為 `../../explain-as-webpage/assets/template.html`
- [ ] 兩個 `SKILL.md` 各 ≤ 約 130 行

**驗證：** `grep -rn 'svg-recipes'` 沒有失效路徑；`claude plugin validate .` 通過；`plugin details` 顯示兩個 skill，token 與 T1 基準比較並記錄。

**相依：** 檢查點 0　**檔案：** 約 8 個（多為一行引用）　**規模：** M

#### T4 觸發測試

**說明：** 檢查 explainer-figure 的 description 不會搶走一般繪圖需求。

**驗收條件：**
- [ ] 5 個一般圖表提示（長條圖、折線圖、架構圖等）都沒有觸發 explainer-figure
- [ ] 2 個說明頁提示觸發 explain-as-webpage

**驗證：** `claude --plugin-dir . -p "<提示>" --output-format stream-json --verbose`，檢查輸出中的 Skill 呼叫。

**相依：** T3　**檔案：** 本計畫檔　**規模：** XS

### 檢查點 A
- [ ] 使用者檢視拆分 diff；提供提交建議

### 第 2 階段：視覺詞彙

#### T5 概念色

**說明：** 加入最多 5 個概念色，與語意色分開，並提供 WCAG 對比檢查指令。

**驗收條件：**
- [ ] `template.html` 的 `:root` 有 `--c1`…`--c5` 與淺底色；SVG class `.c1`…`.c5` 與 HTML `.chip.c1`…
- [ ] `svg-recipes.md` § Colour meaning 拆成語意色與概念色；`writing-rules.md` 加概念色規則（與關鍵概念一一對應，不用語意色表示概念）
- [ ] explainer-figure 自檢加入對比檢查指令（Python 讀 `:root` 變數，文字與底色對比 ≥ 4.5:1）

**驗證：** 對比指令實際執行，全部 ≥ 4.5:1；模板兩種寬度截圖正常。

**相依：** 檢查點 A　**檔案：** 4　**規模：** M

#### T6 歸納卡

**說明：** 加入卡片網格的 CSS、配方與觸發條件。

**驗收條件：**
- [ ] 模板有 `.cards`、`.card`、`.chip` CSS（grid，≤ 768px 單欄，內文 ≥ 13px）與一組示範卡
- [ ] `references/cards.md`：結構、每頁 ≤ 2 張、每張 ≤ 6 格、圖例、計入圖數；參考 component.gallery 的 Card 與 Badge
- [ ] `writing-rules.md` 加觸發條件：4 個以上平行項目且欄位相同時，用卡片取代文字

**驗證：** 390px iframe 檢查輸出 `<title>ok`；寬版截圖卡片不溢出。

**相依：** T5　**檔案：** 3　**規模：** M

#### T7 圖示

**說明：** 放入檢查點 0 選定圖示庫的子集，說明如何把 symbol 複製進頁面。

**驗收條件：**
- [ ] `assets/icons/` 有子集、LICENSE 與版本記錄
- [ ] `references/icons.md`：名稱索引、複製 `<symbol>` 的方法、顏色用 `currentColor`、檢查指令
- [ ] 模板頂部的 `<defs>` 預留 symbol 區塊

**驗證：** 檢查指令在示範頁實際執行一次：符合時沒有輸出，有缺漏時列出；記錄子集大小。

**相依：** 檢查點 0、T5　**檔案：** 3＋圖示子集　**規模：** M

#### T8 具象插圖

**說明：** 寫具象插圖配方：分層容器、剪影加引線標註、物件內部組成（範圍依檢查點 0）。

**驗收條件：**
- [ ] `references/pictorial.md` 的每個配方都有符合網格規則的 SVG 片段
- [ ] 配方使用概念色與圖示的方式與 T5、T7 一致

**驗證：** 三個片段截圖沒有溢出或重疊。

**相依：** T5、T7　**檔案：** 1　**規模：** S

### 檢查點 B
- [ ] 使用者檢視模板截圖（卡片、chip、圖示、概念色）與配方片段；提供提交建議

### 第 3 階段：編排者整合

#### T9 圖說明單接入流程

**說明：** 讓編排者在學習摘要中為每張圖寫圖說明單，並在產出步驟交給 explainer-figure。

**驗收條件：**
- [ ] 編排者第 2 步加入圖說明單（格式在 explainer-figure）；第 5 步指向 `../explainer-figure/SKILL.md`；寫明兩個 skill 需並列安裝
- [ ] `page-types.md` 標出各頁型可用的新圖型
- [ ] 讀圖四問由兩邊互相引用，不重複

**驗證：** 編排者 `SKILL.md` ≤ 約 130 行；逐條比對新舊規則，沒有矛盾。

**相依：** T5–T8　**檔案：** 3　**規模：** S

### 第 4 階段：驗收頁面

#### T10 重做 starship-reusability

**說明：** 以新 skill 重做 topic 模式範例，沿用原頁的來源。

**驗收條件：**
- [ ] 輸出到 `~/Documents/explainers/`，保留 L2 stepper 且正常運作
- [ ] 與原頁兩種寬度並排截圖
- [ ] 記錄散文字數與圖數的前後比較

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
