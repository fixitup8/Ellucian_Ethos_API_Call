# Tests on main client object
import base64
import json

import testing_helper
from client_test_case import EthosClientTestCase


class Helpers(EthosClientTestCase):
    pass


class TestListBasedResourceIterator(Helpers):
    def test_empty_list(self):
        person_iterator = self.ethos_client.get_list_based_resource_iterator(
            login_session=None,
            resource_name="persons",
            version=None,
            resource_id_list=[]
        )
        cur = 0
        for cur_person in person_iterator:
            cur += 1

        self.assertEqual(cur, 0)

    def test_single_item_list(self):
        person_version_in_response = "12"
        person_guid = "testGUID"
        resource_id_list = [person_guid]

        person_iterator = self.ethos_client.get_list_based_resource_iterator(
            login_session=None,
            resource_name="persons",
            version=None,
            resource_id_list=resource_id_list
        )
        cur = 0

        mock_response, mock_response_headers, mock_response_status_code = testing_helper.get_person_mock_result(
            person_guid=person_guid, version=person_version_in_response
        )
        self.ethos_client.mock.registerNextResponse(
            reqFnName="get",
            url="/api/persons/" + person_guid,
            data=None,
            status_code=mock_response_status_code,
            contentBytes=base64.b64encode(json.dumps(mock_response).encode()),
            contentHeaders=mock_response_headers,
            ignoreData=False
        )

        for cur_person in person_iterator:
            cur += 1
            self.assertEqual(type(cur_person).__name__, "PersonsV" + str(person_version_in_response))
            self.assertEqual(cur_person.version, person_version_in_response)
            self.assertEqual(cur_person.data["names"][0]["firstName"], "Joe")

        self.assertEqual(cur, 1)
