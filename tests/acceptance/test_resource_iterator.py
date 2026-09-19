# Tests on main client object
import base64
import json

import testing_helper
from client_test_case import EthosClientTestCase


class Helpers(EthosClientTestCase):
    pass


class TestResourceIterator(Helpers):
    def test_single_page(self):
        person_guid = "personGUID"

        single_person_response_data, _, _ = testing_helper.get_person_mock_result(person_guid=person_guid, version="6")
        mock_response = [single_person_response_data] * 5

        self.ethos_client.mock.registerNextResponse(
            reqFnName="get",
            url="/api/persons?limit=9&offset=5",
            data=None,
            status_code=200,
            contentBytes=base64.b64encode(json.dumps([]).encode()),
            contentHeaders={
                "x-hedtech-media-type": "application/vnd.hedtech.integration.v6+json"
            },
            ignoreData=False
        )
        self.ethos_client.mock.registerNextResponse(
            reqFnName="get",
            url="/api/persons?limit=9&offset=0",
            data=None,
            status_code=200,
            contentBytes=base64.b64encode(json.dumps(mock_response).encode()),
            contentHeaders={
                "x-hedtech-media-type": "application/vnd.hedtech.integration.v6+json"
            },
            ignoreData=False
        )

        person_iterator = self.ethos_client.get_resource_iterator(
            login_session=None,
            resource_name="persons",
            version=None,
            page_size=9
        )
        cur = 0
        for cur_person in person_iterator:
            cur += 1

        self.assertEqual(cur, 5)

    def test_response_with_x_media_type_header_version_header(self):
        person_guid = "personGUID"

        single_person_response_data, _, _ = testing_helper.get_person_mock_result(person_guid=person_guid, version="6")
        mock_response = [single_person_response_data] * 5

        self.ethos_client.mock.registerNextResponse(
            reqFnName="get",
            url="/api/persons?limit=9&offset=5",
            data=None,
            status_code=200,
            contentBytes=base64.b64encode(json.dumps([]).encode()),
            contentHeaders={
                "x-media-type": "application/vnd.hedtech.integration.v6+json"
            },
            ignoreData=False
        )
        self.ethos_client.mock.registerNextResponse(
            reqFnName="get",
            url="/api/persons?limit=9&offset=0",
            data=None,
            status_code=200,
            contentBytes=base64.b64encode(json.dumps(mock_response).encode()),
            contentHeaders={
                "x-media-type": "application/vnd.hedtech.integration.v6+json"
            },
            ignoreData=False
        )

        person_iterator = self.ethos_client.get_resource_iterator(
            login_session=None,
            resource_name="persons",
            version=None,
            page_size=9
        )
        cur = 0
        for cur_person in person_iterator:
            cur += 1

        self.assertEqual(cur, 5)
