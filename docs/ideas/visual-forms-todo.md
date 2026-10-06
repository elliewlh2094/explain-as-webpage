# Todo：擴充視覺表現形式（第四輪）

詳細驗收條件見 `docs/ideas/visual-forms-plan.md`，構想見 `docs/ideas/visual-forms.md`。

## 第 0 階段：風險探測
- [x] T1 基準與圖示庫（token 基準、LICENSE、覆蓋率；建議 Lucide，兩套各缺 3/101）
- [x] T2 具象外形試畫（背包、人體剪影、罐子；未變形，不需限縮）

### 檢查點 0
- [x] 使用者選定圖示庫與具象插圖的範圍（Lucide；三種配方；插圖繪製規範列為後續工作）

## 第 1 階段：拆分（行為不變）
- [x] T3 建立 `skills/explainer-figure/`，搬移 `svg-recipes.md`，更新引用
- [x] T4 觸發測試（7 個提示：explainer-figure 0 次；說明頁 2/2 觸發 explain-as-webpage）

### 檢查點 A
- [ ] 使用者檢視拆分 diff；提供提交建議（使用者先跳過，T3–T6 尚未提交）

## 第 2 階段：視覺詞彙
- [x] T5 概念色與對比檢查（c1–c5、`.chip`、`--green-text`；全部 ≥ 4.5:1）
- [x] T6 歸納卡（`.card-grid`／`.card`、`cards.md`、觸發條件）
- [x] T7 圖示子集與同步指令（106 個 Lucide 圖示、`icons.md`）
- [x] T8 具象插圖配方（P1–P3、`pictorial.md`、6 個模板 class）

### 檢查點 B
- [x] 使用者檢視模板截圖與配方片段（色票易分辨；卡片與圖示待實際案例判斷；配方可接受）

## 第 3 階段：編排者整合
- [ ] T9 圖說明單接入流程

## 第 4 階段：驗收頁面
- [ ] T10 重做 starship-reusability
- [ ] T11 重做 llm-wiki
- [ ] T12 新主題一頁（主題由使用者指定）

### 檢查點 C
- [ ] 使用者判讀並排截圖，決定是否取代 `examples/` 中的兩頁

## 第 5 階段：Codex 與打包
- [ ] T13 Codex 實測（使用者手動）
- [ ] T14 manifest 0.4.0、README、`CLAUDE.md`、構想文件的 Open Questions

### 檢查點 D
- [ ] 全部驗收條件達成；提供最終提交建議
