# 擴充視覺表現形式（visual forms）

## Problem Statement

我們如何讓代理在說明頁中使用方框箭頭以外的視覺形式（歸納卡、具象插圖、統一的圖示與概念配色），讓頁面更容易讀，同時維持單檔離線、不違反授權，也不讓既有的機制圖與 L0–L2 能力退化？

起因：目前頁面的圖只有不同顏色的矩形、圓形、箭頭組成的流程圖與簡易數值圖。使用者收集的例子分成四類：

| 類型 | 例子 | 圖負責的工作 |
|---|---|---|
| A. 引用既有圖片 | ASU 體液分布圖、ESA 音震艙照片、NotebookLM 介面截圖 | 讓讀者看到真實物件或介面長什麼樣、該點哪裡 |
| B. 具象隱喻插圖 | 避難包分層、Unity GameObject 罐子 | 把抽象關係對應到一個具體物件 |
| C. 以假設範例算出的圖 | Welch Labs 雜訊→影像 | 用實際運算結果呈現概念，不用方框代替 |
| D. 簡報式歸納卡 | Agent harness 六個面向、多代理系統總覽 | 用一張圖收斂前幾段文字：標題、卡片網格、圖例 |

## Recommended Direction

把現有的 explain-as-webpage 拆成三個 skill，以「誰決定畫什麼」與「誰決定怎麼畫」為分界：

- **explain-as-webpage（編排者）**：材料、學習摘要、核心問題、層級、確認、頁面骨架與寫作規則、整頁自檢與回報。在學習摘要中為每張圖寫一份「圖說明單」：要回答哪個核心問題、圖型（機制圖／具象插圖／歸納卡／數值圖）、內容事實與來源單位、概念色與圖示對照、靜態／滑桿／stepper。
- **draw-figure（繪圖，MVP 新建）**：接收圖說明單，產出 SVG 或 HTML 片段，並執行單圖截圖自檢。`svg-recipes.md` 從編排者移到這裡；新增具象配方、歸納卡規則與圖示子集。
- **cite-figure（引用圖片，第二階段）**：開放授權圖庫查詢、headless Chrome 截圖、PIL 裁切壓縮、寫入 `<slug>.assets/`、產生含作者與授權的圖說；受版權保護的圖在確認步驟逐張列出。

編排者用相對路徑 `../draw-figure/SKILL.md` 指向繪圖 skill，不依賴平台的自動觸發，Claude Code 與 Codex 都能讀取。層級 L0–L2 的判準不變：圖型和層級是兩個互相獨立的面向。

MVP 只做 B 類具象插圖、D 類歸納卡與圖示，不涉及點陣圖，所以單檔與 150 KB 上限暫時不變。

拆分時要處理三個耦合：

1. **顏色衝突**：`svg-recipes.md` 已經固定紅色代表問題、綠色代表修正、藍色代表中性機制。如果「概念 A」被指定為紅色，讀者會誤以為 A 是問題。解法是把語意色和概念色分開：紅、綠、黃、藍、灰保留為語意色；概念色另外取最多 5 個不重疊的色相，與 SKILL.md「關鍵概念最多 5 個」一一對應。
2. **CSS 歸屬**：「什麼時候用卡片」屬於寫作判斷，放在編排者的 `writing-rules.md`；「卡片怎麼排、密度上限多少」放在 draw-figure。CSS 只能有一份，否則兩邊會逐漸不一致；以 `template.html` 的 `:root` 變數為唯一來源，draw-figure 只引用 class 名稱。
3. **讀圖四問被拆開**：「軸名、單位、圖例放在圖內」改由 draw-figure 負責，「怎麼讀、從哪來」仍由編排者在圖說與來源行中處理。兩邊互相引用，不各寫一套。

使用者已確認（2026-10-04）：

- 授權：以開放授權為主，受版權保護的圖逐張確認。
- 點陣圖：允許放在頁面旁的 `<slug>.assets/` 資料夾（第二階段）。
- 截圖：headless Chrome 只截公開網頁，需要登入的頁面由使用者自己截圖提供。
- MVP：歸納卡、具象插圖與圖示。
- 架構：方案丙（三分），理由是分工明確，並避免 `SKILL.md` 超出行數上限。
- 成功條件：重做既有範例並排比較，加上以新主題產出一頁。
- 外部資源篩選（來自一篇整理 40 個 vibe coding 設計資源的貼文）：只保留 component.gallery 作為歸納卡的參考；視覺風格維持 Sphinx／Read the Docs，不參考華麗風格的網站集錦；CSS 以 `template.html` 為唯一來源。

## Key Assumptions to Validate

- [x] 兩個平台都會依編排者的指示載入 draw-figure —— 在 Claude Code 與 Codex 各產出一頁，檢查是否讀取了 draw-figure 的規則。**結果（T13、T13d）：** 兩次 Codex 實測都讀了 `explainer-figure/SKILL.md`；使用者在另一個 Claude Code session 重跑時，讀了 `cards.md`、`pictorial.md`、`icons.md`
- [x] draw-figure 的 description 不會搶走一般繪圖需求（本機另有 dataviz、artifact-diagramming）—— 用 5 個一般圖表的提示詞測試觸發。**結果（T4）：** Claude Code 中 5 個圖表提示觸發 explainer-figure 0 次（dataviz 3 次、無 2 次），2 個說明頁提示都觸發編排者。Codex 的 `$` 自動補全清單會列出 explainer-figure（T16），是否會被自動觸發未測
- [x] 拆分後每頁的 token 成本沒有明顯增加 —— 拆分前後各執行一次 `claude plugin details` 比較。**結果（T3）：** 實際 always-on 仍約 400 tok（explainer-figure 不載入）；產一頁時讀取的 `SKILL.md` 與繪圖規則從 30,087 B 增為 34,082 B（約 +1k tok、+13%），增加的部分是新功能（圖說明單與圖型表），不是拆分本身
- [x] 歸納卡取代文字後，頁面變短、沒有變長 —— 重做的範例比較字數與閱讀時間。**結果（T10、T11）：** Starship 以卡片取代 9 列試飛表，散文 −5%；LLM Wiki 散文 +10%，來自使用者要求新增的適用情境卡片與引導段落，不是卡片取代文字造成
- [x] 概念色與語意色並用時，讀者不會混淆 —— 重做範例的截圖由使用者判讀。**結果（檢查點 B、C）：** 使用者判讀色票容易分辨；三個主題的新版「效果很不錯」
- [x] 60–100 個圖示足以涵蓋需求 —— 統計 4 個範例加上新主題實際需要的圖示，缺少超過 2 成就改為從 npm 下載並鎖定版本。**結果（T1、T12）：** 子集 106 個；T10–T12 三頁共用到 19 個不同的圖示，缺少 0%
- [x] 代理能穩定畫出具象外形 —— 試畫背包、人體剪影；變形就限縮為「圖示組合＋簡單幾何容器」。**結果（T2）：** 背包、人體剪影、罐子都沒有變形，不需要限縮；問題只在標籤與線條的版面衝突，靠截圖修正。人體剪影接近人台模型
- [x] Lucide／Tabler 的授權允許內嵌與重新散布 —— 查閱儲存庫中的 LICENSE 原文。**結果（T1）：** 兩套都允許。Lucide 為 ISC，衍生自 Feather 的圖示另受 MIT 約束；頁面用到圖示時附授權註解

## MVP Scope

**做：**

- 新建 `skills/draw-figure/`：
  - `SKILL.md`：圖型選擇判準、圖說明單格式、單圖自檢。
  - `references/svg-recipes.md`：自編排者搬入。
  - `references/pictorial.md`：分層容器、剪影加引線標註、物件內部組成。
  - `references/cards.md`：卡片網格與密度上限（每頁最多 2 張、每張最多 6 格、內文至少 13px、窄版單欄）。撰寫時參考 [component.gallery](https://component.gallery) 中 Card、Badge、Alert、Accordion、Tooltip 在各設計系統的做法。
  - 單圖自檢加入色彩對比檢查：文字與背景的對比至少 WCAG 4.5:1，涵蓋新增的概念色。
  - `references/icons.md` 與 `assets/icons/`：單一圖示庫子集與 LICENSE。
- 編排者：`writing-rules.md` 加入卡片觸發條件（4 個以上平行項目且欄位相同時，用卡片取代文字）與概念色規則；學習摘要加入圖說明單；更新 `SKILL.md`、`page-types.md`、`writing-rules.md`、`template.html` 中 8 處對 `svg-recipes.md` 的引用。
- `template.html`：`.cards`、`.chip`、圖示 `<symbol>` 區塊的樣式。
- 驗收：
  - 重做 1–2 個既有範例（例如 starship-reusability、llm-wiki），與舊版並排比較，由使用者判定是否更好讀。
  - 以一個適合具象插圖的新主題產出 1 頁。
  - 其餘範例重新截圖，確認沒有退化。
  - 兩個 `SKILL.md` 各自維持約 130 行以內。
  - `CLAUDE.md` 的驗證指令全部通過。

**不做：** cite-figure、`<slug>.assets/`、在頁面內即時產生計算圖（第二階段以後）。

## Not Doing (and Why)

- **MVP 不做 A 類引用圖片** —— 涉及授權、二進位檔與資料夾規則，等繪圖分工穩定後再做。
- **canvas 即時計算圖（C 類）** —— 每張圖都要寫程式，成本高，排在 A 類之後。
- **混用多套圖示庫** —— 線條粗細與視覺重量不一致；只選一套。
- **使用 BioRender 素材** —— 屬於專有授權，只學構圖方式。
- **AI 生圖** —— 兩個平台不一定都能用，細節可能是捏造的，授權也不明。
- **高密度資訊圖表（如多代理系統總覽那張）** —— 內文字級約 6–7px，在 390px 窄版檢查中讀不清楚，違背易讀的目標。
- **產出時從網路下載圖示** —— 需要網路，版本也會漂移；改為把子集放進儲存庫。
- **更動 L0–L2 判準** —— 圖型是獨立的面向，不和層級綁在一起。
- **Kitbitz 插圖庫**（CC0 手繪向量插圖）—— 畫風不符合使用者喜好。
- **uiverse.io、3dicons.co** —— 與說明頁的風格不搭；3dicons 是點陣 3D 圖，也與扁平樣式不一致。
- **參考華麗風格的網站集錦**（styles.refero.design、minimal.gallery、godly.website、awwwards.com、land-book.com、hoverstat.es、kage.design）—— 過度華麗，頁面維持 Sphinx 風格。
- **React／Tailwind 元件庫**（shadcn/ui、Aceternity、Magic UI、21st.dev 等）—— 需要建置流程，與單檔模板衝突。
- **採用 DESIGN.md 格式**（Google Labs 的設計規則檔格式，Apache-2.0，alpha）—— 數值已在 `template.html` 的 `:root`，用途已在 `svg-recipes.md` § Colour meaning；匯出與換風格用不到；多一處要同步。唯一的缺口「色彩對比檢查」改在 draw-figure 的單圖自檢中直接實作。

## Open Questions

- 選 Lucide（約 1.6k 個，ISC）還是 Tabler（約 5k 個，MIT）？建議先統計需要哪些圖示，再看哪一套涵蓋較完整。
  - **已決定（2026-10-06）**：Lucide。兩套對 101 個圖示概念各缺 3 個；Lucide 單一圖示較小。子集 106 個，見 `docs/plan/04-visual-forms-plan.md` T1、T7。
- skill 名稱：`draw-figure` 太泛用，容易和 dataviz 等 skill 競爭觸發。是否改名，例如 `explainer-figure`、`explainer-cite`？
  - **已決定（2026-10-06）**：繪圖 skill 叫 `explainer-figure`；第二階段的引用 skill 對應命名為 `explainer-cite`。
- draw-figure 是否開放使用者單獨呼叫（例如畫 README 封面）？這會決定它的 description 寫法，以及單獨使用時如何取得 `template.html` 的樣式。
  - **已決定（2026-10-06）**：只由編排者以相對路徑讀取；frontmatter 設 `disable-model-invocation: true`、`user-invocable: false`。T4 確認 Claude Code 不會自動觸發；Codex 的 skill 清單未測。
- （第二階段）頁面樹的 `<slug>.assets/` 要每頁一個資料夾，還是整個主題共用一個？
  - **已移交（2026-10-07）**：排入第 6 輪候選，見 `docs/plan/05-symbols-pictorial-idea.md`〈後續輪次〉。已決定只有引用點陣圖的頁面才允許 assets 資料夾；每頁或共用仍待決。
- 版本號是否升為 0.4.0？
  - **已決定（2026-10-07）**：升為 0.4.0，四個 manifest 檔同步（T14）。
- （未來）L3 層級：以 [anime.js](https://animejs.com)（MIT，v4 完整版約 24.5 KB，有 UMD 單檔版本，可內嵌）實作 SVG 描線、形狀變形、沿路徑移動。L0–L2 是依核心問題的類型定義的，L3 也要先定義它回答哪一類問題（例如連續變形、沿路徑的運動、兩狀態間的漸變），anime.js 只是實作手段；並要決定頁面大小上限如何容納這 24.5 KB。
  - **已移交（2026-10-07）**：排入第 7 輪候選，見 `docs/plan/05-symbols-pictorial-idea.md`〈後續輪次〉。使用者決定直接使用 anime.js；範例頁最大 53 KB，加上 24.5 KB 仍在上限內。
