# This sample shows calling the API directly without trying to cast it to an object

import os
import sys

##If we add the parent directory to the path we will use the development version of the library
##  rather than the insalled version
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import EthosClient

ethos_base_url = os.environ["ETHOSBASEURL"]
ethos_poller_app_api_key = os.environ["ETHOSPOLLERAPIKEY"]

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_poller_app_api_key)

print("Start")

resource_to_fetch = "sections"
resource_guid = "fe524551-f02a-4297-9373-0b9f9bf120c2"
version = None  # "16"


example_url = "/api/" + resource_to_fetch + "/" + resource_guid


def sample_inject_header_function_for_get(headers):
    if version is not None:
        headers["Accept"] = "application/vnd.hedtech.integration.v" + version + "+json"


result = ethos_client.sendGetRequest(
    url=example_url,
    loginSession=login_session,
    injectHeadersFn=sample_inject_header_function_for_get
)

print(result.status_code)
print(result.content)

print("End")
