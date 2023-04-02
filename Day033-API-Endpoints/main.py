import requests

API_ENDPOINT = 'http://api.open-notify.org/iss-now.json'

response = requests.get(url=API_ENDPOINT)
print(response)  # Prints the response code

# Response codes:
# 1XX: Informational: Hold On
# 2XX: Success: Here You Go
# 3XX: Redirection
# 4XX: Client Error
# 5XX: Server Error

# More info on: https://www.webfx.com/web-development/glossary/http-status-codes/

# Can't cover all exception cases
if response.status_code == 404:
    raise Exception("That resource does not exist.")
elif response.status_code == 401:
    raise Exception("You are not authorized to access this data")

# Instead
response.raise_for_status()

# Then
data = response.json()
loc = (data['iss_position']['latitude'], data['iss_position']['longitude'])
print(loc)
