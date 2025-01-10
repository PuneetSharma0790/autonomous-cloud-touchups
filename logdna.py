import requests
import json, os
from datetime import datetime, timedelta

def get_logs_from_view():
    url = "https://<cloud_log_guid>.com/api/v1/query"
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "Authorization": "Bearer " +genrate_identity_token()
    }

    point= get_milliseconds_timeformat()
    data = {
        "queryDef": {
            "type": "freeText",
            "pageSize": 100,
            "queryParams": {
                "query": {
                    "text": '"your_search_string"',
                    "type": "exact",
                    "syntax": "Lucene"
                }
            },
            
            "endDate": point[1],
            "startDate": point[0],
            "selectedViewId": 1703
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(response.status_code)
    print(response.json())

def get_milliseconds_timeformat():
    now = datetime.now()
    start_time = now - timedelta(days=1) 
    end_time = now

    def convert_to_milliseconds(dt: datetime) -> int:
        return int(dt.hour * 3600 + dt.minute * 60 + dt.second) * 1000

    start_time_ms = convert_to_milliseconds(start_time)
    end_time_ms = convert_to_milliseconds(end_time)
    print (start_time_ms, end_time_ms)
    return start_time_ms, end_time_ms

def genrate_identity_token():

    url = "https://iam.services.azurecloud.com/identity/token"
    payload = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": os.environ["MY_CLOUD_APIKEY"]
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    else:
        print("Error:", response.status_code, response.text)

get_logs_from_view()
