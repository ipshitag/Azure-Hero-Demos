# Azure imports
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation.red_team import RedTeam, RiskCategory
import os
from dotenv import load_dotenv
from pyrit.prompt_target import OpenAIChatTarget, PromptChatTarget
load_dotenv()

# Azure AI Project Information
azure_ai_project = {
    "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID"),
    "resource_group_name": os.environ.get("AZURE_RESOURCE_GROUP_NAME"),
    "project_name": os.environ.get("AZURE_PROJECT_NAME"),
}

# Instantiate your AI Red Teaming Agent
red_team_agent = RedTeam(
    azure_ai_project=azure_ai_project, # required
    credential=DefaultAzureCredential(), # required
    risk_categories=[ # optional, defaults to all four risk categories
        RiskCategory.Violence,
        RiskCategory.HateUnfairness,
        RiskCategory.Sexual,
        RiskCategory.SelfHarm
    ], 
    num_objectives=5, # optional, defaults to 10
)

# Configuration for Azure OpenAI model
azure_openai_config = {
    "azure_endpoint": os.environ.get("EUS_AZURE_OPENAI_ENDPOINT"),
    "api_key": os.environ.get("EUS_AZURE_OPENAI_KEY"), #  not needed for entra ID based auth, use az login before running,
    "azure_deployment": os.environ.get("EUS_AZURE_OPENAI_DEPLOYMENT"),
}

chat_target = OpenAIChatTarget(
    model_name=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
    endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_KEY"),
    api_version="2024-12-01-preview",
    
) 

import asyncio

async def main():
    red_team_result = await red_team_agent.scan(target=chat_target)

asyncio.run(main())