"""Generic background thread that runs work on a fixed interval."""
import datetime
import threading
import time

import pytz  # handling time zones and daylight saving (DST) calculation


class WorkerThreadExceptionClass(Exception):
    pass


def get_next_worker_time(last_run_time, cur_time, frequency):
    """Return the next scheduled run time at or after cur_time, frequency seconds apart.

    Steps forward from last_run_time in frequency-second increments rather than just
    adding one interval, so a run that was delayed (e.g. by a slow worker()) doesn't
    cause a burst of catch-up runs.
    """
    ret_val = last_run_time
    while ret_val < cur_time:
        ret_val = ret_val + datetime.timedelta(seconds=int(frequency))
    return ret_val


class WorkerThread(threading.Thread):
    """Base class for a background thread that calls worker() every frequency seconds.

    Subclasses override worker() to do the actual work. The thread also tracks any
    exception worker() raises so the controlling thread can notice via health_check().
    """

    sleep_time = None
    running = None
    stopped = None
    thrown_exception = None
    frequency = None

    next_worker_time = None

    def __init__(self, sleep_time, frequency):
        super().__init__()
        self.sleep_time = sleep_time
        self.running = False
        self.thrown_exception = None
        self.stopped = False
        self.frequency = frequency

        # First run happens immediately when the thread is started.
        self.next_worker_time = datetime.datetime.now(pytz.timezone("UTC"))

    def run(self):
        try:
            self.stopped = False
            self.running = True
            while self.running:
                if datetime.datetime.now(pytz.timezone("UTC")) > self.next_worker_time:
                    self.worker()
                    self.next_worker_time = get_next_worker_time(
                        last_run_time=self.next_worker_time,
                        cur_time=datetime.datetime.now(pytz.timezone("UTC")),
                        frequency=self.frequency
                    )
                time.sleep(self.sleep_time)
            self.stopped = True
        except Exception as exception:
            self.thrown_exception = WorkerThreadExceptionClass("Poller thread threw an exception - " + str(exception))
            self.running = False

    def close(self, wait=True):
        if self.stopped:
            raise WorkerThreadExceptionClass("Should not try to close thread twice")
        self.stopped = False
        self.running = False
        if wait:
            while not self.stopped:
                self.health_check()
                time.sleep(self.sleep_time)

    def health_check(self):
        """Call from the controlling thread to re-raise any exception worker() threw."""
        if self.running:
            if not self.is_alive():
                raise WorkerThreadExceptionClass("Poller thread is no longer alive")
        if self.thrown_exception is not None:
            raise self.thrown_exception

    def worker(self):
        pass  # should be overridden by subclasses
