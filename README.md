# DatalandMCP

This repository contains an MCP Server which allows LLMs to access data from Dataland.

## Table of contents
- [Prerequisites](#prerequisites-)
- [Dataland Client](#dataland-client-)
  - [Installation](#installation)
  - [Pyhon MCP SDK](#python-mcp-sdk)
- [Open WebUI](#open-webui)
  - [Installation](#installation-1)
  - [Launch](#launch)
  - [Connect with Azure OpenAI](#connect-with-azure-openai)
- [Run MCP Servers via mcpo](#run-mcp-servers-via-mcpo)
  - [Installation and Launch](#installation-and-launch)
  - [Connect to Open WebUI](#connect-to-open-webui)

## Prerequisites 
- Have Python 3.11 or 3.12 installed
- Have [PDM installed](https://pdm-project.org/latest/) on your machine (In Windows open Command Prompt execute the following command to download PDM: powershell -ExecutionPolicy ByPass -c "irm https://pdm-project.org/install-pdm.py | py -" Restart PC afterwards)
- Have java installed (if you have attended the d-fine Basic IT training during onboarding you should already have it). It is recommended to use the [IntelliJ IdeA Community Edition](https://www.jetbrains.com/idea/download/?section=windows).
- Have [Visual Studio Code](https://code.visualstudio.com/Download) or [PyCharm Community Edition](https://www.jetbrains.com/pycharm/?msclkid=3f565bed393b11c2a1203379aceeab9a&utm_source=bing&utm_medium=cpc&utm_campaign=EMEA_en_DE_PyCharm_Search&utm_term=python%20coding%20tool&utm_content=python%20coding%20tool) installed.
- Create a personal account on https://dataland.com and https://test.dataland.com
 
## Installation
Clone this repository to a designated folder via `git clone`

### Dataland Client
- Create a `.env` file at the project root based on the `.env_dummy` file. Set Variable `DATALAND_MCP_ROOT_DIR` to the repository root on your machine and `DATALAND_API_KEY` with your API KEY that you can create as described [here](https://github.com/d-fine/Dataland/wiki/Use-the-API).
- Execute `./bin/setup_dev_environment.sh` using a Git Bash shell

### Python MCP SDK
- This repository utilizes the [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#installation) package. It should be installed already by the previous step. If not, install manually within the venv.

## Open WebUI

[Open WebUI](https://github.com/open-webui/open-webui) is an MCP Client that allows user to run local LLMs as well as cloud based OpenAIs.

### Installation
- Open Powershell to install Open WebUI
- Choose a designated folder and create a virtual environment via `python -m venv /path/to/new/virtual/environment`. **Note, that it is only compatible with Python 3.11 & 3.12.**
- Activate it via `venv\Scripts\activate`
- Run the command `pip install open-webui`.


### Launch

- Run the command `open-webui serve` within the venv.
- After successful launch we can now open the UI via http://localhost:8080. For now, no model is connected to the UI; hence we will connect a model via Azure OpenAI.

<img width="1904" height="907" alt="Image" src="https://github.com/user-attachments/assets/de16630b-c70f-45d4-87ea-d6f4bfd91f5e" />

**Optional (Recommended):** 
Open WebUI support Xet storages, which avoids downloading files and models at every launch of the application, causing slow startups.
To use this functionality download the hf_xet package via `pip install hf_xet`

### Connect with Azure OpenAI

Open WebUI supports Azure OpenAI to connect the cloud based LLM.
Go to _Profile -> Admin Panel -> Settings -> Connections -> +_:

<img width="462" height="423" alt="Image" src="https://github.com/user-attachments/assets/4f30b1a1-6637-4d4c-bd0b-5561868c4098" />

In the above screenshot _[resource_name]_, _[deployment_name]_ and _[api_key]_ has to be replaced by the correct names defined in your Azure OpenAI resource.
The deployment name is the given name of the deployed model within the resource (e.g. _d-fine_azure_gpt-4.1_).

You should now be able to see the deployed model in the list of available models:

<img width="513" height="226" alt="Image" src="https://github.com/user-attachments/assets/7abca8c4-64df-41ee-bcba-eaae4c2d01da" />

## Run MCP Servers via mcpo

MCPO exposes any MCP Tool as an OpenAPI-compatible HTTP server. This is needed in our case. \
(**Note:** Resources (Templates) and Prompts are yet not implemented in mcpo but there is are open Pull Requests regarding Resources: [MCPO - Pull Requests](https://github.com/open-webui/mcpo/pulls))

### Installation and Launch

MCPO requires Python3.8+ and can be installed via `pip install mcpo`\
After successful installation you can set up a config file in the same format as for Claude Desktop or Cursor.

**Config Template:**
```
{
    "mcpServers": {
        "DatalandMCP": {
            "type": "stdio",
            "command": "path_to_dataland_venv\\Scirpts\\python.exe",
            "args": ["path_to_server\\server.py", "stdio"],
            "env": {
              "DATALAND_MCP_ROOT_DIR": "",
              "DATALAND_QARG_ROOT_DIR": "",
              "DATALAND_API_KEY": ""
          }
        }
    },
    "port": 8000
}
```

Within Powershell, launch the server via `mcpo --config mcp.json --port 8000 --host localhost`.

Now the server should be running. Its documentation (Swagger UI) should now be accessible via http://localhost:8000/DatalandMCP/docs.

### Connect to Open WebUI

Within Open WebUI you can now add the running server via `Profile -> Settings -> Tools -> +`:

<img width="453" height="240" alt="Image" src="https://github.com/user-attachments/assets/e09cbbd7-a3e6-4680-b89a-f93dad9d2bc8" />

Now the tools of the MCP Server are available in the chat via a toolbox under the input field:

<img width="658" height="327" alt="Image" src="https://github.com/user-attachments/assets/c7531e03-e0db-4994-b94d-ebdb171013cb" />

