# Postman collection: Ethos Integration Examples > Some Basics > Publish array of change-notifications
#
# EthosClient doesn't wrap the /publish endpoint (only /consume, via
# get_change_notification_iterator), so this uses a direct call - see docs/DIRECTCALL.md.
import json
import os
import sys

sys.path.insert(0, os.path.abspath('../'))
import EthosClient

ethos_base_url = "https://integrate.elluciancloud.com"
ethos_api_key = os.environ["ETHOSAPIKEY"]

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_api_key)

change_notifications_to_publish = [
    {
        "resource": {
            "name": "buildings",
            "id": "fee12eb6-dae1-456b-a7c4-063458617478",
            "version": "application/vnd.hedtech.integration.v6+json"
        },
        "operation": "replaced",
        "contentType": "resource-representation",
        "content": {
            "code": "BLD1",
            "title": "Building 1",
            "description": "the first building",
            "id": "fee12eb6-dae1-456b-a7c4-063458617478"
        }
    },
    {
        "resource": {
            "name": "buildings",
            "id": "9d7c0f72-9eb4-4b76-83f1-e4a6a5fcab69",
            "version": "application/vnd.hedtech.integration.v6+json"
        },
        "operation": "replaced",
        "contentType": "resource-representation",
        "content": {
            "code": "BLD2",
            "title": "Building 2",
            "description": "the second building",
            "id": "9d7c0f72-9eb4-4b76-83f1-e4a6a5fcab69"
        }
    }
]


def inject_header_fn(headers):
    headers["Content-Type"] = "application/vnd.hedtech.change-notifications.v2+json"


result = ethos_client.sendPostRequest(
    url="/publish",
    loginSession=login_session,
    injectHeadersFn=inject_header_fn,
    data=json.dumps(change_notifications_to_publish)
)

print(result.status_code)
print(result.content)
