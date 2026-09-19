# Calling Ethos API directly using API


This library wraps a lot of API calls to make them easier to use in Python. Not every API call is wrapped in the library
and they may not be wrapped in the way that is requried. There are functions that allow direct calls to the API:

- sendGetRequest
- sendPostRequest
- sendPutRequest
- sendDeleteRequest

Each takes a loginSession argument. If supplied the loginSession will add the authorization header to calls and handle
retrying 401 responses. If loginSession is passed as "None" then no headers are added.
 
You also need to supply an injectHeadersFn function. This function can be used to add what ever header is required to
the API call. See the examples for mode details.

These four are the ones EthosAPIClient inherits directly from the underlying PythonAPIClientBase library, so
(unlike the rest of the library, e.g. get_resource, create_resource) their argument names stay camelCase.

The following examples show calling the API directly whilst still using the library to handle API security: 

## Example get Request

```
example_url = "/api/persons/SOMEPERSONGUID"
example_version = "6"

def sample_inject_header_function_for_get(headers):
  headers["Accept"] = "application/vnd.hedtech.integration.v" + example_version + "+json"

result = ethos_client.sendGetRequest(
  url=example_url,
  loginSession=login_session,
  injectHeadersFn=sample_inject_header_function_for_get
)

print(result.status_code)
print(result.content)

```

## Example Post Request

```
example_url = "/api/persons/SOMEPERSONGUID"

def sample_inject_header_function_for_post(headers):
    headers["Accept"] = "application/vnd.hedtech.integration.v" + example_version + "+json"
    headers["Content-Type"] = "application/vnd.hedtech.integration.v" + example_version + "+json"

post_data = { "TODO": "PutDataHere" }

result = ethos_client.sendPostRequest(
    url=example_url,
    loginSession=login_session,
    injectHeadersFn=sample_inject_header_function_for_post,
    data=json.dumps(post_data)
)

print(result.status_code)
print(result.content)
```

## Example Put Request

```
example_url = "/api/persons/SOMEPERSONGUID"
example_version = "6"

def sample_inject_header_function_for_put(headers):
  headers["Accept"] = "application/vnd.hedtech.integration.v" + example_version + "+json"
  headers["Content-Type"] = "application/vnd.hedtech.integration.v" + example_version + "+json"

put_data = { "TODO": "PutDataHere" }

result = ethos_client.sendPutRequest(
  url=example_url,
  loginSession=login_session,
  injectHeadersFn=sample_inject_header_function_for_put,
  data=json.dumps(put_data)
)

print(result.status_code)
print(result.content)

```

## Example Delete Request

For delete requests in Ethos no extra headers are required so the injectHeadersFn can be set to None.

```
example_url = "/api/persons/SOMEPERSONGUID"

result = ethos_client.sendDeleteRequest(
    url=example_url,
    loginSession=login_session,
    injectHeadersFn=None
)

print(result.status_code)
print(result.content)

```

## Handling Responses

The return value of these functions is a standard python requests response object.

Note: With built in API calls the library will check the response code is correct and raise Exceptions. When you call
the API's with this method you are responsible for checking the response is correct and for converting the output to a 
python structure, an example for doing this is:

```
if result.status_code != 200:
    raise Exception("An API Error has occured")

result_data = json.loads(result.content)

```
