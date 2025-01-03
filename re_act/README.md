# Restack AI - ReAct Example

## Prerequisites

- Python 3.11
- Poetry (for dependency management)
- Docker (for running the Restack services)

## Usage

2. Open the web UI to see the workflows:

   ```bash
   http://localhost:5233
   ```

3. Clone this repository:

   ```bash
   git clone https://github.com/restackio/examples-python
   cd examples-python/re_act
   ```

4. Install dependencies using Poetry:

   ```bash
   poetry env use 3.11
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

6. Schedule workflow

   ```bash
   poetry run schedule_workflow
   ```

