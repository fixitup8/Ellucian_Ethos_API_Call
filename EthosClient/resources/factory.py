"""Picks the right resource wrapper class for a given resource name and version."""
from .base import BaseResourceWrapper
from .persons import register_known_resources as register_persons_known_resources

KNOWN_RESOURCES = {}
register_persons_known_resources(KNOWN_RESOURCES)


def get_resource_wrapper(client_api_instance, data, version, resource_name):
    """Wrap raw resource data in the most specific wrapper class available.

    Falls back to BaseResourceWrapper when resource_name/version isn't registered.
    """
    if resource_name in KNOWN_RESOURCES:
        wrapper_class = KNOWN_RESOURCES[resource_name](version)
        if wrapper_class is not None:
            return wrapper_class(client_api_instance, data, version, resource_name)
    return BaseResourceWrapper(client_api_instance, data, version, resource_name)
