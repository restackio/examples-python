from __future__ import annotations
import asyncio
import json
import os
import time
import traceback

from dotenv import load_dotenv
from flask import Flask, Response, request, stream_with_context
import google.generativeai as genai
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

def run_async(coro):
    loop = asyncio.new_event_loop()
    return loop.run_until_complete(coro)


@app.route("/chat/completions", methods=["POST"])
def chat_completion():
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        
        # Log that a request has been received
        print("Received a POST request at /chat/completions")

        # Log request headers
        print("Request headers:", request.headers)
        
        start_time = time.perf_counter()
        data = request.json
        messages = data.get("messages", [])
        print("Received messages:", messages)

        # Log request headers
        print("Request headers:", request.headers)

        # transform messages to the format expected by the gemini api
        content_objects = []

        for message in messages:
            part = genai.protos.Part(text=message['content'])
            role = "model" if message['role'] in ["system", "assistant"] else message['role']
            content = genai.protos.Content(parts=[part], role=role)
            content_objects.append(content)

        # Start the completion stream

        completion_stream = genai.GenerativeModel('models/gemini-1.5-flash').generate_content(
            contents=content_objects,
            stream=True
        )

        print(f"Time taken to start streaming: {time.perf_counter() - start_time}")

        def generate():
            for chunk in completion_stream:
                print(chunk)
                # Access the candidates directly from the response
                for candidate in chunk._result.candidates:
                    content = candidate.content.parts[0].text
                    print(content)
                    yield f"data: {json.dumps({'choices': [{'delta': {'content': content}}]})}\n\n"
            yield "data: [DONE]\n\n"

        return Response(stream_with_context(generate()), content_type="text/plain")

    except Exception as e:
        print(f"CHATBOT_STEP: {traceback.format_exc()}")
        return Response(str(e), content_type="text/plain", status=500)


@app.route("/test", methods=["GET"])
def test_route():
    print("Test route accessed")
    return "Test route is working", 200
    
if __name__ == "__main__":
    app.run(debug=True)

def run_llm():
    app.run(debug=True, host='0.0.0.0', port=1337)
