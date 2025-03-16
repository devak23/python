from datetime import datetime

import pytz

created_dt = '2024-01-20T22:12:55Z'

utc_time = datetime.strptime(created_dt, '%Y-%m-%dT%H:%M:%SZ')

utc_time = utc_time.replace(tzinfo=pytz.UTC)

target_tz = pytz.timezone('Australia/Sydney')
target_time = utc_time.astimezone(target_tz)

formatted_time = datetime.strftime(target_time, '%Y-%m-%d %H:%M:%S')
print(f"formatted time: {formatted_time}")

