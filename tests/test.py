from neo4j import GraphDatabase

NEO4J_URI = "bolt://44.200.67.104"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "combustion-majorities-pine"
NEO4J_DATABASE = "neo4j"


def my_code():
    AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

    driver = GraphDatabase.driver(NEO4J_URI, auth=AUTH)
    driver.verify_connectivity()
    print("   Connected to Neo4j!")

    with driver.session() as session:
        query_list = [
            "MATCH (m:Manufacturer)-[:MANUFACTURES]->(d:Drug) WHERE d.name CONTAINS 'TRAMADOL' RETURN DISTINCT m.name AS manufacturer",
            "MATCH (d:diseases)-[:has_symptoms]->(s:symptoms) where d.name ='Diabetes' RETURN s.name",
            "MATCH (s:symptoms)-[:has_symptoms]-(d:diseases) where s.name ='Fever' RETURN d.name",
            "MATCH (n) RETURN n LIMIT 5",
            "MATCH (d:diseases{name: 'Cancer'})-[:has_symptoms]->(s:symptoms {name: 'Coughing'})",
            "MATCH (n) RETURN COUNT(n) AS count LIMIT 5",
            "MATCH (d:Disease {name: 'Cancer'})-[:HAS_SYMPTOMS]->(s:Symptom {name: 'Coughing'}) RETURN d, s",
            'MATCH (a:AgeGroup {ageGroup: "18-25"})<-[:FALLS_UNDER]-(c:Case) MATCH (c)-[:HAS_REACTION]->(r:Reaction) MATCH (c)-[:IS_PRIMARY_SUSPECT]->(d:Drug) RETURN d.name, d.primarySubstabce',
            "MATCH (c:Case)-[:HAS_REACTION]->(r:Reaction) RETURN r.description, count(c) ORDER BY count(c) DESC LIMIT 5;",
        ]

        results = session.run(query_list[1]).data()
        print(results)


def test_generic_query():
    """https://github.com/tomasonjo/blogs/blob/master/llm/generic_cypher_gpt4.ipynb"""
    from neo4j.exceptions import CypherSyntaxError
    from openai import OpenAI

    node_properties_query = """
    CALL apoc.meta.data()
    YIELD label, other, elementType, type, property
    WHERE NOT type = "RELATIONSHIP" AND elementType = "node"
    WITH label AS nodeLabels, collect(property) AS properties
    RETURN {labels: nodeLabels, properties: properties} AS output

    """

    rel_properties_query = """
    CALL apoc.meta.data()
    YIELD label, other, elementType, type, property
    WHERE NOT type = "RELATIONSHIP" AND elementType = "relationship"
    WITH label AS nodeLabels, collect(property) AS properties
    RETURN {type: nodeLabels, properties: properties} AS output
    """

    rel_query = """
    CALL apoc.meta.data()
    YIELD label, other, elementType, type, property
    WHERE type = "RELATIONSHIP" AND elementType = "node"
    RETURN {source: label, relationship: property, target: other} AS output
    """

    def schema_text(node_props, rel_props, rels):
        return f"""
    This is the schema representation of the Neo4j database.
    Node properties are the following:
    {node_props}
    Relationship properties are the following:
    {rel_props}
    Relationship point from source to target nodes
    {rels}
    Make sure to respect relationship types and directions
    """

    class Neo4jGPTQuery:
        def __init__(self, url, user, password, gemini_api_key):
            self.driver = GraphDatabase.driver(url, auth=(user, password))
            self.client = OpenAI(
                api_key="AIzaSyDHaughVboCMlu1m3TzIhHpH_5nkav5SN4"
                if gemini_api_key is None
                else gemini_api_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            )
            # construct schema
            self.schema = self.generate_schema()

        def generate_schema(self):
            node_props = self.query_database(node_properties_query)
            rel_props = self.query_database(rel_properties_query)
            rels = self.query_database(rel_query)
            return schema_text(node_props, rel_props, rels)

        def refresh_schema(self):
            self.schema = self.generate_schema()

        def get_system_message(self):
            return f"""
            Task: Generate Cypher queries to query a Neo4j graph database based on the provided schema definition.
            Instructions:
            Use only the provided relationship types and properties.
            Do not use any other relationship types or properties that are not provided.
            If you cannot generate a Cypher statement based on the provided schema, explain the reason to the user.
            Schema:
            {self.schema}

            Note: Do not include any explanations or apologies in your responses.
            """

        def query_database(self, neo4j_query, params={}):
            with self.driver.session() as session:
                result = session.run(neo4j_query, params)
                output = [r.values() for r in result]
                output.insert(0, result.keys())
                return output

        def construct_cypher(self, question, history=None):
            messages = [
                {"role": "system", "content": self.get_system_message()},
                {"role": "user", "content": question},
            ]
            if history:
                messages.extend(history)

            completions = self.client.chat.completions.create(
                model="gemini-2.0-flash",  # Use a Gemini model
                temperature=0.0,
                max_tokens=1000,
                messages=messages,
            )
            return completions.choices[0].message.content

        def run(self, question, history=None, retry=True):
            cypher = self.construct_cypher(question, history)
            print(cypher)
            try:
                return self.query_database(cypher)
            except CypherSyntaxError as e:
                if not retry:
                    return "Invalid Cypher syntax"
                print("Retrying")
                return self.run(
                    question,
                    [
                        {"role": "assistant", "content": cypher},
                        {
                            "role": "user",
                            "content": f"""This query returns an error: {str(e)} 
                            Give me a improved query that works without any explanations or apologies""",
                        },
                    ],
                    retry=False,
                )

    hc_db = Neo4jGPTQuery(
        url=NEO4J_URI,
        user=NEO4J_USERNAME,
        password=NEO4J_PASSWORD,
        gemini_api_key=None,
    )

    print(
        hc_db.run("""
    What are the top 5 side effects reported?
    """)
    )

    print(
        hc_db.run("""
    Which manufacturers are connected to drugs which contain TRAMADOL in its name?
    """)
    )


def langchain_query():
    """https://github.com/tomasonjo/blogs/blob/master/llm/langchain_neo4j_tips.ipynb"""
    from langchain.chains import GraphCypherQAChain
    from langchain_community.graphs import Neo4jGraph
    from langchain_google_genai import ChatGoogleGenerativeAI

    # Set your Gemini API key (from Google AI Studio or Google Cloud)
    graph = Neo4jGraph(
        url=NEO4J_URI,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD,
    )

    # Initialize Gemini chat model (e.g., Gemini 1.5 Pro)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",  # or another Gemini model
        temperature=0,
        google_api_key="AIzaSyDHaughVboCMlu1m3TzIhHpH_5nkav5SN4",
    )

    chain = GraphCypherQAChain.from_llm(
        llm,
        graph=graph,
        verbose=True,
        allow_dangerous_requests=True,  # Set to True if you want to allow dangerous requests
    )
    chain.invoke(
        {
            "query": """
    Which manufacturers are connected to drugs which contain TRAMADOL in its name?
    """
        }
    )
    chain.invoke(
        {
            "query": """What are the top 5 side effects reported?
    """
        }
    )


if __name__ == "__main__":
    # my_code()
    # test_generic_query()
    langchain_query()
