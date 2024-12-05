from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain import hub
from stripe_agent_toolkit.langchain.toolkit import StripeAgentToolkit
from restack_ai.function import function, FunctionFailure
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

@function.defn()
async def create_payment_link():
    stripe_secret_key = os.getenv("STRIPE_SECRET_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    langchain_api_key = os.getenv("LANGCHAIN_API_KEY")

    if stripe_secret_key is None:
        raise FunctionFailure("STRIPE_SECRET_KEY is not set", non_retryable=True)
    
    if langchain_api_key is None:
       raise FunctionFailure("LANGCHAIN_API_KEY is not set", non_retryable=True)
    
    if openai_api_key is None:
        raise FunctionFailure("OPENAI_API_KEY is not set", non_retryable=True)
    
    try:
        stripe_agent_toolkit = StripeAgentToolkit(
            secret_key=stripe_secret_key,
            configuration={
            "actions": {
                "payment_links": {
                    "create": True,
                },
                "products": {
                    "create": True,
                },
                "prices": {
                    "create": True,
                },
            }
            },
        )

        model = ChatOpenAI(api_key=SecretStr(openai_api_key))
        
        prompt = hub.pull("hwchase17/structured-chat-agent")

        agent = create_structured_chat_agent(model, stripe_agent_toolkit.get_tools(), prompt)
        agent_executor = AgentExecutor(agent=agent, tools=stripe_agent_toolkit.get_tools())

        result = agent_executor.invoke({
          "input": "Create a payment link for a new product called \"Test\" with a price of $100."
        })

        return result["output"]
    except Exception as e:
        raise FunctionFailure(f"Error creating payment link: {e}", non_retryable=True)
