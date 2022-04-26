import asyncio
import time

from typing import Callable

from threading import Thread
from queue import Queue

from tasks import task_1, task_2, task_3, task_4

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
            task_runner(task)
            work_queue.task_done()
        print('----------------------')
        work_queue.join()
        print('Tasks done!')


def blocker_task_controller(func: Callable[..., None], work_queue: Queue, func_type: str, *args):
    global blocking
    task = {'func': func, 'args': args, 'func_type': func_type} 
    if blocking:
        work_queue.put(task)
        print('task added to queue')
    else:
        task_runner(task)


def task_runner(task: dict):
    if task['func_type'] == 'async':
        task_thread = Thread(target=asyncio.run, args=(task['func'](*task['args']),), daemon=True)
    else:
        task_thread = Thread(target=task['func'], args=(*task['args'],), daemon=True)
    task_thread.start()
    task_thread.join()


def blocker_task(queue: Queue):
    global blocking

    print('Blocking')
    blocking = True
    time.sleep(2)
    blocking = False
    print('Blocking done!')
    if not queue.empty():
        Thread(target=queue_controller, args=(queue,)).start()


def main():
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    worker_queue = Queue()
    blocker_task_controller(task_1, worker_queue, 'async', 23)
    blocker_task_controller(task_4, worker_queue, 'sync')

    Thread(target=blocker_task, args=(worker_queue,)).start()
    time.sleep(0.3)
    
    # Put some work in the queue
    blocker_task_controller(task_2, worker_queue, 'async', 12, 21)
    blocker_task_controller(task_3, worker_queue, 'sync')


if __name__ == "__main__":
    main()
