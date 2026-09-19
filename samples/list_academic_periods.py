import os
import sys

# This sample uses a resource iterator to list all the academic periods
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import EthosClient

ethos_base_url      = os.environ["ETHOSBASEURL"]
ethos_app_api_key   = os.environ["ICETHOSDEVAPIKEY"]


ethos_client  = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_app_api_key)

print("Start")


def is_yes(user_input):
    trimmed = user_input.strip().upper()
    if len(trimmed) < 1:
        return False
    return trimmed[0] == "Y"


params = {}
user_input = input("Do you want to restrict to periods with open registration? (Y/N)")

if is_yes(user_input):
    print("Restricting results where registration is open")
    params["criteria"] = "{\"registration\":\"open\"}"

academic_period_iterator = ethos_client.get_resource_iterator(
    login_session=login_session,
    resource_name="academic-periods",
    version  =None,
    params   =params,
    page_size=25
)

cur = 0
for period in academic_period_iterator:
    cur += 1
    print(cur, "period", period.data)

print("End")
