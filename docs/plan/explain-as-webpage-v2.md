# explain-as-webpage 第二輪：英文支援、頁面樹延伸、autoresearch 範例

## Problem Statement

我們如何讓 `explain-as-webpage` 在使用者持續追問、知識逐步累積時，仍然維持「每頁 15 分鐘讀完」，同時支援英文產出，並以一個公開儲存庫示範 L0／L1／L2 與多頁延伸的實際樣貌？

## Recommended Direction

**延伸既有頁面採「判準分流」**：新疑問若是短答且屬於既有疑問，就補進原頁的 `<details>`；若是新疑問，就開子頁；若會改變主結論，就修訂主頁。子頁與主頁放在同一目錄，命名為 `<主頁slug>--<子頁slug>.html`。頁面樹固定兩層（主頁＋子頁），每頁側欄放同一份靜態頁面清單，子頁的麵包屑連回主頁。`<details>` 內容計入篇幅預算，超出預算就改開子頁。這對應使用者在 starlab_swarm 中「ANALYSIS 報告 → 三篇 PRIMER」的實際追問經驗，也對應 `swarm_experiment` 頁面之後「逐檔、逐函式」的追問情境，後者另訂「程式導讀」頁型。

**英文支援只需小幅補規則**：`SKILL.md` 原本就在確認步驟詢問頁面語言，模板預設 `lang="en"`。缺的是 `writing-rules.md` 中的英文寫作規則與固定章節標題的中英對照。README 改為英文為主，另附 `README.zh-TW.md`，兩份都引用 Karpathy 的貼文（https://x.com/karpathy/status/2105819303471976479），說明本 skill 對應貼文中「ASD-STE100 寫作 → 圖 → HTML 網頁」三層，並刻意不做貼文最看好的影片。

**範例**：`examples/autoresearch/` 放一個英文主頁（目的、三個檔案、使用方式；L0 結構、L1 固定時間預算的取捨、L2 實驗迴圈），以及 `train.py`、`prepare.py` 兩個程式導讀子頁。主頁先產出，子頁再以「追問」走延伸流程加入，藉此實際驗證延伸機制。

## Key Assumptions to Validate

- [ ] 代理修改既有 HTML 時不會弄壞手寫 SVG 與連結 —— 範例分兩步產出，延伸後再截圖檢查
- [ ] 判準分流能守住主頁篇幅 —— 延伸前後計算主頁字數，確認在預算內
- [ ] 同一套規則產出的英文頁面一樣好讀 —— 由使用者判讀範例
- [ ] 各頁側欄清單保持同步 —— 自我檢查新增比對指令
- [ ] 沒有本機實測數據也能寫出可信的範例 —— 數字只取自上游 README、`program.md` 範例輸出與程式常數，並標明來源

## MVP Scope

- 包含：`references/extending-pages.md`（新增）、`SKILL.md` 小幅修改（維持約 130 行內）、`writing-rules.md`（英文規則、程式導讀頁型）、`template.html`（側欄頁面樹、麵包屑連結）、英文 `README.md` 與 `README.zh-TW.md`、`examples/autoresearch/` 三頁、manifest 版本號遞增
- 不包含：見下方

## Not Doing (and Why)

- 跨主題索引或知識庫 —— 維持第一輪決定，頁面樹只限單一主題
- 三層以上頁面樹、自動同步腳本 —— 增加複雜度，違反「不附產生器腳本」
- plugin 改名 —— 等遠端儲存庫改名時一起處理
- 影片、GitHub Pages、範例的中文版 —— 不在本輪範圍
- 延伸既有的 starlab_swarm 頁面 —— 本輪只用 autoresearch 驗證，之後可再試用

## Open Questions

- 延伸後的英文範例是否讀得懂（由實作檢查點回答）
