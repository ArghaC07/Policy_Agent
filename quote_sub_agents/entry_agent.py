from datetime import datetime
from google.adk.agents import Agent

def calculate_premium(m_year: int, accident_history: str, brand: str) -> dict:   
    base_premium = 5000 
    premium_multiplier = 1.0
    try:
        current_year = datetime.now().year
        age = current_year - m_year
        
        # brand premium adjustment
        if brand.lower() in ["ferrari", "lamborghini", "bentley","mercedes-benz","audi", "bmw"]:
            premium_multiplier += 1.5 # luxury brands
        elif brand.lower() in ["toyota", "honda", "ford", "hyundai"]:
            premium_multiplier += 1.2 # common brands
        else:
            premium_multiplier += 1.0 # other brands

        # age adjustment
        if age < 5:
            premium_multiplier += 0.1 # new cars
        elif age < 10:
            premium_multiplier += 0.2 # moderately old cars
        else:
            premium_multiplier += 0.3 # old cars
        
        # premium calculation
        if accident_history.lower() == "yes":
            return {
                "message": "Please connect with our insurance agent for further assistance.",
            }
        else:
            premium = base_premium * premium_multiplier
            return {
                "status": "success",
                "car_model": brand,
                "car_manufacture_year": m_year,
                "accident_history_exist": accident_history,
                "premium": premium,
                "message": f"The estimated premium for your {brand} car for one year is ₹{premium}"
            }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error in premium calculation: {str(e)}"
        }

# --- Agent that uses the tool ---
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
    #sub_agents=[fetch_vehicle_details],
)
