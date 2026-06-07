

class Task:
    __slots__ = ['id', 'title', 'done']
    
    def __init__(self, task_id, title):
        self.title = title
        self.id = task_id
        self.done = False    
    @property
    def status(self):
        return "✓" if self.done else "○"
    
    def toggle(self):
        self.done = not self.done
    
    def __str__(self):
        return f"[{self.status}] {self.title}"