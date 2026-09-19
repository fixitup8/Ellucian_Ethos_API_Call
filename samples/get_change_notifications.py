import os
import sys

##If we add the parent directory to the path we will use the development version of the library
##  rather than the insalled version
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import EthosClient

ethos_base_url = os.environ["ETHOSBASEURL"]
ethos_poller_app_api_key = os.environ["ETHOSPOLLERAPIKEY"]

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_poller_app_api_key)

print("Start")

change_notification_iterator = ethos_client.get_change_notification_iterator(
    login_session=login_session,
    page_limit=20,
    max_requests=4
)


num_notifications = 0
for cur_change_notification in change_notification_iterator:
    num_notifications += 1
    print(cur_change_notification.get_simple_dict())

print("End num notifications received:", num_notifications)
