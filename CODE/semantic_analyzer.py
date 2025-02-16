
class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = {}

    def analyze(self):
        for statement in self.ast:
            if statement[0] == "DECLARE":
                var_name = statement[1]
                if var_name in self.symbol_table:
                    raise RuntimeError(f"Variable '{var_name}' already declared")
                self.symbol_table[var_name] = None
            elif statement[0] == "ASSIGN":
                var_name = statement[1]
                if var_name not in self.symbol_table:
                    raise RuntimeError(f"Variable '{var_name}' not declared")
            # Other semantic checks can be added here
    