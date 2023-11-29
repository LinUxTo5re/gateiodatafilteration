import sched
import time
import requests
import pytz
from main import run_my_code
from datetime import datetime, timedelta

s = sched.scheduler(time.time, time.sleep)
IST = pytz.timezone('Asia/Kolkata')
next_scheduled_time = ""


def check_connectivity():
    try:
        requests.get('http://www.google.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False


def schedule_tasks():
    global next_scheduled_time
    ist_now = datetime.now(IST)
    current_time = ist_now.strftime("%H:%M:%S")

    if check_connectivity():
        if "08:30:00" < current_time < "08:45:00":  # morning 8
            scheduled_time = "08:50:00"
            next_scheduled_time = (datetime.strptime("11:30:00", "%H:%M:%S") - datetime.strptime("08:30:00", "%H:%M:%S")).total_seconds() / 60
        elif "11:30:00" < current_time < "11:45:00":  # morning 11
            scheduled_time = "15:50:00"
            next_scheduled_time = (datetime.strptime("15:30:00", "%H:%M:%S") - datetime.strptime("11:30:00", "%H:%M:%S")).total_seconds() / 60
        elif "15:30:00" < current_time < "15:45:00":  # afternoon 3
            scheduled_time = "15:50:00"
            next_scheduled_time = (datetime.strptime("20:30:00", "%H:%M:%S") - datetime.strptime("15:30:00", "%H:%M:%S")).total_seconds() / 60
        elif "20:30:00" < current_time < "20:45:00":  # night 8
            scheduled_time = "20:50:00"
            next_scheduled_time = 30
        else:
            scheduled_time = "08:50:00"
            scheduled_date_time = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d') + f" {scheduled_time}"
            next_scheduled_time = 690
            is_next_day = True

        if not is_next_day:
            scheduled_date_time = f"{ist_now.strftime('%Y-%m-%d')} {scheduled_time}"
        s.enterabs(time.mktime(time.strptime(scheduled_date_time, "%Y-%m-%d %H:%M:%S")), 1, run_my_code, ())
        return True
    else:
        print("No network connectivity. Task not scheduled.")
        return False


while True:
    if schedule_tasks():
        s.run()
        print("Scheduled task executed.")
    else:
        time.sleep(300)  # 300 seconds = 5 minutes
        continue

    now = datetime.now(IST)
    next_minute = now.replace(second=0, microsecond=0) + timedelta(minutes=next_scheduled_time + 5)
    time_remaining = (next_minute - now).total_seconds()
    time.sleep(time_remaining)

