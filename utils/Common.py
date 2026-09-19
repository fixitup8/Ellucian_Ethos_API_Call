# Common functions used in utils
import json
import os


def get_from_environment(environ_variable):
    if environ_variable in os.environ:
        return os.environ[environ_variable]
    raise Exception("Could not find " + environ_variable + " in environment for testing")


def execute_api_call(api, login_session, request_to_test):
    sending_none_data = False
    if request_to_test["method"] == "get":
        sending_none_data = True
        result = api.sendGetRequest(
            loginSession=login_session,
            url=request_to_test["url"]
        )
    if request_to_test["method"] == "post":
        result = api.sendPostRequest(
            loginSession=login_session,
            url=request_to_test["url"],
            data=json.dumps(request_to_test["postData"])
        )
    return (result, sending_none_data)
