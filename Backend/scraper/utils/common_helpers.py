import time
def get_end_time(start):
    end = time.time()
    elapsed_time = end - start
    minutes, seconds = divmod(elapsed_time, 60)
    return f"{int(minutes)}m {int(seconds)}s"