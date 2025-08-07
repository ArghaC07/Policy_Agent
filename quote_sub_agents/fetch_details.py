import os
import pymysql  
from google.adk.agents import Agent

# Tool definition: query_car_database
def query_car_database(vin: str) -> dict:
    """Fetches car details using VIN from RDS MySQL/Postgres DB."""
    try:
        connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor,
        )

        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT make, model, year, value, accident_history FROM cars WHERE vin = %s"
                cursor.execute(sql, (vin,))
                result = cursor.fetchone()
                if result:
                    result["car_age"] = 2025 - result["year"]
                    return result
                else:
                    return {"error": "No record found for VIN."}
    except Exception as e:
        return {"error": str(e)}


# Agent definition: fetch_details_agent
fetch_details_agent = Agent(
    name="quote_sub_agents",
    model="gemini-2.0-flash",
    description="Fetches car details from an RDS database using VIN or car number.",
    instruction="""
You are a data-retrieval expert for car insurance. 
Use the `query_car_database` tool to retrieve car details from the database based on VIN or vehicle number.
Return a structured dictionary containing:
- make
- model
- year
- value
- accident_history
- car_age

if you get all the values then please delegate the task to 
'coverage_agent' sub agent.
""",
    tools=[query_car_database]
)
