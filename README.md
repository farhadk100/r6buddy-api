# R6Buddy API

###### a RESTful API for the [R6Buddy](https://github.com/farhadk100/r6buddy-app) app, deployed using [Deta](https://www.deta.sh)

## Setup

If you are planning to set up your own API, either locally or from a Deta Micro, you first need to make a free Deta
account to be able to use a Deta Base to store your data. When this is done, you'll be shown a project key, which you
will use to deploy your Deta Base (and possibly your Deta Micro).

Start by creating a `.env` file using the template, and put your Deta project key in there.

```bash
cp .env-example .env
```

Next, create a virtual environment,

```bash
python3 -m venv venv
```

activate it,

```bash
source venv/bin/activate
```

and finally install the requirements.

```bash
pip install -r requirements.txt
```

### Run locally

With the `.env` file in place and the requirements installed, you should now be able to run the API locally using
uvicorn.

```bash
uvicorn main:app --reload --env-file .env
```

By default, uvicorn will run the API on localhost using port 8000.
On [http://localhost:8000/docs](http://localhost:8000/docs), you should be able to see the Swagger documentation for the
API endpoints.

### Deploy on Deta Micro

It is also possible to deploy the API to your own Deta Micro.

Start by initializing a Deta Micro.

```bash
deta new
```

Next, provide the `.env` to the Deta Micro, so that it can access the Deta Bases.

```bash
deta update -e .env
```

At this point, your Deta Micro should be up and running. A quick check by running `deta details` should show you
something like this:

```json
{
  "name": "r6buddy-api",
  "id": "<id>",
  "project": "default",
  "runtime": "python3.9",
  "endpoint": "https://<path>.deta.dev",
  "region": "<region>",
  "dependencies": [
    "fastapi",
    "uvicorn",
    "deta",
    "python-dotenv"
  ],
  "environment_variables": [
    "DETA_PROJECT_KEY"
  ],
  "visor": "disabled",
  "http_auth": "disabled"
}
```

You can now visit your API at the address provided in the `endpoint` field.

