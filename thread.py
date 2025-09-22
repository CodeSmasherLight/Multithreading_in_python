from threading import Thread
import time

def square():
    for n in range(5):
        n * n
        time.sleep(1) 


threads = []
thread_count = 10

# creating threads
for i in range(thread_count):
    t = Thread(target=square) 
    threads.append(t)
    
# start all threads
for t in threads:
    t.start()

# join thread, so basically we are waiting for all threads to complete
for t in threads:
    t.join()

print("All threads completed.")    

