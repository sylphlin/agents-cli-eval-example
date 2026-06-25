#!/usr/bin/env python3
# Copyright 2026 Google LLC
# Licensed under the Apache License, Version 2.0.

import json
import sys
import os
from pathlib import Path

def generate_html(base_path: str, cand_path: str, html_path: str):
    with open(base_path, 'r', encoding='utf-8') as f:
        base_data = json.load(f)
    with open(cand_path, 'r', encoding='utf-8') as f:
        cand_data = json.load(f)

    # Determine labels based on filenames
    base_meta = "Baseline"
    cand_meta = "Candidate"
    
    # Try to find candidate name in dataset metadata
    base_ds_list = base_data.get("evaluation_dataset", [])
    if base_ds_list:
        base_meta = base_ds_list[0].get("candidate_name", "Baseline")
    cand_ds_list = cand_data.get("evaluation_dataset", [])
    if cand_ds_list:
        cand_meta = cand_ds_list[0].get("candidate_name", "Candidate")

    # If filename hints specific models/prompts
    if "simple_prompt" in base_path:
        base_meta = "Simple Prompt"
    if "medium" in base_path and "gemini35" in base_path:
        base_meta = "Gemini 3.5 Flash"
    if "gemini25_flash" in base_path:
        base_meta = "Gemini 2.5 Flash"
    if "gemini31_pro" in base_path:
        base_meta = "Gemini 3.1 Pro Preview"
    if "gemini25_pro" in base_path:
        base_meta = "Gemini 2.5 Pro"

    if "simple_prompt" in cand_path:
        cand_meta = "Simple Prompt"
    if "medium" in cand_path and "gemini35" in cand_path:
        cand_meta = "Gemini 3.5 Flash"
    if "gemini25_flash" in cand_path:
        cand_meta = "Gemini 2.5 Flash"
    if "gemini31_pro" in cand_path:
        cand_meta = "Gemini 3.1 Pro Preview"
    if "gemini25_pro" in cand_path:
        cand_meta = "Gemini 2.5 Pro"

    # Extract Summary Metrics
    base_summary = base_data.get("summary_metrics", [])
    cand_summary = cand_data.get("summary_metrics", [])
    
    metrics_map = {}
    for m in base_summary:
        name = m.get("metric_name")
        metrics_map[name] = {"base_mean": m.get("mean_score"), "base_stdev": m.get("stdev_score"), "cand_mean": None, "cand_stdev": None}
    for m in cand_summary:
        name = m.get("metric_name")
        if name not in metrics_map:
            metrics_map[name] = {"base_mean": None, "base_stdev": None, "cand_mean": m.get("mean_score"), "cand_stdev": m.get("stdev_score")}
        else:
            metrics_map[name]["cand_mean"] = m.get("mean_score")
            metrics_map[name]["cand_stdev"] = m.get("stdev_score")

    summary_table_html = ""
    for m_name, vals in metrics_map.items():
        base_val = vals["base_mean"]
        cand_val = vals["cand_mean"]
        base_str = f"{base_val:.4f}" if base_val is not None else "N/A"
        cand_str = f"{cand_val:.4f}" if cand_val is not None else "N/A"
        
        delta_str = ""
        delta_class = ""
        if base_val is not None and cand_val is not None:
            delta = cand_val - base_val
            if delta > 0:
                delta_str = f"+{delta:.4f}"
                delta_class = "delta-plus"
            elif delta < 0:
                delta_str = f"{delta:.4f}"
                delta_class = "delta-minus"
            else:
                delta_str = "0.0000"
                delta_class = "delta-zero"
        else:
            delta_str = "N/A"
            delta_class = "delta-zero"
            
        summary_table_html += f"""
        <tr>
            <td><strong>{m_name}</strong></td>
            <td>{base_str}</td>
            <td>{cand_str}</td>
            <td class="{delta_class}">{delta_str}</td>
        </tr>
        """

    # Extract case results & dataset
    base_cases = base_data.get("eval_case_results", [])
    cand_cases = cand_data.get("eval_case_results", [])
    
    base_eval_cases = []
    if base_ds_list:
        base_eval_cases = base_ds_list[0].get("eval_cases", [])
    cand_eval_cases = []
    if cand_ds_list:
        cand_eval_cases = cand_ds_list[0].get("eval_cases", [])

    cases_html = ""
    num_cases = max(len(base_cases), len(cand_cases), len(base_eval_cases), len(cand_eval_cases))
    
    for i in range(num_cases):
        prompt = ""
        base_resp = ""
        cand_resp = ""
        
        if i < len(base_eval_cases):
            prompt = base_eval_cases[i].get("prompt", "")
            resps = base_eval_cases[i].get("responses", [])
            if resps:
                base_resp = resps[0]
        if i < len(cand_eval_cases):
            resps = cand_eval_cases[i].get("responses", [])
            if resps:
                cand_resp = resps[0]

        base_metrics = {}
        if i < len(base_cases):
            c_res = base_cases[i].get("response_candidate_results", [])
            if c_res:
                base_metrics = c_res[0].get("metric_results", {})
                
        cand_metrics = {}
        if i < len(cand_cases):
            c_res = cand_cases[i].get("response_candidate_results", [])
            if c_res:
                cand_metrics = c_res[0].get("metric_results", {})

        all_metrics_keys = set(base_metrics.keys()) | set(cand_metrics.keys())
        metrics_comparison_html = ""
        has_score_diff = False
        
        for m_name in sorted(all_metrics_keys):
            base_m = base_metrics.get(m_name, {})
            cand_m = cand_metrics.get(m_name, {})
            
            base_score = base_m.get("score")
            cand_score = cand_m.get("score")
            
            base_exp = base_m.get("explanation", "No explanation available.")
            cand_exp = cand_m.get("explanation", "No explanation available.")
            
            base_score_str = f"{base_score}" if base_score is not None else "N/A"
            cand_score_str = f"{cand_score}" if cand_score is not None else "N/A"
            
            score_delta_html = ""
            if base_score is not None and cand_score is not None:
                diff_score = cand_score - base_score
                if diff_score > 0:
                    score_delta_html = f'<span class="badge badge-plus">+{diff_score}</span>'
                    has_score_diff = True
                elif diff_score < 0:
                    score_delta_html = f'<span class="badge badge-minus">{diff_score}</span>'
                    has_score_diff = True
                else:
                    score_delta_html = f'<span class="badge badge-equal">0</span>'
            
            metrics_comparison_html += f"""
            <div class="metric-block">
                <div class="metric-header">
                    <span class="metric-title">{m_name}</span>
                    <span class="score-comparison">
                        <span class="score-val base-score">{base_score_str}</span> 
                        ➔ 
                        <span class="score-val cand-score">{cand_score_str}</span>
                        {score_delta_html}
                    </span>
                </div>
                <div class="side-by-side-explanations">
                    <div class="explanation-column">
                        <div class="column-title">{base_meta} Explanation</div>
                        <div class="markdown-content">{base_exp}</div>
                    </div>
                    <div class="explanation-column">
                        <div class="column-title">{cand_meta} Explanation</div>
                        <div class="markdown-content">{cand_exp}</div>
                    </div>
                </div>
            </div>
            """

        border_class = "case-card diff-highlight" if has_score_diff else "case-card"
        diff_tag_html = '<div class="diff-tag">Score Changed</div>' if has_score_diff else ''

        cases_html += f"""
        <div class="{border_class}">
            {diff_tag_html}
            <div class="case-header">
                <h3>Case #{i + 1}</h3>
            </div>
            <div class="prompt-section">
                <strong>Prompt:</strong>
                <div class="prompt-text">{prompt}</div>
            </div>
            
            <div class="responses-comparison">
                <div class="response-column">
                    <div class="column-title">{base_meta} Response</div>
                    <div class="response-text">{base_resp}</div>
                </div>
                <div class="response-column">
                    <div class="column-title">{cand_meta} Response</div>
                    <div class="response-text">{cand_resp}</div>
                </div>
            </div>

            <div class="metrics-section">
                <h4>Metric Scores & Explanations</h4>
                {metrics_comparison_html}
            </div>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>A/B Comparison Report</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/dompurify/dist/purify.min.js"></script>
    <style>
        body {{
            font-family: 'Inter', -apple-system, sans-serif;
            margin: 0;
            padding: 2em;
            background-color: #0f172a;
            color: #e2e8f0;
        }}
        .container {{
            max-width: 1300px;
            margin: 0 auto;
        }}
        h1 {{
            color: #f8fafc;
            border-bottom: 2px solid #3b82f6;
            padding-bottom: 12px;
            margin-bottom: 24px;
            font-size: 2.2em;
        }}
        h2 {{
            color: #f8fafc;
            margin-top: 32px;
            border-bottom: 1px solid #334155;
            padding-bottom: 8px;
        }}
        h3 {{
            margin: 0;
            color: #60a5fa;
        }}
        h4 {{
            margin: 16px 0 8px 0;
            color: #94a3b8;
            border-bottom: 1px solid #1e293b;
            padding-bottom: 4px;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 0.5px;
        }}
        
        /* Summary Table */
        .summary-card {{
            background: #1e293b;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            margin-bottom: 32px;
            border: 1px solid #334155;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-top: 16px;
        }}
        th, td {{
            padding: 14px;
            text-align: left;
            border-bottom: 1px solid #334155;
        }}
        th {{
            background-color: #0f172a;
            color: #94a3b8;
            font-weight: 600;
        }}
        
        .delta-plus {{
            color: #10b981;
            font-weight: bold;
        }}
        .delta-minus {{
            color: #ef4444;
            font-weight: bold;
        }}
        .delta-zero {{
            color: #64748b;
        }}

        /* Case Cards */
        .case-card {{
            background: #1e293b;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 28px;
            border: 1px solid #334155;
            position: relative;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        .diff-highlight {{
            border: 1px solid #f59e0b;
            box-shadow: 0 0 12px rgba(245, 158, 11, 0.15);
        }}
        .diff-tag {{
            position: absolute;
            top: 16px;
            right: 16px;
            background: #d97706;
            color: #0f172a;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.75em;
            font-weight: 700;
            text-transform: uppercase;
        }}
        
        .prompt-section {{
            background: #0f172a;
            padding: 16px;
            border-radius: 8px;
            margin: 16px 0;
            border-left: 4px solid #3b82f6;
        }}
        .prompt-text {{
            margin-top: 6px;
            color: #f1f5f9;
        }}
        
        /* Side by Side Columns */
        .responses-comparison, .side-by-side-explanations {{
            display: flex;
            gap: 16px;
            margin-top: 16px;
        }}
        .response-column, .explanation-column {{
            flex: 1;
            background: #0f172a;
            padding: 16px;
            border-radius: 8px;
            border: 1px solid #334155;
            min-width: 0; /* Prevents overflow */
        }}
        .column-title {{
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #3b82f6;
            font-weight: bold;
            margin-bottom: 8px;
            border-bottom: 1px solid #1e293b;
            padding-bottom: 4px;
        }}
        .response-text {{
            white-space: pre-wrap;
            color: #cbd5e1;
            font-size: 0.95em;
            line-height: 1.5;
        }}
        .markdown-content {{
            font-size: 0.9em;
            line-height: 1.5;
            color: #94a3b8;
        }}
        .markdown-content p {{
            margin-top: 0;
        }}
        
        /* Metric Blocks */
        .metric-block {{
            background: #1e293b;
            border-radius: 8px;
            padding: 12px 16px;
            margin-top: 12px;
            border: 1px solid #334155;
        }}
        .metric-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}
        .metric-title {{
            font-weight: bold;
            color: #f1f5f9;
            font-size: 0.95em;
        }}
        .score-comparison {{
            font-size: 0.9em;
            color: #94a3b8;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .score-val {{
            font-weight: bold;
            font-size: 1.1em;
        }}
        .base-score {{
            color: #94a3b8;
        }}
        .cand-score {{
            color: #60a5fa;
        }}
        
        /* Badges */
        .badge {{
            display: inline-block;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            margin-left: 4px;
        }}
        .badge-plus {{
            background-color: #064e3b;
            color: #34d399;
        }}
        .badge-minus {{
            background-color: #7f1d1d;
            color: #f87171;
        }}
        .badge-equal {{
            background-color: #334155;
            color: #94a3b8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>A/B Model Comparison Report</h1>
        
        <div class="summary-card">
            <h3>Summary Metrics Comparison</h3>
            <table>
                <thead>
                    <tr>
                        <th>Metric Name</th>
                        <th>{base_meta} (Baseline)</th>
                        <th>{cand_meta} (Candidate)</th>
                        <th>Delta</th>
                    </tr>
                </thead>
                <tbody>
                    {summary_table_html}
                </tbody>
            </table>
        </div>

        <h2>Detailed Case-by-Case Diff</h2>
        {cases_html}
    </div>

    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            // Render markdown inside explanations
            document.querySelectorAll(".markdown-content").forEach(function(el) {{
                var rawMarkdown = el.textContent;
                var cleanHtml = DOMPurify.sanitize(marked.parse(rawMarkdown));
                el.innerHTML = cleanHtml;
            }});
        }});
    </script>
</body>
</html>
"""
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Successfully generated visual HTML report: {html_path}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 generate_compare_html.py <baseline_json_file> <candidate_json_file> <output_html_file>")
        sys.exit(1)
    generate_html(sys.argv[1], sys.argv[2], sys.argv[3])
