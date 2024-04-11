import os
import json
import time
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_calls, period, log_file):
        self.max_calls = max_calls
        self.period = period  # period in seconds, which can still be used to calculate the expiry time
        self.log_file = log_file

        # If log_file exists, load the count and date, otherwise, initialize
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {"Date": "", "Count": 0}
        
        # Ensure that the count is an integer
        self.data["Count"] = int(self.data["Count"])

    def __call__(self):
        current_date_str = datetime.now().strftime("%d/%m/%Y")

        # Check if the stored date is not today or is empty, and reset count if so
        if self.data["Date"] != current_date_str:
            self.data = {"Date": current_date_str, "Count": 0}

        # Check if making a call will exceed the rate limit
        if self.data["Count"] < self.max_calls:
            self.data["Count"] += 1
            self._persist()
            return True
        else:
            # Sleep if rate limit would be exceeded
            expiry_time = datetime.strptime(self.data["Date"], "%d/%m/%Y") + timedelta(seconds=self.period)
            sleep_time = (expiry_time - datetime.now()).total_seconds()
            print(f"Rate limit exceeded. Sleeping for {sleep_time:.2f} seconds.")
            time.sleep(sleep_time)
            # Reset the count and allow the call
            self.data["Count"] = 1
            self.data["Date"] = (expiry_time + timedelta(seconds=1)).strftime("%d/%m/%Y")
            self._persist()
            return True

    def _persist(self):
        # Persist the date and count to log_file
        with open(self.log_file, 'w') as f:
            json.dump(self.data, f)

# Configure rate limiters
rate_limiter_per_day = RateLimiter(max_calls=50000, period=86400, log_file='rate_limit_per_day.json')
