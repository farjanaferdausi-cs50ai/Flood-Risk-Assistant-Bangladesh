"""
Quick local test harness for the Flood Risk Assistant agent.

Prerequisites:
  - Phase 1 data already loaded into BigQuery (see ../data_ingestion/)
  - `gcloud auth application-default login`
  - GOOGLE_API_KEY (or Vertex AI credentials) set for Gemini access —
    see https://ai.google.dev/gemini-api/docs/api-key

Usage:
  python demo.py YOUR_GCP_PROJECT_ID
"""

import asyncio
import sys

from agent import build_agent
from google.adk.runners import InMemoryRunner

SAMPLE_QUESTIONS = [
    "সিরাজগঞ্জে বন্যার ঝুঁকি কেমন?",
    "ঢাকায় কি বন্যার আশঙ্কা আছে?",
    "তুমি কোন কোন জেলার তথ্য জানো?",
]


async def main(project_id: str) -> None:
    agent = build_agent(project_id)
    runner = InMemoryRunner(agent=agent, app_name="flood_risk_demo")

    print("Flood Risk Assistant — local demo\n" + "=" * 40)
    await runner.run_debug(SAMPLE_QUESTIONS)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python demo.py YOUR_GCP_PROJECT_ID")
    asyncio.run(main(sys.argv[1]))
