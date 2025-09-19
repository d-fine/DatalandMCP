# DatalandMCP

This repository contains an MCP Server which allows LLMs to access data from Dataland.
Additionally, the open-source chat clients [Open WebUI](https://docs.openwebui.com/) & [LibreChat](https://www.librechat.ai/) can be launched within this repo which serve as MCP Hosts.

## Table of contents
- [Prerequisites](#prerequisites)
- [Quick Start with Docker Compose](#quick-start-with-docker-compose)
  - [Launch](#launch)
  - [Configure Open WebUI](#configure-open-webui)
  - [Configure LibreChat](#configure-librechat)
- [Troubleshooting](#troubleshooting)
- [Development Setup](#development-setup)
  - [Dataland Client](#dataland-client)
  - [Python MCP SDK](#python-mcp-sdk)

## Prerequisites
- Have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
- Create a personal account on https://dataland.com and https://test.dataland.com

## Quick Start with Docker Compose

The easiest way to get started is using Docker Compose, which starts the MCP server and the MCP hosts (Open WebUI & LibreChat) in one command.

Create a `.env` file at the project root with your Dataland API key:
```
DATALAND_API_KEY=your_api_key_here
```

You can create your API key as described [here](https://github.com/d-fine/Dataland/wiki/Use-the-API).

### Launch

From the repository root directory, start both the MCP server and hosts:

```bash
docker-compose up
```

To run in the background:
```bash
docker-compose up -d
```

To rebuild and start:
```bash
docker-compose up --build
```

After successful launch:
- Open WebUI will be available at http://localhost:8080
- LibreChat will be available at http://localhost:3080
- MCP server documentation (Swagger UI) will be accessible at http://localhost:8000/DatalandMCP/docs

To stop the services:
```bash
docker-compose down
```

**Note**: Open WebUI data (including user accounts, settings, and configurations) is persisted in a Docker volume named `datalandmcp_open-webui`. This means your Open WebUI setup will be preserved between container restarts. If you need to reset Open WebUI to a fresh state, you must explicitly delete this volume:

```bash
# Stop the services first
docker-compose down

# Remove the Open WebUI volume to start fresh
docker volume rm datalandmcp_open-webui

# Start services again
docker-compose up
```

The same holds for LibreChat, which uses a volume named `pgdata2` which contains user accounts and settings. Unlike Open WebUI the base configurations of LibreChat (e.g. API connections) are set via a config file at project root.

### Configure Open WebUI

After the containers are running, you'll need to configure Open WebUI:

1. **Create an Open WebUI account**: Navigate to http://localhost:8080 and create an account.

    <img width="1904" height="907" alt="Image" src="https://github.com/user-attachments/assets/de16630b-c70f-45d4-87ea-d6f4bfd91f5e" />

2. **Connect with Azure OpenAI**: Open WebUI supports Azure OpenAI to connect cloud-based LLMs.
   Go to _Profile -> Admin Panel -> Settings -> Connections -> OpenAI API -> +_:

    <img width="462" height="418" alt="Image" src="https://github.com/user-attachments/assets/5e7e714e-6e7c-4e06-b1ec-91b42c1a9ff3" />

    In the above screenshot _[resource_name]_, _[deployment_name]_, _[API_KEY]_ and [API_VERSION] has to be replaced by the correct values defined in your Azure OpenAI resource. 
The deployment name is the given name of the deployed model within the resource (e.g. _d-fine_azure_gpt-4.1_).
\
\
    You should now be able to see the deployed model in the list of available models and chat with it:

    <img width="513" height="226" alt="Image" src="https://github.com/user-attachments/assets/7abca8c4-64df-41ee-bcba-eaae4c2d01da" />

3. **Connect the MCP Server**: Within Open WebUI, add the running MCP server via `Profile -> Settings -> Tools -> +`:

    <img width="453" height="240" alt="Image" src="https://github.com/user-attachments/assets/e09cbbd7-a3e6-4680-b89a-f93dad9d2bc8" />

    Now the tools of the MCP Server are available in the chat via a toolbox under the input field:

    <img width="658" height="327" alt="Image" src="https://github.com/user-attachments/assets/c7531e03-e0db-4994-b94d-ebdb171013cb" />

4. **Set the system prompt**: The system prompt defines the assistant's role. 
   - Within Open WebUI, go to `Profile` -> `Admin Panel` -> `Models`. Choose your model and go to the box `Model Parameters` -> `System Prompt`. 
   - Copy the prompt from the `system_prompt` file which is located in the project root and paste it into the box. 
   - Click on `Save & Update`.

    Note: You can also set the system prompt model independently in your personal settings. Go to `Profile` -> `Settings` -> `General` and paste the prompt into the field `System Prompt`. 

### Configure LibreChat

After the containers are running, you'll need to configure LibreChat:

1. **Create an LibreChat account**: Navigate to http://localhost:3080 and create an account.

2. **Further Cofiguration**: Currently, LibreChat runs without any modified configurations, i.e. no models or MCP servers are connected. 
The configuration files as well as documentation will be added soon.

**Note**: A separate file `.env.librechat` contains the environmental variables needed for LibreChat. They do not contain private secrets and do not have to be modified.

## Troubleshooting

### WSL Segmentation Errors (Windows Users)

If you're running on Windows with WSL and encounter segmentation errors during `pdm install`, this is likely due to insufficient RAM allocation. Create a `.wslconfig` file in your Windows user directory (`C:\Users\[username]\.wslconfig`) with the following content:

```ini
[wsl2]
memory=8GB
processors=4
swap=2GB
```

Adjust the memory allocation based on your system's available RAM. After creating the file, restart WSL by running `wsl --shutdown` in PowerShell and then reopen your WSL terminal.

## Development Setup

For development purposes, you may want to set up the environment locally without Docker.

### Prerequisites for Development
- Have Python 3.11 or 3.12 installed
- Have [PDM installed](https://pdm-project.org/latest/) on your machine (In Windows open Command Prompt execute the following command to download PDM: powershell -ExecutionPolicy ByPass -c "irm https://pdm-project.org/install-pdm.py | py -" Restart PC afterwards)
- Have java installed (if you have attended the d-fine Basic IT training during onboarding you should already have it). It is recommended to use the [IntelliJ IdeA Community Edition](https://www.jetbrains.com/idea/download/?section=windows).
- Have [Visual Studio Code](https://code.visualstudio.com/Download) or [PyCharm Community Edition](https://www.jetbrains.com/pycharm/?msclkid=3f565bed393b11c2a1203379aceeab9a&utm_source=bing&utm_medium=cpc&utm_campaign=EMEA_en_DE_PyCharm_Search&utm_term=python%20coding%20tool&utm_content=python%20coding%20tool) installed.

Clone this repository to a designated folder via `git clone`.

### Dataland Client
- Create a `.env` file at the project root based on the `.env_dummy` file. Set Variable `DATALAND_MCP_ROOT_DIR` to the repository root on your machine and `DATALAND_API_KEY` with your API KEY that you can create as described [here](https://github.com/d-fine/Dataland/wiki/Use-the-API).
- Execute `.\bin\setup_dev_environment.sh` using a Git Bash shell from your repository root.

### Python MCP SDK
This repository utilizes the [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#installation) package. It should be installed already by the previous step. If not, install manually within the venv.
Check if the mcp package can be found under `.\.venv\Lib\site-packages\`

