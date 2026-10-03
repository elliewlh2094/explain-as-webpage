# Todo：explain-as-webpage 第三輪（材料模式）

詳細驗收條件見 `tasks/plan.md`，規格見 `docs/specs/explain-as-webpage-v3.md`。第二輪的待辦已全部完成（見 git 歷史）。

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
- [ ] T9 topic 模式查證、來源等級與模板 `.grade` 樣式
- [ ] T10 V3：EKF，輕量查證，拒絕輔助 skill（驗證內建退路）
- [ ] T11 V7：first principle

### 檢查點 C
- [ ] 使用者判讀 V3 與 V7，並決定 EKF 是否做成公開範例

## 第 4 階段：讀者設定與高風險主題
- [ ] T12 R6 規則：讀者設定與高風險主題
- [ ] T13 V4：甲狀腺衛教，深度研究，使用研究類輔助 skill
- [ ] T14 V6：緊急避難包（台灣）
- [ ] T15 V5：SpaceX Starship 與可復用火箭

### 檢查點 D
- [ ] 使用者判讀 V4、V5、V6

## 第 5 階段：Codex 與打包
- [ ] T16 Codex 實測
- [ ] T17 `README.md` 與 `README.zh-TW.md`（以及視檢查點 C 的決定加入 EKF 範例）
- [ ] T18 manifest 0.3.0、`CLAUDE.md`、規格狀態、暫存檔刪除方式（`rm` 安全檢查）與回歸檢查

### 檢查點 E
- [ ] 規格 §8 的成功條件全部達成；提供 `git add` 範圍與提交訊息建議
