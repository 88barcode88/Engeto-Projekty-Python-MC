import json
from datetime import datetime

class Task:
    def __init__(self, text, priority, category, due_date=None, date_added=None):
        self.text = text
        self.priority = priority
        self.category = category
        self.due_date = due_date
        self.date_added = date_added or datetime.now().isoformat()

    def to_dict(self):
        return {
        'text': self.text,
        'priority': self.priority,
        'category': self.category,
        'due_date': self.due_date,
        'date_added': self.date_added
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class TaskModel:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def edit_task(self, index, new_task):
        if 0 <= index < len(self.tasks):
            self.tasks[index] = new_task
            self.save_tasks()

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def get_tasks(self):
        return self.tasks

    def save_tasks(self):
        tasks_data = [task.to_dict() for task in self.tasks]
        with open('tasks.json', 'w') as f:
            json.dump(tasks_data, f)

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as f:
                tasks_data = json.load(f)
            self.tasks = [Task.from_dict(task_data) for task_data in tasks_data]
        except FileNotFoundError:
            print("Soubor s úkoly nebyl nalezen. Začínáme s prázdným seznamem.")
        except json.JSONDecodeError:
            print("Chyba při načítání úkolů. Soubor může být poškozen.")
        except Exception as e:
            print(f"Nastala neočekávaná chyba při načítání úkolů: {e}")

    def sort_tasks(self, tasks, key):
        if key == 'priority':
            priority_order = {'Vysoká': 0, 'Střední': 1, 'Nízká': 2}
            return sorted(tasks, key=lambda x: priority_order[x.priority])
        elif key == 'date_added':
            return sorted(tasks, key=lambda x: x.date_added, reverse=True)
        elif key == 'due_date':
            return sorted(tasks, key=lambda x: x.due_date or datetime.max.isoformat())
        return tasks

    def filter_tasks(self, category):
        if category == 'Všechny kategorie':
            return self.tasks
        return [task for task in self.tasks if task.category == category]

    def sort_tasks(self, tasks, key):
        if key == 'priority':
            priority_order = {'Vysoká': 0, 'Střední': 1, 'Nízká': 2}
            return sorted(tasks, key=lambda x: priority_order[x.priority])
        elif key == 'date_added':
            return sorted(tasks, key=lambda x: x.date_added, reverse=True)
        elif key == 'due_date':
            return sorted(tasks, key=lambda x: x.due_date or datetime.max.isoformat())
        return tasks
