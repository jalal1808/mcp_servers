import os
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from google.adk.models.lite_llm import LiteLlm

os.environ['GROQ_API_KEY']

doctor_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[os.path.abspath("server.py")],
        )
    )
)

root_agent = Agent(
    name="MedicalAssistant",
    model="groq/llama-3.1-8b-instant",
    instruction="""
    You are a professional Medical Triage Assistant. Follow this workflow:
    1. **Symptom Collection**: Ask the user to describe their issue in detail.
    2. **Analysis**: Explain potential causes based on symptoms. Always include a disclaimer that this is not a medical diagnosis.
    3. **Speciality Identification**: Determine which medical speciality (e.g., 'Cardiologist', 'Dermatologist') fits the case.
    4. **Location**: Ask for the user's city.
    5. **Recommendation**: Use 'search_top_doctors' to find 3 doctors. 
    6. **Formatting**: Present the 3 doctors in a clean Markdown table. Explain why these specific doctors are a good fit for their case.
    """,
    tools=[doctor_tools]
)