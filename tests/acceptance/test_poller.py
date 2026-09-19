# Tests on main client object
import base64
import json
import queue

import EthosClient
from client_test_case import EthosClientTestCase


class Helpers(EthosClientTestCase):
    pass


class TestPoller(Helpers):
    def test_not_able_to_start_poller_twice_without_close(self):
        poller_queue = queue.Queue()

        mock_response = {}
        self.ethos_client.mock.registerNextResponse(
            reqFnName="get",
            url="/consume?limit=20",
            data=None,
            status_code=200,
            contentBytes=base64.b64encode(json.dumps(mock_response).encode()),
            contentHeaders={"x-remaining": "0"},
            ignoreData=True
        )

        self.ethos_client.start_change_notification_poller_thread(
            login_session=None,
            frequency=60,  # number of seconds between fetches
            page_limit=20,  # number of change notifications to get per requests
            max_requests=4,  # maximum number of requests to use in each fetch
            poller_queue=poller_queue
        )

        with self.assertRaises(EthosClient.CanNotStartChangeNotificationPollerTwiceException):
            self.ethos_client.start_change_notification_poller_thread(
                login_session=None,
                frequency=60,
                page_limit=20,
                max_requests=4,
                poller_queue=poller_queue
            )

        self.ethos_client.close()

    def test_start_then_stop_poller(self):
        poller_queue = queue.Queue()

        mock_response = {}
        self.ethos_client.mock.registerNextResponse(
            reqFnName="get",
            url="/consume?limit=20",
            data=None,
            status_code=200,
            contentBytes=base64.b64encode(json.dumps(mock_response).encode()),
            contentHeaders={"x-remaining": "0"},
            ignoreData=True
        )
        self.ethos_client.start_change_notification_poller_thread(
            login_session=None,
            frequency=60,
            page_limit=20,
            max_requests=4,
            poller_queue=poller_queue
        )

        self.ethos_client.close()

    def test_start_then_stop_poller_function_mode(self):
        def process_single_message(api_client, message_id, change_notification):
            # in a real example this part would write to file or update a db
            print("received ", change_notification.operation, change_notification.resource_name, change_notification.resource_id)
            return True

        mock_response = {}
        self.ethos_client.mock.registerNextResponse(
            reqFnName="get",
            url="/consume?limit=20&lastProcessedID=123",
            data=None,
            status_code=200,
            contentBytes=base64.b64encode(json.dumps(mock_response).encode()),
            contentHeaders={"x-remaining": "0"},
            ignoreData=True
        )
        self.ethos_client.start_change_notification_poller_thread_in_function_mode(
            login_session=None,
            frequency=60,
            page_limit=20,
            max_requests=4,
            last_processed_id="123",
            message_processing_function=process_single_message
        )

        self.ethos_client.close()
