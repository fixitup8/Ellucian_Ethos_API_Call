# Postman collection: Ethos Integration Examples > Next Steps > GET sections filter for academic-period and course
import json
import os
import sys

sys.path.insert(0, os.path.abspath('../'))
import EthosClient

ethos_base_url = "https://integrate.elluciancloud.com"
ethos_api_key = os.environ["ETHOSAPIKEY"]

academic_period_id = "17920c56-7a4c-4f00-9a39-4801b7e6fc58"  # TODO: replace with a real id
course_id = "b5f58254-4d30-4052-ac8b-6d20898e232b"  # TODO: replace with a real id

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_api_key)

params = {
    "criteria": json.dumps({
        "academicPeriod": {"id": academic_period_id},
        "course": {"id": course_id}
    })
}

section_iterator = ethos_client.get_resource_iterator(
    login_session=login_session,
    resource_name="sections",
    version=None,
    params=params,
    page_size=25
)

cur = 0
for section in section_iterator:
    cur += 1
    print(cur, section.data)

print("Total matching sections:", cur)
