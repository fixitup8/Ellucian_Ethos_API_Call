import datetime
import unittest

import pytz

import EthosClient


class TestGetNextWorkerTime(unittest.TestCase):
    def test_next_time_simple(self):
        self.assertEqual(
            EthosClient.get_next_worker_time(
                last_run_time=pytz.timezone('UTC').localize(datetime.datetime(2020, 1, 14, 23, 3, second=5)),
                cur_time=pytz.timezone('UTC').localize(datetime.datetime(2020, 1, 14, 23, 3, second=10)),
                frequency=6
            ),
            pytz.timezone('UTC').localize(datetime.datetime(2020, 1, 14, 23, 3, second=11))
        )

    def test_next_time_missed_run(self):
        self.assertEqual(
            EthosClient.get_next_worker_time(
                last_run_time=pytz.timezone('UTC').localize(datetime.datetime(2020, 1, 14, 23, 3, second=5)),
                cur_time=pytz.timezone('UTC').localize(datetime.datetime(2020, 1, 14, 23, 3, second=13)),
                frequency=6
            ),
            pytz.timezone('UTC').localize(datetime.datetime(2020, 1, 14, 23, 3, second=17))
        )
