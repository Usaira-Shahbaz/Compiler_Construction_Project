import math

class CodeGenerator:
    def __init__(self):
        self.variables = {}
        self.tac = []  # List to store Three-Address Code
        self.assembly = []  # List to store Assembly Code
        self.temp_counter = 0  # For generating temporary variables

    def execute(self, ast):
        output = []  # Store results for PRINT statements
        for statement in ast:
            if statement[0] == "DECLARE":
                _, var_name, expr = statement
                value = self.evaluate(expr)
                self.variables[var_name] = value
                self.add_tac(f"{var_name} = {value}")
                self.add_assembly(f"MOV {var_name}, {value}")
            elif statement[0] == "ASSIGN":
                _, var_name, expr = statement
                value = self.evaluate(expr)
                self.variables[var_name] = value
                self.add_tac(f"{var_name} = {value}")
                self.add_assembly(f"MOV {var_name}, {value}")
            elif statement[0] == "PRINT":
                _, expr = statement
                result = self.evaluate(expr)
                output.append(str(result))  # Store output
                temp_var = self.new_temp()
                self.add_tac(f"{temp_var} = {result}")
                self.add_assembly(f"MOV {temp_var}, {result}")
                self.add_assembly(f"OUT {temp_var}")
        return "\n".join(output)

    def evaluate(self, expr):
        if isinstance(expr, tuple) and len(expr) == 2 and expr[0] == "GROUP":
            return self.evaluate(expr[1])
        if expr[0] == "NUMBER":
            return expr[1]
        elif expr[0] == "ID":
            var_name = expr[1]
            if var_name not in self.variables:
                raise NameError(f"Variable '{var_name}' is not defined")
            return self.variables[var_name]
        elif expr[0] in {"ADD", "SUB", "MUL", "DIV", "MOD", "POW"}:
            op, operands = expr
            operand_values = [self.evaluate(operand) for operand in operands]
            temp_var = self.new_temp()

            # Initialize the result with the first operand
            result = operand_values[0]

            # Perform the operation sequentially
            for i in range(1, len(operand_values)):
                if op == "ADD":
                    result += operand_values[i]
                    self.add_tac(f"{temp_var} = {temp_var} + {operand_values[i]}")
                    self.add_assembly(f"ADD {temp_var}, {temp_var}, {operand_values[i]}")
                elif op == "SUB":
                    result -= operand_values[i]
                    self.add_tac(f"{temp_var} = {temp_var} - {operand_values[i]}")
                    self.add_assembly(f"SUB {temp_var}, {temp_var}, {operand_values[i]}")
                elif op == "MUL":
                    result *= operand_values[i]
                    self.add_tac(f"{temp_var} = {temp_var} * {operand_values[i]}")
                    self.add_assembly(f"MUL {temp_var}, {temp_var}, {operand_values[i]}")
                elif op == "DIV":
                    result /= operand_values[i]
                    self.add_tac(f"{temp_var} = {temp_var} / {operand_values[i]}")
                    self.add_assembly(f"DIV {temp_var}, {temp_var}, {operand_values[i]}")
                elif op == "POW":
                    result **= operand_values[i]
                    self.add_tac(f"{temp_var} = {temp_var} ^ {operand_values[i]}")
                    self.add_assembly(f"POW {temp_var}, {temp_var}, {operand_values[i]}")
            return result
        elif expr[0] == "LOG":
            operand = self.evaluate(expr[1][0])  # Logarithm is unary
            if operand <= 0:
                raise ValueError("Logarithm operand must be positive")
            result = math.log10(operand)
            temp_var = self.new_temp()
            self.add_tac(f"{temp_var} = LOG({operand})")
            self.add_assembly(f"LOG {temp_var}, {operand}")
            return result
        elif expr[0] in {"COS", "SIN", "TAN"}:
            op, operand = expr
            operand_value = self.evaluate(operand[0])  # Trigonometric functions are unary
            temp_var = self.new_temp()
            if op == "COS":
                result = math.cos(math.radians(operand_value))
                self.add_tac(f"{temp_var} = COS({operand_value})")
                self.add_assembly(f"COS {temp_var}, {operand_value}")
            elif op == "SIN":
                result = math.sin(math.radians(operand_value))
                self.add_tac(f"{temp_var} = SIN({operand_value})")
                self.add_assembly(f"SIN {temp_var}, {operand_value}")
            elif op == "TAN":
                result = math.tan(math.radians(operand_value))
                self.add_tac(f"{temp_var} = TAN({operand_value})")
                self.add_assembly(f"TAN {temp_var}, {operand_value}")
            return result

    def add_tac(self, code):
        self.tac.append(code)

    def add_assembly(self, code):
        self.assembly.append(code)

    def new_temp(self):
        self.temp_counter += 1
        return f"T{self.temp_counter}"

    def get_tac(self):
        return "\n".join(self.tac)

    def get_assembly(self):
        return "\n".join(self.assembly)
