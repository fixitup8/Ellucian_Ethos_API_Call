# Tests on main client object
import base64
import json

import testing_helper
from client_test_case import EthosClientTestCase


class Helpers(EthosClientTestCase):
    pass


class TestGetResource(Helpers):
    def test_get_person_no_version_specified(self):
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
        self.assertEqual(type(person).__name__, "PersonsV" + str(person_version_in_response))
        self.assertEqual(person.version, person_version_in_response)

    def test_get_person_version_specified_returns_correct_wrapper_object(self):
        for person_version_to_test in ["6", "8", "12", "12.1.0"]:
            person_guid = "testGUID"
            mock_response, mock_response_headers, mock_response_status_code = testing_helper.get_person_mock_result(
                person_guid=person_guid, version=person_version_to_test
            )
            person = self.get_resource_using_mock(
                guid=person_guid,
                mock_response=mock_response,
                mock_response_headers=mock_response_headers,
                version=person_version_to_test,
                mock_response_status_code=mock_response_status_code
            )
            if person_version_to_test == "12.1.0":
                self.assertEqual(type(person).__name__, "PersonsV12")
            else:
                self.assertEqual(type(person).__name__, "PersonsV" + person_version_to_test)

            self.assertEqual(person.version, person_version_to_test)

    def test_when_unknown_person_version_is_returned_generic_resource_wrapper_is_used(self):
        person_guid = "testGUID"
        mock_response, mock_response_headers, mock_response_status_code = testing_helper.get_person_mock_result(
            person_guid=person_guid, version="99999"
        )
        person = self.get_resource_using_mock(
            guid=person_guid,
            mock_response=mock_response,
            mock_response_headers=mock_response_headers,
            mock_response_status_code=mock_response_status_code
        )
        self.assertEqual(type(person).__name__, "BaseResourceWrapper")
        self.assertEqual(person.version, "99999")

    def test_requesting_unknown_resource_name_returns_generic_resource_wrapper(self):
        guid = "testGUID"
        mock_response, mock_response_headers, mock_response_status_code = testing_helper.get_minimum_resource_mock_result(
            guid=guid, version="99999"
        )
        resource_wrapper = self.get_resource_using_mock(
            guid=guid,
            mock_response=mock_response,
            mock_response_headers=mock_response_headers,
            mock_response_status_code=mock_response_status_code
        )
        self.assertEqual(type(resource_wrapper).__name__, "BaseResourceWrapper")
        self.assertEqual(resource_wrapper.version, "99999")

    def test_get_non_existant_person(self):
        person_version_in_response = "12"
        person_guid = "testGUID"
        mock_response, mock_response_headers, mock_response_status_code = testing_helper.get_person_not_found_mock_result(
            person_guid=person_guid, version=person_version_in_response
        )

        person = self.get_resource_using_mock(
            guid=person_guid,
            mock_response=mock_response,
            mock_response_headers=mock_response_headers,
            mock_response_status_code=mock_response_status_code
        )
        self.assertEqual(person, None)

    def test_refresh_person_no_version_specified(self):
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
        self.assertEqual(type(person).__name__, "PersonsV" + str(person_version_in_response))
        self.assertEqual(person.version, person_version_in_response)
        self.assertEqual(person.data["names"][0]["firstName"], "Joe")

        mock_response2, mock_response_headers2, mock_response_status_code2 = testing_helper.get_person_mock_result(
            person_guid=person_guid, version=person_version_in_response, first_name="Joe Number 2"
        )
        self.ethos_client.mock.registerNextResponse(
            reqFnName="get",
            url="/api/" + "persons" + "/" + person_guid,
            data=None,
            status_code=mock_response_status_code2,
            contentBytes=base64.b64encode(json.dumps(mock_response2).encode()),
            contentHeaders=mock_response_headers2,
            ignoreData=False
        )
        person.refresh(login_session=None)

        self.assertEqual(type(person).__name__, "PersonsV" + str(person_version_in_response))
        self.assertEqual(person.version, person_version_in_response)
        self.assertEqual(person.data["names"][0]["firstName"], "Joe Number 2")

    def test_requesting_unknown_resource_name_with_guid_rather_than_id_returns_generic_resource_wrapper(self):
        guid = "testGUID"
        mock_response, mock_response_headers, mock_response_status_code = testing_helper.get_minimum_resource_mock_result(
            guid=guid, version="99999", use_guid_as_id_key=True
        )
        resource_wrapper = self.get_resource_using_mock(
            guid=guid,
            mock_response=mock_response,
            mock_response_headers=mock_response_headers,
            mock_response_status_code=mock_response_status_code
        )
        self.assertEqual(type(resource_wrapper).__name__, "BaseResourceWrapper")
        self.assertEqual(resource_wrapper.version, "99999")
