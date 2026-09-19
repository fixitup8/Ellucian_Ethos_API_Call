# Postman collection: Ethos Integration Examples > Next Steps > GET  Single Persons version-specific
import os
import sys

sys.path.insert(0, os.path.abspath('../'))
import EthosClient

ethos_base_url = "https://integrate.elluciancloud.com"
ethos_api_key = os.environ["ETHOSAPIKEY"]
version = "8"

person_resource_id = "35b16136-bafd-4b5d-9dd2-995ad9f4ba00"  # TODO: replace with a real id

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_api_key)

person = ethos_client.get_resource(
    login_session=login_session,
    resource_name="persons",
    resource_id=person_resource_id,
    version=version
)
if person is None:
    raise RuntimeError("Person was not found: " + person_resource_id)

print("Resource type object:", type(person).__name__)
print(person.data)
