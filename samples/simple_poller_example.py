# Simple example that uses the poller
# This is a simple non-reliable implementation. All messages will be taken off the queue no matter if they are
# sucessfully processed or not.
import os
import queue
import sys
import time

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import EthosClient

ethos_base_url           = "https://integrate.elluciancloud.com"
ethos_poller_app_api_key = os.environ["ETHOSAPIKEY"]


print("Start")

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_poller_app_api_key)


change_notification_queue = queue.Queue()
ethos_client.start_change_notification_poller_thread(
    login_session=login_session,
    frequency=10,  # number of seconds between fetches
    page_limit=20,  # number of change notifications to get per requests
    max_requests=4,  # maximum number of requests to use in each fetch
    poller_queue=change_notification_queue
)

print("Starting to watch for messages - ctl+c to terminate")
try:
    while True:
        while change_notification_queue.qsize() > 0:
            change_notification = change_notification_queue.get()
            print("Recieved", change_notification.operation, change_notification.resource_name, change_notification.resource_id, change_notification.resource_wrapper)

        ethos_client.health_check()  # detects if thread has died and if so raises an exception
        time.sleep(0.5)
except KeyboardInterrupt:
    print('\nctl+c pressed - so terminating')


ethos_client.close()

print("End")
