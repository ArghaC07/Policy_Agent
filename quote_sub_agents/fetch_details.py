import os
from google.cloud import bigquery
from google.adk.agents import Agent

# Tool: Query BigQuery table
def query_car_database(vin: str) -> dict:
    """Fetches car details using VIN from a BigQuery table."""
    try:
        client = bigquery.Client(project="absolute-accord-465308-g0")
        
        query = f"""
        SELECT *, 2025 - manufacture_year AS car_age
        FROM `absolute-accord-465308-g0.car_insurance.vehicle_data`
        WHERE VIN_no = @vin
        LIMIT 1
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("vin", "STRING", vin)
            ]
        )

        query_job = client.query(query, job_config=job_config)
        result = list(query_job.result())

        if not result:
            return {"error": "No record found for the provided VIN."}
        
        return dict(result[0])  # Convert Row object to dictionary

    except Exception as e:
        return {"error": str(e)}


# Agent definition: fetch_details_agent
fetch_details_agent = Agent(
    name="fetch_vehicle_details",
    model="gemini-2.0-flash",
    description="Fetches car details from an RDS database using VIN or car number.",
    instruction="""
You are a data-retrieval expert for car insurance. 
Use the `query_car_database` tool to retrieve car details from the database based on VIN or vehicle number.
Return the result in more structured format.
show the value to the user and ask if all the details
are correct.
If the user confirms, proceed with the next steps.
if you get all the values then please delegate the task to 
'coverage_agent' sub agent.
""",
    tools=[query_car_database]
)
