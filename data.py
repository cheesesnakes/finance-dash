import requests
import pandas as pd

def get_data(table):
    
    base_url="https://data.cheesesnakes.net"
    endpoint= "/api/v1/db/data/noco/Finance%20Dashboard/"
    table = table
    url = base_url + endpoint + table

    # auth

    headers = {"xc-token":"Ux5RsQvWISsNksbGqn7yZsVRy0GNSA1IWfcH9xIW"}

    # setting query parameters

    offset = 0

    params = {
        "limit":1000,
        "offset":offset
    }

    all_data = []

    while True:

        #GET request from API
        response = requests.get(url, headers=headers, params=params)
        
        # Determine status code and error
        if response.status_code != 200:
            print(response.json()['msg'])
            break
        
        # Add data
        data = response.json()['list']
        all_data.extend(data)
        
        # check if complete
        if response.json()['pageInfo']['isLastPage']:
            break
        
        # increase offset
        offset += 1000
        params['offset']=offset
        
    all_data = pd.DataFrame(all_data)
    
    return all_data