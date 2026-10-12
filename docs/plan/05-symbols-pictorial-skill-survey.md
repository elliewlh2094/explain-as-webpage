# 熱門解釋圖 skill 的設計調查

本文件記錄第 5 輪檢查點 0 期間的一次調查：網路上熱門、以文字敘述產出解釋性圖像的 agent skill 如何設計，哪些做法可以吸收進 explainer-figure。調查日期是 2026-10-12。

## 起因

T4 的 Codex 測試中，g3（Web app 架構圖）由 Codex 內建的 `imagegen` 產生點陣圖，畫面中的每個元件都是可辨識的物件。使用者觀察到：指定本專案的 skill 後，代理就不再畫出這類具象圖。對照結果見 `docs/plan/05-symbols-pictorial-plan.md`〈結果〉T4。

以第一性原理分析後，根本原因是：skill 把「畫成物件的樣子」當成一種**圖型**（具象插圖），只用在「部件在物件中的位置」這類問題；其他圖型的節點一律是方框，物件外觀只剩 24×24 的圖示一個管道，而 `icons.md` 又禁止手繪圖示。使用者保留「把外觀判斷移到節點層級」的方向，並要求先調查外部 skill 的設計。

## 調查方法

- 以網路搜尋找出 Claude Code、Codex 等平台上產出圖表或解釋圖的 skill，再以 GitHub API 取得星數與檔案清單。
- 下載各 skill 的 `SKILL.md` 與主要 references，閱讀全文。
- 只分析設計原則與機制，不複製內容。

## 調查對象

| Skill | 星數 | 產出 | 關聯 |
|---|---|---|---|
| [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | 52k | 單檔 HTML＋SVG，44 種圖型 | 高 |
| [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills)（baoyu-diagram、baoyu-infographic） | 26.6k | 深色主題 SVG；資訊圖以點陣圖生成 | 低 |
| [nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer) | 10.4k | 單檔 HTML，手寫 SVG 圖 | 高，定位最接近本專案 |
| [MengTo/Skills](https://github.com/MengTo/skills)（14 種 `illustration-*` 風格） | 6.7k | 手寫 SVG 插圖 | 高，`illustration-flat-with-black` 與「粗外框＋平塗色」同類 |
| [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy) | 5.2k | 等角投影的實體機械 SVG | 高，把概念畫成實體物件 |
| [coleam00/excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill) | 5k | Excalidraw JSON | 中，設計理念 |
| [konraddzbik/architecture-diagram-skill](https://github.com/konraddzbik/architecture-diagram-skill) | 116 | 可點選的動畫架構圖 | 低 |
| [ericblue/visual-explainer-skill](https://github.com/ericblue/visual-explainer-skill) | 54 | 點陣圖生成 | 不適用 |

星數取自 2026-10-12。搜尋時參考的目錄網站：[Top Agent Skills](https://top-agent-skills.com/guides/best-skills-for-diagrams)、[claudeskills.info](https://claudeskills.info/skills/category/diagrams/)。

## 發現 1：外觀是獨立於圖型的維度

4 個 skill 在節點層級決定外觀，或直接以物件作為解釋：

- **excalidraw**：核心原則是「The shape should BE the meaning」。「Isomorphism Test」要求拿掉所有文字後，結構仍能傳達概念；「Icons decorating text」列為反例；預設不加容器，放在容器內的文字少於 30%。
- **visual-explainer**：架構圖的節點規則寫「Shape says what a thing is」，例如資料庫畫成圓柱、佇列畫成有 3 條分隔線的方框；另有「Draw the mechanism, not the name」。
- **anatomy**：「The object is the explanation」，概念要對應到一台可辨識的機械，例如快取鍵對應到彈子鎖。
- **diagram-design**：ADR 0002 把「行為」設為獨立於圖型的維度，每個行為模式套用最接近的既有圖型，不新增圖型，以免圖型清單膨脹。

**對本專案的意義：** 這些做法支持使用者保留的方向。外觀依節點代表的東西決定，與圖型無關。excalidraw 的 Isomorphism Test 可以直接作為判準，不需要列出元件清單。

## 發現 2：物件的幾何由程式產生

3 個具象品質最高的 skill，都不讓代理手寫物件座標：

| Skill | 做法 |
|---|---|
| MengTo | `scripts/parts.mjs`（269 行）提供 `tube`、`kneeTube`、`sleeve`、`hand`、`head`、`envelope` 等函式；代理寫產生器腳本，由腳本輸出 SVG；另有零件總覽圖（contact sheet）指令 |
| anatomy | 函式庫提供 `extrude`、`cylinder`、`lathe`、`tube`，自動處理明暗與繪製順序；稽核腳本檢查零件間距與交疊 |
| diagram-design | 爆炸等角圖規定「Project every point with one function and never place a coordinate by hand」，範例由建置腳本產生 |

**對本專案的意義：** `pictorial.md` 的對應規則是「Do not trace a detailed outline by hand」。面對手寫座標會跑掉的問題，本專案以降低細節因應，這些 skill 則把幾何交給函式。第 5 輪 T2 遇到的問題都是幾何計算問題：

- 軀幹與腿之間出現圓弧缺口。
- `scale()` 讓外框變細。
- P5 的姿態座標必須從軌跡算出。

產生器只在產頁時執行，輸出的 SVG 片段內嵌在頁面中，頁面仍是單一檔案。本專案已經以 Python 同步圖示，也以 JavaScript 做壓線檢查，加入產生器腳本有前例。

## 發現 3：自檢包含意圖檢查

本專案的自檢（截圖、WCAG 對比、壓線檢查）只找缺陷。這些 skill 另外檢查圖是否達到設計目的：

- **excalidraw**：渲染後先比對原本的設計：結構是否對應概念、視線是否依設計的順序移動；之後才找缺陷。不要只檢查一輪就停，通常需要 2–4 輪。
- **MengTo**：新圖與範例並排，問「same hand, same set?」；放大 4–8 倍檢查交接處；依 5 項標準各給 0–2 分；兩位評審評分時取較低者。
- **anatomy**：問「is it instantly a real object?」，並放大 4 倍檢查。

**對本專案的意義：** 圖說明單已有 Message 欄，可以作為意圖檢查的依據。成本最低的做法是在 Self-check 加入：

1. 遮住文字的截圖：結構仍能表達 Message 中的關係（Isomorphism Test）。
2. 與範例並排比較風格。
3. 放大檢查物件的交接處。

## 本專案已有的做法

下列做法這些 skill 也有，本專案已經具備，不重複加入：

- 每張圖只陳述一個主張，由圖說寫出。
- 網格座標。
- stepper 最多 8 步；diagram-design 的動畫上限也是 8 步。
- 以腳本檢查幾何。diagram-design ADR 0005：「A rule that only lives in prose ships broken examples」，與 R2 壓線檢查的理由一致。
- 語意色。
- 以約 80% 的 ASD-STE100 作為寫作規範；visual-explainer 採用同一規範。

## 不吸收的做法

- **點陣圖生成**（baoyu-infographic、ericblue、imagegen）：Claude Code 沒有圖片生成工具，兩個平台共用同一份 `SKILL.md`；點陣圖的文字無法編輯，也無法做 stepper、深色模式與壓線檢查；單張約 1.1–1.2 MB，超過 150 KB。
- **anatomy 的完整零件庫、WebGL 與 3D**：一張圖 30–90 分鐘、40–80 個零件，與「選最便宜的呈現層級」衝突。
- **diagram-design 的 44 種圖型**：與「依問題選圖型」的做法方向不同。
- **編輯性原則**：重點色最多 2 個、節點最多 9 個（diagram-design）；每個數字都要有圖、尺寸線、small multiples（visual-explainer）。這些與本輪的根本問題無關，留待之後評估。
- **上一輪撤回的 3 項規則**：元件物件清單、連線使用目標元件的顏色、雙向平行箭頭。這些是針對 g3 外觀的個別規則，不處理根本原因。

## 併入第 5 輪的方案

使用者 2026-10-12 同意吸收 3 項發現，並要求連同保留的方向一起評估如何併入現有計畫。下列是提給使用者的方案；使用者的決定與調整見本節最後的〈使用者的決定〉，正式內容以規格 `docs/plan/05-symbols-pictorial-spec.md` 與實作計畫 `docs/plan/05-symbols-pictorial-plan.md` 為準。

### 需求的對應

| 來源 | 需求 | 內容 |
|---|---|---|
| 保留的方向＋發現 1 | 新增 R6 節點外觀 | 所有圖型中，代表具體、外形熟悉的東西的節點畫成那個東西；抽象概念維持方框；形狀不提供額外資訊時（例如所有節點同類）也維持方框。改寫 `SKILL.md` 圖型表後的段落、`pictorial.md` 開頭、`icons.md` 第 55 行的禁令範圍、`svg-recipes.md` Recipe 3 的範例 |
| 發現 2 | 修改 R3 | 物件由 `scripts/parts.py` 產生，取代「可複製的配方片段」。函式接受尺寸參數，直接輸出該尺寸的幾何，不使用 `scale()`；P5 的姿態由函式依軌跡計算位置與角度 |
| 發現 3 | 新增 R7 意圖檢查 | Self-check 加入遮住文字的截圖、與零件總覽圖並排、放大截圖 3 項，各附可執行的指令 |

### 任務與階段

既有任務編號不變，新任務從 T14 起編。

- **第 0 階段**：新增 T14 具象基準測試（使用者在 Codex 手動執行）。
  - (a) 不用本專案的 skill，以 SVG 畫 g3 的主題。
  - (b) 經 explainer-page 產出同一主題。
  - 記錄每張圖中有幾個節點畫成物件。必須在修改規則前執行，結果才能作為基準。
- **第 1 階段**：只保留 T5（符號規則）。T6（EKF 頁）需要以函式庫畫機器人，移到第 3 階段。
- **第 2 階段（繪圖基礎）**：
  - T7 壓線檢查（不變）。
  - T8 改為「風格規範與零件函式庫（含 P5 的姿態計算）」。
  - 新增 T15 節點外觀原則（R6）。
  - 新增 T16 意圖檢查（R7）。
  - 檢查點 B 改為：使用者判讀零件總覽圖，以及依 R6 重畫的 Recipe 3 範例。
- **第 3 階段（驗證案例）**：T6 EKF 頁、T11 Starship 圖 4、T14 (b) 重測。
- **第 4 階段**：T12 新主題頁、T13 收尾。

### 驗證的變更

- **V3 改寫**：零件總覽圖中每個函式的輸出外形正確，T2 的兩個問題（圓弧缺口、外框變細）不再出現；同一參數重跑輸出相同。
- **新增 V8**：T14 (b) 重測時，具體元件畫成物件，抽象元件維持方框，通過全部自檢；範例頁中以抽象概念為主的機制圖不受影響。
- **新增 V9**：R7 的 3 項指令實際執行一次，並在 V7 頁面上使用。

### 預算與風險

- `explainer-figure/SKILL.md` 目前 111 行。原計畫新增約 19 行，加上 R6 的段落改寫（淨增約 2 行）、函式庫指令約 3 行、R7 約 3 行，預計 130 行左右，沒有餘裕。超過時，把 R7 的指令細節移到 references。
- 函式庫是新的維護成本：每個函式都要在零件總覽圖中檢查。
- 代理多一個步驟：先執行函式產生物件，再把片段放進 SVG。

### 待使用者決定

1. **函式庫的語言**：建議 Python 3 標準函式庫。理由：圖示同步指令已要求 Python 3；`check-overlap.js` 在 Chrome 中執行，不需要 Node；改用 Node 會新增一項依賴。
2. **函式庫內建的組合物件**：建議只做有使用者、也有失敗記錄的 3 種：人（T2 的缺口問題）、火箭與助推器（T11）、俯視機器人（T6）。背包與車改由基本形函式組合，作為 `pictorial.md` 的示範，不另寫函式。其他物件依 R6 由基本形組合，不列清單。
3. **階段重排**：是否同意把 T6 移到第 3 階段，並新增 T14–T16。

### 使用者的決定（2026-10-12）

1. 函式庫使用 Python 3。
2. 組合物件改為人體、機器人（不限定俯視）、無人機。不做火箭：T11 的 Starship 要依代理能取得的資料畫出實際外形，而不是套用預設的火箭外形。這一點寫成規格 R6 第 4 點「外形依據」，適用於所有特定實物。
3. 同意階段與任務重排。規劃時另從 T14 拆出 T17（節點外觀重測），讓第 0 階段的基準與第 3 階段的重測分開記錄。
