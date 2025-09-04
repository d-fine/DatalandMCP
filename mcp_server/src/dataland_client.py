"""Provides an intuitive accessor for authenticated dataland API Instances."""

from __future__ import annotations

import dataclasses
import os
import warnings
from urllib.parse import urljoin

import dataland_backend
import dataland_community
import dataland_documents
import dataland_qa
import dataland_users

_global_client: DatalandClient | None = None


class DatalandClient:  # noqa: PLR0904
    """Provides an intuitive accessor for authenticated dataland API Instances.

    Attributes:
        dataland_url (str): The Dataland URL determined by the is_test_dataland switch.
        api_key (str): The API Key to use for authenticating against dataland.
    """

    dataland_url: str
    api_key: str

    def __init__(self, dataland_url: str, api_key: str) -> None:
        """Create a new DatalandClient.

        Args:
            dataland_url: The URL of the dataland instance to connect to.
            api_key: The API Key to use for authenticating against dataland.
        """
        self.dataland_url = dataland_url
        self.api_key = api_key

    @staticmethod
    def get_global_client() -> DatalandClient:
        """Obtain the global dataland client.

        Defaults to the clone instance.
        """
        global _global_client  # noqa: PLW0603
        if _global_client is None:
            _global_client = PRODUCTION_INSTANCE.client
            warnings.warn(
                "No global dataland client set. Using the PRODUCTION Instance. "
                "Explicitly setting an instance should be strongly preferred.",
                UserWarning,
                stacklevel=2,
            )
        return _global_client

    @staticmethod
    def set_global_client(client: DatalandClient) -> None:
        """Set the global dataland client."""
        global _global_client  # noqa: PLW0603
        _global_client = client

    @property
    def backend_client(self) -> dataland_backend.ApiClient:
        """Retrieves the client for accessing the backend API."""
        config = dataland_backend.Configuration(access_token=self.api_key, host=urljoin(self.dataland_url, "api"))
        return dataland_backend.ApiClient(config)

    @property
    def company_api(self) -> dataland_backend.CompanyDataControllerApi:
        """Function to run the company-data-controller API."""
        return dataland_backend.CompanyDataControllerApi(self.backend_client)

    @property
    def documents_client(self) -> dataland_documents.ApiClient:
        """Retrieves the client for accessing the documents API."""
        config = dataland_documents.Configuration(
            access_token=self.api_key, host=urljoin(self.dataland_url, "documents")
        )
        return dataland_documents.ApiClient(config)

    @property
    def documents_api(self) -> dataland_documents.DocumentControllerApi:
        """Function to run the document-controller API."""
        return dataland_documents.DocumentControllerApi(self.documents_client)

    @property
    def datapoint_api(self) -> dataland_backend.DataPointControllerApi:
        """Funtion to run the data-point-controller API."""
        return dataland_backend.DataPointControllerApi(self.backend_client)

    @property
    def sfdr_api(self) -> dataland_backend.SfdrDataControllerApi:
        """Function to run the sfdr-data-controller API."""
        return dataland_backend.SfdrDataControllerApi(self.backend_client)

    @property
    def eu_taxonomy_nf_api(self) -> dataland_backend.EutaxonomyNonFinancialsDataControllerApi:
        """Function to run the eu-taxonomy-non-financials-data-controller API."""
        return dataland_backend.EutaxonomyNonFinancialsDataControllerApi(self.backend_client)

    @property
    def eu_taxonomy_fin_api(self) -> dataland_backend.EutaxonomyFinancialsDataControllerApi:
        """Function to run the eu-taxonomy-non-financials-data-controller API."""
        return dataland_backend.EutaxonomyFinancialsDataControllerApi(self.backend_client)

    @property
    def eu_taxonomy_nuclear_gas_api(self) -> dataland_backend.NuclearAndGasDataControllerApi:
        """Function to run the eu-taxonomy-nuclear-and-gas-data-controller API."""
        return dataland_backend.NuclearAndGasDataControllerApi(self.backend_client)

    @property
    def meta_api(self) -> dataland_backend.MetaDataControllerApi:
        """Function to run the meta-data-controller API."""
        return dataland_backend.MetaDataControllerApi(self.backend_client)

    @property
    def qa_client(self) -> dataland_qa.ApiClient:
        """Retrieves the client for accessing the qa API."""
        config = dataland_qa.Configuration(access_token=self.api_key, host=urljoin(self.dataland_url, "qa"))
        return dataland_qa.ApiClient(config)

    @property
    def community_client(self) -> dataland_community.ApiClient:
        """Retrieves the client for accessing the community API."""
        config = dataland_community.Configuration(
            access_token=self.api_key, host=urljoin(self.dataland_url, "community")
        )
        return dataland_community.ApiClient(config)

    @property
    def users_client(self) -> dataland_users.ApiClient:
        """Retrieves the client for accessing the users API."""
        config = dataland_users.Configuration(access_token=self.api_key, host=urljoin(self.dataland_url, "users"))
        return dataland_users.ApiClient(config)

    @property
    def qa_api(self) -> dataland_qa.QaControllerApi:
        """Function to run the qa-controller API."""
        return dataland_qa.QaControllerApi(self.qa_client)

    @property
    def data_point_qa_api(self) -> dataland_qa.DataPointQaReportControllerApi:
        """Function to run the data-point-qa-controller API."""
        return dataland_qa.DataPointQaReportControllerApi(self.qa_client)

    @property
    def sfdr_qa_api(self) -> dataland_qa.SfdrDataQaReportControllerApi:
        """Function to run the QA report controller for SFDR."""
        return dataland_qa.SfdrDataQaReportControllerApi(self.qa_client)

    @property
    def eu_taxonomy_nf_qa_api(self) -> dataland_qa.EutaxonomyNonFinancialsDataQaReportControllerApi:
        """Function to run the QA report controller for EU Taxonomy non-financials."""
        return dataland_qa.EutaxonomyNonFinancialsDataQaReportControllerApi(self.qa_client)

    @property
    def eu_taxonomy_fin_qa_api(self) -> dataland_qa.EutaxonomyFinancialsDataQaReportControllerApi:
        """Function to run the QA report controller for EU Taxonomy financials."""
        return dataland_qa.EutaxonomyFinancialsDataQaReportControllerApi(self.qa_client)

    @property
    def request_api(self) -> dataland_community.RequestControllerApi:
        """Function to run the request controller API."""
        return dataland_community.RequestControllerApi(self.community_client)

    @property
    def portfolio_api(self) -> dataland_users.PortfolioControllerApi:
        """Function to run the portfolio controller API."""
        return dataland_users.PortfolioControllerApi(self.users_client)


@dataclasses.dataclass(frozen=True)
class DatalandInstance:
    """A Dataland Instance refers to a specific Dataland environment.

    Attributes:
        base_url: The base URL of the Dataland environment.
        api_key_env: The name of the environment variable that holds the API key for the Dataland environment.
    """

    base_url: str
    api_key_env: str

    @property
    def client(self) -> DatalandClient:
        """Creates a DatalandClient for the Dataland environment."""
        return DatalandClient(dataland_url=self.base_url, api_key=os.getenv(self.api_key_env, None))


PRODUCTION_INSTANCE = DatalandInstance("https://dataland.com", "DATALAND_API_KEY")
CLONE_INSTANCE = DatalandInstance("https://clone.dataland.com", "DATALAND_API_KEY")
TEST_INSTANCE = DatalandInstance("https://test.dataland.com", "DATALAND_TEST_API_KEY")
DEV2_INSTANCE = DatalandInstance("https://dev2.dataland.com", "DATALAND_DEV2_API_KEY")
DEV3_INSTANCE = DatalandInstance("https://dev3.dataland.com", "DATALAND_DEV3_API_KEY")