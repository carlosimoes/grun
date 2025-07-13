from google.adk import Agent
from google.adk.agents import SequentialAgent

from . import prompt
from .tool import healthcare_tool
from config import settings

# TODO: https://github.com/Cicatriiz/healthcare-mcp-public
cypher_neo4j_agent = Agent(
    model=settings.agent_model,
    description="You are an expert Cypher query generator for a Neo4j database. Your sole purpose is to translate a user's natural language question into a precise, efficient, and secure read-only Cypher query based on the provided graph schema.",
    name="healthcare_neo4j_agent",
    instruction=prompt.CYPHER_NEO4J_PROMPT,
    output_key="chypher_query",
)

grunenthal_analyst_agent = Agent(
    model=settings.agent_model,
    description="A Grünenthal Heathcare Analyst that can accurately answer any question about questions about healthcare data of complex healthcare datasets, focusing on adverse drug events and medication errors reported in the United States.",
    name="healthcare_neo4j_agent",
    instruction=prompt.HEALTHCARE_NEO4J_PROMPT,
    output_key="chypher_query",
    tools=[healthcare_tool],
)


healthcare_neo4j_agent = SequentialAgent(
    name="healthcare_neo4j_agent",
    sub_agents=[
        cypher_neo4j_agent,
        grunenthal_analyst_agent,
    ],
    description="Executes a sequence of Heathcare investigation generating chypher query, executing it, and answering the user question about healthcare data of complex healthcare datasets.",
)
