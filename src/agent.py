from dotenv import load_dotenv
from google.adk.agents import Agent
from src.prompts import return_instructions_root
from src.tools import read_spreadsheet, update_spreadsheet

load_dotenv()

root_agent = Agent(
        model="gemini-2.5-flash",
        name="Response_Agent",
        instruction=return_instructions_root(),
        tools=[read_spreadsheet, update_spreadsheet],
    )