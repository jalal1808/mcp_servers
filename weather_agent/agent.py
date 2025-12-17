import os
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from google.adk.models.lite_llm import LiteLlm

os.environ['GROQ_API_KEY']


weather_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=["weather_server.py"], 
            env={"WEATHER_API_KEY": os.getenv("WEATHER_API_KEY")}
        )
    )
)

researcher = LlmAgent(
    name="WeatherResearcher",
    model="groq/llama-3.1-8b-instant", 
    instruction="Use the get_weather tool to find the current conditions for the city.",
    tools=[weather_toolset]
)

concierge = LlmAgent(
    name="ActivityConcierge",
    model="groq/llama-3.1-8b-instant", 
    instruction="Suggest 3 activities based on the weather provided by the researcher."
)

root_agent = SequentialAgent(
    name="CityExpert",
    sub_agents=[researcher, concierge]
)