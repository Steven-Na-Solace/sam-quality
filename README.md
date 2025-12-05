# Quality Agents for the SECOM Manufacturing Execution System (MES)

Welcome to the Quality Agents repository for SECOM MES! 
This project provides a robust agent-based solution for managing lots within a manufacturing execution system, leveraging the power of Solace Agent Mesh Enterprise and modern Python tooling. 
Follow the steps below to set up your environment and get started quickly.

---

## Prerequisites

### Solace Event Broker Installation
If you are new to Solace or do not have the Solace Event Broker installed, please follow the official guide to download and launch a software event broker:
- [Solace Event Broker Setup Guide](https://docs.solace.com/Get-Started/tutorial/event-broker-set-up.htm#download-and-launch-a-software-event-broker)

This step is essential for enabling agent communication and event-driven operations within the SECOM MES environment.

### SECOM API Repository
You will also need the SECOM API repository. Please visit the following link to access and set up the required API:
- [SECOM API GitHub Repository](https://github.com/Steven-Na-Solace/sam-secom-api)

---

## Virtual Python Environment Setup

To ensure compatibility and isolation, please use Python 3.13:

```bash
python3.13 -m venv .venv
```

Activate your virtual environment:

```bash
source .venv/bin/activate
```

Verify your Python version:

```bash
(.venv) > python --version        
Python 3.13.5
```

---

## Install SAM Enterprise

Install the required SAM Enterprise package:

```bash
pip install solace_agent_mesh_enterprise-1.14.11-py3-none-any.whl 
```

---

## Environment Configuration

Create a `.env` file in your project root and configure your environment-specific settings:

```bash
LLM_SERVICE_ENDPOINT="https://xxxx"
LLM_SERVICE_API_KEY="xxxxxx"
LLM_SERVICE_PLANNING_MODEL_NAME="openai/claude-3-7-sonnet"
LLM_SERVICE_GENERAL_MODEL_NAME="openai/claude-3-7-sonnet"
NAMESPACE="default_namespace/"
SOLACE_BROKER_URL="ws://xxxxx:8008"
SOLACE_BROKER_VPN="default"
SOLACE_BROKER_USERNAME="default"
SOLACE_BROKER_PASSWORD="default"
SOLACE_DEV_MODE="false"
SESSION_SECRET_KEY="please_change_me_in"
FASTAPI_HOST="127.0.0.1"
FASTAPI_PORT="8002"
FASTAPI_HTTPS_PORT="8444"
SSL_KEYFILE=""
SSL_CERTFILE=""
SSL_KEYFILE_PASSWORD=""
ENABLE_EMBED_RESOLUTION="True"
LOGGING_CONFIG_PATH="configs/logging_config.yaml"
S3_BUCKET_NAME=""
S3_ENDPOINT_URL=""
S3_REGION="us-east-1"
```

---

## PYTHONPATH Setup

Set your PYTHONPATH to include your project directory:

```bash
export PYTHONPATH="/your/project/path:$PYTHONPATH"
```

---

## Starting Quality Agents

Launch the Quality Agents using the following command:

```bash
solace-agent-mesh run
```

---

## Connect to SAM WEB UI

Once the agents are running, access the SAM Web UI at:

- http://127.0.0.1:8002

---
