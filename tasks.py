import asyncio
import time


async def task_1(num_1):
    print('Task 1 running')
    print(f'Number is {num_1}')
    await asyncio.sleep(3)
    print('Task 1 accomplished!')


async def task_2(num_1, num_2):
    print('Task 2 running')
    print(f'Sum: {num_1+num_2}')
    await asyncio.sleep(2)
    print('Task 2 accomplished!')


def task_3():
    print('Task 3 running')
    time.sleep(1)
    print('Task 3 accomplished!')


def task_4():
    print('Task 4 running')
    time.sleep(1)
    print('Task 4 accomplished!')
