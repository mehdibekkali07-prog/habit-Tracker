import json
from pathlib import Path
from datetime import date
import matplotlib.pyplot as plt
from tabulate import tabulate
from datetime import date, datetime



TASKS_PATH = Path("tasks.json")
LOG_PATH = Path("log.json")


def load_json(path, default):
    if not path.exists():
        return default
    try:
        # as f is a short name ( a variable called f )
        with path.open("r", encoding = "utf-8") as f:
            data = json.load(f)
            return data
    except:
        return default 


def save_json(path, data):
    with path.open("w", encoding = "utf-8") as f:
        json.dump(data ,f, indent=4)

def ask_yes_no(prompt):
    while True:
        ans = input(f"{prompt} [y/n]: ")
        ans = ans.lower().strip()
        if ans in ["yes", "y"]:
            return True 
        elif ans in ["no", "n"]:
            return False
        else:
            print("Please type y or n.")

def record_today():
    tasks = load_json(TASKS_PATH, [])
    if not tasks:
        print("No tasks found. Please add some habits first.")
        return 
    today = date.today().isoformat()
    print(f"\n==== Habit Check for {today} ====\n")
    entries = []
    total = 0
    for task in tasks:
        name=task["name"]
        pts = task["points"]
        print(f"-{name} ({pts} points)")
        done_today = ask_yes_no("Did you do this?")
        entries.append({"name" : name, "points" : pts, "done": done_today})
        if done_today:
            total += pts
    max_points = sum(float(task["points"]) for task in tasks)
    percent = (total / max_points *100)  
    percent= round(percent, 2)
    day_record = { 
        "date": today, 
        "entries": entries,
        "total": total,
        "max_points": max_points,
        "percent": percent
    }

    log = load_json(LOG_PATH, [])
    log.append(day_record)
    save_json(LOG_PATH, log )
    print(f"Saved for {today}: {total} / {max_points} points ({percent}%).")


def show_progress():
    log = load_json(LOG_PATH, [])
    dates = []
    percents = []

    for entry in log:
        # Convert to datetime object
        d = datetime.fromisoformat(entry["date"])
        # Format to include weekday name next to date
        formatted_date = d.strftime("%Y-%m-%d (%A)")  # e.g., 2025-11-09 (Sunday)
        dates.append(formatted_date)
        percents.append(entry["percent"])

    plt.figure(figsize=(8, 5))
    plt.plot(dates, percents, marker="o", linestyle="-", color="b")
    plt.xticks(rotation=45, ha="right")
    plt.title("Habit Progress Over Time")
    plt.xlabel("Date")
    plt.ylabel("Completion (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

























