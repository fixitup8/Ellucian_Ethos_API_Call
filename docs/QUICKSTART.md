# Quick Start

This page aims to show a rough and ready quick tour of the libraries basic functionality.

All the following examples require that you run the following setup:

```
pip3 install EthosClient
```

## Call an API to fetch a resource, change it and save back to Ethos

This sample will create a login session for the Ethos hub and use it to retrieve a resource:

Start a python3 REPL console and run the following to setup the varaibles required. In this example I am using the 
persons resource.
 
```
ethos_base_url = "ETHOS BASE URL e.g. https://integrate.elluciancloud.ie no trailing slash"
ethos_api_key = "ETHOS APPLICATION API KEY"
resource_name = "persons"
person_resource_id = "A_PERSON_GuiD"
```
(Replace the values above with values from your environment)

Note: In a real APP ethos_api_key will be read from some sort of secure store, and ethos_base_url should be a configurable 
paramater

Now create client and login session objects:
```
import EthosClient
ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_api_key)
```

Now you can call the API to get a resource:
```
person = ethos_client.get_resource(
  login_session=login_session,
  resource_name=resource_name,
  resource_id=person_resource_id,
  version=None
)
```
The version paramater is optional and if you want to retrieve a specific version you can supply a string such as "12.1.0"

If the resource is not found the get_resource function will return None.
Otherwise it will return an Resource Wrapper Object. You can print the details of the object you returned as follows:

```
print("API version from response:", person.version)
print("GUID of returned resource=", person.resource_id)
print(person.data)
```

Most get_resource calls will return a result class of BaseResourceWrapper however if the resource name and version is 
recognised by the library the object returned will be a class designed for that object and version. This class may provide 
special operations for that resource type. You can find the class that was returned with the following:

```
print("Resource Type Object=", type(person).__name__)
```
                          
See [Resource wrappers](../EthosClient/resources/README.md) for information.

You can make a change to the resource by altering the data structure. The following code adds a 2 to the end of the
persons last name then calls the api to save it back to Ethos:
```
print("Lastname is currently " + person.data["names"][0]["lastName"])
person.data["names"][0]["lastName"] = person.data["names"][0]["lastName"] + "2"
person.save(login_session=login_session)
```

One thing to remember about this method is that the entire person record is saved back to Ethos. If an hour or two has
elapsed between fetching the resource and saving it then there is a danger that any other changes to the source record
will be overwritten. It's best to read a record then immediatadly write it back to minimise this risk.

## Get a list of resources

This library provides a python iterator which handles the pagination. The following example collects
resources 25 at a time using the iterator. (It stops after 123 so it won't run forever) 

You can run this in the REPL:
```
person_hold_iterator = ethos_client.get_resource_iterator(
  login_session=login_session,
  resource_name="person-holds",
  params=None,
  version=None,
  page_size=25
)

max_to_print = 123
cur = 0
for person_hold in person_hold_iterator:
  print("personHold", person_hold.data["person"]["id"], person_hold.data["startOn"])
  cur += 1
  if cur > max_to_print:
    break
```

For more information on using resource iterators see [resource iterators](./RESOURCEITERATORS.md)

## Create a new resource

The following example creates a new person hold. This can be run in the REPL once the GUID's for person and 
person hold category are filled in:

```
person_guid = "TO BE ENTERED"
person_hold_category_guid = "TO BE ENTERED"

person_hold_to_create = {
    'endOn': '2099-12-31T00:00:00Z',
    'person': {'id': person_guid},
    'startOn': '2020-01-17T00:00:00Z',
    'type': {
      'category': 'academic',
      'detail': {
        'id': person_hold_category_guid
      }
    }
  }

created_person_hold = ethos_client.create_resource(
  login_session=login_session,
  resource_name="person-holds",
  resource_data=person_hold_to_create,
  version="6"
)

print("Created a new person-hold resource with id ", created_person_hold.version)
print("GUID of returned resource ", created_person_hold.resource_id)

```

## Delete a resource

There are two ways to delete a resource. Firstly you can use the delete method from a returned resource.
The following examples delete the resource created in the previous example:
```
created_person_hold.delete(login_session=login_session)
```

The disadvantage to this method is that you must first query the resource to obtain an object.
Another method to delete a resource requires just the resource guid:
```
resource_guid_to_be_deleted = created_person_hold.resource_id
ethos_client.delete_resource(
  login_session=login_session,
  resource_name="person-holds",
  resource_id=resource_guid_to_be_deleted
)
```

## Call any other API

This library wraps a lot of API calls to make them easier to use in Python. Not every API call is wrapped in the library
and they may not be wrapped in the way that is reburied. You can still use the library to make these calls and handle
the security. See [direct call guide](DIRECTCALL.md) for examples.

## Next Steps

This quick start guide has stepped through most of the major features of the library.
The library has also an implementation of a poller which can be used to call the publish API and retrieve change 
notifications it is explained in more detail here - [Poller Guide](POLLERGUIDE.md).
