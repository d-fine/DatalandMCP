"""
This is the main module running the MCP Server.
It has to be run by the MCP Client.
"""

__version__ = '0.0.1'

from typing import List
from pydantic import BaseModel

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

from datalandmcp.dataland_client import PRODUCTION_INSTANCE, DatalandClient
from dataland_backend.models.sfdr_data import SfdrData
from dataland_backend.models.sfdr_environmental import SfdrEnvironmentalGreenhouseGasEmissions
from dataland_backend.models.data_type_enum import DataTypeEnum

DatalandClient.set_global_client(PRODUCTION_INSTANCE.client)
client=DatalandClient.get_global_client()

# Create an MCP server
mcp = FastMCP("DatalandMCP")

def retrieve_sfdr_data(company_name: str, reporting_period: str) -> SfdrData:
    """Retrieve the SFDR emissions data for a given company name and fiscal year."""
    company = client.company_api.get_companies(search_string=company_name, data_types=[DataTypeEnum.SFDR])[0]
    company_id = company.company_id
    data = client.sfdr_api.get_all_company_sfdr_data(company_id=company_id, reporting_period=reporting_period)[0].data
    return data

def get_eu_taxonomy_data(company_name: str, reporting_period: str) -> List[BaseModel]:
    """Retrieve all Taxonomy data for a given company name and fiscal year."""
    company = client.company_api.get_companies(search_string=company_name, data_types=[DataTypeEnum.SFDR])[0]
    company_id = company.company_id
    eu_taxonomy_data = []
    if eu_taxonomy_nf_data := client.eu_taxonomy_nf_api.get_all_company_eutaxonomy_non_financials_data(company_id=company_id, reporting_period=reporting_period):
        eu_taxonomy_data.append(eu_taxonomy_nf_data[0].data)
    elif eu_taxonomy_fin_data := client.eu_taxonomy_fin_api.get_all_company_eutaxonomy_financials_data(company_id=company_id, reporting_period=reporting_period):
        eu_taxonomy_data.append(eu_taxonomy_fin_data[0].data)
    if eu_taxonomy_nuclear_and_gas_data := client.eu_taxonomy_nuclear_gas_api.get_all_company_nuclear_and_gas_data(company_id=company_id, reporting_period=reporting_period):
        eu_taxonomy_data.append(eu_taxonomy_nuclear_and_gas_data[0].data)
    return eu_taxonomy_data

@mcp.tool(name="Taxonomy_Report")
def get_taxonomy_data(company_name: str, fiscal_year: str) -> List[BaseModel]:
    """
    Retrieve the EU Taxonomy data for a given company name and fiscal year.

    :param company_name: Name of the company for which the Taxonomy reports are retrieved.
    :param fiscal_year: Reporting year of the Taxonomy reports.
    :return: Returns a list of taxonomy reports for the given company and fiscal year.
    """
    return get_eu_taxonomy_data(company_name=company_name, reporting_period=fiscal_year)

@mcp.tool(name="SFDR_Report")
def get_sfdr_data(company_name: str, fiscal_year: str) -> SfdrData:
    """
    Retrieve the SFDR Greenhouse gas emissions data for a given company name and fiscal year.

    :param company_name: Name of the company for which the SFDR report is retrieved.
    :param fiscal_year: Reporting year of the SFDR report.
    :return: Returns the sfdr_data BaseModel object for the given company and fiscal year.
    """
    return retrieve_sfdr_data(company_name, fiscal_year)

# This is implemented to return fewer data at once in case of comparing multiple reports
# Should be replaced by resources.
@mcp.tool(name="Emissions_Data")
def get_sfdr_greenhouse_gas_emissions(company_name: str, fiscal_year: str) -> SfdrEnvironmentalGreenhouseGasEmissions:
    """
    Retrieve the SFDR Greenhouse gas emissions data for a given company name and fiscal year.

    :param company_name: Name of the company for which the SFDR report is retrieved.
    :param fiscal_year: Reporting year of the SFDR report.
    :return: Returns the sfdr_data.environmental.greenhouse_gas_emissions BaseModel object for the given company and fiscal year.
    """
    sfdr_data = retrieve_sfdr_data(company_name=company_name, reporting_period=fiscal_year)
    return sfdr_data.environmental.greenhouse_gas_emissions

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