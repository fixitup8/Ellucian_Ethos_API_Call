# Tests on main client object
import base64
import json

import testing_helper
from client_test_case import EthosClientTestCase


class Helpers(EthosClientTestCase):
    def create_resource(
        self,
        resource_name,
        resource_data,
        mock_response,
        mock_response_headers,
        mock_response_status_code,
        type,
        version=None
    ):
        self.ethos_client.mock.registerNextResponse(
            reqFnName="post",
            url="/api/" + resource_name,
            data=json.dumps(resource_data),
            status_code=mock_response_status_code,
            contentBytes=base64.b64encode(json.dumps(mock_response).encode()),
            contentHeaders=mock_response_headers,
            ignoreData=False
        )

        resp = self.ethos_client.create_resource(
            login_session=None,
            resource_name=type,
            resource_data=resource_data,
            version=version
        )
        self.assertEqual(resp.resource_name, type)
        self.assertFalse(resp.resource_id is None)
        return resp


class TestCreateResource(Helpers):
    def test_create_person_hold(self):
        created_person_hold_guid = "testPersonHoldGUID"
        person_guid = "testGUID"
        person_hold_category_guid = "personHoldCategoryGUID"
        person_hold = {
            'endOn': '2099-12-31T00:00:00Z',
            'person': {'id': person_guid},
            'startOn': '2020-01-17T00:00:00Z',
            'type': {
                'category': 'academic',
                'detail': {
                    'id': person_hold_category_guid
                }
            }
        }
        version = "6"

        mock_response, mock_response_headers, mock_response_status_code = testing_helper.get_person_hold_mock_result(
            person_hold_guid=created_person_hold_guid,
            person_guid=person_guid,
            person_hold_category_guid=person_hold_category_guid,
            version=version
        )

        created_person_hold = self.create_resource(
            resource_name="person-holds",
            resource_data=person_hold,
            mock_response=mock_response,
            mock_response_headers=mock_response_headers,
            mock_response_status_code=201,
            type="person-holds",
            version=version
        )

        self.assertEqual(created_person_hold.version, version)
