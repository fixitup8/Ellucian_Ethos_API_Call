import os
import sys

##https://resources.elluciancloud.com/bundle/person-holds/page/6.0/index.html

##If we add the parent directory to the path we will use the development version of the library
##  rather than the insalled version
sys.path.insert(0, os.path.abspath('../'))
import EthosClient

ethos_base_url = "https://integrate.elluciancloud.com"
ethos_api_key = os.environ["ETHOSAPIKEY"]

person_resource_id = "01e5f1c3-d0f0-445c-a095-c2884cd6fe4b"
person_hold_category_guid = "45182c89-6bb8-4996-a05a-6fce28f028eb"

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_api_key)

person_hold_iterator = ethos_client.get_resource_iterator(
    login_session=login_session,
    resource_name="person-holds",
    version=None,
    page_size=9
)

max_to_print = 13
cur = 0
for person_hold in person_hold_iterator:
    print("personHold", person_hold.data)
    cur += 1
    if cur > max_to_print:
        break

print("Iterator run so now creating a person-hold")

person_hold_to_create = {
    'endOn': '2099-12-31T00:00:00Z',
    'person': {'id': person_resource_id},
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

print("Deleting using obj method")
created_person_hold.delete(login_session=login_session)

print("Creating another person hold so it can be deleted using id only")
created_person_hold = ethos_client.create_resource(
    login_session=login_session,
    resource_name="person-holds",
    resource_data=person_hold_to_create,
    version="6"
)

print("Created a new person-hold resource with id ", created_person_hold.version)
print("GUID of returned resource ", created_person_hold.resource_id)

print("Deleting using obj method")
ethos_client.delete_resource(
    login_session=login_session,
    resource_name="person-holds",
    resource_id=created_person_hold.resource_id
)


print("End")
