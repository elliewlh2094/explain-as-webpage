# 實作計畫：explain-as-webpage 第二輪

> 第一輪（建立 skill、三頁試用、打包）已完成，內容見 git 歷史（commit `34156de`、`2ec4278`）與 `docs/ideas/explain-as-webpage.md`。本輪構想見 `docs/ideas/explain-as-webpage-v2.md`。

## Overview

本輪處理四件事：
1. 讓 skill 明確支援英文產出；README 改為英文為主，另附繁體中文版。
2. 在 README 引用 Karpathy 的貼文，說明本 skill 的靈感來源。
3. 新增「延伸既有頁面」流程：依判準把使用者的追問分流到原頁的 `<details>`、子頁或修訂主頁，並以兩層頁面樹守住每頁的篇幅。
4. 以 karpathy/autoresearch 產出英文範例：一個展示 L0／L1／L2 的主頁，以及兩個程式導讀子頁。

## Architecture Decisions

| 項目 | 決策 | 理由 |
|---|---|---|
| 延伸落點 | 短答且屬於既有疑問 → 原頁 `<details>`；新疑問 → 子頁；會改變主結論 → 修訂主頁 | 小問題不必開新頁；新疑問不會讓主頁變長 |
| 篇幅 | `<details>` 計入該頁篇幅預算；補充後會超出預算就改開子頁 | 防止主頁越補越長 |
| 頁面樹 | 固定兩層（主頁＋子頁）；子頁與主頁放在同一目錄，命名為 `<主頁slug>--<子頁slug>.html` | 既有頁面不必搬移；相對連結在 `file://` 下可用 |
| 導覽 | 每頁側欄都有同一份靜態頁面清單；子頁的麵包屑連回主頁 | `file://` 下無法用 JS 讀取其他檔案；同一主題的頁數少 |
| 細節位置 | 延伸規則放在新增的 `references/extending-pages.md`；`SKILL.md` 只加入口與判準摘要，維持約 130 行內 | 遵守 CLAUDE.md 的精簡原則 |
| 程式導讀頁型 | 加在 `writing-rules.md`：標題仍是疑問句；圖 1 為檔案內主要函式的呼叫流程；附函式職責表與「設計決策 → 防止的風險」 | 對應 swarm_experiment 的逐檔追問情境 |
| 英文支援 | `writing-rules.md` 補英文寫作規則與固定章節標題的中英對照；`SKILL.md` 第 4 步的語言規則寫得更明確 | 現有流程已會詢問語言，只缺規則 |
| README | `README.md` 改為英文，新增 `README.zh-TW.md`，兩份頂端互相連結 | 使用者選擇英文為主 |
| plugin 名稱 | 維持 `sphinx-style-notes-maker`；三份 manifest 的版本號同步升為 `0.2.0` | 等遠端儲存庫改名時再一起改 |
| 範例位置 | `examples/autoresearch/`，共三個 HTML 檔，英文 | 範例屬於本儲存庫；英文同時驗證第 1 點 |
| 範例的數字來源 | 只取自上游 `README.md`、`program.md` 的範例輸出與程式常數，並標明「上游範例，非本機實測」 | 本機沒有 autoresearch 的實測紀錄 |

## Task List

> 本儲存庫沒有建置或測試系統，以下驗證都是可實際執行的指令或人工檢查。依照使用者的規則，不自行 commit；在檢查點提供 `git add` 範圍與提交訊息建議。

### 第 1 階段：skill 規則

**T1（S）模板：側欄頁面樹與麵包屑連結**
- 說明：在 `template.html` 的側欄加入可選的頁面清單區塊（`.pages`，標示目前頁），麵包屑可放主頁連結；附註解說明「單頁時刪除此區塊」。
- 驗收：
  - [ ] 單頁使用時刪掉區塊後版面不受影響
  - [ ] 窄螢幕的頂部選單也能看到頁面清單
  - [ ] 沒有外部資源
- 驗證：`grep` 外部資源指令無輸出；1280px 與 390px 兩種寬度截圖並實際檢視
- 相依：無
- 檔案：`skills/explain-as-webpage/assets/template.html`

**T2（M）延伸流程：`extending-pages.md` 與 `SKILL.md`**
- 說明：新增 `references/extending-pages.md`，內容包含：如何找到既有頁面、分流判準、子頁命名、側欄清單同步、延伸時的確認內容、篇幅檢查。`SKILL.md` 加入「新頁或延伸」的入口、第 4 步確認落點、第 6 步的同步檢查指令；description 加入追問類的觸發詞。
- 驗收：
  - [ ] `SKILL.md` ≤ 約 130 行，frontmatter 合法，description ≤ 1024 字元
  - [ ] 內文引用的路徑都存在
  - [ ] 新增的 shell 範例實際執行過一次並得到預期結果
- 驗證：行數與 description 長度腳本；`grep` 引用路徑；在暫存目錄建立兩個假頁面，執行同步檢查指令，確認「一致時無輸出、不一致時會報出差異」
- 相依：T1（側欄區塊的 class 名稱）
- 檔案：`references/extending-pages.md`（新增）、`SKILL.md`

**T3（S）`writing-rules.md`：程式導讀頁型與英文規則**
- 說明：新增「程式導讀頁」骨架；新增英文寫作規則（約 80% ASD-STE100、美式拼寫擇一並保持一致）；列出固定章節標題的中英對照（Conclusion／結論、Inference／推論、Terms／名詞、Sources／來源、Pages in this topic／本主題頁面）。
- 驗收：
  - [ ] 規則與 `SKILL.md`、`extending-pages.md` 沒有矛盾
  - [ ] 篇幅預算表涵蓋英文字數
- 驗證：通讀三份文件，交叉比對用詞
- 相依：T2
- 檔案：`references/writing-rules.md`

**檢查點 A**：使用者檢視規則的 diff 與模板截圖。

### 第 2 階段：autoresearch 範例（同時驗證延伸流程）

**T4（M）範例主頁 `examples/autoresearch/autoresearch.html`**
- 說明：照 `SKILL.md` 的流程產出英文主頁，說明目的、三個檔案的分工與使用方式。L0 用來說明結構；L1 用來說明固定 5 分鐘預算的取捨（滑桿：預算長度 ↔ 每晚實驗數）；L2 用 stepper 說明實驗迴圈（修改 → commit → 訓練 → 讀 val_bpb → 保留或 reset）。過程中照常執行第 4 步，向使用者確認疑問清單。
- 驗收：
  - [ ] 通過第 6 步全部自我檢查
  - [ ] 每個數字都有來源
  - [ ] 篇幅在預算內
- 驗證：`FILL` 計數、外部資源 `grep`、檔案大小、英文字數腳本；兩種寬度截圖；stepper 各幀截圖
- 相依：T1–T3
- 檔案：`examples/autoresearch/autoresearch.html`

**T5（M）以延伸流程加入兩個程式導讀子頁**
- 說明：把「train.py／prepare.py 各在做什麼、為什麼這樣設計」當作使用者的追問，照 `extending-pages.md` 執行：先判定落點並確認，再產出 `autoresearch--train-py.html` 與 `autoresearch--prepare-py.html`，並更新三頁的側欄清單。
- 驗收：
  - [ ] 三頁側欄清單一致，所有相對連結都可開啟
  - [ ] 主頁延伸前後的字數都在預算內
  - [ ] 子頁符合程式導讀頁型
- 驗證：同步檢查指令；檢查連結目標檔案存在；字數腳本；每頁兩種寬度截圖
- 相依：T4
- 檔案：`examples/autoresearch/` 下三個 HTML 檔

**檢查點 B**：使用者閱讀英文範例，回饋是否看得懂；依回饋修正 skill 規則。

### 第 3 階段：文件與打包

**T6（M）README 雙語版**
- 說明：`README.md` 改為英文，新增 `README.zh-TW.md`。兩份都：在頂端互相連結；說明靈感來自 Karpathy 的貼文，並對應貼文中的三層（ASD-STE100 寫作、圖、HTML 網頁），說明刻意不做影片；說明語言支援與延伸機制；連到 `examples/autoresearch/`，並註明要 clone 後在本機開啟；更新目錄結構。
- 驗收：
  - [ ] 兩份內容對應，標題為 `Explain As Webpage`
  - [ ] 貼文連結正確
  - [ ] 安裝指令維持舊名
- 驗證：逐段比對兩份內容；`grep` 連結；README 中提到的路徑都存在
- 相依：T5
- 檔案：`README.md`、`README.zh-TW.md`

**T7（XS）manifest 版本號與 CLAUDE.md**
- 說明：三份 manifest 的版本號升為 `0.2.0`；`CLAUDE.md` 的架構段落補上 `extending-pages.md` 與 `examples/`。
- 驗收：
  - [ ] 三份 manifest 的版本號一致
  - [ ] JSON 合法
  - [ ] plugin 驗證通過
- 驗證：`python3 -m json.tool`；`claude plugin validate .`；`claude --plugin-dir . plugin details sphinx-style-notes-maker`
- 相依：T6
- 檔案：`.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json`、`.codex-plugin/plugin.json`、`.agents/plugins/marketplace.json`、`CLAUDE.md`

**檢查點 C**：所有驗收條件完成；提供 `git add` 範圍與提交訊息建議。

## Risks and Mitigations

| 風險 | 影響 | 對策 |
|---|---|---|
| 修改既有頁面時弄壞 SVG 或連結 | 高 | T5 以真實延伸流程驗證；修改後截圖，並檢查連結目標存在 |
| 側欄清單在各頁之間不同步 | 中 | 第 6 步加入比對指令，並在 T2 實際執行 |
| 主頁越補越長 | 中 | `<details>` 計入預算；延伸前後量測字數 |
| 範例中的數字沒有本機實測依據 | 中 | 只用上游文件與程式常數，標明來源；推論放進 Inference 提示框 |
| GitHub 不會直接渲染 HTML | 低 | README 說明要在本機開啟 |
| 引用 autoresearch 的程式碼片段 | 低 | 上游為 MIT 授權；每段 ≤ 15 行，並附上游連結 |

## Open Questions

- 英文範例是否讀得懂：在檢查點 B 由使用者判讀。
