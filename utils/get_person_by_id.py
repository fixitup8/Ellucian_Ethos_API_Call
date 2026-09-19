# Postman collection: Ethos Integration Examples > Next Steps > GET  Single Persons version-less
import os
import sys

sys.path.insert(0, os.path.abspath('../'))
import EthosClient

ethos_base_url = "https://integrate.elluciancloud.com"
ethos_api_key = os.environ["ETHOSAPIKEY"]

person_resource_id = "f657b0e2-4c12-48f5-a6b3-24ea7eed44bd"  # TODO: replace with a real id

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_api_key)

person = ethos_client.get_resource(
    login_session=login_session,
    resource_name="persons",
    resource_id=person_resource_id,
    version=None
)
if person is None:
    raise RuntimeError("Person was not found: " + person_resource_id)

print("API version returned:", person.version)
print(person.data)
