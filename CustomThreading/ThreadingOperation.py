import threading

class Threading(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        try:
            def operation():
                self.result = target(*args, **kwargs)
            super().__init__(group=group, target=operation, name=name, daemon=daemon)
        except Exception as e:
            self.logger_obj.log('INFO', 'Some Exception Occurred during thread initialization. Exception is : '+str(e))
