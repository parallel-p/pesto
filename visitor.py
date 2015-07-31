class Visitor:
    def __init__(self):
        self.result = None

    def update_submit(self, submit):
        pass

    #Returns ready for print string of result data
    def get_stat_data(self):
        return ""