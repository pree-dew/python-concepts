def task_scheduler():
    """A simple cooperative task scheduler."""
    tasks = []
    
    def add_task(task):
        tasks.append(task)
    
    def run():
        while tasks:
            current = tasks.pop(0)
            try:
                # Resume the task
                next_time = next(current)
                # Reschedule the task with the requested delay
                tasks.append(current)
            except StopIteration:
                # Task is completed
                pass
    
    # Return functions to manage the scheduler
    return add_task, run

def countdown_task(name, count):
    """A task that counts down."""
    for i in range(count, 0, -1):
        print(f"{name}: {i}")
        # Yield control back to the scheduler
        yield
    print(f"{name}: Blast off!")

# Usage:
add_task, run = task_scheduler()
add_task(countdown_task("Timer A", 5))
add_task(countdown_task("Timer B", 3))
run()
