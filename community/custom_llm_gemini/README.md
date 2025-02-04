# Custom LLM Demo

This Flask application provides a chat completion API that proxy the stream to Gemini API

Useful for VAPI integration

```bash
uv venv && source .venv/bin/activate
```

```bash
uv sync
```

```
uv run llm
```

```
ngrok http 1337
```

Use the ngrok url in your VAPI custom llm
