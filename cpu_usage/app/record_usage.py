'''Record CPU usage in and fetch them from a file.

cpu_usage/temp/store is the file in which the details are stored.
The CPU usage datas are sampled at the frequency of 1 second. And, the
average of the usages over 60 seconds is also calculated and stored in
a queue for every process.

@created: Mar 21, 2014
@author: Anshu Kumar, <anshu.choubey@imaginea.com>

@todo(Implement Logging)
'''

# pylint: disable=C0103

import json
import psutil
import time

from decimal import Decimal

from settings import SAMPLING_FREQ, AVG_INTERVAL, STORE_FILE


class Queue:
    """Queue data-structure implementation."""

    def __init__(self, maxsize='inf'):
        """Initialise the queue object.

        @param maxsize: Size of the queue. Beyond it the items will be popped
        as per the FIFO mechanism.
        """
        self.maxsize = maxsize
        self.items = []

    def is_full(self):
        """Check if queue is full to the size.
        @return: True if full, False otherwise.
        """
        return self.size() == self.maxsize

    def enqueue(self, item):
        """Puts an item into queue.

        If queue is full to its maximum size, pops the first in element and
        performs the insert operation.
        @param item: Item to be included into the queue.
        """
        if self.is_full():
            self.dequeue()
        self.items.insert(0, item)

    def dequeue(self):
        """Remove  and return the first in element from the present queue."""
        return self.items.pop()

    def size(self):
        """Calculate and return length of the queue."""
        return len(self.items)


# Stores queues for the CPU times of the processes.
# Format: {'1': {'user_q': user_queue, 'sys_q': sys_queue}}
process_queue = dict()
# Stores CPU usage details for the processes.
# Format: {"1": {"status": "sleeping", "user_avg": 0.3, "name": "init",
#                "pid": 1, "sys_avg": 0.56,
#                }}
processes = dict()


def add_processes(avg_interval):
    """Process CPU usage details for current processes and store them.

    Gets the list of current processes, computes their details and feed
    them into the class variables so that they can be stored in the file:
        cpu_usage/temp/store
    The average of CPU usages over the interval is also calculated and
    feed in the queue here.

    @param avg_interval: Interval over which average is to be calculated.
        Used as the length of the queue.
    @handles StopIteration.
    """
    _process = psutil.process_iter()
    try:
        while 1:
            try:
                new_proc = _process.next().\
                    as_dict(attrs=['cpu_times', 'name', 'pid', 'status'])
            except psutil.NoSuchProcess:
                continue
            pid, (user, _sys) = new_proc['pid'], new_proc.pop('cpu_times')
            # Get or create details object for the process.
            existing = processes.setdefault(pid, new_proc)
            # Get or create queue object for the CPU times of the process.
            queue_dict = process_queue.setdefault(pid, dict())
            # Get or create queue object for the user CPU time.
            user_q = queue_dict.setdefault('user_q', Queue(avg_interval))
            # Enqueue user CPU usage value.
            user_q.enqueue(user)
            # Calculate current user average.
            user_avg = get_avg(user_q)
            # Get or create queue object for the system CPU time.
            sys_q = queue_dict.setdefault('sys_q', Queue(avg_interval))
            # Enqueue system CPU usage value.
            sys_q.enqueue(_sys)
            # Calculate current system average.
            sys_avg = get_avg(sys_q)
            # Update the details object for the process.
            existing.update(user_avg=user_avg, sys_avg=sys_avg, **new_proc)
    except StopIteration:
        pass


def get_curr_processes(stored_process):
    """Return details for all current processes.

    @param stored_process: Stored details for the processes.
    @return: List of details of all current processes.
    """
    return [stored_process[str(pid)] for pid in psutil.get_pid_list()
            if str(pid) in stored_process]


def get_avg(q_obj, round_to=2):
    """Calculates average of the CPU usage over the interval.

    @param q_obj: Queue containing usage for process whose average is to
        be calculated.
    @param round_to: Number of places after decimal to round upto.
    @return: Calculated average of the CPU usage for the process.
    """
    return round(Decimal(sum(q_obj.items) / q_obj.size()), round_to)


def record(sampling_freq=SAMPLING_FREQ, avg_interval=AVG_INTERVAL):
    """Function invoked to record usage at every sampling frequency interval.

    Stores the processes' details at the interval of sampling frequency in the
    cpu_usage/temp/store file.

    @param sampling_freq: Time interval in seconds at which usage to be sampled.
        Defaults to 1 second.
    @param avg_interval: Time interval in seconds over which the average is to
        be calculated. Defaults to 60 seconds.
    """
    while 1:
        add_processes(avg_interval)
        with open(STORE_FILE, 'w') as fp:
            fp.write(json.dumps(processes))
        time.sleep(sampling_freq)


if __name__ == '__main__':
    try:
        record()
    except KeyboardInterrupt:
        pass
    except Exception:
        raise
