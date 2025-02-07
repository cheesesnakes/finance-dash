import requests
import pandas as pd


def get_data():
    tables = {
        "transactions": "md_pv36zw55fid66g",
        "budget": "md_2xjrn1xmqp1hf4",
        "debt": "md_l2guwtyazz1yxd",
        "investments": "mfbvxpxlk7claay",
    }

    for table_name, table_id in tables.items():
        base_url = "https://data.cheesesnakes.net"

        endpoint = f"/api/v2/tables/{table_id}/records"
        url = base_url + endpoint

        # auth

        headers = {"xc-token": "Ux5RsQvWISsNksbGqn7yZsVRy0GNSA1IWfcH9xIW"}

        # setting query parameters

        offset = 0
        limit = 1000
        params = {"limit": limit, "offset": offset}

        all_data = []

        while True:
            print(
                f"Loading data for {table_name} from lines {offset} - {offset + limit}"
            )

            # GET request from API
            response = requests.get(url, headers=headers, params=params)

            # Determine status code and error
            if response.status_code != 200:
                print(response.json()["msg"])
                break

            # Add data
            data = response.json()["list"]
            all_data.extend(data)

            # check if complete
            if response.json()["pageInfo"]["isLastPage"]:
                break

            # increase offset

            offset += limit
            params["offset"] = offset

        # Convert to DataFrame named after table

        globals()[table_name] = pd.DataFrame(all_data)

    return transactions, budget, debt, investments  # type: ignore # noqa: F821
