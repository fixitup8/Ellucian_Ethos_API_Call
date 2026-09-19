# Postman collection: Ethos Integration Examples > Some Basics > Create a persons resource
#
# Note: the Postman example body includes a fixed "id" for its demo tenant. That's
# omitted here so this script can be re-run safely - Ethos assigns a new id on create.
import os
import sys

sys.path.insert(0, os.path.abspath('../'))
import EthosClient

ethos_base_url = "https://integrate.elluciancloud.com"
ethos_api_key = os.environ["ETHOSAPIKEY"]
version = "8"

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_api_key)

person_to_create = {
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
            "fullName": "Mr. Alex Green",
            "title": "Mr.",
            "firstName": "Alex",
            "lastName": "Green",
            "preference": "preferred"
        },
        {
            "type": {
                "category": "personal",
                "detail": {
                    "id": "6bf52ca3-3382-4f8e-9ae5-15b0b79f9c79"
                }
            },
            "fullName": "Alexander Green",
            "firstName": "Alexander",
            "lastName": "Green"
        }
    ],
    "dateOfBirth": "1988-09-23",
    "gender": "male",
    "maritalStatus": {
        "maritalCategory": "single",
        "detail": {
            "id": "332b98d6-9e6a-4313-80b4-ee5548d735aa"
        }
    },
    "citizenshipCountry": "USA",
    "metadata": {}
}

created_person = ethos_client.create_resource(
    login_session=login_session,
    resource_name="persons",
    resource_data=person_to_create,
    version=version
)

print("Created person with id:", created_person.resource_id)
print(created_person.data)
