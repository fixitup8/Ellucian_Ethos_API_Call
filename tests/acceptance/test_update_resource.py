# Tests of updating a resource
import base64
import json

import testing_helper
from client_test_case import EthosClientTestCase


class Helpers(EthosClientTestCase):
    def save_resource(
        self,
        resource_wrapper_object,
        mock_response,
        mock_response_headers,
        mock_response_status_code
    ):
        self.ethos_client.mock.registerNextResponse(
            reqFnName="put",
            url="/api/" + resource_wrapper_object.resource_name + "/" + resource_wrapper_object.resource_id,
            data=json.dumps(resource_wrapper_object._get_data_for_put()),
            status_code=mock_response_status_code,
            contentBytes=base64.b64encode(json.dumps(mock_response).encode()),
            contentHeaders=mock_response_headers,
            ignoreData=False
        )

        resource_wrapper_object.save(login_session=None)


class TestUpdateResource(Helpers):
    def test_update_persons(self):
        person_version_in_response = "12"
        person_guid = "testGUID"
        mock_response, mock_response_headers, mock_response_status_code = testing_helper.get_person_mock_result(
            person_guid=person_guid, version=person_version_in_response
        )

        person = self.get_resource_using_mock(
            guid=person_guid,
            mock_response=mock_response,
            mock_response_headers=mock_response_headers,
            mock_response_status_code=mock_response_status_code
        )
        person.data["names"][0]["lastName"] = "ChangedLastName"

        mock_response, mock_response_headers, mock_response_status_code = testing_helper.get_person_mock_result(
            person_guid=person_guid, version=person_version_in_response
        )
        mock_response["names"][0]["lastName"] = person.data["names"][0]["lastName"]
        self.save_resource(
            resource_wrapper_object=person,
            mock_response=mock_response,
            mock_response_headers=mock_response_headers,
            mock_response_status_code=mock_response_status_code
        )

        # Make sure object has updated value
        self.assertEqual(person.data["names"][0]["lastName"], "ChangedLastName")
