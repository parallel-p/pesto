from visitor import Visitor

class CompositorVisitor(Visitor):
    def __init__(self, *visitors):
        super().__init__()
        self.visitors = list(visitors)

    def update_submit(self, update_submit):
        for visitor in self.visitors:
            visitor.update_submit(update_submit)

    def get_stat_data(self):
        if len(self.visitors) == 0:
            return ""
        else:
            return "\n\n".join([visitor.get_stat_data() for visitor in self.visitors])
