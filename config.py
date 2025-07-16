from pydantic import BaseModel
import logging


class Settings(BaseModel):
    agent_name: str = "grunenthal_agent"
    agent_model: str = "gemini-2.0-flash"
    fda_api_url: str = "https://api.fda.gov/drug/event.json"
    logging_level: int = logging.INFO
    neo4j_uri: str = "bolt://35.171.8.98"
    neo4j_username: str = "neo4j"
    neo4j_password: str = "amount-oar-cardboard"
    google_api: str = "AIzaSyDHaughVboCMlu1m3TzIhHpH_5nkav5SN4"
    vertexai_use: str = "FALSE"

settings = Settings()
