# Restack AI - SMTP Send Email Example


## Why SMTP in 2025?



### The SMTP Advantage

*"But why not use [insert latest buzzword solution here]?"*

Listen, I get it. You're probably thinking "SMTP? In 2025? What is this, a museum?" But hear me out:

Want to send emails from `workflow1@yourdomain.com`... `workflow100@yourdomain.com`? All you need is:
1. A domain (your digital real estate)
2. Basic DNS setup
3. A working SMTP server

## Prerequisites

- Python 3.10 or higher
- Poetry (for dependency management)
- Docker (for running the Restack services)
- SMTP Credentials

## Usage

Run Restack local engine with Docker:

```bash
docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 ghcr.io/restackio/restack:main
```

Open the web UI to see the workflows: http://localhost:5233

---

Clone this repository:

```bash
git clone https://github.com/restackio/examples-python
cd examples-python/smtp_send_email/
```

---
  
Reference `.env.example` to create a `.env` file with your SMTP credentials:

```bash
cp .env.example .env
```

```
SMTP_SERVER = "smtp.mailgun.org"
SMTP_PORT = 587
SMTP_USERNAME = "postmaster@domain.xyz"  # Usually starts with 'postmaster@'
SMTP_PASSWORD = "PASSWD"
SENDER_EMAIL = "restack@mg.domain.xyz"
```

Update the `.env` file with the required ENVVARs

---

Install dependencies using Poetry:

   ```bash
   poetry env use 3.12
   poetry shell
   poetry install
   poetry env info # Optional: copy the interpreter path to use in your IDE (e.g. Cursor, VSCode, etc.)
   ```


Run the [services](https://docs.restack.io/libraries/python/services):

```bash
poetry run services
```

This will start the Restack service with the defined [workflows](https://docs.restack.io/libraries/python/workflows) and [functions](https://docs.restack.io/libraries/python/functions).

In the Dev UI, you can use the workflow to manually kick off a test with an example JSON post, and then start inegrating more steps into a workflow that requires sending a SMTP email.

## Development mode

If you want to run the services in development mode, you can use the following command to watch for file changes, if you choose to copy this to build your workflow off of:

```bash
poetry run dev
```
