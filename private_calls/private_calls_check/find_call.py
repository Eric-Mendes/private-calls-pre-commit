from ast import NodeVisitor


class FindCall(NodeVisitor):
    def __init__(self, *args):
        self.result = []
        self.linenos = []

    def visit_Call(self, node):
        self.result.append(node.func.id)
        self.linenos.append(node.func.lineno)
        self.generic_visit(node)
