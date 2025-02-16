from graphviz import Digraph

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def parse(self):
        statements = []
        while self.current_token:
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.current_token[0] == "VAR":
            return self.declaration()
        elif self.current_token[0] == "PRINT":
            return self.print_statement()
        elif self.current_token[0] == "ID":
            return self.assignment()
        else:
            raise SyntaxError(f"Unexpected token in statement: {self.current_token}")

    def declaration(self):
        self.advance()  # Skip VAR
        if self.current_token[0] != "ID":
            raise SyntaxError(f"Expected identifier after VAR, found: {self.current_token}")
        var_name = self.current_token[1]
        self.advance()
        if self.current_token[0] != "ASSIGN":
            raise SyntaxError(f"Expected '=' after identifier '{var_name}', found: {self.current_token}")
        self.advance()
        expr = self.expression()
        return ("DECLARE", var_name, expr)

    def assignment(self):
        var_name = self.current_token[1]
        self.advance()
        if self.current_token[0] != "ASSIGN":
            raise SyntaxError(f"Expected '=' after identifier '{var_name}', found: {self.current_token}")
        self.advance()
        expr = self.expression()
        return ("ASSIGN", var_name, expr)

    def print_statement(self):
        self.advance()  # Skip PRINT
        expr = self.expression()
        return ("PRINT", expr)

    def expression(self):
        if self.current_token[0] in {"ADD", "SUB", "MUL", "DIV", "MOD", "POW", "LOG", "COS", "SIN", "TAN"}:
            return self.operation()
        return self.term()

    def operation(self):
        op = self.current_token[0]
        self.advance()  # Skip operation
        operands = []
        while self.current_token and (self.current_token[0] == "ID" or self.current_token[0] == "NUMBER"):
            operands.append(self.term())
        if op in {"ADD", "SUB", "MUL", "DIV", "MOD"} and len(operands) < 2:
            raise SyntaxError(f"Operation '{op}' requires at least two operands, found: {operands}")
        if op in {"POW", "LOG"} and len(operands) != 2:
            raise SyntaxError(f"Operation '{op}' requires exactly two operands, found: {operands}")
        return (op, operands)

    def term(self):
        token = self.current_token
        if token[0] == "NUMBER":
            self.advance()
            return ("NUMBER", token[1])
        elif token[0] == "ID":
            self.advance()
            return ("ID", token[1])
        else:
            raise SyntaxError(f"Unexpected token in term: {token}")

    def generate_dot_tree(self, ast):
        """Generates a DOT representation of the AST for visualization."""
        graph = Digraph("ParseTree")
        self._add_nodes(graph, ast, "root")
        return graph

    def _add_nodes(self, graph, node, parent_id):
        """Recursively adds nodes and edges to the DOT graph."""
        if isinstance(node, tuple):
            node_id = f"{id(node)}"
            label = node[0]
            graph.node(node_id, label)
            if parent_id:
                graph.edge(parent_id, node_id)
            for child in node[1:]:
                self._add_nodes(graph, child, node_id)
        elif isinstance(node, list):
            for child in node:
                self._add_nodes(graph, child, parent_id)
        else:
            node_id = f"{id(node)}"
            graph.node(node_id, str(node))
            if parent_id:
                graph.edge(parent_id, node_id)