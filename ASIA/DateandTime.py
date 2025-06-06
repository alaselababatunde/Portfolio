from datetime import datetime
import time

# Get the current date and time
now = datetime.now()

# Format the date and time as a string
current_time = now.strftime("%H:%M %p")
current_date = now.strftime("%Y-%m-%d")

# Print the current date and time
print("Current Date:", current_date)
print("Current Time:", current_time)

time.sleep(3)
