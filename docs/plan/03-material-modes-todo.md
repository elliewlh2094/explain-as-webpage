# Todo：explain-as-webpage 第三輪（材料模式）

詳細驗收條件見 `docs/plan/03-material-modes-plan.md`，規格見 `docs/plan/03-material-modes-spec.md`。第二輪的待辦已全部完成（見 git 歷史）。

## 第 0 階段：風險探測
- [x] T1 取得材料與環境探測（WebFetch 全文、`pdftotext`、可見的輔助 skill；Codex 延後到 T16）

## 第 1 階段：document 模式（短文）
- [x] T2 `SKILL.md` 分流與 `references/sources-and-research.md`（document 部分）
- [x] T3 V1：Karpathy LLM Wiki gist

### 檢查點 A
- [x] 使用者檢視規則 diff 與 V1 頁面，依回饋修正規則

## 第 2 階段：頁型與長文
- [x] T4 `references/page-types.md`（新增）與 4 種主軸圖配方
- [x] T5 `extending-pages.md`：第一次產出就建立頁面樹（忠實導讀）
- [x] T6 V2：Ronin PDF，忠實導讀，使用 PDF 輔助 skill
- [x] T7 V8 前提：與使用者互動產出 C++ 學習計畫（儲存庫外，不屬於 skill 流程）
- [x] T8 V8：把 C++ 學習計畫轉成網頁

### 檢查點 B
- [x] 使用者判讀 V2 與 V8，依回饋修正頁型與頁面樹規則

## 第 3 階段：topic 模式
- [x] T9 topic 模式查證、來源等級與模板 `.grade` 樣式
- [x] T10 V3：EKF（依使用者選擇改為深度研究＋deep-research；內建退路改在 T11 驗證）
- [x] T11 V7：first principle（輕量查證、不用輔助 skill，驗證內建退路）

### 檢查點 C
- [x] 使用者判讀 V3 與 V7，並決定 EKF 是否做成公開範例（決定：不公開）

## 第 4 階段：讀者設定與高風險主題
- [x] T12 R6 規則：讀者設定與高風險主題
- [x] T13 V4：甲狀腺衛教，深度研究（使用者選擇不用輔助 skill）
- [x] T14 V6：緊急避難包（台灣，主頁＋子頁）
- [x] T15 V5：SpaceX Starship 與可復用火箭（L2，助推器返回用 stepper）

### 檢查點 D
- [x] 使用者判讀 V4、V5、V6（同意三條新規則；LLM Wiki 與 Starship 收為繁中範例；以最新 skill 重做儲存庫說明頁）

## 第 5 階段：Codex 與打包
- [x] T16 Codex 實測（使用者手動測試；兩個 Codex 假設成立；§1 補上 sandbox 寫入路徑規則）
- [x] T17 `README.md` 與 `README.zh-TW.md`：沒有專案也能用、兩種預設路徑、文件與主題模式的例句、影片不接受為材料、目錄結構補上新 reference 與 `docs/specs/`
- [x] T18 manifest 0.3.0、`CLAUDE.md`、規格狀態、暫存檔刪除方式（`rm` 安全檢查）與回歸檢查

### 檢查點 E
- [x] 規格 §8 的成功條件全部達成；提供 `git add` 範圍與提交訊息建議
