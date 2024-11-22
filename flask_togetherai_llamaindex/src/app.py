import time
from flask import Flask, jsonify, request
from restack_ai import Restack
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Welcome to the TogetherAI LlamaIndex Flask App!"

# New endpoint to schedule workflow and get back result
@app.route('/api/schedule', methods=['POST'])
async def schedule_workflow():
    if request.is_json:
        
        prompt = request.json.get('prompt')
        client = Restack()

        workflow_id = f"{int(time.time() * 1000)}-LlmCompleteWorkflow"
        runId = await client.schedule_workflow(
            workflow_name="LlmCompleteWorkflow",
            workflow_id=workflow_id,
            input=prompt
        )

        result = await client.get_workflow_result(
            workflow_id=workflow_id,
            run_id=runId
        )
        
        return jsonify({'result': result})

    else:
        return jsonify({'error': 'Request must be JSON'}), 400

def run_flask():
    app.run(debug=True) 

if __name__ == '__main__':
    run_flask() 