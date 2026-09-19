# Postman collection: Ethos Integration Examples > Next Steps > Read all persons paging 2
#
# See list_persons_paging_page1.py for why this uses a direct call rather than
# get_resource_iterator().
import json
import os
import sys

sys.path.insert(0, os.path.abspath('../'))
import EthosClient

ethos_base_url = "https://integrate.elluciancloud.com"
ethos_api_key = os.environ["ETHOSAPIKEY"]

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_api_key)

result = ethos_client.sendGetRequest(
    url="/api/persons",
    params={"offset": "100", "limit": "100"},
    loginSession=login_session,
    injectHeadersFn=None
)

persons = json.loads(result.content)
print("Page 2 - persons returned:", len(persons))
for person in persons:
    print(person)
