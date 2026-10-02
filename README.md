# sphinx-style-notes-maker

讓 AI 代理把「你專案裡用到、但你不熟悉的技術或設計」做成一頁**以你的專案為例**的知識網頁。

本儲存庫提供一個 skill：`explain-as-webpage`。它可以在 Claude Code 與 Codex 上使用，兩者共用同一份 `SKILL.md`。

## 它會產出什麼

- **單一 HTML 檔**：外觀仿照 Read the Docs（sphinx_rtd_theme），圖片全部是內嵌 SVG，不連外部資源，可以離線開啟。不需要建置，也不會另外產生 `figures/` 或 `scripts/` 資料夾。
- **以疑問為章節**：先給結論，再畫一條因果鏈。每一節回答一個讀者真正卡住的問題，並用專案的真實檔案、數據與程式碼舉例。
- **依主題選擇成本最低、但仍足以說明的呈現層級**：

| 層級 | 形式 | 適用的疑問 |
|---|---|---|
| L0 | 文字＋靜態 SVG | 結構、組成、因果鏈、前後對照 |
| L1 | L0＋展開區塊、一個滑桿 | 結果隨某個參數變化的取捨 |
| L2 | L1＋逐步動畫（上一步／下一步／播放） | 迭代演算法、隨時間演進的過程 |

代理會先列出疑問清單、建議的層級與輸出路徑，**等你確認後才開始產出**。預設輸出位置是 `~/Documents/explainers/<repo 名稱>/<主題>.html`，不會放進你的專案。

## 安裝

### Claude Code

用 plugin 安裝。安裝後的 skill 名稱會加上 plugin 前綴：`/sphinx-style-notes-maker:explain-as-webpage`。

```bash
claude plugin marketplace add elliewlh2094/sphinx-style-notes-maker   # 或本機路徑
claude plugin install sphinx-style-notes-maker@sphinx-style-notes-maker
```

也可以直接複製 skill 資料夾，之後用 `/explain-as-webpage` 呼叫：

```bash
cp -r skills/explain-as-webpage ~/.claude/skills/
```

### Codex

用 plugin 安裝。安裝後的 skill 名稱同樣會加上 plugin 前綴：`sphinx-style-notes-maker:explain-as-webpage`。

```bash
codex plugin marketplace add elliewlh2094/sphinx-style-notes-maker   # 或本機路徑
codex plugin add sphinx-style-notes-maker@sphinx-style-notes-maker
```

也可以直接複製 skill 資料夾，之後用 `@explain-as-webpage` 呼叫：

```bash
cp -r skills/explain-as-webpage ~/.codex/skills/
```

安裝後請開新的 session，讓工具重新載入 skill。

## 使用方式

直接描述你想看懂的東西，或明確呼叫 skill。例如：

- 「我不懂為什麼影像辨識要加 RANSAC 幾何驗證，參考 `docs/notebooks/XXX.md`，做成知識網頁。」
- 「`src/swarm_experiment` 這個套件在做什麼、為什麼這樣設計？用網頁解釋給我看。」

產出後，用 `xdg-open <路徑>`（Linux）或 `open <路徑>`（macOS）開啟。

## 目錄結構

```text
skills/explain-as-webpage/
├── SKILL.md                    # 流程與層級判準（Claude Code 與 Codex 共用）
├── references/
│   ├── writing-rules.md        # 頁面骨架、圖文綁定、用語與篇幅規則
│   └── svg-recipes.md          # SVG 版面規則、顏色語意、圖形配方、逐步動畫與滑桿
└── assets/
    └── template.html           # RTD 風格的單檔模板
.claude-plugin/                 # Claude Code 的 plugin 與 marketplace manifest
.codex-plugin/                  # Codex 的 plugin manifest
.agents/plugins/                # Codex 的 marketplace manifest
docs/ideas/                     # 構想摘要
tasks/                          # 實作計畫與待辦
```

## 刻意不做的事

- **影片**：最高層級是瀏覽器內的逐步動畫，不使用 manim、ffmpeg 或語音合成。
- **外部 CDN**：例如 MathJax、D3、Mermaid。公式改用 HTML 上下標表示。
- **Sphinx 建置**：只仿照它的外觀。
- **跨主題索引或知識庫**：避免增加管理負擔。

## 授權

MIT
