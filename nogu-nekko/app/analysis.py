from multiprocessing import Pool, Queue

pool = Pool(4)
queue: Queue[int] = Queue()


def analyze_task(analysis_requests: Queue[int]):
    while True:
        stage_id = analysis_requests.get()
        # TODO...


def begin_analyze():
    for i in range(5):
        pool.apply_async(analyze_task, args=(queue, ))
    pool.close()
    pool.join()
