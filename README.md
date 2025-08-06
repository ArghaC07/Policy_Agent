# Policy_Agent
This is a Policy Agentic AI 


The folder structure for this project we are planning below:

car_insurance_bot/
│
├── agents/
│   ├── quote_agent.py            # Central orchestrator  agent
│   ├── fetch_details_agent.py    # Fetches car specs using VIN
│   ├── coverage_agent.py        #  Recommends coverage based 
                                    on user profile
│   └── quote_creation_agent.py  # Calculates the initial quote
│
├── tools/
│   ├── db_connector.py    # DB connection logic (to dummy RDS)
│   └── fetch_car_details.py   # Tool to query VIN data from DB
│
├── prompts/
│   ├── quote_agent_prompt.txt
│   ├── fetch_details_prompt.txt
│   ├── coverage_prompt.txt
│   └── quote_creation_prompt.txt
│
├── .env                 # Database credentials, config for ADK
├── requirements.txt          # Dependencies 
├── agent.py                 # Imports and registers root_agent
├── README.md
