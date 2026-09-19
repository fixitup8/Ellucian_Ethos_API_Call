"""Wraps a single change notification message received from Ethos.

Example raw message (see docs/POLLERGUIDE.md for the full walkthrough):

    {
        "id": "105",
        "published": "2020-06-23 09:26:24.732506+00",
        "resource": {
            "name": "person-holds",
            "id": "7620b51d-acee-44cf-a4f9-85cc16f5c737",
            "version": "application/vnd.hedtech.integration.v6+json"
        },
        "operation": "created",
        "contentType": "resource-representation",
        "content": { ... the person-hold resource itself, when contentType is set ... },
        "publisher": {
            "id": "84592449-455b-40ea-9856-cb9e6878bd21",
            "applicationName": "Imperial Student API - BILD"
        }
    }
"""
from dateutil.parser import parse
import pytz

from .resources import get_resource_wrapper


class ChangeNotificationMessage:
    client_api_instance = None
    message_id      = None
    published       = None
    operation       = None
    resource_name   = None
    resource_id     = None
    resource_version = None
    resource_wrapper = None

    orig_data = None

    def __init__(self, data, client_api_instance):
        self.orig_data = data
        self.client_api_instance = client_api_instance
        self.message_id = data["id"]

        published_at = parse(data["published"])
        self.published = published_at.astimezone(pytz.utc)

        self.operation = data["operation"]  # created, deleted, etc

        # These fields are always present - even for a deleted operation.
        self.resource_name = data["resource"]["name"]
        self.resource_id   = data["resource"]["id"]
        if "version" in data["resource"]:
            # version isn't sent for a deleted operation
            self.resource_version = client_api_instance._get_version_int_from_header(data["resource"]["version"])

        # For operation=deleted, contentType is empty since Ethos doesn't send the
        # resource content. For operation=created it's "resource-representation".
        if data["contentType"] == "resource-representation":
            self.resource_wrapper = get_resource_wrapper(
                client_api_instance=self.client_api_instance,
                data=data["content"],
                version=self.resource_version,
                resource_name=self.resource_name
            )
        else:
            self.resource_wrapper = None

    def get_simple_dict(self):
        return self.orig_data
