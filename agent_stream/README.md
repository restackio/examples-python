# Restack AI - Agent with stream

Build an Agent user can chat with and return streaming response.

## Prerequisites

- Docker (for running Restack)
- Python 3.10 or higher

## Start Restack

To start the Restack, use the following Docker command:

```bash
docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 -p 9233:9233 ghcr.io/restackio/restack:main
```

## Start python shell

If using uv:

```bash
uv venv && source .venv/bin/activate
```

If using pip:

```bash
python -m venv .venv && source .venv/bin/activate
```

## Install dependencies

If using uv:

```bash
uv sync
uv run dev
```

If using pip:

```bash
pip install -e .
python -c "from src.services import watch_services; watch_services()"
```

## Run agent

### from UI

You can run agents from the UI by clicking the "Run" button.

![Run workflows from UI](./chat_post.png)

### from API

You can run agents from the API by using the generated endpoint:

`POST http://localhost:6233/api/agents/AgentStream`

### from any client

You can run agents with any client connected to Restack, for example:

```bash
uv run schedule
```

executes `schedule_agent.py` which will connect to Restack and execute the `AgentStream` workflow.

## Send events to the Agent

### from UI

You can send events like message or end from the UI.

![Send events from UI](./chat_put.png)

And see the events in the run:

![See events in UI](./chat_run.png)

### from API

You can send events to the agent by using the following endpoint:

`PUT http://localhost:6233/api/agents/AgentStream/:agentId/:runId`

with the payload:

```json
{
  "eventName": "messages",
  "eventInput": {
    "messages": [{"role": "user", "content": "tell me a joke"}]
  }
}
```

to send messages to the agent.

or

```json
{
  "eventName": "end"
}
```

to end the conversation with the agent.

### from any client

You can send event to the agent workflows with any client connected to Restack, for example:

Modify agent_id and run_id in event_agent.py and then run:

```bash
uv run event
```

It will connect to Restack and send 2 events to the agent, one to generate another agent and another one to end the conversation.

## Deploy on Restack Cloud

To deploy the application on Restack, you can create an account at [https://console.restack.io](https://console.restack.io)
