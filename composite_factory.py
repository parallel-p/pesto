from compositor_visitor import CompositorVisitor
from visitor_factory import VisitorFactory


class CompositeVisitorFactory(VisitorFactory):
    def __init__(self,  *factories):
        super().__init__()
        self.factories = list(factories)
        
    def create(self, key):
        visitors = []
        for factory in self.factories:
            visitors.append(factory.create(key))
        return CompositorVisitor(*visitors)