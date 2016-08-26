from __future__ import division

import multiprocessing as mp

_tasks, _results = mp.JoinableQueue(), mp.Queue()


class Worker(mp.Process):
    def __init__(self, task_queue, result_queue):
        mp.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                print '%s: Exiting' % proc_name
                self.task_queue.task_done()
                break
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return


class Task(object):
    def __init__(self, call_back, args):
        self.call_back, self.args = call_back, args

    def __call__(self):
        return self.call_back(*self.args)


def init_multiprocessor(num_workers):
    # Init multiple process
    global _tasks, _results
    workers = [Worker(_tasks, _results) for _ in xrange(num_workers)]
    for w in workers:
        w.start()


def put_task(f, args):
    _tasks.put(Task(f, args))


def end_multiprocessor(num_tasks):
    global _tasks
    # end procedure for multi processor
    for _ in xrange(num_tasks):
        _tasks.put(None)
    # Wait for all of the tasks to finish
    _tasks.join()