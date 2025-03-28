import asyncio

def callback(task_name):
    print(f"{task_name} completed!")

async def task(task_name, delay):
    print(f"{task_name} running...")
    await asyncio.sleep(delay)
    return task_name

async def main():
    # Schedule tasks and attach callbacks
    task1 = asyncio.create_task(task("Task A", 2))
    task2 = asyncio.create_task(task("Task B", 1))
    
    task1.add_done_callback(lambda t: callback(t.result()))# registers a function to call when the task completes.
    task2.add_done_callback(lambda t: callback(t.result()))#here we are passing the object Task A as parameter to the lambda function and .result gives the completed 
    
    await asyncio.gather(task1, task2)

asyncio.run(main())