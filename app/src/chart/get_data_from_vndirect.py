import time
from datetime import datetime, timedelta, timezone

import requests

# Define UTC+7 timezone
utc_plus_7 = timezone(timedelta(hours=7))
start_time = int((datetime.now(utc_plus_7) - timedelta(days=730)).timestamp())
end_time = int(datetime.now(utc_plus_7).timestamp())

print(start_time)
print(end_time)

# Define the API endpoint and parameters
url = "https://dchart-api.vndirect.com.vn/dchart/history"
params = {
    "resolution": "1D",
    "symbol": "HPG",
    "from": staticmethod,
    "to": end_time
}

# Make the GET request
response = requests.get(url, params=params)

print(response.json())


# # Check if the request was successful
# if response.status_code == 200:
#     data = response.json()  # Parse the JSON response
#     print
