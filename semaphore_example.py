from threading import Thread, Semaphore, Lock
import time

# simulate a connection pool with limited connections
MAX_CONNECTIONS = 3
semaphore = Semaphore(MAX_CONNECTIONS)
print_lock = Lock()

def safe_print(message):
    """Thread-safe printing"""
    with print_lock:
        print(message)

def access_database(user_id):
    """Simulates accessing a database with limited connections"""
    safe_print(f"User {user_id} is waiting for a database connection...")
    
    # acquire a connection from the pool
    with semaphore:
        safe_print(f"User {user_id} acquired connection! Processing...")
        safe_print(f"  -> Active connections: {MAX_CONNECTIONS - semaphore._value}")
        
        # simulate database operation
        time.sleep(2)
        
        safe_print(f"User {user_id} finished and released connection.")

def example_connection_pool():
    """Example: Limiting concurrent database connections"""
    print("\n=== Connection Pool Example ===")
    print(f"Maximum allowed connections: {MAX_CONNECTIONS}\n")
    
    threads = []
    user_count = 10
    
    # create threads for 10 users trying to access database
    for user_id in range(1, user_count + 1):
        thread = Thread(target=access_database, args=(user_id,))
        threads.append(thread)
        thread.start()
    
    # wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print("\nAll users processed!")

def download_file(file_id, semaphore, print_lock):
    """Simulates downloading a file with rate limiting"""
    with print_lock:
        print(f"File {file_id} waiting to download...")
    
    # only allow limited concurrent downloads
    with semaphore:
        with print_lock:
            print(f"File {file_id} downloading... (Active: {3 - semaphore._value})")
        
        time.sleep(1.5) # this would be the download time
        
        with print_lock:
            print(f"File {file_id} download complete!")

def example_rate_limiting():
    """Example: Rate limiting downloads"""
    print("\n\n=== Rate Limiting Example ===")
    print("Maximum concurrent downloads: 3\n")
    
    download_semaphore = Semaphore(3)
    threads = []
    
    # try to download 8 files
    for file_id in range(1, 9):
        thread = Thread(target=download_file, args=(file_id, download_semaphore, print_lock))
        threads.append(thread)
        thread.start()
        time.sleep(0.2)  # this would be the request interval
    
    for thread in threads:
        thread.join()
    
    print("\nAll downloads complete!")

if __name__ == "__main__":
    
    print("="*50)
    print("SEMAPHORE DEMONSTRATION")
    print("="*50)
    print("\nSemaphore allows N threads to access a resource")
    print("Lock allows only 1 thread to access a resource")
    print("="*50)
    
    # run examples
    example_connection_pool()
    example_rate_limiting()
    
    print("\n" + "="*50)
    print("Finished all examples.")