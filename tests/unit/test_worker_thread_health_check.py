import unittest

from EthosClient.polling import WorkerThread, WorkerThreadExceptionClass


class TestWorkerThreadHealthCheck(unittest.TestCase):
    def test_health_check_uses_python3_thread_api(self):
        worker = WorkerThread(sleep_time=0.01, frequency=1)
        worker.running = True
        worker.stopped = False
        worker.thrown_exception = None
        worker.is_alive = lambda: False

        with self.assertRaises(WorkerThreadExceptionClass):
            worker.health_check()
