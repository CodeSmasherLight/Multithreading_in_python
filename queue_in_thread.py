from threading import Thread, current_thread, Lock
from queue import Queue

def worker(q, lock):
    while True:
        item = q.get()
        # processing
        with lock:
            print(f'in {current_thread().name} got {item}\n')
        q.task_done()

if __name__ == "__main__":

    q = Queue()
    lock = Lock()
    thread_count = 10

    for i in range(thread_count):
        thread = Thread(target=worker, args=(q, lock))
        thread.daemon = True
        thread.start()

    for i in range(1, 21):
        q.put(i)

    q.join()    

    print("main end")    

