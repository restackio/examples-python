# Custom LLM Demo

This Flask application provides a chat completion API that proxy the stream to Gemini API

Useful for VAPI integration

```bash
poetry env use 3.12
```

```bash
poetry shell
```

```bash
poetry install
```

```bash
poetry env info # Optional: copy the interpreter path to use in your IDE (e.g. Cursor, VSCode, etc.)
```

```
poetry run llm
```

```
ngrok http 1337
```

Use the ngrok url in your VAPI custom llm
