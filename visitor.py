class Visitor:
    def __init__(self):
        self.result = None
        self.the_number_of_transmitted_submits = 0

    def update_submit(self, submit):
        self.the_number_of_transmitted_submits += 1

    #Returns ready for print string of result data
    def get_stat_data(self):
        return ""