import time
import os
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def _add_result_to_queue(future, queue):
    aux = future.result()
    if not aux is None:
        queue.put(aux)

def execution_in_parallel(iter_process_criteria):
    start = time.time()

    myqueue = Queue()
    workers = os.cpu_count()

    with ProcessPoolExecutor(max_workers=workers) as executor:

        for process_criteria in iter_process_criteria:
            future = executor.submit(process_criteria.process)
            future.add_done_callback(lambda fut: _add_result_to_queue(fut, myqueue))
        executor.shutdown()
    #end-with

    data = []
    while not myqueue.empty():
        data.append(myqueue.get())

    end_time = time.time()  
    print("Total time: {}".format(end_time - start))
    return data