from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def process_task(task_id):
    """Simulates a task that takes some time to complete"""
    print(f"Task {task_id} starting...")
    time.sleep(2)  # simulate work
    result = task_id * task_id
    print(f"Task {task_id} completed with result: {result}")
    return result

def example_1_basic_map():
    """Example 1: Using map() for simple parallel execution"""
    print("\n=== Example 1: Basic ThreadPoolExecutor with map() ===")
    
    tasks = [1, 2, 3, 4, 5]
    
    # create a thread pool with 3 workers
    with ThreadPoolExecutor(max_workers=3) as executor:
        # map() returns results in the same order as input
        results = executor.map(process_task, tasks)
        
        print("\nAll results:", list(results))

def example_2_submit():
    """Example 2: Using submit() for more control over individual tasks"""
    print("\n=== Example 2: Using submit() for individual task control ===")
    
    tasks = [1, 2, 3, 4, 5]
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        # submit tasks and get Future objects
        futures = [executor.submit(process_task, task) for task in tasks]
        
        # get results as they complete (not in order)
        for future in as_completed(futures):
            result = future.result()
            print(f"Got result from future: {result}")

def example_3_with_different_args():
    """Example 3: Processing tasks with different arguments"""
    print("\n=== Example 3: Tasks with different arguments ===")
    
    def complex_task(name, value, multiplier):
        print(f"Processing {name}...")
        time.sleep(1)
        return f"{name}: {value * multiplier}"
    
    tasks = [
        ("Task-A", 10, 2),
        ("Task-B", 20, 3),
        ("Task-C", 30, 4),
        ("Task-D", 40, 5),
    ]
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        # use submit with unpacked arguments
        futures = [executor.submit(complex_task, *task) for task in tasks]
        
        for future in as_completed(futures):
            print(f"Result: {future.result()}")

if __name__ == "__main__":
    
    start_time = time.time()
    
    # run all examples
    example_1_basic_map()
    example_2_submit()
    example_3_with_different_args()
    
    end_time = time.time()
    
    print(f"\n{'='*50}")
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
    print("Finished all examples.")