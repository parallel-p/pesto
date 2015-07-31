from visitor import Visitor

class CompositorVisitor(Visitor):

    def __init__(self, *visitors):
        self.visitors = visitors

    def update(self):
        for visitor in self.visitors
            visitor.add_submit(self.current_submit)
            visitor.Update()    
        