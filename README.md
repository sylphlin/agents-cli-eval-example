[English (en)](README.md) | [繁體中文 (zh-TW)](README.zh-TW.md) | [简体中文 (zh-CN)](README.zh-CN.md)

# Couplet Creator Robot & agents-cli eval Example (agents-cli-eval-example)

This project is a "Couplet Creator Robot (`couplet_generator`)" built on Google ADK (Agent Development Kit) and `agents-cli`. It is designed to demonstrate how to perform **hard logical constraint verification** and **soft literary aesthetic evaluation** on AI agents. It serves as the standard demonstration project for the `agents-cli eval` framework.

---

## 📂 Project Structure

```text
agents-cli-eval-example/
├── app/                           # Core agent logic and application container
│   ├── agent.py                   # Couplet Creator Robot main program and prompts configuration
│   ├── app_utils/                 # Helper utilities and Telemetry module
│   └── fast_api_app.py            # FastAPI local development server interface
├── benchmark_examples/            # 💡 Benchmark examples (includes JSON logs and HTML visual reports)
├── tests/                         # Unit tests, integration tests, and agent evaluation cases
│   ├── eval/                      # 💡 [Key Folder] Evaluation configuration and datasets
│   │   ├── datasets/              # Dataset directory
│   │   │   ├── basic-dataset.json # Standard couplet evaluation dataset (8 typical scenarios)
│   │   │   └── README.md          # Dataset schema and custom dataset guide
│   │   └── eval_config.yaml       # Custom evaluation metrics configuration (LLM-as-a-Judge)
│   ├── integration/               # Integration tests
│   └── unit/                      # Unit tests
├── artifacts/                     # Generated execution traces and evaluation reports (Git ignored)
├── .gitignore                     # Git ignore rules
├── .agents-cli-spec.md            # Agent specification and design details
├── AGENTS.md                      # AI-assisted development guidelines
└── pyproject.toml                 # Dependencies and configuration
```

---

## 🎯 Dataset and Evaluation Config Locations

When conducting agent evaluation (`agents-cli eval`), the most critical configuration files are located under the `tests/eval/` directory:

### 1. Evaluation Dataset (Test Cases)

- **File Path**: [basic-dataset.json](file:///usr/local/google/home/sylph/Documents/Agy/agents-cli-eval-example/tests/eval/datasets/basic-dataset.json) (under the [tests/eval/datasets/](file:///usr/local/google/home/sylph/Documents/Agy/agents-cli-eval-example/tests/eval/datasets) directory)
- **Description**: Provides user prompts for couplet generation covering **8 typical couplet formats and embedding constraint scenarios**:
  1. `spring_festival_7_char`: A 7-character Chinese New Year couplet embedding "Spring" (春) in the first line and "Fortune" (福) in the second.
  2. `company_opening_5_char`: A 5-character couplet celebrating the opening of a tech company.
  3. `he_ding_ge_7_char`: A 7-character "He-Ding" couplet where the first characters must be "Dragon" (龍) and "Year" (年).
  4. `yan_zu_ge_5_char`: A 5-character "Yan-Zu" couplet where the last characters must be "Longevity" (長) and "Age" (壽).
  5. `fu_qian_ge_7_char`: A 7-character "Fu-Qian" couplet where the middle (4th) characters must be "Grandeur" (鴻) and "Map" (圖).
  6. `kui_dou_ge_7_char`: A 7-character "Kui-Dou" couplet where the first line starts with "Fortune" (福) and the second line ends with "Abundance" (滿).
  7. `lian_li_ge_7_char`: A 7-character "Lian-Li" couplet where "Same Heart" (同心) must appear side-by-side continuously.
  8. `sui_jin_ge_7_char`: A 7-character "Sui-Jin" couplet embedding the idiom "Favorable Weather" (風調雨順) scattered across both lines.

> 💡 **Adding Test Cases**: You can manually copy and expand `basic-dataset.json`, or generate synthetic test cases automatically using:
> ```bash
> agents-cli eval dataset synthesize --count 10
> ```

---

### 2. Evaluation Criteria (Metrics & Scoring Rubrics)

- **File Path**: [eval_config.yaml](file:///usr/local/google/home/sylph/Documents/Agy/agents-cli-eval-example/tests/eval/eval_config.yaml)
- **Description**: Defines metrics to run (`metrics_to_run`) and custom LLM-as-a-Judge metrics (`custom_metrics`):

#### ① Couplet Constraint & Embedding Compliance (`couplet_constraint_compliance`)
Verifies if the agent strictly complies with format and positional requirements:
- **Character Count Accuracy**: Checks if the character count exactly matches the request (excluding punctuation).
- **Structure**: Verifies that both the first line (上聯) and second line (下聯) are explicitly labeled.
- **Positional Embedding**: Checks the exact location of embedded characters (He-Ding, Yan-Zu, Fu-Qian, Kui-Dou, Lian-Li, Sui-Jin).
- **Scoring Rubric (1 to 5 Stars)**:
  - `1 Star (Poor)`: Fails character count, or misses embedded characters entirely.
  - `2 Stars (Fail)`: Correct character count but incorrect embedding positions.
  - `3 Stars (Average)`: Correct count, embeds the characters but with minor alignment issues.
  - `4 Stars (Good)`: Correct count, embeddings are in the correct positions.
  - `5 Stars (Excellent)`: Perfect character count, and embedded characters are exactly at the specified positions.

#### ② Couplet Literary & Aesthetic Quality (`couplet_artistic_quality`)
Evaluates poetic structure, tonal balance, semantic quality, and elegance:
- **Scoring Rubric (1 to 5 Stars)**:
  - `1 Star (Poor)`: Zero semantic alignment, tone mismatch, incoherent phrasing.
  - `2 Stars (Fail)`: Noticeable alignment/tonal flaws, clichés or awkward phrasing.
  - `3 Stars (Average)`: Reasonable alignment and tonal harmony, clear phrasing.
  - `4 Stars (Good)`: Elegant alignment, balanced tones, poetic and evocative phrasing.
  - `5 Stars (Excellent)`: Outstanding poetic vocabulary, perfect tone harmony, deep imagery and meaning.

---

## 🧪 CLI Commands Guide (Running Tests & Evaluations)

This project contains two types of tests: **AI Agent Behavior Evaluations (`agents-cli eval`)** and **Automated Python Tests (`pytest`)**.

### 1. AI Agent Evaluation Commands (`agents-cli eval`)

#### ① E2E Local Evaluation Run
```bash
# 1. Run inference over the dataset and output traces to artifacts/traces/
agents-cli eval generate

# 2. Grade traces against rubrics defined in tests/eval/eval_config.yaml
agents-cli eval grade
```

#### ② Running Custom Datasets and Selecting Metrics
```bash
# Generate traces for a specific dataset file
agents-cli eval generate --dataset tests/eval/datasets/basic-dataset.json --output custom_traces/

# Grade traces selecting specific metrics
agents-cli eval grade --metrics couplet_constraint_compliance,couplet_artistic_quality --traces custom_traces/
```

#### ③ Analyzing and Comparing Evaluation Results
```bash
# Run failure analysis/clustering on grade results
agents-cli eval analyze artifacts/grade_results/<grade_result_json>

# Compare two evaluation runs to check for Regression/Improvements
agents-cli eval compare artifacts/grade_results/<base_json> artifacts/grade_results/<cand_json>
```

#### ④ Auto-Synthesize Dataset expansion
```bash
# Synthesize 10 new test scenarios using LLM simulators
agents-cli eval dataset synthesize --count 10
```

#### ⑤ A/B Testing Prompts & Model Generations
This project leverages an **environment-driven** architecture. Developers can A/B test model versions, reasoning depths, and prompts via environment variables without modifying any code in `app/agent.py`:

##### 🔧 Configurable Environment Variables
| Variable Name | Description | Default | Example Options |
| :--- | :--- | :--- | :--- |
| **`COUPLET_MODEL_NAME`** | Underlying GenAI model | `"gemini-3.5-flash"` | `"gemini-2.5-flash"`, `"gemini-3.1-pro-preview"`, `"gemini-2.5-pro"` |
| **`COUPLET_THINKING_LEVEL`**| Reasoning thinking level | `"medium"` | `"minimal"`, `"medium"`, `"high"` |
| **`COUPLET_PROMPT_MODE`** | Prompt instruction mode | `"detailed"` (Full rules) | `"simple"` (Concise style) |

*(Evaluation reports for standard benchmarks are stored in the root `benchmark_examples/` directory for reference).*

##### 💻 A/B Testing Commands and Report Samples

The following commands demonstrate A/B testing configurations. Link templates of HTML reports and JSON diff results are provided below each step for quick review:

###### 【Experiment A】Prompt Engineering A/B Test (Fixed on Gemini 3.5 Flash + Medium Thinking)

**1. Baseline: Simple Concise Prompt**
```bash
COUPLET_PROMPT_MODE=simple agents-cli eval generate --output benchmark_examples/traces_gemini35_flash_simple_prompt.json
agents-cli eval grade --traces benchmark_examples/traces_gemini35_flash_simple_prompt.json --output benchmark_examples/results_gemini35_flash_simple_prompt.json
```
👉 **[Report Sample: Gemini 3.5 Flash (Simple Prompt) HTML Report](./benchmark_examples/results_gemini35_flash_simple_prompt.html)**

**2. Candidate: Detailed Poetic Prompt**
```bash
COUPLET_PROMPT_MODE=detailed agents-cli eval generate --output benchmark_examples/traces_gemini35_flash_medium.json
agents-cli eval grade --traces benchmark_examples/traces_gemini35_flash_medium.json --output benchmark_examples/results_gemini35_flash_medium.json
```
👉 **[Report Sample: Gemini 3.5 Flash (Detailed Prompt) HTML Report](./benchmark_examples/results_gemini35_flash_medium.html)**

**3. Comparison: Prompt Engineering Diff**
```bash
agents-cli eval compare benchmark_examples/results_gemini35_flash_simple_prompt.json benchmark_examples/results_gemini35_flash_medium.json
```
👉 **[Comparison Diff: Simple vs Detailed Prompt JSON Diff](./benchmark_examples/compare_prompt_simple_vs_detailed.json)**

---

###### 【Experiment B】Model Generation & Tier Comparisons (Fixed on Detailed Prompt + Medium Thinking)

**1. Baseline: Gemini 2.5 Flash**
```bash
COUPLET_MODEL_NAME="gemini-2.5-flash" agents-cli eval generate --output benchmark_examples/traces_gemini25_flash_medium.json
agents-cli eval grade --traces benchmark_examples/traces_gemini25_flash_medium.json --output benchmark_examples/results_gemini25_flash_medium.json
```
👉 **[Report Sample: Gemini 2.5 Flash HTML Report](./benchmark_examples/results_gemini25_flash_medium.html)**

**2. Cross-Generation comparison: 2.5 Flash vs 3.5 Flash**
```bash
agents-cli eval compare benchmark_examples/results_gemini25_flash_medium.json benchmark_examples/results_gemini35_flash_medium.json
```
👉 **[Comparison Diff: Gemini 2.5 Flash vs 3.5 Flash JSON Diff](./benchmark_examples/compare_gemini25_vs_35_flash.json)**

**3. Lightweight vs Literary Master comparison: 3.5 Flash vs 3.1 Pro Preview**
*(Observe `gemini-3.1-pro-preview` score leap in couplet artistic quality)*
```bash
COUPLET_MODEL_NAME="gemini-3.1-pro-preview" agents-cli eval generate --output benchmark_examples/traces_gemini31_pro_medium.json
agents-cli eval grade --traces benchmark_examples/traces_gemini31_pro_medium.json --output benchmark_examples/results_gemini31_pro_medium.json
agents-cli eval compare benchmark_examples/results_gemini35_flash_medium.json benchmark_examples/results_gemini31_pro_medium.json
```
👉 **[Report Sample: Gemini 3.1 Pro Preview HTML Report](./benchmark_examples/results_gemini31_pro_medium.html)**  
👉 **[Comparison Diff: Gemini 3.5 Flash vs 3.1 Pro Preview JSON Diff](./benchmark_examples/compare_gemini35_flash_vs_31_pro.json)**

**4. Tier Architecture comparison: 2.5 Flash vs 2.5 Pro**
*(Observe Pro model performance jump in classical tone and semantic symmetry)*
```bash
COUPLET_MODEL_NAME="gemini-2.5-pro" agents-cli eval generate --output benchmark_examples/traces_gemini25_pro_medium.json
agents-cli eval grade --traces benchmark_examples/traces_gemini25_pro_medium.json --output benchmark_examples/results_gemini25_pro_medium.json
agents-cli eval compare benchmark_examples/results_gemini25_flash_medium.json benchmark_examples/results_gemini25_pro_medium.json
```
👉 **[Report Sample: Gemini 2.5 Pro HTML Report](./benchmark_examples/results_gemini25_pro_medium.html)**  
👉 **[Comparison Diff: Gemini 2.5 Flash vs 2.5 Pro JSON Diff](./benchmark_examples/compare_gemini25_flash_vs_pro.json)**

---

### 2. Running Python Unit & Integration Tests (`pytest`)

```bash
# Run all python tests
uv run pytest

# Run only unit tests
uv run pytest tests/unit/

# Run only integration tests
uv run pytest tests/integration/
```

---

### 3. Cloud-side Deploy & Remote Eval

Once local tests and evaluations are satisfied, developers can deploy the agent to Google Cloud (such as Vertex AI Agent Runtime or Cloud Run) and launch high-concurrency evaluation tasks using **Agent Platform Eval Service** on the cloud:

```bash
# ---------------------------------------------------------------------
# ① Initialize cloud infrastructure (Generate Dockerfile / Terraform)
# ---------------------------------------------------------------------
agents-cli scaffold enhance . --deployment-target agent_runtime -y

# ---------------------------------------------------------------------
# ② Build and deploy to the cloud (supports async deployment with --no-wait)
# ---------------------------------------------------------------------
agents-cli deploy --project <YOUR_PROJECT_ID> --no-confirm-project --no-wait

# Check deployment status
agents-cli deploy --status

# ---------------------------------------------------------------------
# ③ Run cloud-side remote inference and LLM grading
# ---------------------------------------------------------------------
# Submit the evaluation dataset to evaluate a deployed reasoning engine
agents-cli eval submit \
  --dataset tests/eval/datasets/basic-dataset.json \
  --dest gs://<YOUR_GCS_BUCKET_NAME> \
  --resource-name "projects/<PROJECT_ID>/locations/<LOCATION>/reasoningEngines/<REASONING_ENGINE_ID>"

# Check status and download remote evaluation results (add --region if submitted with a specific region)
agents-cli eval results --run-id <EVAL_RUN_RESOURCE_NAME> --region <REGION>
```
```
