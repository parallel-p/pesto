class Visitor:
    def __init__(self):
        self.result = None
        self.current_submit = None

    def add_submit(self, submit):
        self.current_submit = submit

    def update(self):
        pass

    #Returns ready for print string of result data
    def get_stat_data(self):
        return ""