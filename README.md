# DatalandMCP

This repository contains an MCP server that allows LLMs to access data from Dataland.
Additionally, the open-source chat client [LibreChat](https://www.librechat.ai/) can be launched within this repository and serve as the MCP host.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start with Docker Compose](#quick-start-with-docker-compose)
  - [Launch](#launch)
  - [Configure LibreChat](#configure-librechat)
- [Troubleshooting](#troubleshooting)
- [Development Setup](#development-setup)
  - [Dataland Client](#dataland-client)

## Prerequisites
- Have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
- Create a personal account on https://dataland.com and https://test.dataland.com

## Quick Start with Docker Compose

The easiest way to get started is by using Docker Compose, which starts the MCP server and LibreChat with one command.

**Note**: LibreChat requires some configuration prior to launching the service. See instructions [below](#configure-librechat). 

Create a `.env` file at the project root with your Dataland API key:
```env
DATALAND_API_KEY=your_api_key_here
```

You can create your API key as described [here](https://github.com/d-fine/Dataland/wiki/Use-the-API).

### Launch

From the repository root directory, start both the MCP server and host:

```bash
./deployment/local_deployment.sh --profile all
```

After successful launch:
- LibreChat will be available at http://localhost:3080
- DatalandMCP server streams via http://localhost:8001/mcp
- MCP server documentation (Swagger UI) will be accessible at http://localhost:8000/DatalandMCP/docs

To stop the services:
```bash
docker compose --profile all down
```

#### Startup Options

There are three different profiles to only launch and stop specific services. These can be triggered via the `--profile` flag. 

| `--profile` | DatalandMCP | LibreChat |
|:------------|:-----------:|:---------:|
| `mcp`       |      ✅      |     ❌     |
| `librechat` |      ❌      |     ✅     |
| `all`       |      ✅      |     ✅     |

#### Docker Volumes (User data, configurations, ...)

LibreChat stores specific data (e.g. user accounts) in volumes that are preserved between service restarts.

```bash
# List all volumes
docker volume ls

# Stop the services first
docker compose --profile all down

# Remove specific volumes to start fresh
docker volume rm <volume-name1> <volume_name2>

# Start services again
./deployment/local_deployment.sh --profile all
```

### Configure LibreChat

LibreChat can be configured via a `librechat.yaml` file in the project root. 

**Note**: A separate file `.env.librechat` contains the environment variables needed for LibreChat. They do not contain private secrets and do not need to be modified.

The DatalandMCP server is already configured in LibreChat which expects the server to run on port 8001.
Using other ports will require to amend the port also in the `librechat.yaml` file.

```yaml
# DatalandMCP Server Connection
mcpServers:
  Dataland:
    type: http
    url: http://host.docker.internal:8001/mcp
    timeout: 60000
```

The following steps illustrate how to connect an Azure OpenAI model to LibreChat.

1. **Stop running services**:
   ```bash
   docker compose --profile librechat down
   ```

2. **Add API key**: Add the `API_KEY` of the deployed model to the `.env` file:
   ```env
   AZURE_OPENAI_API_KEY=your_api_key_here
   ```

3. **Add model to config file**: Open the `librechat.yaml` file located in the project root. 
   Go to the `endpoints` object and uncomment the `azureOpenAI` configuration:
   ```yaml
   # Azure OpenAI configuration
   endpoints:
     azureOpenAI:
       titleModel: "" # Name of the deployed model in Azure, e.g. "d-fine-azure-gpt-5".
       groups:
         - group: "" # Arbitrary name, e.g. "dataland-group"
           apiKey: "${AZURE_OPENAI_API_KEY}" # Azure OpenAI API KEY from .env
           instanceName: "" # Azure resource name, e.g. "dataland-mcp-resource"
           version: "" # API version, e.g. "2024-12-01-preview"
           models:
             displayed-model-name: # Change to name of the deployed model in Azure, e.g. "d-fine-azure-gpt-5".
               deploymentName: "" # Name of the deployed model in Azure, e.g. "d-fine-azure-gpt-5".
               version: "" # API version same as above, e.g. "2024-12-01-preview"
   ```

   Fill out the configuration with the corresponding values of your deployed model. Note that the `displayed-model-name` key also needs to be changed to your model name.

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

   For `model` use the name of the deployed model (`titleModel` from the previous step). Amend `name` and `label` according to the used GPT version.
   The other values must **not** be changed.

5. **Start the services**:
   ```bash
   ./deployment/local_deployment.sh --profile librechat
   ```
   **Note**: Initially, LibreChat may report that the connection to the MCP server has failed. This occurs because the LibreChat service starts more quickly than the DatalandMCP service; hence, the MCP server might not yet be running. As soon as the server is running, LibreChat will connect without requiring a restart.
   
6. **Create a LibreChat account**: Navigate to http://localhost:3080 and create an account.
   
   <img width="1651" height="927" alt="image" src="https://github.com/user-attachments/assets/319b93d2-059c-40b5-b315-a0779f23efaf" />
   
7. **Select the Dataland MCP server**: Upon successful connection with the MCP server, a button will appear in the chat window. Select **Dataland** and start chatting.
   
   <img width="898" height="159" alt="image" src="https://github.com/user-attachments/assets/33eb9c13-df6d-44b5-8905-c2560325b1ba" />

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
