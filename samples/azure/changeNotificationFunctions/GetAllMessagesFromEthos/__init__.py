import datetime
import logging
import json
import os

import azure.functions as func
import EthosClient
import typing

def main(mytimer: func.TimerRequest, msg: func.Out[typing.List[str]]) -> None:

    ethos_client = EthosClient.EthosAPIClient(base_url=os.environ["ethosBaseURL"])
    login_session = ethos_client.get_login_session_from_api_key(api_key=os.environ["ethosAppAPIKey"])

    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Requesting Change Notifications from Ethos at %s', utc_timestamp)

    change_notification_iterator = ethos_client.get_change_notification_iterator(
        login_session=login_session,
        page_limit=20,
        max_requests=4
    )

    msgs_received = []
    num_notifications = 0
    for cur_change_notification in change_notification_iterator:
        num_notifications += 1
        msgs_received.append(json.dumps(cur_change_notification.get_simple_dict()))

    msg.set(msgs_received)

    logging.info('Complete - Notifications Processed: %s', str(num_notifications))

