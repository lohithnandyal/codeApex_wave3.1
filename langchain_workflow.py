"""
Intelligence Engine — LangChain + Groq LLM

Provides three analysis functions that take a diarized meeting transcript
and return structured intelligence:
    1. Executive Summary
    2. Action Items (JSON)
    3. Risk Analysis

Usage:
    from langchain_workflow import get_executive_summary, get_action_items, get_risk_analysis
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# ── LLM setup ────────────────────────────────────────────────────────────────

_llm = ChatGroq(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
)

# ── Prompt templates ─────────────────────────────────────────────────────────

_SUMMARY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a senior executive assistant. Given a meeting transcript with "
            "speaker labels, produce a concise executive summary (3-5 paragraphs) "
            "covering the key topics discussed, decisions made, and overall outcome.",
        ),
        ("human", "Here is the meeting transcript:\n\n{transcript}"),
    ]
)

_ACTION_ITEMS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a project management assistant. Analyze the meeting transcript "
            "and extract every concrete action item. For each item return a JSON object "
            "with these keys:\n"
            '  - "task": description of the task\n'
            '  - "assignee": the speaker label responsible (e.g. Speaker A)\n'
            '  - "deadline": any mentioned deadline, or "Not specified"\n'
            "Return a JSON array of these objects. Output ONLY valid JSON, no markdown fences.",
        ),
        ("human", "Here is the meeting transcript:\n\n{transcript}"),
    ]
)

_RISK_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a risk analyst. Review the meeting transcript and identify:\n"
            "  • Unresolved questions\n"
            "  • Blockers or dependencies\n"
            "  • Disagreements between speakers\n"
            "  • Potential risks or concerns raised\n"
            "Present your findings as a structured markdown list with clear categories.",
        ),
        ("human", "Here is the meeting transcript:\n\n{transcript}"),
    ]
)

# ── Public API ───────────────────────────────────────────────────────────────


def get_executive_summary(transcript: str) -> str:
    """Return a concise executive summary of the meeting."""
    chain = _SUMMARY_PROMPT | _llm
    response = chain.invoke({"transcript": transcript})
    return response.content


def get_action_items(transcript: str) -> str:
    """Return action items as a JSON string."""
    chain = _ACTION_ITEMS_PROMPT | _llm
    response = chain.invoke({"transcript": transcript})
    return response.content


def get_risk_analysis(transcript: str) -> str:
    """Return a risk analysis in markdown format."""
    chain = _RISK_ANALYSIS_PROMPT | _llm
    response = chain.invoke({"transcript": transcript})
    return response.content


# ── CLI helper ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sample = (
        "Speaker A: Let's kick off. The deadline for the MVP is March 20.\n"
        "Speaker B: I'm blocked on the API credentials. Can you get those today?\n"
        "Speaker A: I'll try, but no promises. Also, we haven't decided on the DB yet.\n"
        "Speaker B: True, that's a risk. Let's finalize by Wednesday.\n"
    )
    print("=== Executive Summary ===")
    print(get_executive_summary(sample))
    print("\n=== Action Items ===")
    print(get_action_items(sample))
    print("\n=== Risk Analysis ===")
    print(get_risk_analysis(sample))
