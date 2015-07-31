from visitor import Visitor

class CompositorVisitor(Visitor):

    def __init__(self, *visitors):
        super().__init__(self)
        self.visitors = visitors

    def update_submit(self, update_submit):
        for visitor in self.visitors:
            visitor.update_submit(self.current_submit)

    def get_stat_data(self):
        "\n\n".join([visitor.get_stat_data() for visitor in self.visitors])
        