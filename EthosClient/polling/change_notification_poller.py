"""Background thread that polls Ethos for change notifications.

See:
https://resources.elluciancloud.com/bundle/ethos_integration_ref_apis/page/r_message_queue_api_retrieve_msgs.html
"""
from ..iterators import fetch_next_change_notification_batch
from .worker_thread import WorkerThread


class EthosChangeNotificationPollerThreadExceptionClass(Exception):
    pass


class EthosChangeNotificationPollerThread(WorkerThread):
    """Base poller thread - fetches batches of change notifications on each tick.

    Not used directly; use QueueModePollerThread or
    FunctionModePollerThread, which provide process_message().
    """

    client_api_instance = None
    login_session   = None
    page_limit      = None
    max_requests    = None
    last_processed_id = None

    def __init__(self, client_api_instance, login_session, frequency, page_limit, max_requests, last_processed_id):
        super().__init__(sleep_time=0.1, frequency=frequency)
        self.client_api_instance = client_api_instance
        self.login_session   = login_session
        self.page_limit      = page_limit
        self.max_requests    = max_requests
        self.last_processed_id = last_processed_id

    def worker(self):
        fetch_running = True
        num_requests_sent = 0
        while fetch_running:
            num_requests_sent += 1
            remaining_messages = self._fetch_and_process_next_batch()
            if remaining_messages == 0:
                fetch_running = False
            if num_requests_sent == self.max_requests:
                fetch_running = False

    def _fetch_and_process_next_batch(self):
        def process_individual_message(change_notification):
            self.process_message(change_notification=change_notification)
            if self.last_processed_id is not None:
                self.last_processed_id = change_notification.message_id

        return fetch_next_change_notification_batch(
            page_limit          =self.page_limit,
            last_processed_id   =self.last_processed_id,
            client_api_instance =self.client_api_instance,
            login_session       =self.login_session,
            process_individual_message=process_individual_message
        )

    def process_message(self, change_notification):
        pass  # overridden by subclasses


class QueueModePollerThread(EthosChangeNotificationPollerThread):
    """Poller that pushes each change notification onto a queue.Queue for you to drain."""

    poller_queue = None

    def __init__(self, client_api_instance, login_session, frequency, page_limit, max_requests, poller_queue):
        super().__init__(
            client_api_instance=client_api_instance,
            login_session      =login_session,
            frequency          =frequency,
            page_limit         =page_limit,
            max_requests       = max_requests,
            last_processed_id  =None
        )
        self.poller_queue = poller_queue

    def process_message(self, change_notification):
        self.poller_queue.put(change_notification)


class FunctionModePollerThread(EthosChangeNotificationPollerThread):
    """Poller that calls a supplied function for each change notification.

    Useful when you need to persist last_processed_id reliably (e.g. to disk) as each
    message is processed, rather than risk losing messages sitting in a queue.
    """

    message_processing_function = None

    def __init__(self, client_api_instance, login_session, frequency, page_limit, max_requests, last_processed_id, message_processing_function):
        super().__init__(
            client_api_instance =client_api_instance,
            login_session       =login_session,
            frequency          =frequency,
            page_limit         =page_limit,
            max_requests       = max_requests,
            last_processed_id  =last_processed_id
        )
        self.message_processing_function = message_processing_function

    def process_message(self, change_notification):
        self.message_processing_function(
            api_client=self.client_api_instance,
            message_id=change_notification.message_id,
            change_notification=change_notification
        )
