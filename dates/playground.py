from datetime import datetime
from dateutil.relativedelta import relativedelta

import pytz

created_dt = '2024-01-20T22:12:55Z'

utc_time = datetime.strptime(created_dt, '%Y-%m-%dT%H:%M:%SZ')

utc_time = utc_time.replace(tzinfo=pytz.UTC)

target_tz = pytz.timezone('Australia/Sydney')
target_time = utc_time.astimezone(target_tz)

formatted_time = datetime.strftime(target_time, '%Y-%m-%d %H:%M:%S')
print(f"formatted time: {formatted_time}")


date1 = datetime(2025, 8, 23)
date2 = datetime (1978, 8, 23)

# subtracting the dates:
diff = date1 - date2
relative_diff = relativedelta(date1, date2)

diff_in_days = diff.days
diff_in_months = relative_diff.years * 12 + relative_diff.months
diff_in_years = relative_diff.years

print(f"difference in days = {diff_in_days}"
      f", difference in months = {diff_in_months}"
      f", difference in years = {diff_in_years}")