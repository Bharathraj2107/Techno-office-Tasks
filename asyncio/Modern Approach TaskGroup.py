import asyncio

def callback(task_name):
    print(f"{task_name} completed!")

async def task(task_name, delay):
    print(f"{task_name} running...")
    await asyncio.sleep(delay)
    return task_name

async def main():
    async with asyncio.TaskGroup() as tg:  # Creates a task group context 
        # Create and add tasks to the group
        task1 = tg.create_task(task("Task A", 2))
        task2 = tg.create_task(task("Task B", 1))
        
        # Attach callbacks (same as before)
        task1.add_done_callback(lambda t: callback(t.result()))
        task2.add_done_callback(lambda t: callback(t.result()))

    # The 'async with' block waits for all tasks to complete automatically
    print("All tasks completed!")

asyncio.run(main())