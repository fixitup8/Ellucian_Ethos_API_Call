# Postman collection: Ethos Integration Examples > Some Basics > Update a persons resource
#
# Sends a full replacement PUT for a persons resource, matching the Postman example's
# body and API version (v8) exactly. person_resource_id below is the example GUID from
# the collection's demo tenant - replace it with a real id from your own environment.
#
# This uses the direct sendPutRequest call (see docs/DIRECTCALL.md) rather than the
# BaseResourceWrapper.save() helper, because the Persons wrapper strips "addresses"
# from updates (see EthosClient/resources/persons.py) and this example body includes one.
import json
import os
import sys

sys.path.insert(0, os.path.abspath('../'))
import EthosClient

ethos_base_url = "https://integrate.elluciancloud.com"
ethos_api_key = os.environ["ETHOSAPIKEY"]
version = "8"

person_resource_id = "e17f9afb-ad01-4727-bd98-6664258decb0"  # TODO: replace with a real id

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_api_key)

person_update = {
    "privacyStatus": {
        "privacyCategory": "unrestricted"
    },
    "names": [
        {
            "type": {
                "category": "legal",
                "detail": {
                    "id": "5e59d3e4-61a8-4f61-9a18-05ae62a5b003"
                }
            },
            "fullName": "Mr. James Smith",
            "title": "Mr.",
            "firstName": "James",
            "lastName": "Smith",
            "preference": "preferred"
        }
    ],
    "dateOfBirth": "1994-12-07",
    "gender": "male",
    "roles": [
        {
            "role": "student"
        }
    ],
    "credentials": [
        {
            "type": "colleaguePersonId",
            "value": "0000255"
        },
        {
            "type": "ssn",
            "value": "135-79-2468"
        }
    ],
    "addresses": [
        {
            "address": {
                "id": "1cd57963-6f6b-4df0-b8eb-dec4a0a72e58"
            },
            "type": {
                "addressType": "home",
                "detail": {
                    "id": "c70b16d2-be85-4d43-a4b6-c13941c50d6e"
                }
            },
            "startOn": "2001-10-08T00:00:00",
            "preference": "primary"
        }
    ],
    "metadata": {},
    "id": person_resource_id
}


def inject_header_fn(headers):
    headers["Content-Type"] = "application/vnd.hedtech.integration.v" + version + "+json"
    headers["Accept"] = "application/vnd.hedtech.integration.v" + version + "+json"


result = ethos_client.sendPutRequest(
    url="/api/persons/" + person_resource_id,
    loginSession=login_session,
    injectHeadersFn=inject_header_fn,
    data=json.dumps(person_update)
)

print(result.status_code)
print(result.content)
