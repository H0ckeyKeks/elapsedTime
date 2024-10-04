import time
from datetime import datetime, timedelta
from rich.console import Console
from rich.live import Live
from rich.table import Table
import os

# Create a console object for rich input
console = Console()

# Create a progress bar
def progress_bar(progress, total, bar_length=20):
    fraction = progress / total
    arrow = '=' * int(fraction * bar_length)
    padding = ' ' * (bar_length - len(arrow))
    return f'[{arrow}{padding}] {fraction * 100:.2f}%'

# Format timedelta into HH:MM:SS
def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    if total_seconds < 0:
        return "00:00:00"
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


# Get current date
today_date = datetime.now().strftime('%Y-%m-%d')

# Get user input
start = input("Start (HH:MM:SS): ")
end = input("End (HH:MM:SS): ")

# Convert input into datetime format
start_format = '%H:%M:%S'
end_format = '%H:%M:%S'

# Combine today's date with the input time
full_start_time = today_date + ' ' + start
full_end_time = today_date + ' ' + end

# Definition of combined format for both date and time
full_start_format = '%Y-%m-%d %H:%M:%S'
full_end_format = '%Y-%m-%d %H:%M:%S'

# Turn start into the datetime format
start_object = datetime.strptime(full_start_time, full_start_format)
end_object = datetime.strptime(full_end_time, full_end_format)

# Get total time
total_time = end_object - start_object

# Convert total_time into seconds for calculation (necessary!)
total_seconds = total_time.total_seconds()

# Dynamic loop to update progress
# Refresh 4 times per second
while True:
    # Get current time
    current_object = datetime.now()

    # Get elapsed time
    elapsed_time = current_object - start_object
    remaining_time = end_object - current_object

    elapsed_seconds = elapsed_time.total_seconds()

    # Prevent division by 0 error
    if total_seconds > 0:
        # Get duration
        duration = (elapsed_seconds / total_seconds) * 100
    else:
        duration = 0

    # Prevent negative times
    if current_object < start_object:
        elapsed_seconds = 0
        remaining_time = total_time
    elif current_object > end_object:
        elapsed_seconds = total_seconds
        remaining_time = timedelta(seconds=0)

    # Clear console
    os.system('cls')

    # Create a rich table dynamically
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Start", justify="center")
    table.add_column("End", justify="center")
    table.add_column("Elapsed", justify="center")
    table.add_column("Remaining", justify="center")

    # Add rows to the table
    table.add_row(
        start_object.strftime('%H:%M:%S'),
        end_object.strftime('%H:%M:%S'),
        format_timedelta(elapsed_time),
        format_timedelta(remaining_time)
    )

    # Create the progress bar string
    progress_str = progress_bar(elapsed_seconds, total_seconds)

    # Update live display of the table
    console.print(table)

    # Update live display of the progress bar
    console.print(progress_str)

    # Break the loop once task is completed
    if elapsed_seconds >= total_seconds:
        break

    # Sleep for 1 second to simulate real-time updates
    time.sleep(3)
