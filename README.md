#  Multi-Modal Meeting Assistant (CodeApex Wave 3.1)

> An AI-powered application that turns raw meeting recordings into actionable intelligence — transcripts with speaker labels, executive summaries, structured action items, risk analysis, and automated email follow-ups.

---

##  What It Does

Upload a recorded meeting file (`.mp3`, `.mp4`, `.wav`, etc.) via the clean Streamlit web interface and the system will:

1. **Transcribe** the audio with speaker diarization (who said what).
2. **Summarize** the meeting into a concise executive overview.
3. **Extract action items** as structured JSON (task, assignee, deadline).
4. **Analyze risks** — flagging unresolved questions, blockers, and disagreements.
5. **Send Automated Emails** — mapping participants from an Excel sheet to the generated action items and sending personalized HTML email follow-ups automatically.

---

## Architecture Overview

```
┌──────────────┐       ┌────────────────────┐       ┌──────────────────────┐
│  Audio/Video │──────▶│   transcriber.py   │──────▶│ langchain_workflow.py│
│  (.mp3/.mp4) │       │  (AssemblyAI SDK)  │       │  (LangChain + Groq)  │
└──────────────┘       └────────────────────┘       └──────────┬───────────┘
                               │                               │
                               ▼                               ▼
                      Diarized Transcript             3 Parallel LLM Chains
                      (Speaker A, B, …)              ┌─────────────────────┐
                                                     │ • Executive Summary │
                                                     │ • Action Items JSON │
                                                     │ • Risk Analysis     │
                                                     └──────────┬──────────┘
                                                                │
                                                                ▼
                                                     ┌─────────────────────┐
                                                     │   email_agent.py    │
                                                     │ (SMTP Data Mapping) │
                                                     └─────────────────────┘
```

### Module Breakdown

| Module | Role | Tech |
|---|---|---|
| `app.py` | Web UI & Pipeline Orchestration | Streamlit |
| `transcriber.py` | Speech-to-text + speaker diarization | AssemblyAI SDK |
| `langchain_workflow.py` | Meeting intelligence extraction | LangChain + Groq (Llama 3/4) |
| `email_agent.py` | Participant mapping and email automation | smtplib, pandas |
| `generate_mock_excel.py` | Utility to create sample participant data | pandas, openpyxl |

---

##  Quick Start

### 1. Clone & Set Up

```bash
# Clone the repository
git clone https://github.com/lohithnandyal/CodeApex_wave3.1.git
cd CodeApex_wave3.1

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create your `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` to include your API keys and email credentials:
```env
ASSEMBLYAI_API_KEY=your_assemblyai_key_here
GROQ_API_KEY=your_groq_key_here
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

| Key | Where to Get It |
|---|---|
| `ASSEMBLYAI_API_KEY` | [assemblyai.com/dashboard](https://www.assemblyai.com/dashboard) |
| `GROQ_API_KEY` | [console.groq.com/keys](https://console.groq.com/keys) |
| `EMAIL_ADDRESS` & `EMAIL_PASSWORD` | Use a Gmail App Password (2FA must be enabled) |

### 3. Generate Mock Data (Optional)

To test the email functionality, generate a sample `participants.xlsx` file:

```bash
python generate_mock_excel.py
```
*(Update the Excel file with your actual email addresses to receive the test emails!)*

### 4. Run the Application

Launch the Streamlit web app:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 📂 Project Structure

```
CodeApex_wave3.1/
├── app.py                   # Streamlit Frontend Web App
├── transcriber.py           # Speech-to-text + speaker diarization
├── langchain_workflow.py    # LangChain intelligence engine
├── email_agent.py           # Automated Email Follow-ups
├── generate_mock_excel.py   # Script to generate sample participant data
├── participants.xlsx        # Excel file mapping speakers to emails
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── .env                     # Actual credentials (gitignored)
└── README.md                # This file
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend UI** | **Streamlit** | Interactive user interface |
| **Transcription** | **AssemblyAI** | Industry-grade STT with speaker diarization |
| **LLM Inference** | **Groq** | Ultra-fast inference for meeting analysis |
| **Orchestration** | **LangChain** (LCEL) | Prompt management & LLM chaining |
| **Automation** | **SMTP / Pandas** | Data extraction and automated emailing |

---

## 🎯 Key Features Iteration (Wave 3.1)

This version introduces several key advancements:
1. **Full Web UI:** Replaced CLI-only execution with a rich, interactive Streamlit frontend.
2. **Automated Follow-ups:** Integrated an `email_agent` that automatically maps recognized speakers to email addresses using an Excel sheet and dispatches personalized action item summaries.
3. **Enhanced Robustness:** Better error handling across all API limits and parsing edges.

---

## 📝 License

Built for CodeApex Wave 3.1.
