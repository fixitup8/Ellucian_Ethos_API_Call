"""EthosClient - a Python client for the Ellucian Ethos integration API.

Start here:
- client.py: EthosAPIClient, the main entry point (create/read/update/delete
  resources, plus change-notification polling).
- auth.py: ApiKeyLoginSession, used to log in with an API key.
- resources/: turns raw resource JSON into Python objects.
- iterators/: pages through resource collections and change notifications.
- polling/: the background thread used for change-notification polling.

See docs/QUICKSTART.md in the repo root for a guided tour.
"""
from .client import PollerAlreadyRunningException, EthosAPIClient
from .messages import ChangeNotificationMessage
from .polling import get_next_worker_time

__all__ = [
    "EthosAPIClient",
    "PollerAlreadyRunningException",
    "ChangeNotificationMessage",
    # exported so unit tests can exercise it directly
    "get_next_worker_time",
]
