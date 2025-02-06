import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from restack_ai.function import FunctionFailure, function, log
from stripe_agent_toolkit.langchain.toolkit import StripeAgentToolkit

load_dotenv()


@function.defn()
async def create_payment_link() -> str:
    stripe_secret_key = os.getenv("STRIPE_SECRET_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    langchain_api_key = os.getenv("LANGCHAIN_API_KEY")

    if stripe_secret_key is None:
        error_message = "STRIPE_SECRET_KEY is not set"
        log.error(error_message)
        raise FunctionFailure(error_message, non_retryable=True)

    if langchain_api_key is None:
        error_message = "LANGCHAIN_API_KEY is not set"
        log.error(error_message)
        raise FunctionFailure(error_message, non_retryable=True)

    if openai_api_key is None:
        error_message = "OPENAI_API_KEY is not set"
        log.error(error_message)
        raise FunctionFailure(error_message, non_retryable=True)

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
                },
            },
        )

        model = ChatOpenAI(api_key=SecretStr(openai_api_key))

        prompt = hub.pull("hwchase17/structured-chat-agent")

        agent = create_structured_chat_agent(
            model,
            stripe_agent_toolkit.get_tools(),
            prompt,
        )
        agent_executor = AgentExecutor(
            agent=agent,
            tools=stripe_agent_toolkit.get_tools(),
        )

        result = agent_executor.invoke(
            {
                "input": """
                Create a payment link for a new product
                called 'Test' with a price of $100.
                """,
            },
        )

        return str(result["output"])
    except Exception as e:
        error_message = f"Error creating payment link: {e}"
        log.error(error_message)
        raise FunctionFailure(error_message, non_retryable=True) from e
