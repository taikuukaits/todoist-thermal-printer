class JJ_Button_Config:
    def __init__(self,button_dict):
        self.button_pin = button_dict["button_pin"]
        self.hold_time = button_dict["hold_time"]
        self.tap_time = button_dict["tap_time"]
        self.debounce_time = button_dict["debounce_time"]
        self.invert_pin = button_dict["invert_pin"]