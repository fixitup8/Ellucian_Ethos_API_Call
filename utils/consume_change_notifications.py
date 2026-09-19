# Postman collection: Ethos Integration Examples > Some Basics > Retrieve change-notifications (subscriptions)
#
# See docs/POLLERGUIDE.md for the background-thread version of this (better suited to
# a long-running app); this is the one-shot equivalent of the Postman GET /consume call.
import os
import sys

sys.path.insert(0, os.path.abspath('../'))
import EthosClient

ethos_base_url = "https://integrate.elluciancloud.com"
ethos_api_key = os.environ["ETHOSAPIKEY"]

ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)
login_session = ethos_client.get_login_session_from_api_key(api_key=ethos_api_key)

change_notification_iterator = ethos_client.get_change_notification_iterator(
    login_session=login_session,
    page_limit=20,
    max_requests=4
)

num_notifications = 0
for cur_change_notification in change_notification_iterator:
    num_notifications += 1
    print(cur_change_notification.get_simple_dict())

print("Total change notifications received:", num_notifications)
