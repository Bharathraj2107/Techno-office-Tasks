import threading
import time

# Function to simulate a time-consuming task
def task(name, duration):
    print(f"Task {name} started")
    time.sleep(duration)  # Simulating work being done
    print(f"Task {name} completed after {duration} seconds")

# Create and start multiple threads
thread1 = threading.Thread(target=task, args=("A", 2))
thread2 = threading.Thread(target=task, args=("B", 1))
thread3 = threading.Thread(target=task, args=("C", 3))

print("Main program started")

thread1.start()  # Start thread 1 (Task A)
thread2.start()  # Start thread 2 (Task B)
thread3.start()  # Start thread 3 (Task C)

print("All threads started")

# Wait for all threads to complete
thread1.join()
thread2.join()
thread3.join()

print("Main program ended")
# Asynchronous Execution:

# Tasks run independently without waiting for others to finish

# Notice how all tasks "start" before any "complete"

# Non-Blocking:

# The main program continues while threads run in background

# "All threads started" prints immediately after starting threads

# Join Importance:

# Without join(), the program might exit before threads finish

# join() ensures we wait for all threads to complete