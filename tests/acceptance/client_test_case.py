import base64
import json
import unittest

import EthosClient

ethos_base_url = "MOCK"


class EthosClientTestCase(unittest.TestCase):
    """Base class for acceptance tests - sets up a mocked EthosAPIClient."""

    ethos_client = None

    def setUp(self):
        self.ethos_client = EthosClient.EthosAPIClient(base_url=ethos_base_url)

    def tearDown(self):
        self.ethos_client.testComplete()
        self.ethos_client = None

    def get_resource_using_mock(
        self,
        guid,
        mock_response,
        mock_response_headers,
        mock_response_status_code,
        type="persons",
        version=None
    ):
        self.ethos_client.mock.registerNextResponse(
            reqFnName="get",
            url="/api/" + type + "/" + guid,
            data=None,
            status_code=mock_response_status_code,
            contentBytes=base64.b64encode(json.dumps(mock_response).encode()),
            contentHeaders=mock_response_headers,
            ignoreData=False
        )

        resp = self.ethos_client.get_resource(
            login_session=None,
            resource_name=type,
            resource_id=guid,
            version=version
        )
        if resp is None:
            return resp
        self.assertEqual(resp.resource_name, type)
        self.assertEqual(resp.resource_id, guid)
        return resp
