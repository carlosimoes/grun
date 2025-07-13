from pydantic import BaseModel
import logging

class Settings(BaseModel):
    agent_name: str = "grunenthal_agent"
    agent_model: str = "gemini-2.0-flash"
    fda_api_url: str = "https://api.fda.gov/drug/event.json"
    logging_level: int = logging.INFO
    neo4j_uri: str = "bolt://44.200.67.104"
    neo4j_username: str = "neo4j"
    neo4j_password: str = "combustion-majorities-pine"

settings = Settings()