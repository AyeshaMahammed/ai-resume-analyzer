# summarize.py
import os
import json
from typing import Optional
import ollama

# -----------------------------
# OpenAI Client (lazy import)
# -----------------------------
def _call_openai(model_name: str, system_msg: str, user_msg: str) -> str:
    from openai import OpenAI
    client = OpenAI()

    response = client.chat.completions.create(
        model=model_name,
        temperature=0.1,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
    )

    return response.choices[0].message.content.strip()


# -----------------------------
# Ollama Caller
# -----------------------------
def _call_ollama(model_name: str, system_msg: str, user_msg: str) -> str:
    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
    )
    return response["message"]["content"].strip()


# -----------------------------
# MAIN LLM CALL
# -----------------------------
def summarize_resume(
    resume_text: str,
    job_title: Optional[str],
    jd_text: str,
    provider: str,
    model_name: str,
) -> dict:
    """
    LLM returns STRICT JSON:
    {
      "fit_score": 0-100,
      "summary": "...",
      "top_skills": [...],
      "top_gaps": [...],
      "recommendation": "..."
    }
    """

    system_msg = (
        "You are an expert recruiter. ALWAYS output a strict, valid JSON object. "
        "No commentary. No markdown. No extra text."
    )

    user_msg = f"""
Analyze the resume for the job role: "{job_title}"

JOB DESCRIPTION:
{jd_text}

RESUME:
{resume_text}

Return ONLY this JSON object:

{{
  "fit_score": <0-100>,
  "summary": "3-4 line recruiter-friendly summary",
  "top_skills": ["skill1", "skill2"],
  "top_gaps": ["gap1", "gap2"],
  "recommendation": "concise recommendation"
}}
"""

    # Choose backend
    if provider == "openai":
        raw = _call_openai(model_name, system_msg, user_msg)
    else:
        raw = _call_ollama(model_name, system_msg, user_msg)

    # Parse JSON strictly
    try:
        return json.loads(raw)
    except Exception:
        print("LLM returned non-JSON:", raw)
        return {
            "fit_score": 0,
            "summary": "Invalid JSON received from model.",
            "top_skills": [],
            "top_gaps": [],
            "recommendation": "Unable to evaluate."
        }

