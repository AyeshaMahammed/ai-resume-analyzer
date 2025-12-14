# ai-resume-analyzer
LLM-powered single + bulk resume analyzer with GPT-4o-mini / Ollama

# 🧠 AI Resume Fit Analyzer

Analyze single or bulk resumes against a Job Description using:
- OpenAI GPT-4o-mini (default)
- Ollama (optional local LLM)

## ✨ Features
- Single resume analysis (Fit Score, skills, gaps, summary)
- Bulk resume ranking (CSV export)
- Async parallel LLM evaluation (super fast)
- Safe: No API keys stored in code

---
If you're a recruiter, hiring manager, or TA team, here are the simple steps to use it immediately:
## 🔧 Setup

### 1. Clone the repo
```bash
git clone https://github.com/AyeshaMahammed/ai-resume-analyzer.git
cd ai-resume-analyzer
𝐒𝐭𝐞𝐩 𝟐: 𝗖𝗿𝗲𝗮𝘁𝗲 𝗮 𝘃𝗶𝗿𝘁𝘂𝗮𝗹 𝗲𝗻𝘃 (𝗸𝗲𝗲𝗽𝘀 𝗲𝘃𝗲𝗿𝘆𝘁𝗵𝗶𝗻𝗴 𝗶𝘀𝗼𝗹𝗮𝘁𝗲𝗱)
Windows:
python -m venv venv
venv\Scripts\activate
Mac/Linux:
python3 -m venv venv
source venv/bin/activate
𝐒𝐭𝐞𝐩 𝟑: 𝗜𝗻𝘀𝘁𝗮𝗹𝗹 𝗮𝗹𝗹 𝗱𝗲𝗽𝗲𝗻𝗱𝗲𝗻𝗰𝗶𝗲𝘀
pip install -r requirements.txt
𝐒𝐭𝐞𝐩 𝟒: 𝗔𝗱𝗱 𝘆𝗼𝘂𝗿 𝗢𝗽𝗲𝗻𝗔𝗜 𝗔𝗣𝗜 𝗸𝗲𝘆 (𝗼𝗻𝗹𝘆 𝗶𝗳 𝘂𝘀𝗶𝗻𝗴 GPT-4o-mini)
Create a file named .env and add:
OPENAI_API_KEY=your_key_here
Your key stays private.
𝐒𝐭𝐞𝐩 𝟓: (𝗢𝗽𝘁𝗶𝗼𝗻𝗮𝗹) 𝗨𝘀𝗲 𝗮 𝗹𝗼𝗰𝗮𝗹 𝗺𝗼𝗱𝗲𝗹 𝗶𝗻𝘀𝘁𝗲𝗮𝗱
Install Ollama: ollama.ai
Pull a model:
ollama pull llama3.2:1b
This lets everything run offline.
𝐒𝐭𝐞𝐩 𝟔: 𝗤𝘂𝗶𝗰𝗸 𝗮𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗲 𝗼𝘃𝗲𝗿𝘃𝗶𝗲𝘄
• Input Layer: PDF/TXT/CSV resumes
• Processing Layer: Extracts & cleans text
• AI Layer: GPT-4o-mini or local model
• Analysis Layer: Skills match, JD alignment, experience relevance
• Output Layer: JSON summaries or CSV
Runs locally, no database needed.
𝐒𝐭𝐞𝐩 𝟕: 𝗦𝘁𝗮𝗿𝘁 𝘁𝗵𝗲 𝗮𝗽𝗽 𝗮𝗻𝗱 𝗰𝗵𝗼𝗼𝘀𝗲 𝘁𝗵𝗲 𝗺𝗼𝗱𝗲 𝘆𝗼𝘂 𝘄𝗮𝗻𝘁
Once the app is up & running using python app.py, the user interface can be accessed using http://127.0.0.1:7860/ 
User sees two tabs:
• 𝗦𝗶𝗻𝗴𝗹𝗲 𝗥𝗲𝘀𝘂𝗺𝗲 Analysis
• 𝗕𝘂𝗹𝗸 𝗥𝗲𝘀𝘂𝗺𝗲 Analysis
Select the tab you want & upload your file(s).
𝐒𝐭𝐞𝐩 𝟖: 𝗩𝗶𝗲𝘄 𝗼𝘂𝘁𝗽𝘂𝘁 𝗿𝗲𝘀𝘂𝗹𝘁𝘀
Single-resume mode displays a detailed AI summary.
Bulk mode generates a CSV with candidate-wise scores & insights.

Note:
• Data Privacy - Resumes aren’t stored, no logs saved, offline mode available, ideal for hiring teams handling confidential profiles.

𝗪𝗵𝗮𝘁 𝘁𝗵𝗶𝘀 𝗣𝗢𝗖 𝗱𝗲𝗺𝗼𝗻𝘀𝘁𝗿𝗮𝘁𝗲𝘀
• Resume parsing + JD matching
• AI-based candidate scoring
• Async bulk processing
• Recruiter-friendly summaries

𝗪𝗵𝗼 𝗰𝗮𝗻 𝘂𝘀𝗲 𝗶𝘁
Recruiters
TA teams
Startups screening applicants
Job seekers optimizing their resume
𝗣𝗼𝘀𝘀𝗶𝗯𝗹𝗲 𝗻𝗲𝘅𝘁 𝗲𝗻𝗵𝗮𝗻𝗰𝗲𝗺𝗲𝗻𝘁𝘀
• Streamlit UI
• PDF candidate reports
• Skill heatmaps
• ATS score analysis
