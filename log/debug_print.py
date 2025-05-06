import time


def dprint(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time() + 9*3600))
    print(f"********* DEBUGGING [{timestamp}]: {msg}")