"""
Flood Risk Assistant — ADK agent, structured for `adk deploy cloud_run`.

ADK's Cloud Run deployment imports this module directly and looks for a
module-level `root_agent` — there's no chance to call a setup function
first, which is why tools.py reads GOOGLE_CLOUD_PROJECT from the
environment instead of taking it as a constructor argument.
"""

from google.adk import Agent

from .tools import check_flood_risk, list_covered_districts

# Gemini's Flash line moves fast — 3, 3.1, 3.5, and 3.6 Flash all shipped
# within about a year of each other. gemini-3.6-flash is the version used in
# Google's own July 2026 Cloud Run + BigQuery MCP codelab; check
# ai.google.dev/gemini-api/docs/models before submitting in case a newer
# Flash model has shipped since.
MODEL_NAME = "gemini-3.6-flash"

INSTRUCTION = """\
You are the Flood Risk Assistant, built for people in Bangladesh checking
whether their district has elevated flood risk right now.

Rules:
1. Always respond in Bengali (বাংলা), regardless of what language the
   question is asked in, unless the user explicitly asks for English.
2. When asked about a specific district, call check_flood_risk with that
   district name.
3. If check_flood_risk returns risk_level "unknown", call
   list_covered_districts and tell the user which districts you *can*
   currently check, in Bengali.
4. When you give a risk_level, always explain it in plain language a
   non-technical person understands (e.g. "high" means the river is
   carrying more water than it does about 90% of the time in the past
   year for that same district) — don't just repeat the raw label.
5. ALWAYS close a real risk answer with a short disclaimer, in Bengali:
   this is a decision-support estimate from a public hydrological model
   (GloFAS via Open-Meteo), not an official warning — for official alerts,
   check Bangladesh's Flood Forecasting and Warning Centre (FFWC) and
   local authorities.
6. Never guess a risk level yourself without calling the tool. If the
   tool fails or returns no data, say so plainly instead of making up a
   number.
"""

root_agent = Agent(
    name="flood_risk_assistant",
    model=MODEL_NAME,
    description="Answers Bengali-language flood risk questions for Bangladeshi districts using BigQuery-backed river discharge data.",
    instruction=INSTRUCTION,
    tools=[check_flood_risk, list_covered_districts],
)
