from datetime import datetime
from google.adk.agents import Agent
from Policy_Agent.quote_sub_agents.fetch_details import fetch_details_agent

quote_agent = Agent(
    name="quote_sub_agent",
    model="gemini-1.5-flash",
    description="Agent that calculates car insurance premium.",
    instruction="""
You are a quote request agent.
1. Ask the user to provide the vehicle or VIN number.
if the user provides the vehicle number then tell the user your reuest is being processed.
and delegate the task to the 'fetch_vehicle_details' agent
""",
    sub_agents=[fetch_details_agent],
)
