import re
class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.token_specification = [
            ("NUMBER", r"-?\d+(\.\d+)?"),   # Integer or decimal number
            ("ADD", r"ADD"),             # Addition keyword
            ("SUB", r"SUB"),             # Subtraction keyword
            ("MUL", r"MUL"),             # Multiplication keyword
            ("DIV", r"DIV"),             # Division keyword
            ("MOD", r"MOD"),             # Modulo keyword
            ("POW", r"POW"),             # Power keyword
            ("LOG", r"LOG"),             # Logarithm keyword
            ("SIN", r"SIN"),             # Sine function
            ("COS", r"COS"),             # Cosine function
            ("TAN", r"TAN"),             # Tangent function
            ("VAR", r"VAR"),             # Variable declaration
            ("PRINT", r"PRINT"),         # Print statement
            ("ASSIGN", r"="),            # Assignment operator
            ("ID", r"[a-zA-Z_]\w*"),     # Identifiers
            ("SKIP", r"[ \t]+"),         # Skip spaces and tabs
            ("MISMATCH", r"."),          # Any other character
        ]

    def tokenize(self):
        token_regex = "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in self.token_specification)
        for mo in re.finditer(token_regex, self.code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == "NUMBER":
                value = float(value) if '.' in value else int(value)
            elif kind == "SKIP":
                continue
            elif kind == "MISMATCH":
                raise SyntaxError(f"Unexpected character: {value}")
            self.tokens.append((kind, value))
        return self.tokens
