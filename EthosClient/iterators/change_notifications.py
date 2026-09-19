"""Iterator over change notifications from the Ethos /consume endpoint.

fetch_next_change_notification_batch() is the shared core used both here and by
polling/change_notification_poller.py, since both need to request a batch of
messages, turn each one into a ChangeNotificationMessage, and hand it to a callback.
"""
import json

from ..messages import ChangeNotificationMessage


def fetch_next_change_notification_batch(page_limit, last_processed_id, client_api_instance, login_session, process_individual_message):
    """Fetch one page of change notifications and call process_individual_message for each.

    Returns the number of messages Ethos reports are still remaining to be consumed.
    """
    params = {"limit": str(page_limit)}
    if last_processed_id is not None:
        params["lastProcessedID"] = last_processed_id
    result = client_api_instance.sendGetRequest(
        url="/consume",
        params=params,
        loginSession=login_session,
        injectHeadersFn=None
    )
    if result.status_code != 200:
        client_api_instance.raiseResponseException(result)

    remaining_messages = int(result.headers["x-remaining"])
    result_data = json.loads(result.content)

    for cur_result in result_data:
        change_notification = ChangeNotificationMessage(data=cur_result, client_api_instance=client_api_instance)
        process_individual_message(change_notification=change_notification)

    return remaining_messages


class ChangeNotificationIterator:
    """Python iterator over change notifications, fetching new pages as needed."""

    client_api_instance = None
    login_session   = None
    page_limit      = None
    max_requests    = None

    requests_remaining = None
    cur_idx         = None
    cur_result_list = None

    def __init__(self, login_session, page_limit, max_requests, client_api_instance):
        self.client_api_instance = client_api_instance
        self.login_session   = login_session
        self.page_limit      = page_limit
        self.max_requests    = max_requests

        self.requests_remaining = self.max_requests
        self.cur_idx         = 0
        self.cur_result_list = []

    def __iter__(self):
        self.requests_remaining = self.max_requests
        self.cur_idx         = 0
        self.cur_result_list = []
        return self

    def _load_new_page_of_results(self):
        self.cur_idx         = 0
        self.cur_result_list = []

        def process_individual_message(change_notification):
            self.cur_result_list.append(change_notification)

        fetch_next_change_notification_batch(
            page_limit          =self.page_limit,
            client_api_instance =self.client_api_instance,
            login_session       =self.login_session,
            process_individual_message=process_individual_message,
            last_processed_id   =None
        )

    def __next__(self):
        if self.cur_idx >= len(self.cur_result_list):
            if self.requests_remaining == 0:
                raise StopIteration
            self.requests_remaining -= 1
            self._load_new_page_of_results()

        if self.cur_idx >= len(self.cur_result_list):
            # We tried getting a new page but there are still no results, so terminate.
            raise StopIteration

        ret_val = self.cur_result_list[self.cur_idx]
        self.cur_idx += 1
        return ret_val
