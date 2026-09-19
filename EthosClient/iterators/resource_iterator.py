"""Iterator that pages through every resource of a given type."""
import json

from ..resources import get_resource_wrapper


class ResourceIterator:
    """Python iterator that transparently pages through an Ethos resource collection.

    Fetches page_size resources at a time, yielding wrapped resource objects one by
    one and requesting the next page once the current one is exhausted.
    """

    api_client = None
    login_session = None
    resource_name = None
    version = None
    page_size = None
    cur_list = None
    cur_idx = None
    cur_offset = None
    version_returned = None
    params = None

    def __init__(self, api_client, login_session, resource_name, version, page_size, params):
        self.api_client = api_client
        self.login_session = login_session
        self.resource_name = resource_name
        self.version = version
        self.page_size = page_size

        self.cur_list = []
        self.cur_idx = 0
        self.cur_offset = 0
        self.params = {} if params is None else params
        self.version_returned = None

    def __iter__(self):
        self.cur_list = []
        self.cur_idx = 0
        self.cur_offset = 0
        return self

    def __next__(self):
        if self.cur_idx >= len(self.cur_list):
            self._collect_next_page()
            if self.cur_idx >= len(self.cur_list):
                raise StopIteration
        cur = self.cur_idx
        self.cur_idx += 1
        return get_resource_wrapper(
            client_api_instance=self.api_client,
            data=self.cur_list[cur],
            version=self.version_returned,
            resource_name=self.resource_name
        )

    def _collect_next_page(self):
        def inject_header_fn(headers):
            if self.version is not None:
                headers["Accept"] = "application/vnd.hedtech.integration.v" + self.version + "+json"

        self.params["limit"] = str(self.page_size)
        self.params["offset"] = str(self.cur_offset)
        result = self.api_client.sendGetRequest(
            url="/api/" + self.resource_name,
            params=self.params,
            loginSession=self.login_session,
            injectHeadersFn=inject_header_fn
        )
        if result.status_code != 200:
            self.api_client.raiseResponseException(result)

        if self.version_returned is None:
            self.version_returned = self.api_client.get_version_from_result(result)

        self.cur_list = json.loads(result.content)
        self.cur_idx = 0
        self.cur_offset += len(self.cur_list)
