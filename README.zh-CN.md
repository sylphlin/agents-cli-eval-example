[English (en)](README.en.md) | [繁體中文 (zh-TW)](README.md) | [简体中文 (zh-CN)](README.zh-CN.md)

# 对联创作机器人与 agents-cli eval 评估范例 (agents-cli-eval-example)

本项目是一个基于 Google ADK（Agent Development Kit）与 `agents-cli` 构建的“对联创作机器人 (`couplet_generator`)”，专门用来展示如何对 AI 代理执行**硬性逻辑条件验证**与**软性文学意境美学评估**，是 `agents-cli eval` 系统的标准示范项目。

---

## 📂 项目结构说明

```text
agents-cli-eval-example/
├── app/                           # 核心代理逻辑与应用程序容器
│   ├── agent.py                   # 对联创作机器人主程序与创作提示词设置
│   ├── app_utils/                 # 应用程序辅助工具与遥测 (Telemetry) 模块
│   └── fast_api_app.py            # FastAPI 本地开发服务接口
├── benchmark_examples/            # 💡 测试报告范例档 (含 JSON 数据与 HTML 视觉化报告)
├── tests/                         # 单元测试、集成测试与代理评估测试案例
│   ├── eval/                      # 💡 [重点目录] 测试案例与评分标准核心设置
│   │   ├── datasets/              # 评估测试数据集目录
│   │   │   ├── basic-dataset.json # 标准对联创作评估测试题库 (8大典型场景)
│   │   │   └── README.md          # 数据集结构与自定义数据集说明指南
│   │   └── eval_config.yaml       # 评分标准与自定义评量指标配置文件 (LLM-as-a-Judge)
│   ├── integration/               # 集成测试案例
│   └── unit/                      # 单元测试案例
├── artifacts/                     # 执行 eval 产生的轨迹档 (traces) 与评分报告 (grade_results)
├── .gitignore                     # Git 忽略文件配置
├── .agents-cli-spec.md            # 代理规格与核心设计说明文件
├── AGENTS.md                      # AI 辅助开发准则指南
└── pyproject.toml                 # 项目依赖套件与配置
```

---

## 🎯 测试案例与评分标准位置说明

进行 AI 代理评估 (`agents-cli eval`) 时，最核心的两大配置对应于本项目的 `tests/eval/` 目录：

### 1. 测试案例 (Evaluation Datasets / Test Cases)

- **文件位置**：[basic-dataset.json](file:///usr/local/google/home/sylph/Documents/Agy/agents-cli-eval-example/tests/eval/datasets/basic-dataset.json)（以及 [tests/eval/datasets/](file:///usr/local/google/home/sylph/Documents/Agy/agents-cli-eval-example/tests/eval/datasets) 目录）
- **内容说明**：提供多组对联创作的用户提示词（单一提示词 Shape A 结构），涵盖 **8 种典型对联创作与嵌字格律验证场景**：
  1. `spring_festival_7_char`：7字春节贺岁对联，要求上联嵌『春』、下联嵌『福』。
  2. `company_opening_5_char`：5字庆祝科技公司开工对联。
  3. `he_ding_ge_7_char`：7字鹤顶格（冠头格），首字必须为『龙』与『年』。
  4. `yan_zu_ge_5_char`：5字雁足格（藏尾格），末字必须为『长』与『寿』。
  5. `fu_qian_ge_7_char`：7字腹嵌格，正中央第4字必须为『鸿』与『图』。
  6. `kui_dou_ge_7_char`：7字魁斗格，上联首字嵌『福』、下联末字嵌『满』。
  7. `lian_li_ge_7_char`：7字连理格，要求『同心』二字相邻连续出现。
  8. `sui_jin_ge_7_char`：7字碎锦格（散嵌），要求『风调雨顺』分散出现在上下联中。

> 💡 **扩充测试案例**：您可以直接复制 `basic-dataset.json` 进行手动扩充，或执行指令自动生成测试情境：
> ```bash
> agents-cli eval dataset synthesize --count 10
> ```

---

### 2. 评分标准 (Evaluation Criteria / Metrics & Scoring Standards)

- **文件位置**：[eval_config.yaml](file:///usr/local/google/home/sylph/Documents/Agy/agents-cli-eval-example/tests/eval/eval_config.yaml)
- **内容说明**：定义了评估默认执行的指标 (`metrics_to_run`) 与自定义的 LLM-as-a-Judge 评分指标 (`custom_metrics`)：

#### ① 对联规范与嵌字格律落点检验 (`couplet_constraint_compliance`)
负责检验代理是否精准遵守出题者的硬性条件规范，检验项目包含：
- **上下联字数精准度**：汉字数是否完全等于题目要求字数（标点符号不计入）。
- **对联基本结构**：内容中是否明确包含「上联」与「下联」标示。
- **嵌字格律落点检验**：鹤顶格（首字）、雁足格（末字）、腹嵌格（中央）、魁斗格（首尾对角）、连理格（连续相邻）、碎锦格（分散出现在句中）。
- **严格评分标准 (1 ~ 5 分)**：
  - `1分（差劲）`：完全未达字数要求，或完全遗漏嵌字。
  - `2分（不及格）`：字数正确但嵌字落点完全错误（例如鹤顶格嵌到了中间或句尾）。
  - `3分（普通）`：字数正确，嵌字出现但个别落点有轻微偏差。
  - `4分（良好）`：精准符合字数，嵌字格律落点基本正确。
  - `5分（优异）`：字数丝毫不差，且嵌字完全精准落在体格规范的指定落点，无可挑剔。

#### ② 对联文学品质与美学评估 (`couplet_artistic_quality`)
精通平仄对仗与诗词美学的文学品质评估，综合考量「词性对仗」、「平仄协调」与「语意层次」：
- **严格评分标准 (1 ~ 5 分)**：
  - `1分（差劲）`：词性完全不对仗、平仄严重失调，且语意模糊或语句不通顺。
  - `2分（不及格）`：词性对仗或平仄协调有明显瑕疵，语意勉强可通但过于俗套。
  - `3分（普通）`：词性对仗与平仄协调尚可，语意通顺清晰。
  - `4分（良好）`：词性工整对仗、平仄基本协调，语意流畅且具备文雅情致。
  - `5分（优异）`：词性严谨工整对仗、平仄和谐协调，且文辞优美雅致、意境深远。

---

## 🧪 跑测试案例指令指南 (Running Test Cases & Evaluations)

本项目提供两类测试案例：**AI 代理行为评估测试 (`agents-cli eval`)** 与 **自动化单元/集成测试 (`pytest`)**。以下为完整的指令清单：

### 1. 执行 AI 代理评估测试案例 (`agents-cli eval`)

#### ① 一键执行默认测试数据集与评分标准
```bash
# 1. 对测试案例产生执行轨迹 (导出至 artifacts/traces/)
agents-cli eval generate

# 2. 依据 tests/eval/eval_config.yaml 的评分标准进行自动打分
agents-cli eval grade
```

#### ② 指定特定测试数据集与输出目录
```bash
# 对指定的数据集 JSON 执行生成
agents-cli eval generate --dataset tests/eval/datasets/basic-dataset.json --output custom_traces/

# 指定评分标准对生成的轨迹档进行打分
agents-cli eval grade --metrics couplet_constraint_compliance couplet_artistic_quality --traces custom_traces/
```

#### ③ 检视、聚类分析与比较评分结果
```bash
# 聚类分析评分报告 JSON 中的失败模式与常规错误
agents-cli eval analyze artifacts/grade_results/<grade_result_json>

# 比较新旧两份打分结果（检查是否发生能力回归 Regression）
agents-cli eval compare artifacts/grade_results/<base_json> artifacts/grade_results/<cand_json>
```

#### ④ 通过 AI 自动合成扩充测试数据集
```bash
# 自动生成 10 组对联创作测试情境
agents-cli eval dataset synthesize --count 10
```

#### ⑤ 【进阶实验】动态驱动提示词与多模型对比（不改动主程序的基准线测试）
本项目采用 **Environment-driven (环境变量动态驱动)** 架构设计，将「模型选型」、「思考预算」与「提示词写法」完全解耦。开发者无须修改 `app/agent.py` 任何一行代码，即可在命令行与 CI/CD 中灵活注入变量来执行 A/B 测试对比：

##### 🔧 外部配置环境变量一览
| 环境变量名称 | 功能说明 | 默认值 | 允许替换范例 |
| :--- | :--- | :--- | :--- |
| **`COUPLET_MODEL_NAME`** | 代理底层模型选型 | `"gemini-3.5-flash"` | `"gemini-2.5-flash"`, `"gemini-3.1-pro-preview"`, `"gemini-2.5-pro"` |
| **`COUPLET_THINKING_LEVEL`**| 推理思考深度等级 | `"medium"` | `"minimal"`, `"medium"`, `"high"` |
| **`COUPLET_PROMPT_MODE`** | 创作提示词版本 | `"detailed"` (完整格律版) | `"simple"` (简易常规版) |

*(测试报告范例皆收录于根目录 `benchmark_examples/` 下，内含 JSON 数据与 HTML 视觉化报告)*

##### 💻 A/B 对比实验执行指令与报告样板

以下示范如何通过命令行注入变量执行 A/B 测试。每个步骤后方附有对应产出的 HTML 单点测试报告与 JSON 两两对比报告样板，方便您快速检视与对照：

###### 【实验 A】提示词工程对比（固定模型为 Gemini 3.5 Flash + Medium Thinking）

**1. 测试 Baseline：简易提示词 (`Simple Prompt`)**
```bash
COUPLET_PROMPT_MODE=simple agents-cli eval generate --output benchmark_examples/traces_gemini35_flash_simple_prompt.json
agents-cli eval grade --traces benchmark_examples/traces_gemini35_flash_simple_prompt.json --output benchmark_examples/results_gemini35_flash_simple_prompt.json
```
👉 **[范例报告：Gemini 3.5 Flash (简易提示词) 单点测试 HTML 报告](./benchmark_examples/results_gemini35_flash_simple_prompt.html)**

**2. 测试 Candidate：详细说明提示词 (`Detailed Prompt`)**
```bash
COUPLET_PROMPT_MODE=detailed agents-cli eval generate --output benchmark_examples/traces_gemini35_flash_medium.json
agents-cli eval grade --traces benchmark_examples/traces_gemini35_flash_medium.json --output benchmark_examples/results_gemini35_flash_medium.json
```
👉 **[范例报告：Gemini 3.5 Flash (详细说明提示词) 单点测试 HTML 報告](./benchmark_examples/results_gemini35_flash_medium.html)**

**3. 执行分析报告（观测提示词优化对联格律理解的具体成效）**
```bash
agents-cli eval compare benchmark_examples/results_gemini35_flash_simple_prompt.json benchmark_examples/results_gemini35_flash_medium.json
```
👉 **[范例报告：简易提示词 vs 详细说明提示词 HTML 差异对比报告](./benchmark_examples/compare_prompt_simple_vs_detailed.html)**

---

###### 【实验 B】多模型世代与架构选型对比（固定为 Detailed Prompt + Medium Thinking）

**1. 测试 Baseline：Gemini 2.5 Flash**
```bash
COUPLET_MODEL_NAME="gemini-2.5-flash" agents-cli eval generate --output benchmark_examples/traces_gemini25_flash_medium.json
agents-cli eval grade --traces benchmark_examples/traces_gemini25_flash_medium.json --output benchmark_examples/results_gemini25_flash_medium.json
```
👉 **[范例报告：Gemini 2.5 Flash 单点测试 HTML 报告](./benchmark_examples/results_gemini25_flash_medium.html)**

**2. 跨世代进化对比 (2.5 Flash vs 3.5 Flash)**
```bash
agents-cli eval compare benchmark_examples/results_gemini25_flash_medium.json benchmark_examples/results_gemini35_flash_medium.json
```
👉 **[检視样板：Gemini 2.5 Flash vs Gemini 3.5 Flash HTML 差异对比报告](./benchmark_examples/compare_gemini25_vs_35_flash.html)**

**3. 主力与文学旗舰大师对比 (3.5 Flash vs 3.1 Pro Preview)**
*(观测 `gemini-3.1-pro-preview` 在严格格律与文学美学 `artistic_quality` 跃升至 4.250 高分的旗舰表现)*
```bash
COUPLET_MODEL_NAME="gemini-3.1-pro-preview" agents-cli eval generate --output benchmark_examples/traces_gemini31_pro_medium.json
agents-cli eval grade --traces benchmark_examples/traces_gemini31_pro_medium.json --output benchmark_examples/results_gemini31_pro_medium.json
agents-cli eval compare benchmark_examples/results_gemini35_flash_medium.json benchmark_examples/results_gemini31_pro_medium.json
```
👉 **[范例报告：Gemini 3.1 Pro Preview 单点测试 HTML 报告](./benchmark_examples/results_gemini31_pro_medium.html)**  
👉 **[范例报告：Gemini 3.5 Flash vs Gemini 3.1 Pro Preview HTML 差异对比报告](./benchmark_examples/compare_gemini35_flash_vs_31_pro.html)**

**4. 跨架构能力对比 (2.5 Flash vs 2.5 Pro)**
*(观测 Pro 架构模型在古典对仗与平仄意境上的大师级提升)*
```bash
COUPLET_MODEL_NAME="gemini-2.5-pro" agents-cli eval generate --output benchmark_examples/traces_gemini25_pro_medium.json
agents-cli eval grade --traces benchmark_examples/traces_gemini25_pro_medium.json --output benchmark_examples/results_gemini25_pro_medium.json
agents-cli eval compare benchmark_examples/results_gemini25_flash_medium.json benchmark_examples/results_gemini25_pro_medium.json
```
👉 **[范例报告：Gemini 2.5 Pro 单点测试 HTML 报告](./benchmark_examples/results_gemini25_pro_medium.html)**  
👉 **[范例报告：Gemini 2.5 Flash vs Gemini 2.5 Pro HTML 差异对比报告](./benchmark_examples/compare_gemini25_flash_vs_pro.html)**

---

### 2. 执行自动化单元与集成测试案例 (`pytest`)

```bash
# 执行所有自动化测试案例
uv run pytest

# 仅执行单元测试案例 (tests/unit/)
uv run pytest tests/unit

# 仅执行集成测试案例 (tests/integration/)
uv run pytest tests/integration
```

---

### 3. 雲端部署與線上遠端評估服務 (`Cloud-side Deploy & Remote Eval`)

当本地测试与合规评估满分后，开发者可一键将机器人部署至 Google Cloud 生产环境（如 Vertex AI Agent Runtime 全托管引擎或 Cloud Run），并启动云端异步的 **Agent Platform Eval Service** 对线上已部署的实例进行高并发推论对话测试与 LLM-as-a-Judge 评分：

```bash
# ---------------------------------------------------------------------
# ① 初始化云端托管基础建设架构 (生成 Dockerfile / Terraform 脚本)
# ---------------------------------------------------------------------
agents-cli scaffold enhance . --deployment-target agent_runtime -y

# ---------------------------------------------------------------------
# ② 正式建置并部署上云 (支持异步启动 --no-wait)
# ---------------------------------------------------------------------
agents-cli deploy --project <YOUR_PROJECT_ID> --no-confirm-project --no-wait

# 随时查询后端推论引擎部署进度状态
agents-cli deploy --status

# ---------------------------------------------------------------------
# ③ 执行云端线上推论与自动裁判评估 (由云端平行并发处理，零本地运算压力)
# ---------------------------------------------------------------------
# 将题库提交至云端，对线上 Reasoning Engine 跑推论对话 + LLM 裁判自动打分
agents-cli eval submit \
  --dataset tests/eval/datasets/basic-dataset.json \
  --dest gs://<YOUR_GCS_BUCKET_NAME> \
  --resource-name "projects/<PROJECT_ID>/locations/<LOCATION>/reasoningEngines/<REASONING_ENGINE_ID>"

# 异步轮询与下载云端产出的评估报告 (若 submit 时有带 --region，此处也必须加上对应 region)
agents-cli eval results --run-id <EVAL_RUN_RESOURCE_NAME> --region <REGION>
```
```
