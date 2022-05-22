import todoist
from datetime import datetime, date, timedelta
from JJ_Print.JJ_Todoist_Config import JJ_Todoist_Config
from PIL import Image
from pytz import timezone

class JJ_Todo_Data:
    def __init__(self, projects, completed_yesterday):
        self.project_list = projects
        self.completed_yesterday = completed_yesterday

class JJ_Todo_Project:
    def __init__(self, name, tasks):
        self.project_name = name
        self.tasks = tasks

class JJ_Todo_Task:
    def __init__(self, title):
        self.task_title = title

class JJ_TodoistApi:
    def __init__(self, api):
        self.api = api

    def calculate(self, today, yesterday):
        projects = []
        completed_yesterday = 0

        for project in self.api.state['projects']:

            project_tasks_raw = [task for task in self.api.state['items'] if project['id'] == task['project_id']]
            project_tasks_current = [task for task in project_tasks_raw if task['in_history'] == 0]
            project_tasks_completed = [task for task in project_tasks_raw if task['date_completed'] != None]
            project_tasks_completed_yesterday = [task for task in project_tasks_completed if task['date_completed'].startswith(yesterday)]
            print(str(project_tasks_completed_yesterday))
            completed_yesterday = completed_yesterday + len(project_tasks_completed_yesterday)

            project_tasks_sorted = sorted(project_tasks_current, key=lambda task: task['child_order'])

            project_tasks = []
            for task in project_tasks_sorted:
                if task['due'] != None:
                    due_dict = task['due']
                    if due_dict['date'].startswith(today):
                        project_tasks.append(JJ_Todo_Task(task['content']))
                if task['date_completed'] != None:
                    if task['date_completed'].startswith(yesterday):
                        completed_yesterday = completed_yesterday + 1

            if len(project_tasks) > 0:
                projects.append(JJ_Todo_Project(project['name'], project_tasks))

        return JJ_Todo_Data(projects, completed_yesterday)



class JJ_Todoist:
    def __init__(self, todoist_config, printer):
        self.morning_image = todoist_config.morning_image
        self.token = todoist_config.token
        self.refresh_time = todoist_config.refresh_time
        self.current_refresh_time = self.refresh_time
        self.printer = printer
        self.api  = todoist.TodoistAPI(self.token)
        self.last_date = ""
        self.days = 0
        self.calculator = JJ_TodoistApi(self.api)
        print("Will refresh every: " + str(self.refresh_time))

    def tick(self, time):
        self.current_refresh_time = self.current_refresh_time + time
        if self.current_refresh_time > self.refresh_time:
            self.current_refresh_time = 0
            self.refresh()
    
    def calculate_today(self):
        return datetime.now(timezone('US/Eastern')) + timedelta(hours=-6) # since we subtract 6 hours, date will change at 6AM instead of 12AM. (6AM - 6 hours = 12AM)

    def refresh(self):
        today = self.calculate_today().strftime("%Y-%m-%d")
        if self.last_date == today: 
            print("skipping task print")
        else:
            print("printing!")
            self.days = self.days + 1
            self.print_tasks()

    def print_tasks(self):

        today_date = self.calculate_today()
        today = today_date.strftime("%Y-%m-%d")
        yesterday_date = today_date - timedelta(days = 1)
        yesterday = yesterday_date.strftime("%Y-%m-%d")

        self.last_date = today
        self.api.sync()

        data = self.calculator.calculate(today, yesterday)

        self.printer.println("Good Morning!")
        self.printer.printImage(Image.open(self.morning_image), False)
        self.printer.println("Today is " + self.last_date + ".")
        self.printer.println("")
        self.printer.println(str(self.days) + " Day(s) Without Incident")
        self.printer.println("")
        self.printer.println(str(data.completed_yesterday) + " Completed Yesterday")

        for project in data.project_list:
            if len(project.tasks) > 0:
                self.printer.println("")
                self.printer.println(project.project_name)
                for task in project.tasks:
                    self.printer.println("  - " + task.task_title)

        self.printer.println("")
        self.printer.println("Good Luck!")
        self.printer.feed(6)

    def finish(self):
        print("Button finished.")
