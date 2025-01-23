# Restack AI SDK - FastAPI + Gemini Generate Content Example

## Prerequisites

- Python 3.9 or higher
- Poetry (for dependency management)
- Docker (for running the Restack services)
- Active [Google AI Studio](https://aistudio.google.com) account with API key

## Usage

1. Run Restack local engine with Docker:

   ```bash
   docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 ghcr.io/restackio/restack:main
   ```

2. Open the web UI to see the workflows:

   ```bash
   http://localhost:5233
   ```

3. Clone this repository:

   ```bash
   git clone https://github.com/restackio/examples-python
   cd examples-python/examples/fastapi_gemini_feedback
   ```

4. Install dependencies using Poetry:

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

5. Configure your Gemini API key using one of these methods:

   a. Set as environment variable:

   ```bash
   export GEMINI_API_KEY=<your-api-key>
   ```

   b. Create a `.env` file:

   - Copy `.env.example` to `.env` in the `fastapi_gemini_feedback` folder
   - Add your API key from [Google AI Studio](https://aistudio.google.com):

   ```bash
   GEMINI_API_KEY=<your-api-key>
   ```

6. Run the services:

   ```bash
   poetry run services
   ```

   This will start the Restack service with the defined workflows and functions.

7. In a new terminal, run flask app:

   ```bash
   poetry shell
   ```

   ```bash
   poetry run app
   ```

   The app will run at http://0.0.0.0:5001

8. POST to `http://0.0.0.0:5000/api/schedule` with the following JSON body:

   ```json
   {
     "user_content": "Tell me a story"
   }
   ```

   Or using curl in a new terminal:

   ```bash
   curl -X POST http://0.0.0.0:5001/api/schedule -H "Content-Type: application/json" -d '{"user_content": "Tell me a story"}'
   ```

   This will schedule the `GeminiGenerateWorkflow` and print the result. The workflow will continue running, waiting for feedback.

9. POST to `http://0.0.0.0:5000/api/event/feedback` with the following JSON body:

   ```json
   {
     "feedback": "The story is too long",
     "workflow_id":"<workflow_id>",
     "run_id":"<run_id>""
   }
   ```

   Or using curl:

   ```bash
   curl -X POST http://0.0.0.0:5001/api/event/feedback -H "Content-Type: application/json" -d '{"feedback": "The story is too long", "workflow_id": "<workflow_id>", "run_id": "<run_id>"}'
   ```

   Use the `workflow_id` and `run_id` returned from the previous schedule API call to send feedback to the workflow.

10. POST to `http://0.0.0.0:5001/api/event/end` to end the workflow with the following JSON body:

```json
{
  "workflow_id":"<workflow_id>",
  "run_id":"<run_id>""
}
```

Or using curl:

```bash
curl -X POST http://0.0.0.0:5001/api/event/end -H "Content-Type: application/json" -d '{"workflow_id": "<workflow_id>", "run_id": "<run_id>"}'
  -H "Content-Type: application/json"
```

## Project Structure

- `src/`: Main source code directory
  - `client.py`: Initializes the Restack client
  - `functions/`: Contains function definitions
  - `workflows/`: Contains workflow definitions
  - `services.py`: Sets up and runs the Restack services
  - `app.py`: Flask app to schedule and run workflows
