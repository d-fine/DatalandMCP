"""This module contains the Dataland MCP server and its defined tools."""

from typing import Optional, Dict, Union

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from dataland_client import DatalandClient
from server_utils import DatalandMCPUtils
from dataland_backend.models.sfdr_data import SfdrData
from dataland_backend.models.eutaxonomy_financials_data import EutaxonomyFinancialsData
from dataland_backend.models.eutaxonomy_non_financials_data import EutaxonomyNonFinancialsData
from dataland_backend.models.nuclear_and_gas_data import NuclearAndGasData
from dataland_backend.models.data_type_enum import DataTypeEnum


class DatalandMCPServer:

    def __init__(self, client: DatalandClient):
        self.client: DatalandClient = client
        self.app = FastMCP("DatalandMCP")
        self.utils: DatalandMCPUtils = DatalandMCPUtils(self.client)
        self._register_tools()
        self._register_custom_routes()

    def run(self, transport: str = "stdio", host: Optional[str] = "0.0.0.0", port: Optional[int] = 8001) -> None:
        """
        Run the MCP server.

        :param transport: Transport type (http, streamable-http, stdio). Default is stdio.
        :param host: Host of URL. Only used for http, streamable-http transport.
        :param port: Port of URL. Only used for http, streamable-http transport.
        """
        t = (transport or "").strip().lower()
        if t in {"http", "streamable-http"}:
            self.app.run(transport="streamable-http", host=host, port=port)
        else:
            # stdio mode: no host/port
            self.app.run(transport="stdio")

    def _register_tools(self):
        """Register tools for the Dataland MCP Server."""
        self.app.tool(name="Company_Available_Reports")(self._get_company_available_reports)
        self.app.tool(name="SFDR_Report")(self._get_sfdr_data)
        self.app.tool(name="EU_Taxonomy_Financial_Report")(self._get_eu_fin_taxonomy_data)
        self.app.tool(name="EU_Taxonomy_Non_Financial_Report")(self._get_eu_nf_taxonomy_data)
        self.app.tool(name="EU_Taxonomy_Nuclear_Gas_Report")(self._get_eu_nuclear_gas_taxonomy_data)

    def _register_custom_routes(self):
        """Register custom routes to perform health checks."""
        self.app.custom_route("/health", methods=["GET"])(self._health_check)

    def _get_company_available_reports(self, company_name: str):
        """
        Retrieves a list of the available reports and its metadata for a given company from Dataland.
        It contains the active and accepted reports of all available frameworks and reporting periods.

        :param company_name: Name of the company for which the SFDR report is retrieved, e.g. "BASF SE".

        :return: Returns a list of data types and reporting periods of the available reports if the company is found,
        otherwise an Exception string.
        """
        try:
            available_reports = self.utils.get_available_company_reports(company_name=company_name)
        except Exception as exc:
            return str(exc)
        else:
            return available_reports

    def _get_sfdr_data(self, company_name: str, reporting_period: str) -> Union[str, Dict[str, SfdrData]]:
        """
        Retrieves the SFDR data for a given company name and reporting period from Dataland.
        This data refers to the environmental, social, and governance (ESG) metrics and
        disclosures required by EU regulations

        :param company_name: Name of the company for which the SFDR report is retrieved, e.g. "BASF SE".
        :param reporting_period: The fiscal year of the SFDR report as a string, e.g. "2024".

        :return: The SFDR data for the given company name and reporting period if found, otherwise an Exception string.
        """
        try:
            sfdr_data = self.utils.get_report_data(
                company_name=company_name,
                reporting_period=reporting_period,
                data_type=DataTypeEnum.SFDR
            )
        except Exception as exc:
            return str(exc)
        else:
            return sfdr_data

    def _get_eu_fin_taxonomy_data(self, company_name: str, reporting_period: str) -> Union[str, Dict[str, EutaxonomyFinancialsData]]:
        """
        Retrieves the EU Taxonomy data of financial companies for a given company name and
        reporting period from Dataland. It encompasses disclosures on how financial products manage
        environmental, social, and governance (ESG) risks and adverse sustainability impacts.

        :param company_name: Name of the financial company for which the Taxonomy report is retrieved, e.g. "Allianz SE".
        :param reporting_period: The fiscal year of the Taxonomy report as a string, e.g. "2024".

        :return: The financial Taxonomy data for the given company name and reporting period if found,
        otherwise an Exception string.
        """
        try:
            tax_fin_data = self.utils.get_report_data(
                company_name=company_name,
                reporting_period=reporting_period,
                data_type=DataTypeEnum.EUTAXONOMY_MINUS_FINANCIALS
            )
        except Exception as exc:
            return str(exc)
        else:
            return tax_fin_data

    def _get_eu_nf_taxonomy_data(self, company_name: str, reporting_period: str) -> Union[str, Dict[str, EutaxonomyNonFinancialsData]]:
        """
        Retrieves the EU Taxonomy data of non-financial companies for a given company name and
        reporting period from Dataland. It encompasses disclosures on how financial products manage
        environmental, social, and governance (ESG) risks and adverse sustainability impacts.

        :param company_name: Name of the non-financial company for which the Taxonomy report is retrieved, e.g. "BASF SE".
        :param reporting_period: The fiscal year of the Taxonomy report as a string, e.g. "2024".

        :return: The non-financial Taxonomy data for the given company name and reporting period if found,
        otherwise an Exception string.
        """
        try:
            tax_nf_data = self.utils.get_report_data(
                company_name=company_name,
                reporting_period=reporting_period,
                data_type=DataTypeEnum.EUTAXONOMY_MINUS_NON_MINUS_FINANCIALS
            )
        except Exception as exc:
            return str(exc)
        else:
            return tax_nf_data

    def _get_eu_nuclear_gas_taxonomy_data(self, company_name: str, reporting_period: str) -> Union[str, Dict[str, NuclearAndGasData]]:
        """
        Retrieves the EU Nuclear and Gas Taxonomy data for a given company name and reporting period from Dataland.
        It outlines the inclusion of nuclear energy and natural gas as transitional activities,
        provided they meet strict criteria such as safety, emissions thresholds.

        :param company_name: Name of the company for which the nuclear and gas Taxonomy report is retrieved, e.g. "BASF SE".
        :param reporting_period: The fiscal year of the Taxonomy report as a string, e.g. "2024".

        :return: The nuclear and gas Taxonomy data for the given company name and reporting period if found,
        otherwise an Exception string.
        """
        try:
            tax_nuclear_gas_data = self.utils.get_report_data(
                company_name=company_name,
                reporting_period=reporting_period,
                data_type=DataTypeEnum.NUCLEAR_MINUS_AND_MINUS_GAS
            )
        except Exception as exc:
            return str(exc)
        else:
            return tax_nuclear_gas_data

    @staticmethod
    async def _health_check(request: Request) -> Response:
        """This custom route is used to perform health checks on the server."""
        return JSONResponse({"status": "healthy", "service": "DatalandMCP"})
