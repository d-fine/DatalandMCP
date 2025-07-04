# DatalandMCP
### Prerequisites 
- Have Python 3.11 installed (please stick to version 3.11 and remove potentially installed other/higher versions (including restart), as they can lead to problems): You can download Python 3.11 from https://www.python.org/downloads/release/python-3110/
- Have PDM installed on your machine (In Windows open Command Prompt execute the following command to download PDM: powershell -ExecutionPolicy ByPass -c "irm https://pdm-project.org/install-pdm.py | py -" Restart PC afterwards)
- Have java installed (if you have attended the d-fine Basic IT training during onboarding you should already have it). It is recommended to use the [IntelliJ IdeA Community Edition](https://www.jetbrains.com/idea/download/?section=windows).
- Have Visual Studio Code installed: https://code.visualstudio.com/Download
- Create a personal account on https://dataland.com and https://test.dataland.com

### Installation
- Create a `.env` file at root based on the `.env_dummy` file. Set Variable `DATALAND_MCP_ROOT_DIR` the the repository root on your machine and `DATALAND_API_KEY` with your API KEY that you can create as described [here](https://github.com/d-fine/Dataland/wiki/Use-the-API).
- Execute `./bin/setup_dev_environment.sh` using a Git Bash shell