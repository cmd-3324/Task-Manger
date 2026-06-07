
import sys
import os
import platform
from abc import ABC, abstractmethod
from typing import Callable
from dataclasses import dataclass, field
from storage import load_tasks, save_tasks, export_csv
from task import Task
# Create, toggle, save

# Load back
loaded = load_tasks()
print(loaded[0].done)
tasks = load_tasks()
@dataclass
class MenuItem:
    key : int 
    label : str   
    action : Callable
    args : tuple = ()
    kwargs : dict = field(default_factory=dict)
    
class Menu(ABC):
    def __init__(self, title):
        self.title = title
        self.items = []
        self.is_running = True
    def add_item(self, key, label, action, *args, **kwargs):
        self.items.append(MenuItem(key, label, action , *args, **kwargs))
        
    @staticmethod
    def clean_screen():
        os.system("cls" if platform.system() == "Windows" else "clear")
    @abstractmethod
    def render_menu(self):
        pass
    
    def handle_choice(self, choice):
        for item in self.items:
            if choice.lower() == item.key.lower():
                item.action(*item.args, **item.kwargs)
                return True   
        return False   
    def run2(self):
        while self.is_running:
            self.clean_screen()
            self.render_menu()
            choice = input("Enter your choice : ").strip()
            if not self.handle_choice(choice):
                print("Invalide")
class BoxMenu(Menu):
    WIDTH = 44
    def _line(self, char="═", corners=("╔","╗","╝","╚")):
            return f"{corners[0]}{char * self.WIDTH}{corners[1]}"
    
    def render_menu(self):
        print(self._line())
        print(f"║{self.title.center(self.WIDTH)}║")
        print(self._line("═", ("╠","╣","╝","╚")))
        for item in self.items:
            print(f"║  {item.key}. {item.label:<{self.WIDTH-5}}║")
        print(self._line("═", ("╚","╝","╝","╚")))
class App: 
    def __init__(self):
        self.menu = None 
    def registering_menu(self , menu):
        self.menu = menu

    def start(self):
        if not self.menu:
            raise RuntimeError("There is no menu")
        self.menu.run2()
def show_tasks():
    if not tasks:
        print("  No tasks.")
    else:
        sorted_tasks = sorted(tasks, key=lambda t: t.title.lower())
        for i, task in enumerate(sorted_tasks, start=1):
            print(f"  {i}. {task}")
def require_tasks(func):
    def wrapper(*args, **kwargs):
        if not tasks:
            print("  No tasks found.")
            input("\n  ...Press Enter...")
            return
        return func(*args, **kwargs)
    return wrapper
def load_from_f():
    global tasks 
    tasks = load_tasks()
    print(f"  Loaded {len(tasks)} tasks.")
    input("...Press Enter...")
def unqite_title(func):
    def wrapper(*args, **kwargs):
        title = input("Enter Task Title:").strip() 
        if any(t.title.lower() == title for t in tasks):
            print(f"  Task '{title}' already exists.")
            input("  ...Press Enter...")
            return
        return func(*args, **kwargs) 
    return wrapper
#@unqite_title
def action_addTaks():
    title = input("  Task title: ").strip()
    if not title:
        print("  Title cannot be empty.")
        input("  ...Press Enter...")
        return
    if any(t.title.lower() == title for t in tasks):
        print(f"  Task '{title}' already exists.")
        input("  ...Press Enter...")
        return
    else:
        task_id = len(tasks) + 1
        tasks.append(Task(task_id, title))
        save_tasks(tasks)
        print(f"  Added: {title}")
    input("...Press Enter...")
@require_tasks
def action_listTaks():
    show_tasks()     
    input("\n  ...Press Enter...") 
@require_tasks
def delele_task(): 
    
    show_tasks()                    # No pause here
    try:
        idx = int(input("  Task number to delete: ")) - 1
        removed = tasks.pop(idx)
        save_tasks(tasks)
        print(f"  Deleted: {removed.title}")
    except (ValueError, IndexError):
        print("  Invalid number.")
    input("\n  ...Press Enter...") 
        
@require_tasks        
def save_to_file():
    save_tasks(tasks)
    print(f"  Saved {len(tasks)} tasks.")
    input("...Press Enter...")
@require_tasks
def action_toggle():
   
    show_tasks()
    try:
        idx = int(input("  Task number to toggle: ")) - 1
        tasks[idx].toggle()
        save_tasks(tasks)
        print(f"  Toggled: {tasks[idx].title}")
    except (ValueError, IndexError):
        print("  Invalid number.")
    input("\n  ...Press Enter...")
@require_tasks
def delete_all():
    show_tasks()
    ver = input("Are you sure to delete All Tasks(Y/N) ?").strip()
    if ver.lower() == "y":
        tasks.clear()
        save_tasks(tasks)
        print("Deleted All")
@require_tasks
def search_task():
    keyword = input("Searhc By title: ").strip()
    matches = [(i, task) for i, task in enumerate(tasks, start=1) 
               if keyword in task.title.lower()]
    if not matches:
        print(f"  No tasks match '{keyword}'.")
    else:
        print(f"\n  Found {len(matches)} match(es):")
        for i , k in matches:
            print(f"{i} : {k}")
        input("...Press Enter ..")

def action_export_csv():
    export_csv(tasks)           
    print("  Exported to CSV.")
    input("  ...Press Enter...")
def main_33():
    my_menu = BoxMenu("TaskManager")
    my_menu.add_item("1","Add Task", action_addTaks)
    my_menu.add_item("2","List Tasks", action_listTaks)
    my_menu.add_item("3", "Toggle Task (done/undone)", action_toggle)  
    my_menu.add_item("4", "Delete Tasks", delele_task)
    my_menu.add_item("5", "Delete All ", delete_all)
    my_menu.add_item("6", "Search Task", search_task)
    my_menu.add_item("7", "Export Csv", action_export_csv)
    my_menu.add_item("8", "Save To FIle", save_to_file)
    my_menu.add_item("9","Load From File", action = load_from_f)
    app = App()
    app.registering_menu(my_menu)
    app.start()
if __name__ == "__main__":
  main_33()    
        
        