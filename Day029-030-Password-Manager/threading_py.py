import threading
import time

done = False

def worker():
    counter = 0
    while not done:
        time.sleep(1)
        counter += 1
        print(counter)

def worker_2():
    response = input("Any script in @main after t.join() will not run until you hit enter:\n")

threading.Thread(target=worker, daemon=True).start()
t = threading.Thread(target=worker_2, daemon=True)

t.start()
t.join()

response = input("Press enter again to quit :)\n")
# done = True  # Required only if the thread is not a daemon thread (daemon=False, default)
               # Meaning that it is a backend thread that should terminate whenever main terminates
