from langchain.agents import AgentExecutor, create_structured_chat_agent
from stripe_agent_toolkit.langchain.toolkit import StripeAgentToolkit
from restack_ai.function import function, log, FunctionFailure
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

@function.defn()
async def create_payment_link():
    stripe_secret_key = os.getenv("STRIPE_SECRET_KEY")
    if stripe_secret_key is None:
        raise FunctionFailure("STRIPE_SECRET_KEY is not set", non_retryable=True)
    
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

    openai_api_key = os.getenv("OPENAI_API_KEY")

    if openai_api_key is None:
        raise FunctionFailure("OPENAI_API_KEY is not set", non_retryable=True)

    model = ChatOpenAI(api_key=openai_api_key)

    agent = create_structured_chat_agent(model, stripe_agent_toolkit.get_tools(),ChatPromptTemplate([
                ("system", "You are a helpful AI bot that will create a payment link for a new product on stripe."),
            ]))
    agent_executor = AgentExecutor(agent=agent, tools=stripe_agent_toolkit.get_tools())

    agent_executor.invoke({
        "input": "Create a payment link for a new product called \"Test\" with a price of $100."
  })
