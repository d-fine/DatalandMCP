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
from dataland_backend.models.eutaxonomy_financials_data import EutaxonomyFinancialsData
from dataland_backend.models.eutaxonomy_non_financials_data import EutaxonomyNonFinancialsData
from dataland_backend.models.nuclear_and_gas_data import NuclearAndGasData
from dataland_backend.models.data_type_enum import DataTypeEnum
from dataland_backend.models.qa_status import QaStatus

DatalandClient.set_global_client(PRODUCTION_INSTANCE.client)
client=DatalandClient.get_global_client()

# Create an MCP server
dataland_mcp = FastMCP("DatalandMCP")

REPORT_DISPATCH = {
    DataTypeEnum.SFDR: client.sfdr_api.get_all_company_sfdr_data,
    DataTypeEnum.EUTAXONOMY_MINUS_FINANCIALS: client.eu_taxonomy_fin_api.get_all_company_eutaxonomy_financials_data,
    DataTypeEnum.EUTAXONOMY_MINUS_NON_MINUS_FINANCIALS: client.eu_taxonomy_nf_api.get_all_company_eutaxonomy_non_financials_data,
    DataTypeEnum.NUCLEAR_MINUS_AND_MINUS_GAS: client.eu_taxonomy_nuclear_gas_api.get_all_company_nuclear_and_gas_data,
}

def get_company_id(company_name: str) -> str:
    """
    Fetches the Dataland internal company identifier for a given company name.

    :param company_name: The name of the company as a string, e.g. "BASF SE"

    :return: The unique company identifier used in Dataland.
    :raises Exception: If no company was found or an unexpected error ocurred.
    """
    try:
        company_data = client.company_api.get_companies(search_string=company_name)
    except Exception as exc:
        raise Exception(f'Error retrieving company data for {company_name}: {str(exc)}!')
    if not company_data:
        raise Exception(f'No company was found under the name {company_name} in Dataland!')
    else:
        return company_data[0].company_id

def get_report_data(
        company_name: str,
        reporting_period: str,
        data_type: DataTypeEnum) -> Union[SfdrData, EutaxonomyFinancialsData, EutaxonomyNonFinancialsData, NuclearAndGasData]:
    """
    Fetches the Dataland reports data for a given company name, reporting period and data framework (SFDR, EU Taxonomy,...).
    Calls the respective GET-Endpoint of Dataland API via the REPORT_DISPATCH.

    :param company_name: Name of the company for which the SFDR report is retrieved, e.g. "BASF SE".
    :param reporting_period: The fiscal year of the published report as a string, e.g. "2024".
    :param data_type: The type of reporting framework, e.g. DataTypeEnum.SFDR.

    :return: The report data for the given company name, reporting period and data framework.
    :raises Exception: If no company or report was found or an unexpected error ocurred.
    """
    try:
        company_id = get_company_id(company_name=company_name)
    except Exception as exc:
        raise Exception(exc)
    try:
        report_data = REPORT_DISPATCH[data_type](company_id=company_id, reporting_period=reporting_period)
    except Exception as exc:
        raise Exception(exc)
    if not report_data:
        raise Exception(f'No {data_type.value} data was found for reporting period {reporting_period} for company {company_name} in Dataland!')
    else:
        return report_data

## MCP TOOLS

@dataland_mcp.tool(name="Company_Available_Reports")
def get_company_available_reports(company_name: str):
    """
    Retrieves a list of the available reports and its metadata for a given company.
    It contains the active and accepted reports of all available frameworks and reporting periods.

    :param company_name: Name of the company for which the SFDR report is retrieved, e.g. "BASF SE".

    :return: Returns a list of DataMetaInformation Objects of the available reports.
    :raises Exception: If no company or report was found or an unexpected error ocurred.
    """
    try:
        company_id = get_company_id(company_name=company_name)
    except Exception as exc:
        return str(exc)
    else:
        try:
            meta_data = client.meta_api.get_list_of_data_meta_info(
                company_id=company_id,
                show_only_active=True,
                qa_status=QaStatus.ACCEPTED)
        except Exception as exc:
            raise Exception(exc)
    if not meta_data:
        raise Exception(
            f'No meta information was found for the company {company_name} in Dataland!')
    else:
        return meta_data


@dataland_mcp.tool(name="SFDR_Report")
def get_sfdr_report(company_name: str, reporting_period: str):# -> Union[SfdrData, str]:
    """
    Retrieves the SFDR report for a given company name and reporting period from Dataland.
    This data refers to the environmental, social, and governance (ESG) metrics and
    disclosures required by EU regulations

    :param company_name: Name of the company for which the SFDR report is retrieved, e.g. "BASF SE".
    :param reporting_period: The fiscal year of the SFDR report as a string, e.g. "2024".

    :return: The SFDR data for the given company name and reporting period if found, otherwise an Exception string.
    :raises Exception: If no company or report was found or an unexpected error ocurred.
    """
    try:
        sfdr_data = get_report_data(
            company_name=company_name,
            reporting_period=reporting_period,
            data_type=DataTypeEnum.SFDR
        )
    except Exception as exc:
        return str(exc)
    else:
        return sfdr_data

@dataland_mcp.tool(name="EU_Taxonomy_Financial_Report")
def get_eu_fin_taxonomy_data(company_name: str, reporting_period: str):# -> List[BaseModel]:
    """
    Retrieves the EU Taxonomy data of financial companies for a given company name and
    reporting period from Dataland. It encompasses disclosures on how financial products manage
    environmental, social, and governance (ESG) risks and adverse sustainability impacts.

    :param company_name: Name of the financial company for which the Taxonomy report is retrieved, e.g. "Allianz SE".
    :param reporting_period: The fiscal year of the Taxonomy report as a string, e.g. "2024".

    :return: The financial Taxonomy data for the given company name and reporting period if found,
    otherwise an Exception string.
    :raises Exception: If no company or report was found or an unexpected error ocurred.
    """
    try:
        tax_fin_data = get_report_data(
            company_name=company_name,
            reporting_period=reporting_period,
            data_type=DataTypeEnum.EUTAXONOMY_MINUS_FINANCIALS
        )
    except Exception as exc:
        return str(exc)
    else:
        return tax_fin_data

@dataland_mcp.tool(name="EU_Taxonomy_Non_Financial_Report")
def get_eu_nf_taxonomy_data(company_name: str, reporting_period: str):# -> List[BaseModel]:
    """
    Retrieves the EU Taxonomy data of non-financial companies for a given company name and
    reporting period from Dataland. It encompasses disclosures on how financial products manage
    environmental, social, and governance (ESG) risks and adverse sustainability impacts.


    :param company_name: Name of the non-financial company for which the Taxonomy report is retrieved, e.g. "BASF SE".
    :param reporting_period: The fiscal year of the Taxonomy report as a string, e.g. "2024".

    :return: The non-financial Taxonomy data for the given company name and reporting period if found,
    otherwise an Exception string.
    :raises Exception: If no company or report was found or an unexpected error ocurred.
    """
    try:
        tax_nf_data = get_report_data(
            company_name=company_name,
            reporting_period=reporting_period,
            data_type=DataTypeEnum.EUTAXONOMY_MINUS_NON_MINUS_FINANCIALS
        )
    except Exception as exc:
        return str(exc)
    else:
        return tax_nf_data

@dataland_mcp.tool(name="EU_Taxonomy_Nuclear_Gas_Report")
def get_eu_nulear_gas_taxonomy_data(company_name: str, reporting_period: str):# -> List[BaseModel]:
    """
    Retrieves the EU Nuclear and Gas Taxonomy data for a given company name and reporting period from Dataland.
    It outlines the inclusion of nuclear energy and natural gas as transitional activities,
    provided they meet strict criteria such as safety, emissions thresholds.

    :param company_name: Name of the company for which the nuclear and gas Taxonomy report is retrieved, e.g. "BASF SE".
    :param reporting_period: The fiscal year of the Taxonomy report as a string, e.g. "2024".

    :return: The nuclear and gas Taxonomy data for the given company name and reporting period if found,
    otherwise an Exception string.
    :raises Exception: If no company or report was found or an unexpected error ocurred.
    """
    try:
        tax_nuclear_gas_data = get_report_data(
            company_name=company_name,
            reporting_period=reporting_period,
            data_type=DataTypeEnum.NUCLEAR_MINUS_AND_MINUS_GAS
        )
    except Exception as exc:
        return str(exc)
    else:
        return tax_nuclear_gas_data


if __name__ == "__main__":
    dataland_mcp.run(transport="stdio")