import threading, queue, time

q = queue.Queue()

def worker():
    while True:
        try:
            item = q.get(block=False)
            print(f'Working on {item}')
            print(f'Finished {item}')
            q.task_done()
        except queue.Empty:
            print("Nothing to work on!")

threading.Thread(target=worker, daemon=True).start()
for item in range(30):
    q.put(item)

q.join()
print("All work completed")