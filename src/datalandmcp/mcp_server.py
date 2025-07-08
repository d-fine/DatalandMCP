#!\bin\bash
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

from datalandmcp.dataland_client import PRODUCTION_INSTANCE, DatalandClient
from dataland_backend.models.sfdr_data import SfdrData
from dataland_backend.models.data_type_enum import DataTypeEnum

DatalandClient.set_global_client(PRODUCTION_INSTANCE.client)
client=DatalandClient.get_global_client()

# Create an MCP server
mcp = FastMCP("DatalandMCP")


@mcp.tool()
def get_sfdr_data(company_name: str, fiscal_year: str) -> SfdrData:
    """
    Retrieve the SFDR reports for a given company name and fiscal year.
    """
    company = client.company_api.get_companies(search_string=company_name, data_types=[DataTypeEnum.SFDR])[0]
    company_id = company.company_id
    # Fetch SFDR data
    sfdr_data = client.sfdr_api.get_all_company_sfdr_data(company_id=company_id, reporting_period=fiscal_year)[0].data
    return sfdr_data

@mcp.prompt(title="Data Format")
def data_request() -> list[base.Message]:
    """This prompt gives an additionally requests the LLM to present the data in table format."""
    return [base.UserMessage("Please present your findings in table format.")]


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()