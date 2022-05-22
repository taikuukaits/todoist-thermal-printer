class JJ_Todoist_Config:
    def __init__(self,event_log_dict):
        self.token = event_log_dict["token"]
        self.refresh_time = event_log_dict["refresh_time"]
        self.morning_image = event_log_dict["morning_image"]