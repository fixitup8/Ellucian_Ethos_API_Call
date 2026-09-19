# Utility used to call API and generate mock data.
#  the mock data can then be inserted into the tests

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

person_resource_id = "01e5f1c3-d0f0-445c-a095-c2884cd6fe4b"
person_hold_resource_id = "0e1f48c4-5669-4a94-92ad-d64d37af811a"

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)

login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_api_key)

test_requests = {}
test_requests["getSinglePerson"] = {
    "url": "/api/persons/" + person_resource_id,
    "method": "get",
    "postData": None
}
test_requests["getPersonHold"] = {
    "url": "/api/person-holds/" + person_hold_resource_id,
    "method": "get",
    "postData": None
}
test_requests["consumeChangeNotification"] = {
    "url": "/consume?limit=20",
    "method": "get",
    "postData": None
}

request_to_test = test_requests["consumeChangeNotification"]

(result, sending_none_data) = common.execute_api_call(api=ethos_client, login_session=login_session, request_to_test=request_to_test)


print("Response status_code was:" + str(result.status_code))
print("Response headers were:" + str(result.headers))
print("Response contentDict was:" + result.content.decode("utf-8"))


if sending_none_data:
    print("data=None")
else:
    print("data=DDD")
    raise Exception("Not Implemented")
print("#response=base64.b64encode(json.dumps({")
print("#  ##TODO")
print("#}).encode(\"UTF-8\")")
print("response=" + str(result.content))
print("mock.registerNextResponse(")
print("  reqFnName=\"get\",")
print("  url=\"" + request_to_test["url"] + "\",")
print("  data=data,")
print("  status_code=200,")
print("  contentBytes=base64.b64encode(json.dumps(response)),")
print("  ignoreData=False")
print(")")

print("Code END ----------------------")
