
# Restack AI - Agent with telephony - Vapi

Build an AI agent that do an outbound call with Vapi and can interact with in realtime with voice.

This readme explains how to run this example.
For a complete documentation on how the agent works and how to setup the services, visit https://docs.restack.io/telephony-video-voice/telephony

## Prerequisites

- Docker (for running Restack)
- Python 3.10 or higher
- Vapi account

### Create a Vapi account

See more on [Vapi documentation](https://docs.vapi.ai/quickstart/phone/outbound)

## Start Restack

To start the Restack, use the following Docker command:

```bash
docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 -p 9233:9233 ghcr.io/restackio/restack:main
```

## Configure environment variables

In all subfolders, duplicate the `env.example` file and rename it to `.env`.

Obtain a Restack API Key to interact with the 'gpt-4o-mini' model at no cost from [Restack Cloud](https://console.restack.io/starter)


## Start Restack Agent with Twilio

### Start python shell

If using uv:

```bash
uv venv && source .venv/bin/activate
```

If using pip:

```bash
python -m venv .venv && source .venv/bin/activate
```

### Install dependencies

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

## Start Livekit voice pipeline

### Start python shell

If using uv:

```bash
uv venv && source .venv/bin/activate
```

If using pip:

```bash
python -m venv .venv && source .venv/bin/activate
```

### Install dependencies

If using uv:

```bash
uv sync
uv run python src/pipeline.py dev
```

If using pip:

```bash
pip install -e .
python src/pipeline.py dev
```

## Configure Your Environment Variables

Duplicate the `env.example` file and rename it to `.env`.

Obtain a Restack API Key to interact with the 'gpt-4o-mini' model at no cost from [Restack Cloud](https://console.restack.io/starter)

## Create a new Agent

### from UI

Run the agent from the UI by clicking the "Run" button for the agent "`POST http://localhost:6233/api/agents/AgentVapi`
".

### from API

Run the agent from the API by using the generated endpoint:

`POST http://localhost:6233/api/agents/AgentVapi`

Restack agent will create a Livekit WebRTC room and will ask a livekit pipeline to connect to it, ready for a phone call.

## Trigger an outbound phone call

### from API

You can send events to the agent by using the following endpoint:

`PUT http://localhost:6233/api/agents/AgentVapi/:agentId/:runId`

with the payload:

```json
{
  "eventName": "call",
  "eventInput": {
    "assistant_id": "assistant_id",
    "phone_number": "+XXXXXXX"
  }
}
```

to trigger an outbound phone call.

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

If using uv:

```bash
uv run event
```

If using pip:

```bash
python -c "from src.event_agent import run_event_agent; run_event_agent()"
```

![Trigger outbound call](./agent_call.png)

## Follow the agent run

You can replay and follow the agent run in the UI.

![Replay agent run](./agent_replay.png)

## Deploy on Restack Cloud

To deploy the application on Restack, you can create an account at [https://console.restack.io](https://console.restack.io)
