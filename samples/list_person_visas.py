import os
import sys

# This sample uses a resource iterator to list all the visas for a particular person
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import EthosClient

ethos_base_url           = os.environ["ETHOSBASEURL"]
ethos_app_api_key        = os.environ["ICETHOSDEVAPIKEY"]

person_resource_id = "01e5f1c3-d0f0-445c-a095-c2884cd6fe4b"

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_app_api_key)

print("Start")

print("First obtain the person object")

person = ethos_client.get_resource(
    login_session=login_session,
    resource_name="persons",
    resource_id=person_resource_id,
    version=None
)
print("Found:", person.data["names"][0]["fullName"])

print("Next list all the persons visas")
cur = 0
for cur_visa in person.get_visas(login_session=login_session):
    cur += 1
    print(cur, "visa", cur_visa.data)

print("End")
