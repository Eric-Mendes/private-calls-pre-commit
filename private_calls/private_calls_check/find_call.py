from ast import NodeVisitor


class FindCall(NodeVisitor):
    def __init__(self, *args):
        self.result = []

    def visit_Call(self, node):
        self.result.append(node.func.id)
        self.generic_visit(node)
