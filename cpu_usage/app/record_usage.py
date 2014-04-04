'''Record CPU usage in a concurrent thread.

The CPU usage datas are sampled at the frequency of 1 second. The average of
the usages over 60 seconds is also calculated and updated for every process.

@created: Mar 21, 2014
@author: Anshu Kumar, <anshu.choubey@imaginea.com>

@todo(Implement Logging)
'''

# pylint: disable=C0103

import psutil
import time

from decimal import Decimal
from threading import Lock

import settings


class PeekableQueue(object):
    """Queue data-structure implementation. Different from inbuilt queue, in
    terms that, the elements can be iterated and fetched all at once for some
    operation, e.g. computing average.
    """

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
        self.items.append(item)

    def dequeue(self):
        """Remove  and return the first in element from the present queue."""
        if self.size():
            return self.items.pop(0)

    def size(self):
        """Calculate and return length of the queue."""
        return len(self.items)

    def get_avg(self, round_to=settings.ROUND_TO):
        """Calculates average of the CPU usage over the interval.

        @param round_to: Number of places after the decimal to round the value
            upto. Defaults to 2.
        @raise ZeroDivisionError: Empty queue average calculation attempt.
        @return: Calculated average of the CPU usage for the process.
        """
        try:
            return round(
                Decimal(sum(self.items) / float(self.size())), round_to)
        except ZeroDivisionError:
            raise


class RecordUsage(object):
    """Records CPU usage sampled at a certain rate and averaged over a
    certain interval.
    """
    # Stores queues for the CPU times of the processes.
    # Format: {1: {'user_avg_q': user_queue, 'sys_avg_q': sys_queue},
    #          }
    process_queue = dict()
    # Stores CPU usage details for the processes.
    # Format: {1: {
    #              "status": "sleeping", "user_avg": 0.3, "name": "init",
    #              "pid": 1, "sys_avg": 0.56,
    #              },
    #          }
    processes = dict()

    def __init__(self, sampling_freq=settings.SAMPLING_FREQ,
                 avg_interval=settings.AVG_INTERVAL, _lock=Lock()):
        """Initialise class object.

        @param sampling_freq: Time interval in seconds at which the usage
            is to be sampled. Defaults to 1 second.
        @param avg_interval: Time interval in seconds over which the average
            is to be calculated. Defaults to 60 seconds.
        @param _lock: Thread lock instance.
        """
        self.sampling_freq = sampling_freq
        self.avg_interval = avg_interval
        # Uses lock while reading and writing dictionaries.
        self.lock = _lock

    def add_processes(self,):
        """Process CPU usage details for current processes and store them.

        Gets the list of current processes, computes their details and store
        them in memory. The details include average of CPU usages over the
        required time interval.
        @return: Set of current PIDs. To cull dead processes.
        """
        curr_pids = set()
        for _process in psutil.process_iter():
            try:
                _proc = _process.\
                    as_dict(attrs=['cpu_times', 'name', 'pid', 'status'])
            except psutil.NoSuchProcess:
                continue
            pid, (user, _sys) = _proc['pid'], _proc.pop('cpu_times')
            curr_pids.add(pid)
            # Delete ZOMBIE process details.
            if _proc['status'] in [psutil.STATUS_ZOMBIE]:
                try:
                    map(lambda x: x.pop(pid),
                        [self.processes, self.process_queue])
                except KeyError:
                    pass
                continue
            # Get or create details object for the process.
            with self.lock:
                existing = self.processes.setdefault(pid, _proc)
            # PID reuse case. Emptying average count queue for the PID.
            if _proc['name'] != existing['name']:
                map(lambda x: x.pop(pid), [self.process_queue])
            # Get or create queue object for the CPU times of the process.
            avg_q = self.process_queue.setdefault(pid, dict())

            # User CPU time.
            user_avg_q = avg_q.setdefault('user_avg_q',
                                          PeekableQueue(self.avg_interval))
            user_avg_q.enqueue(user)
            user_avg = user_avg_q.get_avg()

            # System CPU time.
            sys_avg_q = avg_q.setdefault('sys_avg_q',
                                         PeekableQueue(self.avg_interval))
            sys_avg_q.enqueue(_sys)
            sys_avg = sys_avg_q.get_avg()
            # Update the details object for the process.
            with self.lock:
                existing.update(user_avg=user_avg, sys_avg=sys_avg, **_proc)
        return curr_pids

    def cull_dead_processes(self, curr_pids):
        """Cull dead processes.

        @param curr_pids: Set of current PIDs. Cull other PID process.
        """
        def cull_dead(process_details):
            """Return a new dictionary having details for the processes
            in current PID set."""
            return {pid: details
                    for pid, details in process_details.iteritems()
                    if pid in curr_pids}
        with self.lock:
            self.processes = cull_dead(self.processes)
        self.process_queue = cull_dead(self.process_queue)

    def get_curr_processes(self):
        """Return details for all current processes.
        @return: List of current processes' details.
        """
        curr = list()
        for _process in psutil.process_iter():
            try:
                _proc = _process.as_dict(attrs=['name', 'pid', 'status'])
                # Delete process details if gone ZOMBIE.
                if _proc['status'] in [psutil.STATUS_ZOMBIE]:
                    continue
                with self.lock:
                    details = self.processes[_proc['pid']]
                # PID reuse case. Emptying average count queue for the PID.
                if _proc['name'] != details['name']:
                    continue
            except (psutil.NoSuchProcess, KeyError):
                continue
            curr.append(details)
        return curr

    def record(self):
        """Function invoked to record usage at sampling frequency interval."""
        while True:
            curr_pids = self.add_processes()
            self.cull_dead_processes(curr_pids)
            time.sleep(self.sampling_freq)


if __name__ == '__main__':
    ru_obj = RecordUsage()
    ru_obj.add_processes()
