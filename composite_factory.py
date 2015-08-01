from compositor_visitor import CompositorVisitor
from visitor_factory import VisitorFactory


class CompositeVisitorFactory(VisitorFactory):
    @staticmethod
    def create(key, *factories):
        visitors = []
        for factory in factories:
            visitors.append(factory.create(key))
        return CompositorVisitor(*visitors)