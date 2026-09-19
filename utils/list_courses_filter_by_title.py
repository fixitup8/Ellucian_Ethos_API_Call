# Postman collection: Ethos Integration Examples > Next Steps > Read courses filter on title
import json
import os
import sys

sys.path.insert(0, os.path.abspath('../'))
import EthosClient

ethos_base_url = "https://integrate.elluciancloud.com"
ethos_api_key = os.environ["ETHOSAPIKEY"]

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_api_key)

params = {
    "criteria": json.dumps({
        "title": "Introduction to Psychology"
    })
}

course_iterator = ethos_client.get_resource_iterator(
    login_session=login_session,
    resource_name="courses",
    version=None,
    params=params,
    page_size=25
)

cur = 0
for course in course_iterator:
    cur += 1
    print(cur, course.data)

print("Total matching courses:", cur)
