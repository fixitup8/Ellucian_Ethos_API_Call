'''
This utility is designed to continously call Ethos API's until it is terminated by keyboard input (ctrl+c)
The reason for this is so that I can test and demo the poller functinoality of the library

It works by continously creating, then deleting person holds.

'''
import os
import queue
import sys
import time

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import EthosClient

ethos_base_url = os.environ["ETHOSBASEURL"]
ethos_api_key = os.environ["ICETHOSDEVAPIKEY"]

change_delay_time = 3

print("Sample Start")

person_resource_id_list = [
    "01e5f1c3-d0f0-445c-a095-c2884cd6fe4b",
    "f41aa35d-431e-4301-aa2b-d0799ea53ac5",
    "4c89b26e-8cf9-4697-856f-ab677265b2ce",
    "fb7db2a8-1c79-4d77-8bb7-e54ce202c42b",
    "c4b1718a-3fa8-452d-86cc-92eaa671ae23",
    "6ca9c61b-d441-4d29-befa-d841bf0bc767",
    "4b09bcbd-629b-4e5a-8439-6f1027770f97",
    "7ecdf9a8-5112-475c-99b5-ba3fedc547b6",
    "ac1388f2-a687-4a17-b600-5dace001dbdd",
    "5bcbc3b1-cf8a-4ea6-9042-1dc3e14aa3ba",
    "8c77d8b8-3dd2-4be3-a6b5-2ce6682af310",
    "741cf943-88e8-49e3-85f4-3e90d2e19c40",
    "4b781745-6f0f-47d7-80d8-147d2707222d",
    "f9247aee-a9fe-446e-b01b-a2758f4e1701",
    "93e81e3d-4541-4605-8994-6aa74c7ccd3f",
    "f1d31dd9-b141-4932-a8b6-d09637f1876d",
    "46c03542-9c45-46df-beaa-8db2a09bb460"
]

person_hold_category_guid = "45182c89-6bb8-4996-a05a-6fce28f028eb"

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_api_key)


def create_person_hold_and_return_guid(person_guid):
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
    return created_person_hold.resource_id


def delete_person_hold(person_hold_guid):
    ethos_client.delete_resource(
        login_session=login_session,
        resource_name="person-holds",
        resource_id=person_hold_guid
    )


print("Starting to send stream of changes to Ethos API's")
print("Press ctl+c to end")
creating = True
next_person_id_to_use = 0
q = queue.Queue()
try:
    while True:
        if q.empty():
            creating = True
            next_person_id_to_use = 0
        else:
            if q.qsize() == len(person_resource_id_list):
                creating = False

        if creating:
            person_hold_guid = create_person_hold_and_return_guid(person_guid=person_resource_id_list[next_person_id_to_use])
            print("+", end="", flush=True)
            q.put(person_hold_guid)
            next_person_id_to_use += 1
        else:
            item = q.get()
            delete_person_hold(item)
            print("-", end="", flush=True)

        time.sleep(change_delay_time)
except KeyboardInterrupt:
    print('\nctl+c pressed - so terminating')

print("Deleting any remaing resources")
while not q.empty():
    item = q.get()
    delete_person_hold(item)
    print("-", end="", flush=True)

ethos_client.close()


print("\nSample End")
