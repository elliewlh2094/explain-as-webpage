# Explain As Webpage

[English](README.md) | 繁體中文

讓 AI 代理把「你專案裡用到、但你不熟悉的技術或設計」做成**以你的專案為例**的知識網頁。

本儲存庫提供一個 skill：`explain-as-webpage`。它可以在 Claude Code 與 Codex 上使用，兩者共用同一份 `SKILL.md`。

## 靈感來源

本 skill 的靈感來自 Andrej Karpathy 的貼文：[x.com/karpathy/status/2105819303471976479](https://x.com/karpathy/status/2105819303471976479)。貼文指出，隨著 LLM 代為完成越來越多工作，我們會花更多時間理解它們的產出；並依序建議幾種更容易理解的輸出形式：以 ASD-STE100（源自航太維修文件的受控英語規範）撰寫、改畫成圖、改做成 HTML 網頁，以及最看好的解說影片。

本 skill 實作前三項：寫作規則約為「八成的 ASD-STE100」，圖片是內嵌 SVG，成品是單一 HTML 網頁，並可加上瀏覽器內的逐步動畫。本 skill **刻意不做影片**，理由見[刻意不做的事](#刻意不做的事)。

## 它會產出什麼

- **單一 HTML 檔**：外觀仿照 Read the Docs（sphinx_rtd_theme），圖片全部是內嵌 SVG，不連外部資源，可以離線開啟。不需要建置，也不會另外產生 `figures/` 或 `scripts/` 資料夾。
- **以疑問為章節**：先給結論，再畫一條因果鏈。每一節回答一個讀者真正卡住的問題，並用專案的真實檔案、數據與程式碼舉例。
- **依主題選擇成本最低、但仍足以說明的呈現層級**：

| 層級 | 形式 | 適用的疑問 |
|---|---|---|
| L0 | 文字＋靜態 SVG | 結構、組成、因果鏈、前後對照 |
| L1 | L0＋展開區塊、一個滑桿 | 結果隨某個參數變化的取捨 |
| L2 | L1＋逐步動畫（上一步／下一步／播放） | 迭代演算法、隨時間演進的過程 |

- **英文或繁體中文**：頁面語言依你的要求決定；沒有指定時，跟隨你提問使用的語言。繁體中文預設使用台灣用語。
- **可依追問延伸**：對既有頁面繼續追問時，代理會依判準決定落點。短答且屬於既有疑問，補進原頁的展開區塊；新的疑問，另開子頁並與主頁互相連結；會改變主結論，則修訂主頁。每一頁各自遵守篇幅預算，主頁不會越補越長。

代理會先列出疑問清單、建議的層級與輸出路徑，**等你確認後才開始產出**。預設輸出位置是 `~/Documents/explainers/<repo 名稱>/<主題>.html`，不會放進你的專案。

## 範例

[`examples/autoresearch/`](examples/autoresearch/) 以 [karpathy/autoresearch](https://github.com/karpathy/autoresearch)（commit `228791f`，MIT 授權）為例，產出三頁英文網頁：

| 頁面 | 層級 | 內容 |
|---|---|---|
| `autoresearch.html`（主頁） | L2 | 儲存庫的目的、三個檔案的分工、使用方式。以靜態圖說明結構（L0），以滑桿說明 5 分鐘時間預算的取捨（L1），以逐步動畫說明實驗迴圈（L2） |
| `autoresearch--train-py.html` | L1 | `train.py` 程式導讀：模型大小、兩種最佳化器、依時間計算的學習率排程 |
| `autoresearch--prepare-py.html` | L0 | `prepare.py` 程式導讀：資料、驗證分片、資料打包、`val_bpb` 的計算 |

兩個子頁是以「追問」的方式，透過延伸流程加入的。GitHub 不會直接顯示 HTML，請 clone 後在本機開啟：

```bash
xdg-open examples/autoresearch/autoresearch.html   # macOS 用 open
```

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
- 「接續 `swarm-experiment-package.html`，我想知道每個程式檔各在做什麼。」（延伸既有頁面）
- 「用英文做一頁網頁，解釋這個儲存庫的目的與使用方式。」

產出後，用 `xdg-open <路徑>`（Linux）或 `open <路徑>`（macOS）開啟。

## 目錄結構

```text
skills/explain-as-webpage/
├── SKILL.md                    # 流程與層級判準（Claude Code 與 Codex 共用）
├── references/
│   ├── writing-rules.md        # 頁面骨架、程式導讀頁型、圖文綁定、語言與篇幅規則
│   ├── svg-recipes.md          # SVG 版面規則、顏色語意、圖形配方、逐步動畫與滑桿
│   └── extending-pages.md      # 依追問延伸頁面：落點判準、頁面樹、同步檢查
└── assets/
    └── template.html           # RTD 風格的單檔模板
examples/autoresearch/          # 範例：主頁＋兩個程式導讀子頁
.claude-plugin/                 # Claude Code 的 plugin 與 marketplace manifest
.codex-plugin/                  # Codex 的 plugin manifest
.agents/plugins/                # Codex 的 marketplace manifest
docs/ideas/                     # 構想摘要
tasks/                          # 實作計畫與待辦
```

## 刻意不做的事

- **影片**：最高層級是瀏覽器內的逐步動畫，不使用 manim、ffmpeg 或語音合成。影片的工具鏈與產出成本高，而「過程」類的疑問用逐步動畫已能說明。
- **外部 CDN**：例如 MathJax、D3、Mermaid。公式改用 HTML 上下標表示。
- **Sphinx 建置**：只仿照它的外觀。
- **跨主題索引或知識庫**：頁面樹只限於同一主題（一個主頁加上它的子頁），避免增加管理負擔。

## 授權

MIT
