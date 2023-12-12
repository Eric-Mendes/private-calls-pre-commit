from ast import Attribute, Name, NodeVisitor


class FindCall(NodeVisitor):
    def __init__(self, *args):
        self.result = []

    def visit_Call(self, node):
        if isinstance(node.func, Name):
            self.result.append(node.func.id)
        elif isinstance(node.func, Attribute):
            self.result.append(node.func.attr)
        self.generic_visit(node)
