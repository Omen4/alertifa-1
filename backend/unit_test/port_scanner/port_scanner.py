#!/usr/bin/env python3
from asyncio import open_connection, wait_for, Queue, Task, create_task, gather, run
from asyncio.exceptions import TimeoutError
import traceback
import subprocess
import logging



LOG_FILENAME = '/logs/port_scanner.log'
LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format=LOG_FORMAT)


async def worker(ip_address: str, queue: Queue):
    while True:
        port = await queue.get()
        try:
            conn = open_connection(ip_address, port)
            await wait_for(conn, timeout=0.5)
            logging.info(f"OPEN: {port}")
            # print(f"OPEN: {port}")
        except (ConnectionRefusedError) as err:
            logging.info(f"REFUSED: {port}")
            # print(f"REFUSED: {port}")
        except TimeoutError as err:
            pass
            # logging.info(f"TIMEOUT: {port}")
            # print(f"TIMEOUT: {port}")
        except Exception as e:
            traceback.print_exc()
        queue.task_done()
        print(f"{queue.qsize()}/{0xffff}")

async def main():
    MAX_WORKERS = 10
    queue: Queue = Queue()
    TARGET_IP = '127.0.0.1'
    # TARGET_IP = '51.77.210.177'
    LOWER_RANGE = 0
    UPPER_RANGE = 0xffff

    try:
        iterable: list[int] = [ i for i in range(LOWER_RANGE, UPPER_RANGE)]
        for i in iterable:
            queue.put_nowait(i)

        tasks: list[Task] = []
        for _ in range(MAX_WORKERS):
            task: Task = create_task(worker(TARGET_IP, queue) )
            tasks.append(task)

        await queue.join()
        for task in tasks:
            task.cancel()
        await gather(*tasks, return_exceptions=True)

    except Exception as err:
        traceback.print_exc()
        print(err)

run(main(), debug=True)