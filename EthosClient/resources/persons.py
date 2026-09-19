"""Resource wrapper for the "persons" resource, with version-specific subclasses."""
import copy

from .base import BaseResourceWrapper


def register_known_resources(resource_registry):
    """Add "persons" to the shared resource registry used by resources/factory.py."""

    def get_known_resource(version):
        major_version = version.split(".")[0]
        if major_version == "6":
            return PersonsV6
        if major_version == "8":
            return PersonsV8
        if major_version == "12":
            return PersonsV12
        return None

    resource_registry["persons"] = get_known_resource


class Persons(BaseResourceWrapper):
    address_list_cache = None

    def _get_data_for_put(self):
        ret_val = copy.deepcopy(self.data)

        # Updating addresses isn't supported yet - sending them to the API causes an error.
        if "addresses" in ret_val:
            del ret_val["addresses"]
        return ret_val

    def _after_data_changed(self):
        self.address_list_cache = None

    def get_addresses(self, login_session):
        """Return this person's addresses, fetching the full address resource for each."""
        if self.address_list_cache is None:
            self.address_list_cache = []
            for cur_address in self.data["addresses"]:
                new_entry = copy.deepcopy(cur_address)
                new_entry["address"] = self.client_api_instance.get_resource(
                    login_session=login_session,
                    resource_name="addresses",
                    resource_id=cur_address["address"]["id"],
                    version=None
                )
                self.address_list_cache.append(new_entry)

        return self.address_list_cache

    def get_visas(self, login_session):
        """Return a resource iterator over this person's visas."""
        params = {
            "criteria": "{\"person\": {\"id\": \"" + self.resource_id + "\"}}"
        }
        return self.client_api_instance.get_resource_iterator(
            login_session=login_session,
            resource_name="person-visas",
            version=None,
            params=params,
            page_size=25
        )


class PersonsV6(Persons):
    pass


class PersonsV8(Persons):
    pass


class PersonsV12(Persons):
    pass
