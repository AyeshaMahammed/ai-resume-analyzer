# app.py
import gradio as gr
import os
import json
import asyncio
import csv
from typing import List

from file_utils import load_text_from_file
from summarizer import summarize_resume


# -----------------------------
# PIE CHART
# -----------------------------
def pie_chart(score: int):
    score = max(0, min(100, int(score)))
    return f"""
    <div style='display:flex;justify-content:center;margin-top:10px;'>
      <div style="
        width:160px;height:160px;border-radius:50%;
        background:conic-gradient(#2ecc71 0% {score}%, #e74c3c {score}% 100%);
        display:flex;align-items:center;justify-content:center;
        box-shadow:0 4px 12px rgba(0,0,0,0.15);
        font-family:Inter,system-ui;
      ">
        <div style='text-align:center;'>
          <div style='font-size:24px;font-weight:700;color:#0f172a;'>{score}%</div>
          <div style='font-size:12px;color:#555;'>Fit Score</div>
        </div>
      </div>
    </div>
    """


# -----------------------------
# MODEL SELECTION
# -----------------------------
def get_model_backend(choice: str):
    choice = choice.lower()

    if choice.startswith("openai"):
        return "openai", "gpt-4o-mini"

    return "ollama", "llama3.2:1b"


# -----------------------------
# SINGLE RESUME PROCESSOR
# -----------------------------
def process_single_resume(file, job_title, jd_text, model_choice):
    if not file:
        return "⚠️ Upload a resume.", ""

    resume_text, _ = load_text_from_file(file)
    provider, model_name = get_model_backend(model_choice)

    result = summarize_resume(
        resume_text=resume_text,
        job_title=job_title,
        jd_text=jd_text,
        provider=provider,
        model_name=model_name,
    )

    fit = result.get("fit_score", 0)
    summary = result.get("summary", "")
    skills = result.get("top_skills", [])
    gaps = result.get("top_gaps", [])
    rec = result.get("recommendation", "")

    md = f"""
## 🧑‍💻 Recruiter Summary
{summary}

### ⭐ Top Skills
- {", ".join(skills) if skills else "Not listed"}

### ⚠️ Top Gaps
- {", ".join(gaps) if gaps else "None"}

### ✅ Recommendation
{rec}
"""

    return md, pie_chart(fit)


# -----------------------------
# ASYNC BULK PROCESSING
# -----------------------------
async def analyze_one_resume(file, job_title, jd_text, provider, model_name):
    resume_text, _ = load_text_from_file(file)
    result = summarize_resume(
        resume_text=resume_text,
        job_title=job_title,
        jd_text=jd_text,
        provider=provider,
        model_name=model_name,
    )
    return file, result


async def process_bulk_async(files, job_title, jd_text, provider, model_name):
    tasks = [
        analyze_one_resume(f, job_title, jd_text, provider, model_name)
        for f in files
    ]
    results = await asyncio.gather(*tasks)
    return results


def process_bulk(files, job_title, jd_text, model_choice):
    if not files:
        return gr.DataFrame(value=[]), None

    provider, model_name = get_model_backend(model_choice)

    # Run async LLM calls
    results = asyncio.run(process_bulk_async(files, job_title, jd_text, provider, model_name))

    table_rows = []
    for file, result in results:
        file_name = os.path.basename(file)
        row = {
            "file_name": file_name,
            "fit_score": result.get("fit_score", 0),
            "summary": result.get("summary", ""),
            "top_skills": ", ".join(result.get("top_skills", [])),
            "top_gaps": ", ".join(result.get("top_gaps", [])),
            "recommendation": result.get("recommendation", "")
        }
        table_rows.append(row)

    # Sort descending by fit_score
    table_rows = sorted(table_rows, key=lambda r: r["fit_score"], reverse=True)

    return gr.DataFrame(value=table_rows), table_rows


# -----------------------------
# CSV EXPORT
# -----------------------------
def export_csv(table_rows: List[dict]):
    file_path = "bulk_results.csv"
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "file_name",
                "fit_score",
                "summary",
                "top_skills",
                "top_gaps",
                "recommendation",
            ],
        )
        writer.writeheader()
        writer.writerows(table_rows)
    return file_path


# -----------------------------
# UI
# -----------------------------
with gr.Blocks(title="AI Resume Analyzer — Single & Bulk") as demo:

    gr.Markdown("# 🧠 AI Resume Analyzer (GPT-4o-mini / Ollama)")

    model_choice = gr.Dropdown(
        ["OpenAI GPT-4o-mini", "Ollama (llama3.2:1b)"],
        value="OpenAI GPT-4o-mini",
        label="Choose Model"
    )

    # -------------------------
    # TAB 1 — SINGLE
    # -------------------------
    with gr.Tab("Single Resume Analysis"):
        resume_file = gr.File(label="Upload Resume", type="filepath")
        job_title = gr.Textbox(label="Target Role")
        jd_text = gr.Textbox(label="Job Description", lines=10)

        btn_single = gr.Button("Analyze Resume 🚀")
        out_md = gr.Markdown()
        out_pie = gr.HTML()

        btn_single.click(
            process_single_resume,
            inputs=[resume_file, job_title, jd_text, model_choice],
            outputs=[out_md, out_pie],
        )

    # -------------------------
    # TAB 2 — BULK
    # -------------------------
    with gr.Tab("Bulk Resume Ranking"):
        bulk_files = gr.File(label="Upload Multiple Resumes", file_count="multiple", type="filepath")
        bulk_job_title = gr.Textbox(label="Target Role")
        bulk_jd_text = gr.Textbox(label="Job Description", lines=10)

        btn_bulk = gr.Button("Analyze All Resumes 🚀")
        table_output = gr.DataFrame()
        csv_download = gr.File(label="Download CSV")

        def bulk_action(files, job_title, jd):
            table, rows = process_bulk(files, job_title, jd, model_choice.value)
            if not rows:
                return table, None
            csv_path = export_csv(rows)
            return table, csv_path

        btn_bulk.click(
            bulk_action,
            inputs=[bulk_files, bulk_job_title, bulk_jd_text],
            outputs=[table_output, csv_download],
        )


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)

