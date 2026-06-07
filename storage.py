import json 
from task import Task
import csv

def save_tasks(tasks, filepath="tasks.json"):
    # Convert list of Task objects to list of dicts
    # Save to JSON
    data = [{"id":t.id, "title":t.title, "done":t.done} for t in tasks]
    with open(filepath , "w+") as f:
        json.dump(data, f, indent=2)
    
def load_tasks(filepath="tasks.json"):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        tasks = []
        for d in data:
            t = Task(d["id"], d["title"])
            t.done = d["done"]          # Restore done state
            tasks.append(t)
        return tasks
    except FileNotFoundError:
        return []
    

def export_csv(tasks, filepath="tasks.csv"):
    data = [{"id": t.id, "title": t.title, "done": t.done} for t in tasks]
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "title", "done"])
        writer.writeheader()
        writer.writerows(data)