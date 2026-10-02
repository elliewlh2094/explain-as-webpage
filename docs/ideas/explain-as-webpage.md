# explain-as-webpage

## Problem Statement

我們如何讓 AI 代理以使用者自己專案中的真實數據與程式碼為例，把一項陌生技術的因果關係畫出來並寫清楚，產出單一、輕量、可回頭重讀的網頁，並且依主題性質選擇最便宜但足夠的呈現方式？

## Recommended Direction

做成單一 skill：`SKILL.md` 規定流程（收集背景 → 學習摘要 → 選層級 → 一次性確認 → 產出 → 自我檢查 → 回報），細節放在 `references/`，外觀由 `assets/template.html` 提供。Claude Code 與 Codex 共用同一份 `SKILL.md`，只各自附 plugin manifest。

使用者既有的痛點是「篇幅太長、文字太密、缺少因果主線、圖與論述脫節」，而不是單純缺少圖片（`LANDMARK_PRIMER_2_GEOMETRIC_VERIFICATION.md` 已附 matplotlib 圖仍然難懂）。因此設計重點放在寫作結構：疑問驅動的章節、因果鏈圖、用專案真實數據做反事實對照、圖文緊鄰並互相引用。

呈現分為三級：L0 文字＋靜態 SVG、L1 加簡單互動、L2 瀏覽器內逐步動畫。預設採用最低足夠的層級，產出前與使用者確認。

## Key Assumptions to Validate

- [ ] 「疑問清單＋因果鏈＋反事實對照」能讓使用者看懂 RANSAC 與 RTF —— 以 skill 實際產出兩頁，由使用者判讀
- [ ] 代理手寫的 inline SVG 不會錯位 —— 規定固定網格並以 headless Chrome 截圖自檢
- [ ] 同一份 `SKILL.md` 在 Codex 上可正常觸發 —— 以本地 marketplace 實際安裝測試

## MVP Scope

- 包含：`SKILL.md`、兩份 references、一份 HTML 模板、兩個平台的 plugin manifest、README
- 不包含：影片、外部 CDN、Sphinx 建置、索引頁或知識庫、產生器腳本

## Not Doing (and Why)

- 真正的影片（manim／ffmpeg／TTS）—— 工具鏈與推論成本高，逐步動畫已能涵蓋「過程」類疑問
- 外部 CDN（MathJax、D3、Mermaid）—— 破壞離線與單檔原則
- 跨主題索引或知識庫 —— 增加管理負擔
- 拆成多個 skill —— 需要跨 skill 串接，Codex 路由不一定可靠
- 兩份平台專屬的 skill 內容 —— 兩個平台使用相同的 frontmatter 格式

## Open Questions

- 試用頁面完成後，使用者是否真的看得懂（由檢查點 B 回答）
