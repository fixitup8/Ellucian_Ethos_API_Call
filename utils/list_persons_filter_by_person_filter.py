# Postman collection: Ethos Integration Examples > Next Steps > Read persons filter on person-filters
import json
import os
import sys

sys.path.insert(0, os.path.abspath('../'))
import EthosClient

ethos_base_url = "https://integrate.elluciancloud.com"
ethos_api_key = os.environ["ETHOSAPIKEY"]

person_filter_id = "5305f3ee-a0a8-4893-9722-4c50ac9557a1"  # TODO: replace with a real person-filters id

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_api_key)

params = {
    "criteria": json.dumps({
        "personFilter": person_filter_id
    })
}

person_iterator = ethos_client.get_resource_iterator(
    login_session=login_session,
    resource_name="persons",
    version=None,
    params=params,
    page_size=25
)

cur = 0
for person in person_iterator:
    cur += 1
    print(cur, person.data)

print("Total matching persons:", cur)
