# write a retry function that executes another function a specified number of times
# signature: retry(func, max_tries=3)
# sample api invocation function to test:
import random
import time


def invoke_api():
    """Assume that this invokes an API somewhere that fails 50% of the time."""
    if random.randint(0, 1) == 0:
        print("Invocation failed!")
        raise ValueError("Transient error!")
    else:
        print("API invoked successfully")
        return 42


def delayed_retry(func, max_retries=3):
    for i in range(max_retries):
        try:
            return func()
        except ValueError as e:
            seconds_to_sleep = i * 2
            print(f"Error encountered: {e}. Sleeping for {seconds_to_sleep} seconds.")
            time.sleep(seconds_to_sleep)
            print(f"Retrying again...")

    raise ValueError(f"Tried invocation for {max_retries} times and did not succeed. Failing permanently.")

result = delayed_retry(invoke_api, max_retries=5)