import time
from dataclasses import dataclass

from flask import Flask, jsonify, request
from flask_cors import CORS
from restack_ai import Restack

app = Flask(__name__)
CORS(app)


# Example route for the home page
@app.route("/")
def home() -> str:
    return "Welcome to the Flask App!"


@app.route("/test", methods=["GET", "POST"])
def test_route() -> str:
    return "This is a test route", 200


@dataclass
class InputParams:
    user_content: str


# New endpoint to schedule workflow and get back result
@app.route("/api/schedule", methods=["POST"])
async def schedule_workflow() -> dict[str, str]:
    if request.is_json:
        data = request.get_json()

        user_content = data.get("user_content", "this is a story")

        client = Restack()

        workflow_id = f"{int(time.time() * 1000)}-GeminiGenerateWorkflow"
        run_id = await client.schedule_workflow(
            workflow_name="GeminiGenerateWorkflow",
            workflow_id=workflow_id,
            input=InputParams(user_content=user_content),
        )

        result = await client.get_workflow_result(
            workflow_id=workflow_id,
            run_id=run_id,
        )
        return jsonify(result), 200

    return jsonify({"error": "Request must be JSON"}), 400


def run_flask() -> None:
    app.run()


if __name__ == "__main__":
    run_flask()
