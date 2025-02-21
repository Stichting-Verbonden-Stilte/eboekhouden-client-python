"""E-Boekhouden API Client"""

import os
import json
from typing import Dict, Optional

import logging
import requests

from .enums import DateFilterOperator

log = logging.getLogger(__name__)


class EBoekhoudenClient:
    """EBoekhoudenClient is a client for interacting with the E-Boekhouden API.
    Attributes:
        BASE_URL (str): The base URL for the E-Boekhouden API.
        PAGE_LIMIT (int): The maximum number of items per page for paginated requests.
        api_version (str): The version of the API to use.
        api_url (str): The full URL for the API, including the version.
        access_token (Optional[str]): The access token for authenticating with the API.
        source (Optional[str]): The source identifier for the API.
        session_token (Optional[str]): The session token for the current session.
        api_headers (Optional[dict]): The headers to use for API requests.
    Methods:
        __init__(credentials: str, api_version: str = "v1") -> None:
            Initializes the EBoekhoudenClient with the given credentials and API version.
        _parse_service_account_file(credentials: str) -> None:
            Parses the service account file to extract the access token and source.
        _authenticate() -> None:
            Authenticates the client with the E-Boekhouden API and retrieves a session token.
        _get_date_filter(operator: DateFilterOperator, parameter: str = "date", start_date:
            Optional[str] = None, end_date: Optional[str] = None) -> str:
            Generates a date filter query parameter.
        _get_headers() -> dict:
            Returns the headers to use for API requests, including the session token.
        get_cost_centers() -> dict:
            Retrieves a list of cost centers from the API.
        get_cost_center(cc_id: str) -> dict:
            Retrieves details of a specific cost center by its ID.
        get_invoices() -> dict:
            Retrieves a list of invoices from the API.
        get_invoice(inv_id: str) -> dict:
            Retrieves details of a specific invoice by its ID.
        get_ledgers() -> Union[dict, pd.DataFrame]:
            Retrieves a list of ledgers from the API.
        get_ledger(led_id: str) -> dict:
            Retrieves details of a specific ledger by its ID.
        get_balance(led_id: str) -> dict:
            Retrieves the balance of a specific ledger by its ID.
        get_mutations(start_date: Optional[str] = None, end_date: Optional[str] = None,
            date_range: Optional[DateFilterOperator] = None) -> Union[dict, pd.DataFrame]
            Retrieves a list of mutations (transactions) between the specified start and
            end dates with pagination.
        get_mutation(mut_id: str) -> Union[dict, pd.DataFrame]:
            Retrieves details of a specific mutation by its ID.
        get_outstanding_invoices() -> dict:
            Retrieves a list of outstanding invoices from the API.
        get_relation(rel_id: str) -> dict:
            Retrieves details of a specific relation by its ID.
        get_relations() -> Optional[dict]:
            Retrieves a list of relations from the API.
        close() -> bool:
    """

    BASE_URL = "https://api.e-boekhouden.nl"
    PAGE_LIMIT = 100

    def __init__(self, credentials: str, api_version: str = "v1") -> None:
        """
        Initializes the EBoekhoudenClient with the given credentials and API version.

        Args:
            credentials (str): The credentials as a file path or JSON string.
            api_version (str): The API version to use. Defaults to "v1".
        """
        self.api_version: str = api_version
        self.api_url: str = f"{self.BASE_URL}/{self.api_version}"

        self.access_token: Optional[str] = None
        self.source: Optional[str] = None
        self.session_token: Optional[str] = None
        self.api_headers: Optional[dict] = None

        # Parse Service Account File
        self._parse_service_account_file(credentials)

        # Authenticate the client
        self._authenticate()

    def _parse_service_account_file(self, credentials: str) -> None:
        """
        Parses the service account data to extract the access token and source.

        Args:
            credentials (str): The path to the service account file or a JSON string.
        """
        data: Dict = {}
        try:
            if os.path.isfile(credentials):
                with open(credentials, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = json.loads(credentials)
        except Exception as e:
            log.error("Failed to load service account credentials: %s", e)
            raise

        try:
            if not data.get("access_token") or not data.get("source"):
                raise ValueError(
                    "Service Account file must contain 'access_token' and 'source' fields."
                )

            self.access_token = data.get("access_token")
            self.source = data.get("source")

        except FileNotFoundError:
            log.error("Service Account file not found: %s", credentials)

    def _authenticate(self) -> None:
        url = f"{self.api_url}/session"
        payload = {"accessToken": self.access_token, "source": self.source}
        headers = {"accept": "application/json", "Content-Type": "application/json"}

        log.info("Authenticating with E-Boekhouden API...")
        response = requests.post(url, json=payload, headers=headers, timeout=10)

        if response.status_code == 200:
            self.session_token = response.json().get("token")
            log.info("Authenticated with E-Boekhouden API.")
        else:
            log.warning("Failed to authenticate with E-Boekhouden API.")
            response.raise_for_status()

    def _get_date_filter(
        self,
        parameter: str = "date",
        operator: Optional[DateFilterOperator] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict:
        """
        Generates a date filter query parameter.

        Args:
            parameter (str): The query parameter name.
            operator (Optional[DateFilterOperator]): The filter operator.
            start_date (Optional[str]): The start date string (YYYY-MM-DD).
            end_date (Optional[str]): The end date string (YYYY-MM-DD) for range filtering.

        Returns:
            Dict: A dictionary with the formatted date filter query parameter.
        """
        if not operator:
            raise ValueError(f"Operator is required for date filtering on {parameter}")

        if operator == DateFilterOperator.RANGE:
            if not start_date or not end_date:
                raise ValueError("Range operator requires both start_date and end_date")
            return {f"{parameter}[{operator.value}]": f"{start_date},{end_date}"}

        if not start_date:
            raise ValueError(f"Operator {operator.value} requires a start_date value")

        return {f"{parameter}[{operator.value}]": f"{start_date}"}

    def _get_headers(self) -> dict:
        if not self.session_token:
            raise ValueError("Authentication required. Call authenticate() first.")

        return {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.session_token}",
        }

    def get_cost_centers(self) -> dict:
        """
        Fetches cost centers from the API.
        This method sends a GET request to the cost center endpoint of the API
        and returns the JSON response if the request is successful.
        Returns:
            dict: A dictionary containing the cost centers data.
        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        url = f"{self.api_url}/costcenter"
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()

        response.raise_for_status()
        return {}

    def get_cost_center(self, cc_id: str) -> dict:
        """
        Retrieve the details of a cost center by its ID.
        Args:
            cc_id (str): The ID of the cost center to retrieve.
        Returns:
            dict: A dictionary containing the cost center details if the request is successful.
        Raises:
            requests.exceptions.HTTPError: If the request to the API fails.
        """
        url = f"{self.api_url}/costcenter/{cc_id}"
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()

        response.raise_for_status()
        return {}

    def get_invoices(self) -> dict:
        """
        Fetches invoices from the API.

        This method sends a GET request to the invoice endpoint of the API and retrieves
        the list of invoices. If the request is successful (status code 200), it returns
        the response in JSON format. If the request fails, it raises an HTTPError.

        Returns:
            dict: A dictionary containing the invoices data if the request is successful.

        Raises:
            requests.exceptions.HTTPError: If the request to the API fails.
        """
        url = f"{self.api_url}/invoice"
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()

        response.raise_for_status()
        return {}

    def get_ledgers(self) -> Dict:
        """
        Fetches ledger data from the API.
        This method sends a GET request to the ledger endpoint of the API and retrieves
        the ledger data. The data is returned either as a JSON object.
        Returns:
            dict: The ledger data is returned as a JSON object.
        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        url = f"{self.api_url}/ledger"
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()

        response.raise_for_status()
        return {}

    def get_ledger(self, led_id: str) -> dict:
        """
        Retrieve ledger information from the API.
        Args:
            led_id (str): The ID of the ledger to retrieve.
        Returns:
            dict: The JSON response from the API containing ledger information.
        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """
        url = f"{self.api_url}/ledger/{led_id}"
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()

        response.raise_for_status()
        return {}

    def get_mutations(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        date_range: Optional[DateFilterOperator] = None,
    ) -> Dict:
        """
        Retrieve financial mutations within a specified date range.
        Args:
            start_date (Optional[str]): The start date for filtering
                mutations (inclusive). Format: 'YYYY-MM-DD'.
            end_date (Optional[str]): The end date for filtering
                mutations (inclusive). Format: 'YYYY-MM-DD'.
            date_range (Optional[DateFilterOperator]): The operator to use
                for date filtering.
        Returns:
            dict: A dictionary containing the mutations.
        """
        url = f"{self.api_url}/mutation"
        params = {}

        if start_date or end_date:
            params = self._get_date_filter(
                operator=date_range,
                start_date=start_date,
                end_date=end_date,
            )

        all_items = []
        page_offset = 0

        while True:
            params["offset"] = page_offset
            params["limit"] = self.PAGE_LIMIT

            response = requests.get(
                url, headers=self._get_headers(), params=params, timeout=10
            )
            if response.status_code == 200:
                items = response.json().get("items", [])
                if not items:
                    break
                all_items.extend(items)
                page_offset += self.PAGE_LIMIT
            else:
                response.raise_for_status()

        return {"items": all_items}

    def get_mutation(self, mutation_id: str) -> Dict:
        """
        Retrieve a mutation by its ID.
        Args:
            mut_id (str): The ID of the mutation to retrieve.
        Returns:
            dict: The mutation data is returned as a dictionary.
        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        url = f"{self.api_url}/mutation/{mutation_id}"
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()

        response.raise_for_status()
        return {}

    def get_outstanding_invoices(self):
        """
        Retrieve outstanding invoices from the API.
        This method sends a GET request to the API endpoint for outstanding invoices
        and returns the JSON response if the request is successful.
        Returns:
            dict: A dictionary containing the JSON response from the API
                if the request is successful.
        Raises:
            requests.exceptions.HTTPError: If the request to the API fails.
        """
        url = f"{self.api_url}/mutation/invoice/outstanding"
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()

        response.raise_for_status()
        return {}

    def get_relation(self, rel_id: str):
        """
        Retrieve relation details from the API.
        Args:
            rel_id (str): The ID of the relation to retrieve.
        Returns:
            dict: A dictionary containing the relation details if the
                request is successful.
        Raises:
            requests.exceptions.HTTPError: If the request to the API fails.
        """
        url = f"{self.api_url}/relation/{rel_id}"
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()

        response.raise_for_status()
        return {}

    def get_relations(self) -> Dict:
        """
        Fetches relations from the API.
        This method sends a GET request to the API endpoint for relations and returns
            the response as a dictionary if the request is successful.

        Returns:
            Optional[dict]: A dictionary containing the relations data
                if the request is successful, otherwise None.
        """

        url = f"{self.api_url}/relation"
        response = requests.get(url, headers=self._get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()

        return {}

    def close(self) -> bool:
        """
        Closes the current session by sending a DELETE request to the API.
        Returns:
            bool: True if the session was successfully closed (HTTP status code 204),
                  False otherwise.
        """

        url = f"{self.api_url}/session"
        response = requests.delete(url, headers=self._get_headers(), timeout=10)
        if response.status_code == 204:
            self.session_token = None
            return True

        return False
