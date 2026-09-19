# Postman collection: Ethos Integration Examples > Some Basics > Use API Key to get Access Token
#
# Exchanges an Ethos application API key for a short-lived bearer access token.
# EthosAPIClient.get_login_session_from_api_key() does this exchange for you (POST /auth)
# and then attaches the resulting token to every subsequent request automatically.
import os
import sys

sys.path.insert(0, os.path.abspath('../'))
import EthosClient

ethos_base_url = "https://integrate.elluciancloud.com"
ethos_api_key = os.environ["ETHOSAPIKEY"]

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_api_key)

print("Access token:", login_session.current_auth_key)
