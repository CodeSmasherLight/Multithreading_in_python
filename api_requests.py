from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import time
import random

# simulate API responses (in real code, use requests or httpx)
def mock_api_call(url, delay=None):
    """Simulates an API call with random delay"""
    if delay is None:
        delay = random.uniform(0.5, 2.0)
    time.sleep(delay)
    return {
        "url": url,
        "status": 200,
        "data": f"Data from {url}",
        "response_time": delay
    }

class APIClient:
    """Thread-safe API client with statistics tracking"""
    
    def __init__(self):
        self.lock = Lock()
        self.success_count = 0
        self.fail_count = 0
        self.total_response_time = 0.0
    
    def fetch_data(self, url):
        """Fetch data from a URL"""
        try:
            print(f"Fetching: {url}")
            response = mock_api_call(url)
            
            # update statistics (thread-safe)
            with self.lock:
                self.success_count += 1
                self.total_response_time += response["response_time"]
            
            print(f"✓ Success: {url} (took {response['response_time']:.2f}s)")
            return response
        
        except Exception as e:
            with self.lock:
                self.fail_count += 1
            print(f"✗ Failed: {url} - Error: {e}")
            return None
    
    def get_statistics(self):
        """Get request statistics"""
        with self.lock:
            total = self.success_count + self.fail_count
            avg_time = self.total_response_time / self.success_count if self.success_count > 0 else 0
            return {
                "total_requests": total,
                "successful": self.success_count,
                "failed": self.fail_count,
                "avg_response_time": avg_time
            }

def example_sequential():
    """Example 1: Sequential API calls (slow)"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Sequential API Calls (No Threading)")
    print("="*60 + "\n")
    
    urls = [
        "https://api.example.com/users/1",
        "https://api.example.com/users/2",
        "https://api.example.com/users/3",
        "https://api.example.com/users/4",
        "https://api.example.com/users/5",
    ]
    
    client = APIClient()
    start_time = time.time()
    
    # sequential calls
    for url in urls:
        client.fetch_data(url)
    
    elapsed = time.time() - start_time
    stats = client.get_statistics()
    
    print(f"\n--- Statistics ---")
    print(f"Total wall-clock time: {elapsed:.2f}s")
    print(f"Requests: {stats['total_requests']}")
    print(f"Successful: {stats['successful']}")
    print(f"Average response time per request: {stats['avg_response_time']:.2f}s")
    print(f"Speedup: Threading doesn't change individual response times!")

def example_threaded():
    """Example 2: Concurrent API calls with ThreadPoolExecutor"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Concurrent API Calls (With Threading)")
    print("="*60 + "\n")
    
    urls = [
        "https://api.example.com/users/1",
        "https://api.example.com/users/2",
        "https://api.example.com/users/3",
        "https://api.example.com/users/4",
        "https://api.example.com/users/5",
    ]
    
    client = APIClient()
    start_time = time.time()
    
    # concurrent calls using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=3) as executor:
        # submit all tasks
        futures = [executor.submit(client.fetch_data, url) for url in urls]
        
        # wait for all to complete
        for future in as_completed(futures):
            future.result()  # this will raise any exceptions that occurred
    
    elapsed = time.time() - start_time
    stats = client.get_statistics()
    
    print(f"\n--- Statistics ---")
    print(f"Total wall-clock time: {elapsed:.2f}s")
    print(f"Requests: {stats['total_requests']}")
    print(f"Successful: {stats['successful']}")
    print(f"Average response time per request: {stats['avg_response_time']:.2f}s")

def example_batch_processing():
    """Example 3: Processing large batches of URLs"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Batch Processing (20 URLs)")
    print("="*60 + "\n")
    
    # this will generate 20 URLs
    urls = [f"https://api.example.com/data/{i}" for i in range(1, 21)]
    
    client = APIClient()
    start_time = time.time()
    
    # process with 5 concurrent workers
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(client.fetch_data, url) for url in urls]
        
        # wait for all to complete
        for future in as_completed(futures):
            future.result()  # ensures exceptions are raised if any occurred
    
    elapsed = time.time() - start_time
    stats = client.get_statistics()
    
    print(f"\n--- Statistics ---")
    print(f"Total wall-clock time: {elapsed:.2f}s")
    print(f"Total requests: {stats['total_requests']}")
    print(f"Successful: {stats['successful']}")
    print(f"Failed: {stats['failed']}")
    print(f"Average response time per request: {stats['avg_response_time']:.2f}s")
    print(f"Throughput: {stats['total_requests']/elapsed:.2f} requests/second")

if __name__ == "__main__":
    
    print("\n" + "="*60)
    print("REAL-WORLD EXAMPLE: API Request Processing")
    print("="*60)
    print("\nThis demonstrates the performance benefit of multithreading")
    print("for I/O-bound operations like API calls.\n")
    
    # run all examples
    example_sequential()
    example_threaded()
    example_batch_processing()
    
    print("\n" + "="*60)
    print("Key Takeaway: Threading dramatically reduces wait time for I/O!")
    print("="*60)
    print("\nFinished all examples.")