from concurrent.futures import ThreadPoolExecutor#manage multiple threads easily

def greet(name):
    print(f"Hello, {name}!")

with ThreadPoolExecutor(max_workers=3) as executor:
    executor.submit(greet, "Alice")
    executor.submit(greet, "Bob")
    executor.submit(greet, "Charlie")

# ThreadPoolExecutor(max_workers=3) creates a pool with maximum 3 worker threads

# The with statement ensures proper cleanup when we're done

# executor is our manager that will handle the thread pool   

 
# Each submit() adds a new task to the pool:

#First argument is the function to run (greet)

#Subsequent arguments are passed to that function ("Alice", "Bob", etc.) 

#When we submit "Alice":

#One worker thread is assigned to run greet("Alice")