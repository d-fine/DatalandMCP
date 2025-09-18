"""This is a helper module containing helper functions for the server."""

from typing import Union, Dict, List, Callable

from pydantic import BaseModel

from dataland_client import DatalandClient
from dataland_backend.models.sfdr_data import SfdrData
from dataland_backend.models.eutaxonomy_financials_data import EutaxonomyFinancialsData
from dataland_backend.models.eutaxonomy_non_financials_data import EutaxonomyNonFinancialsData
from dataland_backend.models.nuclear_and_gas_data import NuclearAndGasData
from dataland_backend.models.data_type_enum import DataTypeEnum
from dataland_backend.models.qa_status import QaStatus


class DatalandMCPUtils:

    def __init__(self, client: DatalandClient):
        self.client: DatalandClient = client
        self.report_dispatch: Dict[DataTypeEnum, Callable[..., BaseModel]] = {
            DataTypeEnum.SFDR: self.client.sfdr_api.get_all_company_sfdr_data,
            DataTypeEnum.EUTAXONOMY_MINUS_FINANCIALS: self.client.eu_taxonomy_fin_api.get_all_company_eutaxonomy_financials_data,
            DataTypeEnum.EUTAXONOMY_MINUS_NON_MINUS_FINANCIALS: self.client.eu_taxonomy_nf_api.get_all_company_eutaxonomy_non_financials_data,
            DataTypeEnum.NUCLEAR_MINUS_AND_MINUS_GAS: self.client.eu_taxonomy_nuclear_gas_api.get_all_company_nuclear_and_gas_data,
        }

    def get_company_id(self, company_name: str) -> str:
        """
        Fetches the Dataland internal company identifier for a given company name.

        :param company_name: The name of the company as a string, e.g. "BASF SE"

        :return: The unique company identifier used in Dataland.
        :raises Exception: If no company was found or an unexpected error occurred.
        """
        company_data = self.client.company_api.get_companies(search_string=company_name)

        if not company_data:
            raise ValueError(f"No company found with name '{company_name}' in Dataland")

        return company_data[0].company_id

    def get_available_company_reports(
            self,
            company_name: str) ->  List[Dict[str, Union[str, DataTypeEnum]]]:
        """
        Retrieves a list of the available reports and its metadata for a given company.

        :param company_name: Name of the company for which the available reports are retrieved, e.g. "BASF SE".

        :return: Returns a list of data types and reporting periods of the available reports if the company is found,
        :raises Exception: If no meta_data was found or an unexpected error occurred.
        """
        company_id = self.get_company_id(company_name=company_name)
        meta_data = self.client.meta_api.get_list_of_data_meta_info(
            company_id=company_id,
            show_only_active=True,
            qa_status=QaStatus.ACCEPTED)

        if not meta_data:
            raise ValueError(f"No meta information was found for the company {company_name} in Dataland!")
        else:
            available_reports = []
            for report in meta_data:
                available_reports.append({
                    "dataType": report.data_type,
                    "reportingPeriod": report.reporting_period,
                })
            return available_reports

    def get_report_data(
            self,
            company_name: str,
            reporting_period: str,
            data_type: DataTypeEnum) -> Dict[str, Union[SfdrData, EutaxonomyFinancialsData, EutaxonomyNonFinancialsData, NuclearAndGasData]]:
        """
        Fetches the Dataland reports data for a given company name, reporting period and data framework (SFDR, EU Taxonomy,...).
        Calls the respective GET-Endpoint of Dataland API via the REPORT_DISPATCH.

        :param company_name: Name of the company for which the SFDR report is retrieved, e.g. "BASF SE".
        :param reporting_period: The fiscal year of the published report as a string, e.g. "2024".
        :param data_type: The type of reporting framework, e.g. DataTypeEnum.SFDR.

        :return: The report data and source URL for the given company name, reporting period and data framework.
        :raises Exception: If no company or report was found or an unexpected error occurred.
        """
        company_id = self.get_company_id(company_name=company_name)
        report_data = self.report_dispatch[data_type](company_id=company_id, reporting_period=reporting_period)

        if not report_data:
            raise ValueError(
                f"No {data_type.value} data found in Dataland for "
                f"reporting period {reporting_period} and company '{company_name}'"
            )

        data_url = self.construct_data_url(
            company_id=company_id,
            reporting_period=reporting_period,
            data_type=data_type,
        )
        return {"data_url": data_url, "report_data": report_data}

    @staticmethod
    def construct_data_url(company_id: str, reporting_period: str, data_type: DataTypeEnum) -> str:
        """
        Construct a link to the Dataland website which should be provided as a source of the retrieved reports.

        :param company_id: The unique identifier of a company used in Dataland.
        :param reporting_period: The fiscal year of the published report as a string, e.g. "2024".
        :param data_type: The type of reporting framework, e.g. DataTypeEnum.SFDR.

        :return: Constructed Dataland URL of the given company, data framework and reporting period.
        """
        return f"https://dataland.com/companies/{company_id}/frameworks/{data_type.value}/reportingPeriods/{reporting_period}"
