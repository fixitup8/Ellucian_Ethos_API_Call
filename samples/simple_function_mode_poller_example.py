# Simple example that uses the poller
# This is a simple non-reliable implementation. All messages will be taken off the queue no matter if they are
# sucessfully processed or not.
import os
import sys
import time

##If we add the parent directory to the path we will use the development version of the library
##  rather than the insalled version
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import EthosClient

ethos_base_url           = "https://integrate.elluciancloud.com"
ethos_poller_app_api_key = os.environ["ETHOSAPIKEY"]


lastprocessid_file_name = "./pollerguideTempFileForLastProcessedID.txt"

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_poller_app_api_key)


def process_single_message(api_client, message_id, change_notification):
    # in a real example this part would write to file or update a db
    print("received ", change_notification.operation, change_notification.resource_name, change_notification.resource_id)
    with open(lastprocessid_file_name, 'w') as filetowrite:
        filetowrite.write(message_id)
    return True


print("Start")


print("Reading lastprocessedid from file")
last_processed_id = ""
with open(lastprocessid_file_name, 'r') as filetowrite:
    last_processed_id = filetowrite.read()
print(" - last_processed_id", last_processed_id)

print("Starting receive thread")
ethos_client.start_change_notification_poller_thread_in_function_mode(
    login_session=login_session,
    frequency=10,  # number of seconds between fetches
    page_limit=20,  # number of change notifications to get per requests
    max_requests=4,  # maximum number of requests to use in each fetch
    last_processed_id=last_processed_id,
    message_processing_function=process_single_message
)

print("Main loop - ctl+c to terminate")
try:
    while True:
        ethos_client.health_check()  # detects if thread has died and if so raises an exception
        time.sleep(0.5)
except KeyboardInterrupt:
    print('\nctl+c pressed - so terminating')

ethos_client.close()

print("End")
