# Postman collection: Ethos Integration Examples > Next Steps > GET institution-jobs filter for person
import json
import os
import sys

sys.path.insert(0, os.path.abspath('../'))
import EthosClient

ethos_base_url = "https://integrate.elluciancloud.com"
ethos_api_key = os.environ["ETHOSAPIKEY"]

person_resource_id = "08bb7310-0da7-4a0f-b5cc-4fcc516d4d8a"  # TODO: replace with a real id

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_api_key)

params = {
    "criteria": json.dumps({
        "endOn": "2013-01-31",
        "person": person_resource_id
    })
}

institution_job_iterator = ethos_client.get_resource_iterator(
    login_session=login_session,
    resource_name="institution-jobs",
    version=None,
    params=params,
    page_size=25
)

cur = 0
for institution_job in institution_job_iterator:
    cur += 1
    print(cur, institution_job.data)

print("Total matching institution-jobs:", cur)
