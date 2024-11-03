import time
from flask import Flask, jsonify, request
from pydantic import BaseModel
from restack_ai import Restack
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Example route for the home page
@app.route('/')
def home():
    return "Welcome to the Flask App!"

@app.route('/test', methods=['GET', 'POST'])
def test_route():
    return 'This is a test route', 200

class InputParams(BaseModel):
    user_content: str
    
# New endpoint to schedule workflow and get back result
@app.route('/api/schedule', methods=['POST'])
async def schedule_workflow():
    if request.is_json:
        data = request.get_json()

        print('data', data)

        user_content = data.get('user_content', 'this is a story')
        
        client = Restack()

        workflow_id = f"{int(time.time() * 1000)}-GeminiGenerateWorkflow"
        runId = await client.schedule_workflow(
            workflow_name="GeminiGenerateWorkflow",
            workflow_id=workflow_id,
            input=InputParams(user_content=user_content)
        )

        print(f"Scheduled workflow with ID: {workflow_id}")

        result = await client.get_workflow_result(
            workflow_id=workflow_id,
            run_id=runId
        )
        return jsonify(result), 200

    else:
        return jsonify({'error': 'Request must be JSON'}), 400


def run_flask():
    app.run(debug=True) 

if __name__ == '__main__':
    run_flask()