class Visitor:
    def __init__(self):
        self.result = None
        self.the_number_of_transmitted_submits = 0

    def visit(self, submit):
        self.the_number_of_transmitted_submits += 1

    # Returns ready for print string of result data
    def pretty_print(self):
        return ""

    def get_stat_data(self):
        return self.result

    def close(self):
        pass
