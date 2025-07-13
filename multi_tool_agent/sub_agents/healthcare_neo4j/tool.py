import pandas as pd
from neo4j import GraphDatabase

from config import settings


class Neo4jHealthcareTool:
    """
    A tool for connecting to and querying a Neo4j database with healthcare data.
    """

    def __init__(self, uri, user, password):
        """
        Initializes the tool and verifies the database connection.
        """
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.driver.verify_connectivity()
            print("✅ Successfully connected to Neo4j.")
        except Exception as e:
            print(f"🔥 Failed to connect to Neo4j: {e}")
            self.driver = None

    def run_query(self, query: str):
        """
        Runs a Cypher query against the database and returns the result as a pandas DataFrame.
        """
        if not self.driver:
            return "Database connection is not available."
        if not query or query.strip().upper().startswith("ERROR"):
            return f"Invalid or errored query provided: {query}"

        try:
            with self.driver.session() as session:
                result = session.run(query)
                # The .data() method extracts the records as a list of dictionaries
                df = pd.DataFrame([r.data() for r in result])
                return df
        except Exception as e:
            return f"An error occurred while running the query: {e}"

    def close(self):
        """
        Closes the database connection.
        """
        if self.driver:
            self.driver.close()
            print("🔌 Neo4j connection closed.")


def get_llm_prompt():
    """
    Returns the full, structured prompt for the LLM.
    """
    return """
        You are an expert Cypher query generator for a Neo4j database. Your sole purpose is to translate a user's natural language question into a precise, efficient, and secure read-only Cypher query based on the provided graph schema.

        ### 1. Graph Schema
        Here is the schema of the healthcare database you will be querying. You MUST adhere to this schema strictly.

        **Node Labels and Properties:**
        * `Manufacturer`: `name` (string)
        * `Drug`: `name` (string, always in UPPERCASE), `description` (string)
        * `Patient`: `gender` (string), `age` (integer), `ageUnit` (string)
        * `InsurancePlan`: `name` (string), `state` (string), `planType` (string)
        * `Reaction`: `description` (string)

        **Relationships:**
        * `(:Manufacturer)-[:MANUFACTURES]->(:Drug)`
        * `(:Patient)-[:HAS_INSURANCE]->(:InsurancePlan)`
        * `(:Patient)-[:IS_PRIMARY_SUSPECT]->(:Drug)`
        * `(:Patient)-[:HAS_REACTION]->(:Reaction)`

        ### 2. Rules and Constraints
        * **Read-Only:** You MUST NOT generate queries that create, update, or delete data (e.g., `CREATE`, `SET`, `DELETE`, `MERGE`).
        * **Schema Adherence:** ONLY use the node labels, properties, and relationship types and directions defined in the schema.
        * **Case Sensitivity:** `Drug.name` is always stored in UPPERCASE. Your queries must reflect this.
        * **Efficiency:** Return only the relevant property (e.g., `m.name`), not the entire node.
        * **Output Format:** Your output MUST be the raw Cypher query and nothing else.
        * **Error Handling:** If a question cannot be answered, return a single line starting with `ERROR:` and a brief explanation.

        ### 3. Examples (Question to Cypher)

        **Question:** "Which manufacturers are connected to drugs which contain TRAMADOL in its name?"
        **Cypher Query:**
        ```cypher
        MATCH (m:Manufacturer)-[:MANUFACTURES]->(d:Drug)
        WHERE d.name CONTAINS 'TRAMADOL'
        RETURN DISTINCT m.name AS manufacturer
        ```

        **Question:** "How many patients experienced 'Dizziness'?"
        **Cypher Query:**
        ```cypher
        MATCH (p:Patient)-[:HAS_REACTION]->(r:Reaction)
        WHERE r.description = 'Dizziness'
        RETURN count(p) AS numberOfPatients
        ```

        ### Translate the following user question into a Cypher query.
        """


def healthcare_tool(cypher_query: str) -> str:
    """
    Executes a Cypher query against the Neo4j healthcare database.

    Args:
        cypher_query (str): The Cypher query to execute.

    Returns:
        dict: A dictionary containing the status and results or error message.
    """
    NEO4J_URI = settings.neo4j_uri
    NEO4J_USERNAME = settings.neo4j_username
    NEO4J_PASSWORD = settings.neo4j_password
    AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

    driver = GraphDatabase.driver(NEO4J_URI, auth=AUTH)
    driver.verify_connectivity()
    print("   Connected to Neo4j!")
    print(f"   Executing Cypher query: {cypher_query}")

    with driver.session() as session:
        results = session.run(cypher_query).data()
        print(results)
    print("   Query executed successfully!")
    driver.close()
    return str(results) if results else "No results found."

"""
def healthcare_tool(cypher_query: str):
    
    Main function to run the interactive query tool.
    ""
    print("--- Neo4j Natural Language Query Tool ---")

    # Get credentials securely from environment variables or user input
    NEO4J_URI = settings.neo4j_uri
    NEO4J_USERNAME = settings.neo4j_username
    NEO4J_PASSWORD = settings.neo4j_password

    # Initialize the Neo4j tool
    tool = Neo4jHealthcareTool(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)
    if not tool.driver:
        return "Connection Failed"  # Exit if connection failed

    try:
        print(f"🔍 Generated Cypher:\n{cypher_query}")

        if cypher_query.startswith("ERROR:"):
            print(f"❗️ {cypher_query}")
            return f"Cypher query is wrong❗️ {cypher_query}"

        print("\n2. ⚡️ Executing query against the database...")
        results = tool.run_query(cypher_query)

        print("\n3. ✅ Results:")
        if isinstance(results, pd.DataFrame):
            if results.empty:
                print("Query returned no results.")
            else:
                print(results.to_string())
        else:
            print(results)  # Print error message if not a DataFrame
    except Exception as e:
        print(f"🔥 An error occurred: {e}")

    finally:
        tool.close()
        print("\n--- Tool session ended. ---")
    """
