from datetime import datetime
class ApplicationLogger:
    def __init__(self, name='logfile.log'):
        self.file_name = name

    def log(self, log_type, log_msg):
        self.now = datetime.now()
        self.current_time = self.now.strftime("%d-%m-%Y %H:%M:%S")
        file = open(self.file_name, "a+")
        file.write(self.current_time + "," + log_type + "," + log_msg + "\n")
        file.close()
