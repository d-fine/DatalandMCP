"""
This is the main module running the MCP Server.
It has to be run by the MCP Client.
"""

__version__ = '0.0.1'

from typing import List, Union
from pydantic import BaseModel

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

from datalandmcp.dataland_client import PRODUCTION_INSTANCE, DatalandClient
from dataland_backend.models.sfdr_data import SfdrData
from dataland_backend.models.data_type_enum import DataTypeEnum

DatalandClient.set_global_client(PRODUCTION_INSTANCE.client)
client=DatalandClient.get_global_client()

# Create an MCP server
mcp = FastMCP("DatalandMCP")

## Helper Functions

def get_eu_taxonomy_data(company_name: str, reporting_period: str) -> List[BaseModel]:
    """Retrieve all Taxonomy data for a given company name and fiscal year from Dataland."""
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

def fetch_sfdr_report(company_name: str, reporting_period: str) -> SfdrData:
    """Retrieve the SFDR emissions data for a given company name and fiscal year from Dataland."""
    try:
        company_data = client.company_api.get_companies(search_string=company_name, data_types=[DataTypeEnum.SFDR])
    except Exception as exc:
        raise Exception(f'Error retrieving company data for {company_name}: {str(exc)}!')
    if not company_data:
        raise Exception(f'No company was found under the name {company_name} in Dataland!')
    else:
        company_id = company_data[0].company_id
    try:
        sfdr_data = client.sfdr_api.get_all_company_sfdr_data(company_id=company_id, reporting_period=reporting_period)
    except Exception as exc:
        raise Exception(f'Error retrieving SFDR data for {company_name} and reporting period {reporting_period}: {str(exc)}!')
    if not sfdr_data:
        raise Exception(f'No SFDR data was found for reporting period {reporting_period} for company {company_name} in Dataland!')
    else:
        return sfdr_data[0].data

# Currently not used
def fetch_sfdr_reports(company_names: List[str], reporting_periods: List[str]) -> List[Union[SfdrData, str]]:
    """Fetch SFDR reports for given list of company names and reporting periods."""
    sfdr_reports: list = []
    for company_name in company_names:
        for reporting_period in reporting_periods:
            try:
                sfdr_data = fetch_sfdr_report(company_name, reporting_period)
            except Exception as exc:
                sfdr_data = str(exc)
            sfdr_reports.append(sfdr_data)
    return sfdr_reports


## MCP TOOLS

@mcp.tool(name="SFDR_Report")
def get_sfdr_report(company_name: str, reporting_period: str):# -> List[SfdrData]:
    """
    Retrieve the SFDR report for a given company and reporting period from Dataland.
    These include Scope 1-3 Greenhouse gas emissions.

    :param company_name: Name of the company for which the SFDR report is retrieved.
    :param reporting_period: Reporting period of the SFDR report.
    :return: Returns sfdr_data BaseModel object for the given company and reporting period.
    """
    return fetch_sfdr_report(company_name, reporting_period)

@mcp.tool(name="Scope1_GHG_Data")
def get_scope1_ghg_emissions(company_name: str, fiscal_year: str):# -> Union[ExtendedDataPointBigDecimal, str]:
    """
    Retrieve the SFDR Scope 1 Greenhouse gas emissions data in tonnes CO2 for a given company name and fiscal year from Dataland.

    :param company_name: Name of the company for which the SFDR report is retrieved.
    :param fiscal_year: Reporting year of the SFDR report.
    :return: Returns the scope1_ghg_emissions_in_tonnes object for the given company and fiscal year.
    """
    try:
        sfdr_data = fetch_sfdr_report(company_name=company_name, reporting_period=fiscal_year)
    except Exception as exc:
        return str(exc)
    else:
        return sfdr_data.environmental.greenhouse_gas_emissions.scope1_ghg_emissions_in_tonnes

@mcp.tool(name="Scope2_GHG_Location_Data")
def get_scope2_ghg_location_emissions(company_name: str, fiscal_year: str):# -> Union[ExtendedDataPointBigDecimal, str]:
    """
    Retrieve the SFDR location-based Scope 2 Greenhouse gas emissions data in tonnes CO2 for a given company name and fiscal year from Dataland.
    If the user generically asks for Scope 2 emissions, the location-based and market-based data should be returned.

    :param company_name: Name of the company for which the SFDR report is retrieved.
    :param fiscal_year: Reporting year of the SFDR report.
    :return: Returns the scope2_ghg_emissions_location_based_in_tonnes object for the given company and fiscal year.
    """
    try:
        sfdr_data = fetch_sfdr_report(company_name=company_name, reporting_period=fiscal_year)
    except Exception as exc:
        return str(exc)
    else:
        return sfdr_data.environmental.greenhouse_gas_emissions.scope2_ghg_emissions_location_based_in_tonnes

@mcp.tool(name="Scope2_GHG_Market_Data")
def get_scope2_ghg_market_emissions(company_name: str, fiscal_year: str):# -> Union[ExtendedDataPointBigDecimal, str]:
    """
    Retrieve the SFDR market-based Scope 2 Greenhouse gas emissions data in tonnes CO2 for a given company name and fiscal year from Dataland.
    If the user generically asks for Scope 2 emissions, the location-based and market-based data should be returned.

    :param company_name: Name of the company for which the SFDR report is retrieved.
    :param fiscal_year: Reporting year of the SFDR report.
    :return: Returns the scope2_ghg_emissions_market_based_in_tonnes object for the given company and fiscal year.
    """
    try:
        sfdr_data = fetch_sfdr_report(company_name=company_name, reporting_period=fiscal_year)
    except Exception as exc:
        return str(exc)
    else:
        return sfdr_data.environmental.greenhouse_gas_emissions.scope2_ghg_emissions_market_based_in_tonnes

@mcp.tool(name="Scope3_GHG_Data")
def get_scope3_ghg_emissions(company_name: str, fiscal_year: str):# -> Union[ExtendedDataPointBigDecimal, str]:
    """
    Retrieve the SFDR Scope 3 Greenhouse gas emissions data in tonnes CO2 for a given company name and fiscal year from Dataland.

    :param company_name: Name of the company for which the SFDR report is retrieved.
    :param fiscal_year: Reporting year of the SFDR report.
    :return: Returns the scope3_ghg_emissions_in_tonnes object for the given company and fiscal year.
    """
    try:
        sfdr_data = fetch_sfdr_report(company_name=company_name, reporting_period=fiscal_year)
    except Exception as exc:
        return str(exc)
    else:
        return sfdr_data.environmental.greenhouse_gas_emissions.scope3_ghg_emissions_in_tonnes

@mcp.tool(name="Scope3_GHG_down_Data")
def get_scope3_ghg_downstream_emissions(company_name: str, fiscal_year: str):# -> Union[ExtendedDataPointBigDecimal, str]:
    """
    Retrieve the SFDR downstream Scope 3 Greenhouse gas emissions data in tonnes CO2 for a given company name and fiscal year from Dataland.

    :param company_name: Name of the company for which the SFDR report is retrieved.
    :param fiscal_year: Reporting year of the SFDR report.
    :return: Returns the scope3_downstream_ghg_emissions_in_tonnes object for the given company and fiscal year.
    """
    try:
        sfdr_data = fetch_sfdr_report(company_name=company_name, reporting_period=fiscal_year)
    except Exception as exc:
        return str(exc)
    else:
        return sfdr_data.environmental.greenhouse_gas_emissions.scope3_downstream_ghg_emissions_in_tonnes

@mcp.tool(name="Scope3_GHG_up_Data")
def get_scope3_ghg_upstream_emissions(company_name: str, fiscal_year: str):# -> Union[ExtendedDataPointBigDecimal, str]:
    """
    Retrieve the SFDR upstream Scope 3 Greenhouse gas emissions data in tonnes CO2 for a given company name and fiscal year from Dataland.

    :param company_name: Name of the company for which the SFDR report is retrieved.
    :param fiscal_year: Reporting year of the SFDR report.
    :return: Returns the scope3_upstream_ghg_emissions_in_tonnes object for the given company and fiscal year.
    """
    try:
        sfdr_data = fetch_sfdr_report(company_name=company_name, reporting_period=fiscal_year)
    except Exception as exc:
        return str(exc)
    else:
        return sfdr_data.environmental.greenhouse_gas_emissions.scope3_upstream_ghg_emissions_in_tonnes

@mcp.tool(name="Taxonomy_Report")
def get_taxonomy_data(company_name: str, fiscal_year: str):# -> List[BaseModel]:
    """
    Retrieve the EU Taxonomy data for a given company name and fiscal year from Dataland.

    :param company_name: Name of the company for which the Taxonomy reports are retrieved.
    :param fiscal_year: Reporting year of the Taxonomy reports.
    :return: Returns a list of taxonomy reports for the given company and fiscal year.
    """
    return get_eu_taxonomy_data(company_name=company_name, reporting_period=fiscal_year)


## Prompts and Resources - for now not used

# @mcp.prompt(title="Data Format")
# def data_request() -> list[base.Message]:
#     """This prompt gives an additionally requests the LLM to present the data in table format."""
#     return [base.UserMessage("Please present your findings in table format.")]
#
# # Add a dynamic greeting resource
# @mcp.resource("greeting://{name}")
# def get_greeting(name: str) -> str:
#     """Get a personalized greeting"""
#     return f"Hello, {name}!"
#
# # Add a resource
# @mcp.resource("data://sfdr/adidas")
# def get_adidas_sfdr_data() -> SfdrData:
#     """Get the SFDR data for adidas containing all emissions data for 2024."""
#     return retrieve_sfdr_data("Adidas", "2024")
#
# @mcp.resource("data://sfdr/basf")
# def get_basf_sfdr_data() -> SfdrData:
#     """Get the SFDR data for BASF containing all emissions data for 2023."""
#     return retrieve_sfdr_data("BASF", "2023")

if __name__ == "__main__":
    mcp.run(transport="stdio")