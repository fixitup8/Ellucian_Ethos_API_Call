"""EthosAPIClient - the main entry point for this library.

Create one instance per Ethos application, get a login session from an API key, and
use the client to fetch/create/update/delete resources or start a change-notification
poller. See docs/QUICKSTART.md for a full walkthrough.
"""
import json

import PythonAPIClientBase

from .auth      import EthosLoginSessionBasedOnAPIKey
from .iterators import ChangeNotificationIterator, ListBasedResourceIterator, ResourceIterator
from .polling   import EthosChangeNotificationPollerThreadFunctionMode, EthosChangeNotificationPollerThreadQueueMode
from .resources import get_resource_wrapper


class CanNotStartChangeNotificationPollerTwiceException(Exception):
    pass


class MissingHeaderException(Exception):
    result  = None
    msg     = None

    def __init__(self, msg, result):
        self.result = result
        self.msg    = msg

    def get_description_string(self):
        ret = ""
        ret += "Failed API request - " + self.msg + "\n"
        ret += "Request: " + str(self.result.request.method) + ":" + str(self.result.request.url) + "\n"
        ret += "Response: " + str(self.result.status_code) + ":" + self.result.content.decode() + "\n"
        ret += "Response Headers: " + str(self.result.headers) + "\n"
        return ret

    def __str__(self):
        return self.get_description_string()


class EthosAPIClient(PythonAPIClientBase.APIClientBase):
    change_notification_poller_thread = None

    def __init__(self, base_url, mock=None, verbose_logging=PythonAPIClientBase.VerboseLoggingNullLogClass()):
        super().__init__(baseURL=base_url, mock=mock, forceOneRequestAtATime=True, verboseLogging=verbose_logging)
        self.change_notification_poller_thread = None

    def get_login_session_from_api_key(self, api_key):
        return EthosLoginSessionBasedOnAPIKey(api_client=self, api_key=api_key)

    def _get_resource_raw(self, login_session, resource_name, resource_id, version=None):
        def inject_header_fn(headers):
            if version is not None:
                headers["Accept"] = "application/vnd.hedtech.integration.v" + version + "+json"

        result = self.sendGetRequest(
            url="/api/" + resource_name + "/" + resource_id,
            loginSession=login_session,
            injectHeadersFn=inject_header_fn
        )
        if result.status_code == 404:
            return (None, None, None)
        if result.status_code != 200:
            self.raiseResponseException(result)

        version_returned = self.get_version_from_result(result)
        return (result.content, version_returned, resource_name)

    def get_resource(self, login_session, resource_name, resource_id, version=None):
        """Fetch a single resource by ID, or None if it doesn't exist.

        See https://xedocs.ellucian.com/xe-banner-api/ethos_apis/foundation/persons/person_get_guid_v6.html
        for an example of the underlying API this wraps.
        """
        (result_content, version_returned, resource_name) = self._get_resource_raw(
            login_session = login_session,
            resource_name = resource_name,
            resource_id   = resource_id,
            version       = version
        )
        if result_content is None:
            return None
        return get_resource_wrapper(
            client_api_instance=self,
            data         = json.loads(result_content),
            version      = version_returned,
            resource_name= resource_name
        )

    def get_resource_iterator(self, login_session, resource_name, version=None, page_size=25, params=None):
        """Return a Python iterator that pages through every resource of resource_name."""
        return ResourceIterator(self, login_session, resource_name, version, page_size, params=params)

    def get_list_based_resource_iterator(self, login_session, resource_name, resource_id_list, version=None):
        """Return a Python iterator that fetches exactly the given list of resource IDs."""
        return ListBasedResourceIterator(self, login_session, resource_name, version, resource_id_list=resource_id_list)

    def get_change_notification_iterator(self, login_session, page_limit=25, max_requests=4):
        """Return a Python iterator over change notifications from the /consume endpoint."""
        return ChangeNotificationIterator(
            login_session   = login_session,
            page_limit      = page_limit,
            max_requests    = max_requests,
            client_api_instance=self
        )

    def get_version_from_result(self, result):
        version_header = None
        if "x-hedtech-media-type" in result.headers:
            version_header = result.headers["x-hedtech-media-type"]
        elif "x-media-type" in result.headers:
            version_header = result.headers["x-media-type"]

        if version_header is None:
            raise MissingHeaderException("Response is missing header x-hedtech-media-type (or x-media-type)", result)
        return self._get_version_int_from_header(version_header)

    def _get_version_int_from_header(self, media_type_header_value):
        # example: application/vnd.hedtech.integration.v6+json
        required_start = "application/vnd.hedtech.integration.v"
        required_end = "+json"
        if not media_type_header_value.startswith(required_start):
            raise Exception("Could not determine resource version")
        media_type_header_value = media_type_header_value[len(required_start):]
        if not media_type_header_value.endswith(required_end):
            raise Exception("Could not determine resource version - header didn't end with " + required_end)
        media_type_header_value = media_type_header_value[:-len(required_end)]
        return media_type_header_value

    def create_resource(self, login_session, resource_name, resource_data, version=None):
        if version is None:
            raise Exception("Must supply version when creating resource")

        def inject_header_fn(headers):
            headers["Accept"] = "application/vnd.hedtech.integration.v" + version + "+json"
            headers["Content-Type"] = "application/vnd.hedtech.integration.v" + version + "+json"

        result = self.sendPostRequest(
            url             = "/api/" + resource_name,
            loginSession    = login_session,
            injectHeadersFn = inject_header_fn,
            data            = json.dumps(resource_data)
        )
        if result.status_code != 201:
            self.raiseResponseException(result)

        version_returned = self.get_version_from_result(result)

        return get_resource_wrapper(
            client_api_instance=self,
            data         =json.loads(result.content),
            version      =version_returned,
            resource_name=resource_name
        )

    def delete_resource(self, login_session, resource_name, resource_id):
        url = "/api/" + resource_name + "/" + resource_id

        result = self.sendDeleteRequest(
            url          = url,
            loginSession =login_session,
            injectHeadersFn=None
        )
        if result.status_code != 200:
            self.raiseResponseException(result)

    def start_change_notification_poller_thread(self, login_session, frequency, page_limit, max_requests, poller_queue):
        """Start a background thread that pushes change notifications onto poller_queue.

        frequency: seconds between fetches.
        page_limit: number of change notifications to request per page.
        max_requests: maximum number of pages to request per fetch.
        """
        if self.change_notification_poller_thread is not None:
            raise CanNotStartChangeNotificationPollerTwiceException()
        self.change_notification_poller_thread = EthosChangeNotificationPollerThreadQueueMode(
            client_api_instance=self,
            login_session   =login_session,
            frequency       =frequency,
            page_limit      =page_limit,
            max_requests    = max_requests,
            poller_queue    =poller_queue
        )
        self.change_notification_poller_thread.start()

    def start_change_notification_poller_thread_in_function_mode(
        self,
        login_session,
        frequency,  # seconds between fetches
        page_limit,  # number of change notifications to request per page
        max_requests,  # maximum number of pages to request per fetch
        last_processed_id,
        message_processing_function
    ):
        """Like start_change_notification_poller_thread, but calls message_processing_function
        for each message instead of using a queue, so last_processed_id can be persisted
        reliably as each message is handled. See docs/POLLERGUIDE.md.
        """
        if self.change_notification_poller_thread is not None:
            raise CanNotStartChangeNotificationPollerTwiceException()
        self.change_notification_poller_thread = EthosChangeNotificationPollerThreadFunctionMode(
            client_api_instance=self,
            login_session   =login_session,
            frequency       =frequency,
            page_limit      =page_limit,
            max_requests    = max_requests,
            last_processed_id=last_processed_id,
            message_processing_function=message_processing_function
        )
        self.change_notification_poller_thread.start()

    def health_check(self):
        """Re-raise any exception the change-notification poller thread has thrown."""
        if self.change_notification_poller_thread is not None:
            self.change_notification_poller_thread.health_check()

    def close(self):
        if self.change_notification_poller_thread is not None:
            self.change_notification_poller_thread.close()
            self.change_notification_poller_thread = None

    def status(self):
        print("Ethos Client status")
        if self.change_notification_poller_thread is None:
            print("Change notification poller thread NOT RUNNING")
        else:
            print("Change notification poller thread Running")
