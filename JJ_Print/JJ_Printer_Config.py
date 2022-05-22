class JJ_Printer_Config:
    def __init__(self,printer_dict):
        self.serial = printer_dict["serial"]
        self.baud = printer_dict["baud"]
        self.timeout = printer_dict["timeout"]