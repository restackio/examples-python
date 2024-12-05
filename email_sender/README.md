# Restack AI - Email Sender example

This example showcases how to send emails with a Restack workflow using the sendgrid api. You can easily choose another email provider and update the code.
You can schedule two scenarios of the workflow.

1. It will be successfull and send an email.
2. The email content generation step will fail once to showcase how Restack handles retries automatically. Once failure is caught, step will be retry automatically and rest of workflow will be executed as expected and email will be sent.


## Prerequisites

- Python 3.10 or higher
- Poetry (for dependency management)
- Docker (for running the Restack services)

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
   cd examples-python/examples/get-started
   ```
  
4. Create .env file with: STRIPE_SECRET_KEY and OPENAI_API_KEY

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

5. Run the services:

   ```bash
   poetry run services
   ```

   This will start the Restack service with the defined workflows and functions.

6. In a new terminal, schedule the workflow:

   ```bash
   poetry shell
   ```

   ```bash
   poetry run schedule
   ```

   This will schedule the `SendEmailWorkflow` and print the result.

7. To simulate a flow where the step for sending email fails and the retry is automatically handled by Restack AI use run:
   ```bash
   poetry run schedule_failure
   ```
