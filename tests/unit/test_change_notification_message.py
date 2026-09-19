import unittest

import EthosClient


class TestChangeNotification(unittest.TestCase):
    def test_simple_dict_output(self):
        ethos_client = EthosClient.EthosAPIClient(base_url="MOCK")

        sample_fn_call_response = {
            'id': '3764', 'published': '2020-07-02 13:38:38.183489+00',
            'resource': {'name': 'person-holds', 'id': 'c997507d-4f46-4cde-bee0-a75cc412e734',
                         'version': 'application/vnd.hedtech.integration.v6+json'}, 'operation': 'created',
            'contentType': 'resource-representation',
            'content': {'endOn': '2099-12-31T00:00:00Z', 'id': 'c997507d-4f46-4cde-bee0-a75cc412e734',
                        'person': {'id': '5bcbc3b1-cf8a-4ea6-9042-1dc3e14aa3ba'}, 'startOn': '2020-01-17T00:00:00Z',
                        'type': {'category': 'academic', 'detail': {'id': '45182c89-6bb8-4996-a05a-6fce28f028eb'}}},
            'publisher': {'id': '84592449-455b-40ea-9856-cb9e6878bd21', 'applicationName': 'Imperial Student API - BILD'}
        }

        change_notification = EthosClient.ChangeNotificationMessage(data=sample_fn_call_response, client_api_instance=ethos_client)

        self.assertEqual(change_notification.get_simple_dict(), sample_fn_call_response)
