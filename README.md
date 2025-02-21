# Client for E-Boekhouden API

**Introduction:**
> This package provides a Python client for interacting with the E-Boekhouden API. It simplifies authentication, data fetching, and handling of financial records (cost centers, invoices, ledgers, and mutations) while maintaining clear and organized code. Designed for rapid integration and ease of maintenance, it leverages modern logging and error-handling mechanisms.

## Example for retrieving Mutations

```python
"""Example script to process the API."""

import logging
from datetime import datetime, timedelta

from eboekhouden_client import EBoekhoudenClient, DateFilterOperator

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

log: logging.Logger = logging.getLogger(__name__)


def main() -> None:
    """Main function to process the data pipeline."""

    mutation_details: list = []
    client = EBoekhoudenClient(
        credentials={
            "source": "<Source for the Application>",
            "access_token": "<Acces Token from the Portal>",
        },
    )

    # Determine the processing period (Last 3 Days, including Today)
    today = datetime.now().date()
    start_date = today - timedelta(days=3)
    end_date = today

    # Process the Transactions
    mutations = client.get_mutations(
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
        date_range=DateFilterOperator.RANGE,
    )

    for mutation in mutations:
        mutation_id = mutation.get("id")
        get_mutation_details = client.get_mutation(mutation_id=mutation_id)
        mutation_details.append(get_mutation_details)


if __name__ == "__main__":
    main()

```
