from datetime import datetime, date, timedelta
from JJ_Print.JJ_Todoist_Config import JJ_Todoist_Config
from pytz import timezone
import requests

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
    def __init__(self, token):
        self.token = token


    def calculate(self, today, yesterday):
        
        completed_yesterday = 0

        tasks_request = requests.get(
            "https://api.todoist.com/api/v1/tasks/filter?query=today%7Coverdue",
            headers={"Authorization": "Bearer " + self.token},
            params={"filter": "today%7Coverdue"},
        )
        tasks_request.raise_for_status()
        tasks_data = tasks_request.json()

        projects_request = requests.get(
            "https://api.todoist.com/api/v1/projects",
            headers={"Authorization": "Bearer " + self.token},
        )
        projects_request.raise_for_status()
        projects_data = projects_request.json()

        jj_projects = []
        for project in projects_data["results"]:
            found_tasks = []
            for task in tasks_data["results"]:
                if task["project_id"] == project["id"]:
                    found_tasks.append(JJ_Todo_Task(task["content"]))

            if len(found_tasks) > 0:
                jj_projects.append(JJ_Todo_Project(project["name"], found_tasks))

        return JJ_Todo_Data(jj_projects, completed_yesterday)



class JJ_Todoist:
    def __init__(self, todoist_config, printer):
        self.morning_image = todoist_config.morning_image
        self.token = todoist_config.token
        self.refresh_time = todoist_config.refresh_time
        self.current_refresh_time = self.refresh_time
        self.printer = printer
        self.last_date = ""
        self.days = 0
        self.calculator = JJ_TodoistApi(self.token)
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

        data = self.calculator.calculate(today, yesterday)

        self.printer.println("Good Morning!")
        self.printer.println("Today is " + self.last_date + ".")
        self.printer.println("")
        self.printer.println(str(self.days) + " Day(s) Without Incident")

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
