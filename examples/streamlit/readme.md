# Streamlit example

This example shows how to use Streamlit to trigger a workflow and display the result.

## Running the example

```
poetry install
```

```
poetry shell
```

```
poetry run streamlit run main.py
```

## You will need to have Restack Engine running locally.

```bash
docker run -d --pull always --name studio -p 5233:5233 -p 6233:6233 -p 7233:7233 ghcr.io/restackio/restack:main
```

And your restack services, for example:

```
cd..
cd examples/get-started
poetry install
poetry run services
```

In the streamlit UI, you can trigger the workflow with the following:

- Workflow Name: `GreetingWorkflow`
- Workflow ID: `1727432400000-GreetingWorkflow`
- Input Data: `{"name": "John"}`
