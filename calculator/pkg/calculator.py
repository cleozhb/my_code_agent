# calculator.py
import math

class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "**": lambda a, b: a ** b,
        }
        self.functions = {
            "log": lambda x: math.log10(x),
            "ln": lambda x: math.log(x),
            "log2": lambda x: math.log2(x),
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "**": 3,  # Highest precedence for exponentiation
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token in self.operators:
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
                i += 1
            elif token in self.functions:
                # For functions, we need to evaluate the entire expression that follows
                # until we hit an operator or end of tokens
                function = token
                
                # Find the argument for the function
                j = i + 1
                while j < len(tokens) and tokens[j] not in self.operators and tokens[j] not in self.functions:
                    j += 1
                
                # Extract the argument tokens
                arg_tokens = tokens[i+1:j]
                if not arg_tokens:
                    raise ValueError(f"no argument provided for function {function}")
                
                # Evaluate the argument
                if len(arg_tokens) == 1:
                    # Single number
                    try:
                        arg_value = float(arg_tokens[0])
                    except ValueError:
                        raise ValueError(f"invalid argument for function {function}: {arg_tokens[0]}")
                else:
                    # Expression - evaluate it recursively
                    arg_value = self._evaluate_infix(arg_tokens)
                
                # Apply the function
                values.append(self.functions[function](arg_value))
                i = j
            else:
                try:
                    values.append(float(token))
                    i += 1
                except ValueError:
                    raise ValueError(f"invalid token: {token}")

        # Process remaining operators
        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))