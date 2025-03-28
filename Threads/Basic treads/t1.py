import threading
import time

def calculate_square(number):
    print("Calculating square...")
    time.sleep(2)  # Simulate slow calculation
    print(f"Square: {number * number}")

def calculate_cube(number):
    print("Calculating cube...")
    time.sleep(1)  # Simulate slow calculation
    print(f"Cube: {number * number * number}")

# Create threads
t1 = threading.Thread(target=calculate_square, args=(10,))#target=calculate_square - Specifies which function the thread should runThe thread will call this function when startedWe're passing the function object itself (not calling it - no parentheses)
t2 = threading.Thread(target=calculate_cube, args=(10,))

# Start threads
t1.start()
t2.start()

# Wait for both threads to finish
t1.join()#t1.join() makes the main program wait for Thread 1 to finish
t2.join()

print("Both calculations done!")

# args=(10,) - Provides arguments to pass to the target function

# This must be a tuple (that's why we have the comma after 10)

# Equivalent to calling calculate_square(10)

# If no arguments needed, you can omit this or use args=()

# The created Thread object is assigned to variable t1