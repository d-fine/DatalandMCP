# DatalandMCP

This repository contains an MCP Server which connects Clients like Claude to Dataland.

### Prerequisites 
- Have a current Python version (>=3.10) installed
- Have [PDM installed](https://pdm-project.org/latest/) on your machine (In Windows open Command Prompt execute the following command to download PDM: powershell -ExecutionPolicy ByPass -c "irm https://pdm-project.org/install-pdm.py | py -" Restart PC afterwards)
- Have java installed (if you have attended the d-fine Basic IT training during onboarding you should already have it). It is recommended to use the [IntelliJ IdeA Community Edition](https://www.jetbrains.com/idea/download/?section=windows).
- Have Visual Studio Code installed: https://code.visualstudio.com/Download
- Create a personal account on https://dataland.com and https://test.dataland.com

## Installation 
### Dataland Client
- Create a `.env` file at root based on the `.env_dummy` file. Set Variable `DATALAND_MCP_ROOT_DIR` to the repository root on your machine and `DATALAND_API_KEY` with your API KEY that you can create as described [here](https://github.com/d-fine/Dataland/wiki/Use-the-API).
- Execute `./bin/setup_dev_environment.sh` using a Git Bash shell

### Python MCP SDK
- Install [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#installation) and add to the virtual environment (this can be done by installing the package within the venv)

### MCP Client - Claude Desktop
- In order to use the server we need an MCP Client like [Claude Desktop](https://claude.ai/download)
- Install it on your local machine and create an account

## Configuration
### Claude Desktop
- Now to connect Claude to the MCP Server we need to set up the configuration file `claude_desktop_config.json`
- The location of the config file can be found via the Claude Desktop Application: `Menu` -> `File` -> `Settings` -> `Developer` -> `Edit Config`
- Paste the content of `claude_config_dummy.json` into the file
  - `{project_root_dir}` has to be replaced by the repository root
  - The environmental variables have to be pasted from the `.env` file
- Save the config file and restart the Claude Desktop Application to apply the changes

After successful configuration the MCP Server should be shown as running under `Menu` -> `File` -> `Settings` -> `Developer`.

## Desktop Extensions
### TBA