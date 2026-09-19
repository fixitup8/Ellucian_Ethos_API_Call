"""Generic wrapper around a raw Ethos API resource JSON payload."""
import copy
import json

NO_ID_IN_DATA = "NO_ID_IN_DATA"


class BaseResourceWrapper:
    """Wraps a resource's raw data and adds save/delete/refresh helpers.

    This is the fallback wrapper used for any resource that doesn't have a more
    specific wrapper registered in resources/factory.py. Resource-specific wrappers
    (e.g. resources/persons.py) subclass this to add resource-specific behavior.
    """

    client_api_instance = None
    data = None
    version = None
    resource_name = None
    resource_id = None

    def __init__(self, client_api_instance, data, version, resource_name):
        self.client_api_instance = client_api_instance
        self.data = data
        self.version = version
        self.resource_name = resource_name
        if not isinstance(version, str):
            raise Exception("Version passed must be a string")
        self.resource_id = self._get_resource_id_from_data(data)
        self._after_data_changed()

    def _get_resource_id_from_data(self, data):
        if "id" in data:
            return data["id"]
        if "guid" in data:
            return data["guid"]
        return NO_ID_IN_DATA

    def get_major_version(self):
        return self.version.split(".")[0]

    def _get_data_for_put(self):
        # Subclasses override this to strip fields the API rejects on update.
        return copy.deepcopy(self.data)

    def save(self, login_session):
        """Send this resource's current data back to Ethos as an update (PUT)."""
        if self.resource_id == NO_ID_IN_DATA:
            raise Exception("Can not save - no id in data")

        def inject_header_fn(headers):
            headers["Accept"] = "application/vnd.hedtech.integration.v" + self.get_major_version() + "+json"
            headers["Content-Type"] = "application/vnd.hedtech.integration.v" + self.get_major_version() + "+json"

        url = "/api/" + self.resource_name + "/" + self.resource_id

        result = self.client_api_instance.sendPutRequest(
            url=url,
            loginSession=login_session,
            injectHeadersFn=inject_header_fn,
            data=json.dumps(self._get_data_for_put())
        )
        if result.status_code != 200:
            self.client_api_instance.raiseResponseException(result)

        self.data = json.loads(result.content)
        self._after_data_changed()

    def delete(self, login_session):
        """Delete this resource from Ethos."""
        if self.resource_id == NO_ID_IN_DATA:
            raise Exception("Can not delete - no id in data")

        url = "/api/" + self.resource_name + "/" + self.resource_id

        result = self.client_api_instance.sendDeleteRequest(
            url=url,
            loginSession=login_session,
            injectHeadersFn=None,
        )
        if result.status_code != 200:
            self.client_api_instance.raiseResponseException(result)

    def refresh(self, login_session):
        """Re-fetch this resource from Ethos and replace the local data with the result."""
        if self.resource_id == NO_ID_IN_DATA:
            raise Exception("Can not refresh - no id in data")

        (result_content, version_returned, resource_name) = self.client_api_instance._get_resource_raw(
            login_session=login_session,
            resource_name=self.resource_name,
            resource_id=self.resource_id,
            version=self.version
        )
        if version_returned is None:
            raise Exception("Refresh failed - no resource found")
        if version_returned != self.version:
            raise Exception("Internal Error wrong version on refresh")
        if resource_name != self.resource_name:
            raise Exception("Internal Error wrong resource_name on refresh")
        self.data = json.loads(result_content)
        self._after_data_changed()

    def _after_data_changed(self):
        # Called after self.data is replaced (e.g. after creation, save or refresh).
        # Subclasses override this to clear any caches derived from the old data.
        pass
