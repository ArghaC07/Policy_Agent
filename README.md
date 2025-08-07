# Policy_Agent
This is a Policy Agentic AI 


The folder structure for this project we are planning below:

car_insurance_bot/
│
├── agents/
│   ├── quote_agent.py              # Central orchestrator agent
│   ├── fetch_details_agent.py      # Fetches car specs using VIN
│   ├── coverage_agent.py           # Recommends coverage based on car + user profile
│   └── quote_creation_agent.py     # Calculates the initial quote
│
├── tools/
│   ├── db_connector.py             # DB connection logic (to dummy RDS)
│   └── fetch_car_details.py        # Tool to query VIN data from DB
│
├── prompts/
│   ├── quote_agent_prompt.txt
│   ├── fetch_details_prompt.txt
│   ├── coverage_prompt.txt
│   └── quote_creation_prompt.txt
│
├── data/
│   └── dummy_car_data.sql          # Optional: to initialize dummy DB
│
├── .env                            # Database credentials, config for ADK
├── requirements.txt                # Dependencies (GCP ADK, Gemini, SQL libs)
├── agent.py                        # Imports and registers root_agent
├── README.md

🚗 Initial Quote Agent – Step-by-Step Flow
✅ Goal:
Collect vehicle and driver information ➝ Recommend a coverage plan ➝ Return an initial quote.

🔁 Step 1: User Input – Vehicle Number
Accept license plate number or VIN from user.

Confirm vehicle number via LLM (optional: “Got it. Let me fetch your vehicle details.”)

🔍 Step 2: Fetch Vehicle Info from dummy database present in cloud.

💬 Step 3: Use LLM Prompt to Recommend a Coverage Plan
Based on the vehicle type and year, let the LLM suggest:

Comprehensive

Collision

Liability-only

Third-party, etc.

🧠 Example prompt to LLM:

“This is a 2021 Honda Civic. Suggest the best coverage plan based on age and value of the car.”

👤 Step 4: Ask for Driver Information
You must collect these manually:

ZIP code (for location-based risk)

Driver’s age

Ask via chatbot:
“Great! To calculate the quote, please share your ZIP code and age.”

🧮 Step 5: Quote Calculation
Use a Python tool agent or API to estimate the quote.

Factors:

Vehicle value

ZIP risk factor (e.g., city traffic, accident rate)

Driver age (younger = riskier)

Chosen coverage plan

def calculate_quote_with_tax(car_value, accident_history, driver_age, zip_risk, tax_rate=0.09):
    plans = []

    # Always include Liability
    liability = {
        "name": "Liability",
        "description": "Covers damages to other vehicles and property.",
        "base_price": 300
    }
    plans.append(liability)

    # Add Collision if needed
    if car_value > 15000 or accident_history or driver_age < 25:
        plans.append({
            "name": "Collision",
            "description": "Covers your vehicle in case of accidents.",
            "base_price": 450
        })

    # Add Comprehensive if car is valuable or ZIP is risky
    if car_value > 25000 or zip_risk == "high":
        plans.append({
            "name": "Comprehensive",
            "description": "Covers theft, vandalism, natural disasters.",
            "base_price": 550
        })

    # Calculate tax and total
    for plan in plans:
        plan["tax"] = round(plan["base_price"] * tax_rate, 2)
        plan["total"] = round(plan["base_price"] + plan["tax"], 2)

    return {"recommended_plans": plans}


{
  "recommended_plans": [
    {
      "name": "Liability",
      "description": "Covers damages to other vehicles and property.",
      "base_price": 300,
      "tax": 27.0,
      "total": 327.0
    },
    {
      "name": "Collision",
      "description": "Covers your vehicle in case of accidents.",
      "base_price": 450,
      "tax": 40.5,
      "total": 490.5
    },
    {
      "name": "Comprehensive",
      "description": "Covers theft, vandalism, natural disasters.",
      "base_price": 550,
      "tax": 49.5,
      "total": 599.5
    }
  ]
}


input value: 1HGCM660487647wLnG
