"""Login session that authenticates to Ethos using an application API key."""
from PythonAPIClientBase import LoginSession
import requests


class ApiKeyLoginSession(LoginSession):
    """Exchanges an Ethos application API key for a short-lived bearer token.

    injectHeaders() and refresh() are required override names - they're called by
    PythonAPIClientBase.APIClientBase whenever it sends a request or gets a 401.
    """

    api_client       = None
    api_key          = None
    current_auth_key = None

    def __init__(self, api_client, api_key):
        self.api_client = api_client
        self.api_key    = api_key

        self._get_new_auth_token()
        if self.current_auth_key is None:
            raise Exception("Failed to establish login session using APIKey")

    def _get_new_auth_token(self, from_refresh=False):
        self.current_auth_key = None
        charset = "UTF-8"

        def inject_header_fn(headers):
            headers["Accept-Charset"] = charset
            headers["Content-Type"] = "application/x-www-form-urlencoded" + ";charset=" + charset
            headers["Authorization"] = "Bearer " + self.api_key

        result = self.api_client.sendRequest(
            reqFn=requests.post,   origin=None,   url="/auth",  data=[],
            loginSession=None,     injectHeadersFn=inject_header_fn,
            skipLockCheck=from_refresh
        )
        if result.status_code != 200:
            return None

        self.current_auth_key = result.content.decode(charset)

    def injectHeaders(self, headers):
        headers["Authorization"] = "Bearer " + self.current_auth_key

    def refresh(self):
        # Returns True to signal the original request should be retried.
        self._get_new_auth_token(from_refresh=True)
        if self.current_auth_key is None:
            return False
        return True
