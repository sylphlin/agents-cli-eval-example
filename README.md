# 對聯創作機器人與 agents-cli eval 評估範例 (agents-cli-eval-example)

本專案是一個基於 Google ADK（Agent Development Kit）與 `agents-cli` 建構的「對聯創作機器人 (`couplet_generator`)」，專門用來展示如何對 AI 代理執行**硬性邏輯條件驗證**與**軟性文學意境美學評估**，是 `agents-cli eval` 系統的標準示範專案。

---

## 📂 專案結構說明

```text
agents-cli-eval-example/
├── app/                           # 核心代理邏輯與應用程式容器
│   ├── agent.py                   # 對聯創作機器人主程式與創作提示詞設定
│   ├── app_utils/                 # 應用程式輔助工具與遙測 (Telemetry) 模組
│   └── fast_api_app.py            # FastAPI 本機開發服務介面
├── benchmark_examples/            # 💡 測試報告範例檔 (含 JSON 數據與 HTML 視覺化報告)
├── tests/                         # 單元測試、整合測試與代理評估測試案例
│   ├── eval/                      # 💡 [重點目錄] 測試案例與評分標準核心設定
│   │   ├── datasets/              # 評估測試資料集目錄
│   │   │   ├── basic-dataset.json # 標準對聯創作評估測試題庫 (8大典型場景)
│   │   │   └── README.md          # 資料集結構與自訂資料集說明指南
│   │   └── eval_config.yaml       # 評分標準與自訂評量指標設定檔 (LLM-as-a-Judge)
│   ├── integration/               # 整合測試案例
│   └── unit/                      # 單元測試案例
├── artifacts/                     # 執行 eval 產生的軌跡檔 (traces) 與評分報告 (grade_results)
├── .gitignore                     # Git 忽略檔案設定
├── .agents-cli-spec.md            # 代理規格與核心設計說明文件
├── AGENTS.md                      # AI 輔助開發準則指南
└── pyproject.toml                 # 專案相依套件與設定
```

---

## 🎯 測試案例與評分標準位置說明

進行 AI 代理評估 (`agents-cli eval`) 時，最核心的兩大設定對應於本專案的 `tests/eval/` 目錄：

### 1. 測試案例 (Evaluation Datasets / Test Cases)

- **檔案位置**：[basic-dataset.json](file:///usr/local/google/home/sylph/Documents/Agy/agents-cli-eval-example/tests/eval/datasets/basic-dataset.json)（以及 [tests/eval/datasets/](file:///usr/local/google/home/sylph/Documents/Agy/agents-cli-eval-example/tests/eval/datasets) 目錄）
- **內容說明**：提供多組對聯創作的用戶提示詞（單一提示詞 Shape A 結構），涵蓋 **8 種典型對聯創作與嵌字格律驗證場景**：
  1. `spring_festival_7_char`：7字春節賀歲對聯，要求上聯嵌『春』、下聯嵌『福』。
  2. `company_opening_5_char`：5字慶祝科技公司開工對聯。
  3. `he_ding_ge_7_char`：7字鶴頂格（冠頭格），首字必須為『龍』與『年』。
  4. `yan_zu_ge_5_char`：5字雁足格（藏尾格），末字必須為『長』與『壽』。
  5. `fu_qian_ge_7_char`：7字腹嵌格，正中央第4字必須為『鴻』與『圖』。
  6. `kui_dou_ge_7_char`：7字魁鬥格，上聯首字嵌『福』、下聯末字嵌『滿』。
  7. `lian_li_ge_7_char`：7字連理格，要求『同心』二字相鄰連續出現。
  8. `sui_jin_ge_7_char`：7字碎錦格（散嵌），要求『風調雨順』分散出現在上下聯中。

> 💡 **擴充測試案例**：您可以直接複製 `basic-dataset.json` 進行手動擴充，或執行指令自動生成測試情境：
> ```bash
> agents-cli eval dataset synthesize --count 10
> ```

---

### 2. 評分標準 (Evaluation Criteria / Metrics & Scoring Standards)

- **檔案位置**：[eval_config.yaml](file:///usr/local/google/home/sylph/Documents/Agy/agents-cli-eval-example/tests/eval/eval_config.yaml)
- **內容說明**：定義了評估預設執行的指標 (`metrics_to_run`) 與自訂的 LLM-as-a-Judge 評分指標 (`custom_metrics`)：

#### ① 對聯規範與嵌字格律落點檢驗 (`couplet_constraint_compliance`)
負責檢驗代理是否精準遵守出題者的硬性條件規範，檢驗項目包含：
- **上下聯字數精準度**：漢字數是否完全等於題目要求字數（標點符號不計入）。
- **對聯基本結構**：內容中是否明確包含「上聯」與「下聯」標示。
- **嵌字格律落點檢驗**：鶴頂格（首字）、雁足格（末字）、腹嵌格（中央）、魁鬥格（首尾對角）、連理格（連續相鄰）、碎錦格（分散出現在句中）。
- **嚴格評分標準 (1 ~ 5 分)**：
  - `1分（差勁）`：完全未達字數要求，或完全遺漏嵌字。
  - `2分（不及格）`：字數正確但嵌字落點完全錯誤（例如鶴頂格嵌到了中間或句尾）。
  - `3分（普通）`：字數正確，嵌字出現但個別落點有輕微偏差。
  - `4分（良好）`：精準符合字數，嵌字格律落點基本正確。
  - `5分（優異）`：字數絲毫不差，且嵌字完全精準落在體格規範的指定落點，無可挑剔。

#### ② 對聯文學品質與美學評估 (`couplet_artistic_quality`)
精通平仄對仗與詩詞美學的文學品質評估，綜合考量「詞性對仗」、「平仄協調」與「語意層次」：
- **嚴格評分標準 (1 ~ 5 分)**：
  - `1分（差勁）`：詞性完全不對仗、平仄嚴重失調，且語意模糊或語句不通順。
  - `2分（不及格）`：詞性對仗或平仄協調有明顯瑕疵，語意勉強可通但過於俗套。
  - `3分（普通）`：詞性對仗與平仄協調尚可，語意通順清晰。
  - `4分（良好）`：詞性工整對仗、平仄基本協調，語意流暢且具備文雅情致。
  - `5分（優異）`：詞性嚴謹工整對仗、平仄和諧協調，且文辭優美雅致、意境深遠。

---

## 🧪 跑測試案例指令指南 (Running Test Cases & Evaluations)

本專案提供兩類測試案例：**AI 代理行為評估測試 (`agents-cli eval`)** 與 **自動化單元/整合測試 (`pytest`)**。以下為完整的指令清單：

### 1. 執行 AI 代理評估測試案例 (`agents-cli eval`)

#### ① 一鍵執行預設測試資料集與評分標準
```bash
# 1. 對測試案例產生執行軌跡 (匯出至 artifacts/traces/)
agents-cli eval generate

# 2. 依據 tests/eval/eval_config.yaml 的評分標準進行自動打分
agents-cli eval grade
```

#### ② 指定特定測試資料集與輸出目錄
```bash
# 對指定的資料集 JSON 執行生成
agents-cli eval generate --dataset tests/eval/datasets/basic-dataset.json --output custom_traces/

# 指定評分標準對生成的軌跡檔進行打分
agents-cli eval grade --metrics couplet_constraint_compliance couplet_artistic_quality --traces custom_traces/
```

#### ③ 檢視、聚類分析與比較評分結果
```bash
# 聚類分析評分報告 JSON 中的失敗模式與常規錯誤
agents-cli eval analyze artifacts/grade_results/<grade_result_json>

# 比較新舊兩份打分結果（檢查是否發生能力迴歸 Regression）
agents-cli eval compare artifacts/grade_results/<base_json> artifacts/grade_results/<cand_json>
```

#### ④ 透過 AI 自動合成擴充測試資料集
```bash
# 自動生成 10 組對聯創作測試情境
agents-cli eval dataset synthesize --count 10
```

#### ⑤ 【進階實驗】動態驅動提示詞與多模型對比（不改動主程式的基準線測試）
本專案採用 **Environment-driven (環境變數動態驅動)** 架構設計，將「模型選型」、「思考預算」與「提示詞寫法」完全解耦。開發者無須修改 `app/agent.py` 任何一行程式碼，即可在命令列與 CI/CD 中靈活注入變數來執行 A/B 測試對比：

##### 🔧 外部配置環境變數一覽
| 環境變數名稱 | 功能說明 | 預設值 | 允許替換範例 |
| :--- | :--- | :--- | :--- |
| **`COUPLET_MODEL_NAME`** | 代理底層模型選型 | `"gemini-3.5-flash"` | `"gemini-2.5-flash"`, `"gemini-3.1-pro-preview"`, `"gemini-2.5-pro"` |
| **`COUPLET_THINKING_LEVEL`**| 推理思考深度等級 | `"medium"` | `"minimal"`, `"medium"`, `"high"` |
| **`COUPLET_PROMPT_MODE`** | 創作提示詞版本 | `"detailed"` (完整格律版) | `"simple"` (簡易常規版) |

*(測試報告範例皆收錄於根目錄 `benchmark_examples/` 下，內含 JSON 數據與 HTML 視覺化報告)*

##### 💻 A/B 對比實驗執行指令與報告樣板

以下示範如何透過命令列注入變數執行 A/B 測試。每個步驟後方附有對應產出的 HTML 單點測試報告與 JSON 兩兩比對報告樣板，方便您快速檢視與對照：

###### 【實驗 A】提示詞工程對比（固定模型為 Gemini 3.5 Flash + Medium Thinking）

**1. 測試 Baseline：簡易提示詞 (`Simple Prompt`)**
```bash
COUPLET_PROMPT_MODE=simple agents-cli eval generate --output benchmark_examples/traces_gemini35_flash_simple_prompt.json
agents-cli eval grade --traces benchmark_examples/traces_gemini35_flash_simple_prompt.json --output benchmark_examples/results_gemini35_flash_simple_prompt.json
```
👉 **[檢視樣板：Gemini 3.5 Flash (簡易提示詞) 單點測試 HTML 報告](./benchmark_examples/results_gemini35_flash_simple_prompt.html)**

**2. 測試 Candidate：詳細說明提示詞 (`Detailed Prompt`)**
```bash
COUPLET_PROMPT_MODE=detailed agents-cli eval generate --output benchmark_examples/traces_gemini35_flash_medium.json
agents-cli eval grade --traces benchmark_examples/traces_gemini35_flash_medium.json --output benchmark_examples/results_gemini35_flash_medium.json
```
👉 **[檢視樣板：Gemini 3.5 Flash (詳細說明提示詞) 單點測試 HTML 報告](./benchmark_examples/results_gemini35_flash_medium.html)**

**3. 執行分析報告（觀測提示詞優化對聯格律理解的具體成效）**
```bash
agents-cli eval compare benchmark_examples/results_gemini35_flash_simple_prompt.json benchmark_examples/results_gemini35_flash_medium.json
```
👉 **[檢視樣板：簡易提示詞 vs 詳細說明提示詞 JSON 差異對比報告](./benchmark_examples/compare_prompt_simple_vs_detailed.json)**

---

###### 【實驗 B】多模型世代與架構選型對比（固定為 Detailed Prompt + Medium Thinking）

**1. 測試 Baseline：Gemini 2.5 Flash**
```bash
COUPLET_MODEL_NAME="gemini-2.5-flash" agents-cli eval generate --output benchmark_examples/traces_gemini25_flash_medium.json
agents-cli eval grade --traces benchmark_examples/traces_gemini25_flash_medium.json --output benchmark_examples/results_gemini25_flash_medium.json
```
👉 **[檢視樣板：Gemini 2.5 Flash 單點測試 HTML 報告](./benchmark_examples/results_gemini25_flash_medium.html)**

**2. 跨世代進化對比 (2.5 Flash vs 3.5 Flash)**
```bash
agents-cli eval compare benchmark_examples/results_gemini25_flash_medium.json benchmark_examples/results_gemini35_flash_medium.json
```
👉 **[檢視樣板：Gemini 2.5 Flash vs Gemini 3.5 Flash JSON 差異對比報告](./benchmark_examples/compare_gemini25_vs_35_flash.json)**

**3. 主力與文學旗艦大師對比 (3.5 Flash vs 3.1 Pro Preview)**
*(觀測 `gemini-3.1-pro-preview` 在嚴格格律與文學美學 `artistic_quality` 躍升至 4.250 高分的旗艦表現)*
```bash
COUPLET_MODEL_NAME="gemini-3.1-pro-preview" agents-cli eval generate --output benchmark_examples/traces_gemini31_pro_medium.json
agents-cli eval grade --traces benchmark_examples/traces_gemini31_pro_medium.json --output benchmark_examples/results_gemini31_pro_medium.json
agents-cli eval compare benchmark_examples/results_gemini35_flash_medium.json benchmark_examples/results_gemini31_pro_medium.json
```
👉 **[檢視樣板：Gemini 3.1 Pro Preview 單點測試 HTML 報告](./benchmark_examples/results_gemini31_pro_medium.html)**  
👉 **[檢視樣板：Gemini 3.5 Flash vs Gemini 3.1 Pro Preview JSON 差異對比報告](./benchmark_examples/compare_gemini35_flash_vs_31_pro.json)**

**4. 跨架構能力對比 (2.5 Flash vs 2.5 Pro)**
*(觀測 Pro 架構模型在古典對仗與平仄意境上的大師級提升)*
```bash
COUPLET_MODEL_NAME="gemini-2.5-pro" agents-cli eval generate --output benchmark_examples/traces_gemini25_pro_medium.json
agents-cli eval grade --traces benchmark_examples/traces_gemini25_pro_medium.json --output benchmark_examples/results_gemini25_pro_medium.json
agents-cli eval compare benchmark_examples/results_gemini25_flash_medium.json benchmark_examples/results_gemini25_pro_medium.json
```
👉 **[檢視樣板：Gemini 2.5 Pro 單點測試 HTML 報告](./benchmark_examples/results_gemini25_pro_medium.html)**  
👉 **[檢視樣板：Gemini 2.5 Flash vs Gemini 2.5 Pro JSON 差異對比報告](./benchmark_examples/compare_gemini25_flash_vs_pro.json)**

---

### 2. 執行自動化單元與整合測試案例 (`pytest`)

```bash
# 執行所有自動化測試案例
uv run pytest

# 僅執行單元測試案例 (tests/unit/)
uv run pytest tests/unit

# 僅執行整合測試案例 (tests/integration/)
uv run pytest tests/integration
```

---

## 🚀 快速上手與常規開發指令

| 指令 | 說明 |
| --- | --- |
| `agents-cli install` | 使用 uv 安裝與同步專案相依套件 |
| `agents-cli playground` | 啟動本機網頁互動開發游樂場（儲存 `app/agent.py` 時自動熱重載） |
| `agents-cli lint` | 執行程式碼格式與靜態型別檢查 (`ruff` / `ty`) |
| `agents-cli eval --help` | 查看完整的代理評估 CLI 參數與使用說明 |
