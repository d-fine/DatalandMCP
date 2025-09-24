# DatalandMCP

This repository contains an MCP server that allows LLMs to access data from Dataland.
Additionally, the open-source chat clients [LibreChat](https://www.librechat.ai/) and [Open WebUI](https://docs.openwebui.com/) can be launched within this repository and serve as MCP hosts.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start with Docker Compose](#quick-start-with-docker-compose)
  - [Launch](#launch)
  - [Configure LibreChat](#configure-librechat)
  - [Configure Open WebUI](#configure-open-webui)
- [Troubleshooting](#troubleshooting)
- [Development Setup](#development-setup)
  - [Dataland Client](#dataland-client)
  - [Python MCP SDK](#python-mcp-sdk)

## Prerequisites
- Have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
- Create a personal account on https://dataland.com and https://test.dataland.com

## Quick Start with Docker Compose

The easiest way to get started is by using Docker Compose, which starts the MCP server and the MCP hosts (LibreChat and Open WebUI) with one command.

**Note**: LibreChat requires some configuration prior to launching the containers. See instructions [below](#configure-librechat). 

Create a `.env` file at the project root with your Dataland API key:
```env
DATALAND_API_KEY=your_api_key_here
```

You can create your API key as described [here](https://github.com/d-fine/Dataland/wiki/Use-the-API).

### Launch

From the repository root directory, start both the MCP server and hosts:

```bash
docker compose up
```

To run in the background:
```bash
docker compose up -d
```

To rebuild and start:
```bash
docker compose up --build
```

After successful launch:
- LibreChat will be available at http://localhost:3080
- Open WebUI will be available at http://localhost:8080
- MCP server documentation (Swagger UI) will be accessible at http://localhost:8000/DatalandMCP/docs

To stop the services:
```bash
docker compose down
```

**Note**: Open WebUI data (including user accounts, settings, and configurations) is persisted in a Docker volume named `datalandmcp_open-webui`. This means your Open WebUI setup will be preserved between container restarts. If you need to reset Open WebUI to a fresh state, you must explicitly delete this volume:

```bash
# Stop the services first
docker compose down

# Remove the Open WebUI volume to start fresh
docker volume rm datalandmcp_open-webui

# Start services again
docker compose up
```

The same holds for LibreChat, which uses several named volumes that contain user accounts and settings. Unlike Open WebUI, the base configuration of LibreChat (e.g., API connections) is set via a config file at the project root.

### Configure LibreChat

LibreChat can be configured via a `librechat.yaml` file in the project root. The DatalandMCP server is already configured. 
The following steps illustrate how to connect an Azure OpenAI model to LibreChat.

**Note**: A separate file `.env.librechat` contains the environment variables needed for LibreChat. They do not contain private secrets and do not need to be modified.

1. **Stop running containers**:
   ```bash
   docker compose down
   ```

2. **Add API key**: Add the `API_KEY` of the deployed model to the `.env` file:
   ```env
   AZURE_OPENAI_API_KEY=your_api_key_here
   ```

3. **Add model to config file**: Open the `librechat.yaml` file located in the project root. 
   Go to the `endpoints` object and uncomment the `azureOpenAI` configuration:
   ```yaml
   # Azure OpenAI connection
   endpoints:
     azureOpenAI:
       titleModel: "" # Change to the deployed model name in Azure, e.g. "d-fine-azure-gpt-5".
       plugins: True # Enables plugins
       groups:
         - group: "" # Arbitrary name, e.g. "dataland-group"
           apiKey: "${AZURE_OPENAI_API_KEY}" # Azure OpenAI API KEY from .env
           instanceName: "" # Azure resource name, e.g. "dataland-mcp-resource"
           version: "" # API version, e.g. "2024-12-01-preview"
           models:
             displayed-model-name: # Change to the deployed model name in Azure, e.g. "d-fine-azure-gpt-5".
               deploymentName: "" # Change to the deployed model name in Azure, e.g. "d-fine-azure-gpt-5".
               version: "" # API version same as above, e.g. "2024-12-01-preview"
   ```

   Fill out the configuration with the corresponding values of your deployed model.

4. **Add model specifications**: Within the `librechat.yaml` file, go to the `modelSpecs` object and uncomment the configuration.

   ```yaml
   # Model Specification
   modelSpecs:
     enforce: false
     prioritize: true
     list:
       - name: "dataland-mcp-gpt-X" # Unique identifier, change accordingly
         label: "Dataland Assistant (GPT-X)" # Displayed name, change accordingly
         default: true
         description: "Retrieves and analyzes ESG data from Dataland."
         preset:
           endpoint: "azureOpenAI"
           model: "your_model_here" # Model name of the configured endpoint below
           ...
   ```

   For `model` use the chosen name for `titleModel` from the previous step. Amend `name` and `label` according to the used GPT version.
   The other values must **not** be changed.

5. **Start the containers**:
   ```bash
   docker compose up -d
   ```
   **Note**: Initially, LibreChat may report that the connection to the MCP server has failed. This occurs because the LibreChat container starts more quickly than the DatalandMCP container; hence, the MCP server might not yet be running. As soon as the server is running, LibreChat will connect without requiring a container restart.
   
6. **Create a LibreChat account**: Navigate to http://localhost:3080 and create an account.
   
   <img width="1651" height="927" alt="image" src="https://github.com/user-attachments/assets/319b93d2-059c-40b5-b315-a0779f23efaf" />
   
7. **Select the Dataland MCP server**: Upon successful connection with the MCP server, a button will appear in the chat window. Select **Dataland** and start chatting.
   
   <img width="898" height="159" alt="image" src="https://github.com/user-attachments/assets/33eb9c13-df6d-44b5-8905-c2560325b1ba" />

### Configure Open WebUI

After the containers are running, you'll need to configure Open WebUI:

1. **Create an Open WebUI account**: Navigate to http://localhost:8080 and create an account.

    <img width="1904" height="907" alt="Image" src="https://github.com/user-attachments/assets/de16630b-c70f-45d4-87ea-d6f4bfd91f5e" />

2. **Connect with Azure OpenAI**: Open WebUI supports Azure OpenAI to connect cloud-based LLMs.
  Go to _Profile -> Admin Panel -> Settings -> Connections -> OpenAI API -> +_:

    <img width="462" height="418" alt="Image" src="https://github.com/user-attachments/assets/5e7e714e-6e7c-4e06-b1ec-91b42c1a9ff3" />

    In the above screenshot, replace _[resource_name]_, _[deployment_name]_, _[API_KEY]_, and _[API_VERSION]_ with the correct values defined in your Azure OpenAI resource.
The deployment name is the given name of the deployed model within the resource (e.g., _d-fine_azure_gpt-5_).

    You should now be able to see the deployed model in the list of available models and chat with it:

    <img width="513" height="226" alt="Image" src="https://github.com/user-attachments/assets/7abca8c4-64df-41ee-bcba-eaae4c2d01da" />

3. **Connect the MCP server**: Within Open WebUI, add the running MCP server via `Profile -> Settings -> Tools -> +`:

    <img width="453" height="240" alt="Image" src="https://github.com/user-attachments/assets/e09cbbd7-a3e6-4680-b89a-f93dad9d2bc8" />

    Now the tools of the MCP Server are available in the chat via a toolbox under the input field:

    <img width="658" height="327" alt="Image" src="https://github.com/user-attachments/assets/c7531e03-e0db-4994-b94d-ebdb171013cb" />

4. **Set the system prompt**: The system prompt defines the assistant's role. 
   - Within Open WebUI, go to `Profile` -> `Admin Panel` -> `Models`. Choose your model and go to the box `Model Parameters` -> `System Prompt`. 
   - Copy the prompt from the `system_prompt` file located in the project root and paste it into the box. 
   - Click on `Save & Update`.

   Note: You can also set the system prompt independently in your personal settings. Go to `Profile` -> `Settings` -> `General` and paste the prompt into the `System Prompt` field.

## Troubleshooting

### WSL Segmentation Errors (Windows Users)

If you're running on Windows with WSL and encounter segmentation faults during `pdm install`, this is likely due to insufficient RAM allocation. Create a `.wslconfig` file in your Windows user directory (`C:\Users\[username]\.wslconfig`) with the following content:

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
- Have [PDM installed](https://pdm-project.org/latest/) on your machine (on Windows, open Command Prompt and execute the following command to download PDM, then restart your PC):
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://pdm-project.org/install-pdm.py | py -"
  ```
- Have Java installed (if you have attended the d-fine Basic IT training during onboarding you should already have it). It is recommended to use the [IntelliJ IDEA Community Edition](https://www.jetbrains.com/idea/download/?section=windows).
- Have [Visual Studio Code](https://code.visualstudio.com/Download) or [PyCharm Community Edition](https://www.jetbrains.com/pycharm/) installed.

Clone this repository to a designated folder via `git clone`.

### Dataland Client
- Create a `.env` file at the project root based on the `.env.example` file. Set `DATALAND_MCP_ROOT_DIR` to the repository root on your machine and `DATALAND_API_KEY` to your API key (you can create one as described [here](https://github.com/d-fine/Dataland/wiki/Use-the-API)).
- Execute `.\bin\setup_dev_environment.sh` using a Git Bash shell from your repository root.
