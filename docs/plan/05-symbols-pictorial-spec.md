# 規格：符號對照圖與具象插圖品質（第五輪）

> 狀態：規格（2026-10-08）。構想見 `docs/plan/05-symbols-pictorial-idea.md`；實作計畫與待辦見 `docs/plan/05-symbols-pictorial-plan.md`。需求有變動時，先更新本文件再實作。

## 0. 問題陳述與範圍

**問題陳述（How Might We）**：我們如何讓頁面上的圖直接連結公式符號與實際物件（機器人、感測器、量測值），並穩定畫出可辨識、可切開標註的具象物件，同時維持單一 HTML 檔與現有的配色規則？

起因、使用者的 4 個例子與量測數據見構想文件〈Problem Statement〉。

**已與使用者確認的決策**：

- 第 5 輪做 D（符號對照圖）與 A（具象插圖品質）；之後先做 explainer-cite，再做規格表＋L3（2026-10-07）。
- 具象物件來源採混合方式：Noto Emoji 子集負責「辨識」，基本形加風格規範負責「結構」（切開、分層、標註部位）（2026-10-07）。
- 插圖風格為「粗外框＋平塗色」（2026-10-07）。
- `<slug>.assets/` 只在頁面引用點陣圖時允許；本輪不使用（2026-10-07）。
- 不放寬 150 KB 上限（2026-10-07）。
- Codex 是否自動觸發 explainer-figure 的測試併入本輪（2026-10-07）。
- 壓線檢查的程式放在獨立檔 `skills/explainer-figure/scripts/check-overlap.js`，`SKILL.md` 只放執行指令（2026-10-08）。
- Codex 觸發測試由使用者手動執行（2026-10-08）。
- 驗收用的新主題，由使用者在該任務開始前指定（2026-10-08）。
- 實作計畫與待辦清單合併成一份文件（2026-10-08）。

**範圍檢查**：下列 5 項需求都在 explainer-figure 的同一個繪圖流程中交會。殘影會用到風格規範，壓線檢查要跑在所有新圖上，符號標註也是一種圖上文字。因此比照第 3 輪，採用單一規格加上需求編號，不拆成多份規格。各需求的相依如下：

| 需求 | 內容 | 相依 |
|---|---|---|
| R1 | 符號對照圖 | — |
| R2 | 壓線檢查 | — |
| R3 | 插圖風格規範與姿態 | — |
| R4 | Noto Emoji 子集 | R3（共用 `pictorial.md` 的規則） |
| R5 | Codex 觸發測試 | — |

## 1. 需求

### R1 符號對照圖

現有的 `writing-rules.md` § Ground the symbols in one running example 要求一張「符號 → 例子中的意義」對照表。R1 把符號放進圖裡，並讓公式與圖使用相同的顏色。

1. **圖說明單新增「Symbols」欄**（`explainer-figure/SKILL.md` § Figure brief）：每一列寫出符號、它在圖上對應的部位、它的概念色；圖上沒有公式符號時寫「none」。
2. **圖上標出符號**：符號放在對應部位旁，後面接一般文字，例如「x̂ₖ 估計位置」。有 Unicode 下標字時直接使用（ₖ、ₜ、ᵢ、₀–₉）；沒有對應字元時，用 `<tspan baseline-shift="sub" class="sm">`。
3. **公式中的符號上色**：模板目前只為 SVG 文字、`.chip` 與 `.card` 定義概念色，HTML 段落中的文字沒有。新增一個 HTML class，暫定寫法為 `<span class="sym c2">P<sub>k</sub></span>`，CSS 為 `.sym { color: var(--cc) }`。實際的 class 名稱在實作時確定。
4. **上色的範圍**：只有關鍵概念的符號使用概念色，所以一頁最多 5 個符號上色，與 `SKILL.md` 第 2 步「關鍵概念最多 5 個」一致。其餘符號仍在圖上標出，也列在符號對照表中，但用一般文字色。
5. **同一個符號在整頁使用同一個顏色**：公式、圖、對照表三處一致。
6. **引用**：`writing-rules.md` § Ground the symbols 加一行，指向 explainer-figure 的符號規則。規則本身寫在 explainer-figure。
7. **對比**：`.sym` 的文字色就是 `c1`–`c5`。既有的對比檢查已涵蓋這 5 個顏色，不需要新增檢查項目，只需確認 `.sym` 沒有使用其他顏色。

### R2 壓線檢查

1. **檔案**：新增 `skills/explainer-figure/scripts/check-overlap.js`，執行時不需要網路。
2. **執行方式**：把頁面複製成暫存檔，在 `</body>` 前插入這支腳本，以 headless Chrome 開啟，再用 `--dump-dom` 讀出報告。`SKILL.md` § Self-check 只放一段執行指令。
3. **檢查範圍**：頁面中每一個 `<figure>` 的 SVG。stepper 要逐幀檢查，只檢查該幀可見的元素。
4. **檢查項目**：

| 類別 | 內容 | 例子（第 4 輪記錄的缺陷） |
|---|---|---|
| 1 文字重疊 | 兩個文字框重疊 | — |
| 2 線條穿過文字 | 有外框線的元素（`line`、`path`、`polyline`，以及 `rect`、`circle`、`ellipse` 的邊）穿過文字框。以 `getTotalLength` 與 `getPointAtLength` 沿線取樣 | 虛線箭頭穿過標籤；拖曳箭頭穿過檔名；箭頭穿過欄位名；註解與引線重疊；「側袋」標籤壓到包身 |
| 3 文字跨在填色邊界上 | 文字框一部分在填色形狀內、一部分在外。以 `isPointInFill` 判斷 | `sm` 標籤壓到長條左緣 |

5. **排除**：元素加上 `data-touch` 屬性時，不參與類別 2、3 的檢查。這個屬性用在本來就應接觸文字的線，例如指到文字的引線端點。
6. **輸出**：每個問題一行，格式為 `fig-N [frame k] 類別: "文字內容" × 元素描述`。全部通過時不印出任何內容，與其他自檢指令一致。
7. **不檢查**：語意錯誤（例如箭頭指錯對象）、間距過小但沒有重疊（例如兩條註解太近）。這兩類仍靠截圖判讀。

### R3 插圖風格規範與姿態

1. **一種風格：粗外框＋平塗色**。這份規範寫在 `pictorial.md`，適用於所有自繪的具象插圖。
   - 外框：統一使用一個線寬，以及圓角的線端與轉角。線寬由 T2 試畫決定，候選值為 3px。
   - 填色：只使用模板變數，包括 `--*-bg` 淺底與概念色淺底。不使用漸層。
   - 陰影：最多一層。做法是在同一個形狀的一側，以低不透明度疊一層較深的同色。
   - 需要時在模板新增 class，命名比照現有的 `outline`、`edge`、`area`。
2. **物件配方**：人、背包、俯視機器人、俯視車、火箭，都用基本形組合。人體剪影改用新風格，這一項併入原 backlog「更自然的人體剪影」。
3. **新配方 P5「物件與姿態」**：
   - 物件只定義一次，放在圖自己的 `<defs>` 中，id 以圖號開頭（例如 `f4-booster`），並且朝向 +x 方向。
   - 每個姿態用 `<use href="#f4-booster" transform="translate(x y) rotate(θ)">` 擺放。
   - 殘影：除了目前的姿態以外，其餘姿態都用淡色 class 顯示。
   - 每個姿態旁標上編號，對應圖說或 stepper 的步驟。每張圖最多 6 個姿態。
   - 與 stepper 並用時，每一幀多顯示一個姿態。
4. **修改既有規則**：`pictorial.md` 原本寫「物件要自己畫，不用圖示」。這條改成：需要切開、分層或擺姿態的物件仍然自己畫；只需要辨識的物件可以用 R4 的 emoji。

### R4 Noto Emoji 子集

1. **檔案**：
   - `skills/explainer-figure/assets/emoji/noto.svg`：子集，開頭放授權聲明。
   - `skills/explainer-figure/assets/emoji/LICENSE`。
   - 版本鎖定在一個 Noto Emoji 的發行版，由 T1 決定。
2. **格式**：每個 emoji 是一行 `<symbol id="e-<name>" viewBox="…">`。emoji 內部的 id（例如漸層的 id）要加上 `e-<name>-` 前綴，避免同一頁的多個 emoji 互相衝突。
3. **新的 reference `references/emoji.md`**，內容包括：
   - 名稱表。
   - 使用時機：只用於辨識，不切開、不分層、不擺姿態。
   - 尺寸：放在 SVG 網格上，以及與文字並排時的尺寸。
   - 與自繪物件並用時的規則。
   - 同步指令：做法比照 `icons.md`。指令把頁面用到的 `<symbol>` 與授權聲明複製進模板的 emoji 區塊（新增 `<!-- emoji:start -->`／`<!-- emoji:end -->`），移除沒有用到的 symbol，並印出子集沒有的名稱。全部找到時不印出任何內容。
4. **圖型選擇表**：`explainer-figure/SKILL.md` § Choosing the figure type 加入一列「只需要辨識的物件」，指向 `references/emoji.md`。
5. **子集內容**：約 30 個物件，選法比照第 4 輪圖示：先統計範例與候選主題實際需要的物件。
6. **不在產頁時下載**：子集放進儲存庫，產頁時只複製用到的 symbol。

### R5 Codex 觸發測試

1. 使用者在 Codex 中手動執行 5 個一般圖表提示。提示內容依第 4 輪 T4 的 g1–g5 主題重寫，寫在實作計畫 T4 中。
2. 判讀方式：檢查 Codex 是否讀取 `explainer-figure/SKILL.md`，或在回應中依它的規則作圖。
3. 只要有 1 次觸發，就改寫 explainer-figure 的 description，或改用其他隱藏方式，然後重測。

## 2. 技術組成與指令

本儲存庫沒有建置系統或測試套件。下列指令都是驗證用。

```bash
# 既有：manifest、plugin、模板外部資源、兩種寬度截圖（見 CLAUDE.md〈驗證指令〉）
for f in .claude-plugin/*.json .codex-plugin/plugin.json .agents/plugins/marketplace.json; do python3 -m json.tool "$f" >/dev/null && echo "ok $f"; done
claude plugin validate .
wc -l skills/*/SKILL.md                       # 各約 130 行以內

# 既有：自檢指令（explainer-page/SKILL.md 第 6 步；explainer-figure/SKILL.md § Self-check 的對比檢查、圖示同步）
```

本輪新增的指令要在實作後寫進 skill，並實際執行一次：

- 壓線檢查（R2）：輸入頁面路徑，全部通過時不印出任何內容。
- emoji 同步（R4）：全部找到時不印出任何內容。

## 3. 會動到的檔案

| 檔案 | 需求 | 變更 |
|---|---|---|
| `skills/explainer-figure/SKILL.md` | R1、R2、R4 | 圖說明單加 Symbols 欄；圖型表加一列；Self-check 加壓線檢查指令 |
| `skills/explainer-figure/references/svg-recipes.md` | R1 | 符號標註的寫法（放在 § Colour meaning 附近） |
| `skills/explainer-figure/references/pictorial.md` | R3、R4 | 風格規範、5 種物件配方、P5、修改「不用圖示」規則 |
| `skills/explainer-figure/references/icons.md` | R4 | 交叉引用 `emoji.md`：器官等不在圖示子集中的物件，先查 emoji |
| `skills/explainer-figure/references/emoji.md`（新增） | R4 | 見 R4 第 3 點 |
| `skills/explainer-figure/scripts/check-overlap.js`（新增） | R2 | 見 R2 |
| `skills/explainer-figure/assets/emoji/`（新增） | R4 | `noto.svg`、`LICENSE` |
| `skills/explainer-page/assets/template.html` | R1、R3、R4 | `.sym`、風格 class、emoji 區塊標記 |
| `skills/explainer-page/references/writing-rules.md` | R1 | § Ground the symbols 加一行引用 |
| `.claude-plugin/*.json`、`.codex-plugin/plugin.json`、`.agents/plugins/marketplace.json` | — | 版本升為 0.5.0 |
| `CLAUDE.md`、`README.md`、`README.zh-TW.md` | — | 架構段落加入 `scripts/`、`assets/emoji/`、`emoji.md` |

`skills/explainer-page/SKILL.md` 已有 130 行，本輪不修改它。`skills/explainer-figure/SKILL.md` 目前 111 行，新增內容以約 19 行為上限，細節放進 references。

## 4. 寫作風格

- skill 的檔案用英文，句型比照現有 references：短句、一句一個動作、規則後面附上它要防止的失敗。
- 規格與計畫文件用繁體中文與台灣用語，並遵守 `writing-rules.md`。
- 新的配方附一段可以直接複製的 SVG 片段，格式比照 `pictorial.md` 的 P1。

## 5. 驗證策略

| # | 驗證項目 | 需求 | 判定方式 |
|---|---|---|---|
| V1 | EKF 頁 v2：以 R1 改版圖 3 與公式段落。原頁在 `~/Documents/explainers/extended-kalman-filter/`，新版另存一個檔案，只放在本機 | R1 | 與原版並排，由使用者判讀公式是否更容易對應到圖 |
| V2 | Starship 圖 4：以 P5 殘影重畫助推器返回 | R3 | 讀者看得出「翻轉」與「折返」；由使用者決定是否取代 `examples/` 中的圖 |
| V3 | 5 種物件（人、背包、俯視機器人、俯視車、火箭）各畫 3 次 | R3 | 同一物件的 3 次外形一致，沒有歪掉或破損 |
| V4 | 壓線檢查的準確度 | R2 | 依 R2 表中 6 個已記錄的缺陷，在現有頁面的副本中重新放入，再加 1 個人工的文字重疊案例，7 個都要抓到。在 7 個範例頁與 EKF 頁上，每一個回報都必須是真缺陷，或已由 `data-touch` 消除 |
| V5 | Noto Emoji 子集 | R4 | 授權允許內嵌與重新散布；在整頁截圖與「只看圖」截圖中都正常顯示（包括漸層）；放 5 個 emoji 的頁面仍 ≤ 150 KB；同步指令不印出任何內容 |
| V6 | Codex 觸發 | R5 | 5 個提示觸發 explainer-figure 0 次 |
| V7 | 新主題頁（使用者在任務開始前指定） | R1–R4 | 用到符號對照、自繪物件（含姿態或殘影）與 emoji；通過全部自檢，包括壓線檢查；由使用者判讀 |

**回歸檢查**：

- 模板的示範內容在 1280px 與 390px 兩種寬度都通過檢查。
- 壓線檢查在 7 個範例頁上的結果，與 V4 的判讀一致。
- 兩個 `SKILL.md` 都在約 130 行以內。

範例頁各自內嵌 CSS，修改模板不會影響它們，所以範例的重新截圖只在範例本身被修改時才需要。

### 待驗證的假設

沿用構想文件〈Key Assumptions to Validate〉的 6 項，並補充 2 項：

- [ ] SVG 文字中的組合字元（例如 x̂ 的 U+0302）在 Linux 的 Chrome 中能正確顯示。在 T5 截圖確認；顯示不正確時，改用 `<tspan>` 疊加符號。
- [ ] emoji 的漸層引用放在頁面共用的隱藏 `<svg>` 中時，在兩種截圖中都能顯示。在 T1 確認；不能顯示時，改為在每張圖內嵌 emoji，並在 id 加上圖號前綴。

## 6. 邊界

- **Always**
  - 維持單檔 HTML，不使用外部資源。
  - 頁面大小維持 ≤ ~150 KB。
  - 兩個 `SKILL.md` 各在約 130 行以內。
  - 四個 manifest 檔的版本號同步。
  - 新的指令寫進 skill 後實際執行一次。
  - 每個檢查點提供 `git add` 範圍與提交訊息，由使用者提交。
- **Ask first**
  - 新增第 3 節以外的 reference、腳本或資產。
  - 取代 `examples/` 中的頁面或圖。
  - 改變 L0–L2 的判準或篇幅預算。
  - 修改 `skills/explainer-page/SKILL.md`。
- **Never**
  - 產頁時從網路下載 emoji 或圖示。
  - 混用多套 emoji 庫，或在 emoji 之外再引入其他插圖庫。
  - 用手寫座標描繪有機形狀（胃、大陸輪廓）。
  - 把 EKF 頁這類以第三方材料或主題查證產出的頁面加入版本控制，除非使用者決定。
  - 代替使用者 commit。

## 7. 成功條件

- V1–V7 都完成，使用者判讀 V1、V2、V7 後認為比原版更好懂。
- 壓線檢查符合 V4：7 個重建缺陷全部抓到，範例頁上沒有未說明的回報。
- Codex 觸發 explainer-figure 0 次。
- Noto Emoji 子集附上 LICENSE 與授權聲明，同步指令與壓線檢查在 V7 頁面上都不印出任何內容。
- 兩個 `SKILL.md` 各在約 130 行以內，`claude plugin validate .` 通過，四個 manifest 檔都是 0.5.0。

## 8. 不做的事（及理由）

沿用構想文件〈Not Doing (and Why)〉：

- 放寬 150 KB 上限。
- 規格表與 L3。
- explainer-cite。
- 公式與圖的滑鼠連動。
- 多種插圖風格。
- 用手寫座標描繪有機形狀。
- C 類計算圖。

另外，本輪也不做：

- **壓線檢查涵蓋語意錯誤與間距**：無法用幾何判斷，仍靠截圖判讀。
- **修改 `skills/explainer-page/SKILL.md`**：它已有 130 行，本輪的需求都能放在 explainer-figure 與 references 中。

## 9. 待決問題

- 驗收用的新主題（使用者在 T12 開始前指定）。
- 版本號：預設在收尾時升為 0.5.0。
- `.sym` 與風格 class 的正式名稱：實作時確定。
- Noto Emoji 要鎖定哪一個發行版、收哪些物件：T1 決定。
