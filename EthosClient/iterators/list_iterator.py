"""Iterator that fetches a specific, known list of resource IDs one at a time."""


class ListBasedResourceIterator:
    """Python iterator over a fixed list of resource IDs.

    Unlike ResourceIterator (which pages through an entire collection), this fetches
    exactly the resources whose IDs you already know, one API call per ID.
    """

    api_client     = None
    login_session  = None
    resource_name  = None
    version        = None
    resource_id_list = None
    cur_idx        = None

    def __init__(self, api_client, login_session, resource_name, version, resource_id_list):
        self.api_client     = api_client
        self.login_session  = login_session
        self.resource_name  = resource_name
        self.version        = version
        self.resource_id_list = resource_id_list
        self.cur_idx        = 0

    def __iter__(self):
        self.cur_idx        = 0
        return self

    def __next__(self):
        if self.cur_idx < len(self.resource_id_list):
            ret_val = self.api_client.get_resource(
                login_session=self.login_session,
                resource_name=self.resource_name,
                resource_id  =self.resource_id_list[self.cur_idx],
                version      =self.version
            )
            self.cur_idx += 1
            return ret_val

        raise StopIteration
