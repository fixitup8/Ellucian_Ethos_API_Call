# Simple utility to use API to retrieve a person

import os
import sys

import common

##If we add the parent directory to the path we will use the development version of the library
##  rather than the insalled version
sys.path.insert(0, os.path.abspath('../'))
import EthosClient

print("Using EthosClient from the local source tree")

ethos_base_url = "https://integrate.elluciancloud.com"
ethos_api_key = os.environ["ETHOSAPIKEY"]

person_resource_id = "03C39271F08025FBE0546EB6A642217D"  # Jeremy Mavorick

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_api_key)

person = ethos_client.get_resource(
    login_session=login_session,
    resource_name="persons",
    resource_id=person_resource_id,
    version="12"  # 9 to 16
)
if person is None:
    raise RuntimeError(
        "Person was not found: " + person_resource_id +
        " (verify the ID exists in the configured Ethos tenant)"
    )

print("Person Type Object=", type(person).__name__)
print("Person Type ID=", person.resource_id)
print("Person Retrieved lastName=", person.data["names"][0]["lastName"])
input("Press Enter to continue and update or ctrl+c to quit...")

# Known issue - See an error AddressLine is required
# - it might be that person needs to load all the addresses as well in order to save any change sucessfully

person.data["names"][0]["lastName"] = person.data["names"][0]["lastName"] + "x"
print("Trying to change lastName to=", person.data["names"][0]["lastName"])

person.save(login_session=login_session)

print("Name in obj after put sent=", person.data["names"][0]["lastName"])
