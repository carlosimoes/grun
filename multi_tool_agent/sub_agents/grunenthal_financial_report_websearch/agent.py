from google.adk import Agent
from google.adk.tools import google_search

from . import prompt
from config import settings



grunenthal_financial_report_websearch_agent = Agent(
    model=settings.agent_model,
    description="A Grünenthal financial report expert that can accurately answer any question about Grünenthal’s financial or annual reports, providing clear explanations of key figures, trends, and disclosures.",
    name="grunenthal_financial_report_websearch_agent",
    instruction=prompt.GRUNENTAL_FINANCIAL_REPORT_WEBSEARCH_PROMPT,
    output_key="gru_finance_report",
    tools=[google_search],
)
