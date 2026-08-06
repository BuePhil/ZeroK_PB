class BreakSignal(Exception):
    def __init__(self, value):
        self.value = value

class OnBreakSignal(Exception):
    def __init__(self, value):
        self.value = value

class ContinueSignal(Exception):
    def __init__(self, value):
        self.value = value