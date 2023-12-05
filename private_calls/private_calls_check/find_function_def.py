from ast import NodeVisitor


class FindFunctionDef(NodeVisitor):
    def __init__(self):
        self.result = []

    def visit_FunctionDef(self, node):
        self.result.append(node.name)
        self.generic_visit(node)
