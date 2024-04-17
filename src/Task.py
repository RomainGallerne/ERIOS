import machine
from typing import Dict
import uasyncio
from Singleton import Singleton

@Singleton
class TaskManager:
    def __init__(self):
        self.tasks : Dict[str,uasyncio.Task]  = {}

    def create_task(self, name, coroutine):
        if name in self.tasks:
            print("Une tâche avec ce nom existe déjà.")
            return
        task = asyncio.create_task(coroutine(), name=name)
        self.tasks[name] = task
        print("Tâche '{}' créée.".format(name))

    def start_task(self, name):
        if name in self.tasks:
            self.tasks[name].resume()
            print("Tâche '{}' démarrée.".format(name))
        else:
            print("Aucune tâche avec ce nom.")

    def suspend_task(self, name):
        if name in self.tasks:
            self.tasks[name].suspend()
            print("Tâche '{}' arrêtée.".format(name))
        else:
            print("Aucune tâche avec ce nom.")
    def get_suspend_tasks(self):
        return [name for name, task in self.tasks.items() if task.suspended()]
        

    def cancel_task(self, name):
        if name in self.tasks:
            self.tasks[name].cancel()
            del self.tasks[name]
            print("Tâche '{}' annulée.".format(name))
        else:
            print("Aucune tâche avec ce nom.")

    def cancel_all_tasks(self):
        for name, task in self.tasks.items():
            task.cancel()
            del self.tasks[name]
        print("Toutes les tâches ont été annulées.")

    def task_exists(self, name):
        return name in self.tasks

    def task_running(self, name):
        if name in self.tasks:
            return not self.tasks[name].cancelled() and not self.tasks[name].done()
        return False

    def get_task_names(self):
        return list(self.tasks.keys())