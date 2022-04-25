import time
from typing import Callable

from threading import Thread
from queue import Queue

from tasks import task_1, task_2, task_3

blocking = False

def queue_controller(work_queue: Queue):
    if work_queue.empty():
        print("Queue nothing to do")
    else:
        print("Queue running")
        print('----------------------')
        while not work_queue.empty():
            print(f'Queue size: {work_queue.qsize()}')
            task = work_queue.get()

            task_thread = Thread(target=task['func'], args=(*task['args'],), daemon=True)
            task_thread.start()
            task_thread.join()
            work_queue.task_done()
        print('----------------------')


def blocker_task_controller(func: Callable[..., None], work_queue: Queue, *args):
    global blocking
    task = {'func': func, 'args': args}
    if blocking:
        work_queue.put(task)
        print('task added to queue')
    else:
        work_thread = Thread(target=func, args=(*args,), daemon=True)
        work_thread.start()
        work_thread.join()


def blocker_task(queue: Queue):
    global blocking

    print('Blocking')
    blocking = True
    time.sleep(2)
    blocking = False
    print('Blocking done!')
    if not queue.empty():
        Thread(target=queue_controller, args=(queue,)).start()
        queue.join()
        print('Tasks done!')


def main():
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    worker_queue = Queue()

    blocker_task_controller(task_1, worker_queue, 23)

    Thread(target=blocker_task, args=(worker_queue,)).start()
    time.sleep(0.3)
    
    # Put some work in the queue
    blocker_task_controller(task_2, worker_queue, 12, 21)
    blocker_task_controller(task_3, worker_queue)


if __name__ == "__main__":
    main()
