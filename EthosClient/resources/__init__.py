"""Resource wrapper classes - turn raw Ethos API JSON into Python objects.

Start with BaseResourceWrapper (base.py) if you want to see the generic save/
delete/refresh behavior every resource gets. See persons.py for an example of
a resource-specific wrapper, and factory.py for how the right wrapper class
gets chosen for a given resource name and version.
"""
from .base import BaseResourceWrapper, NO_ID_IN_DATA
from .factory import get_resource_wrapper

__all__ = [
    "BaseResourceWrapper",
    "NO_ID_IN_DATA",
    "get_resource_wrapper",
]
