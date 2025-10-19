from enum import Enum, auto
import json

class NumberException(Exception):
    def __init__(self, message="Wrong number formatting style, error !"):
        super().__init__(message)

class ExpressionException(Exception):
    def __init__(self, message="This expression are illegal to have!!!"):
        super().__init__(message)

class IdentifierException(Exception):
    def __init__(self, message="This is not an identifier!"):
        super().__init__(message)

class TokenType(Enum):
    Number = auto()
    Plus = auto()
    Minus = auto()
    Mult = auto()
    Equals = auto()
    Conditional = auto()
    Lambda = auto()
    Let = auto()
    Lparen = auto()
    Rparen = auto()
    Identifier = auto()

class Token:
    def __init__(self, valueOrType):
        if valueOrType.isnumeric():
            self.value = valueOrType
            self.type = TokenType.Number
        elif valueOrType.isalpha() and valueOrType != 'λ':
            self.value = valueOrType
            self.type = TokenType.Identifier
        else:
            self.value = -1
            self.type = self.typeOf(valueOrType)

    def isNumber(self):
        return self.type == TokenType.Number

    def getType(self):
        return self.type

    def getValue(self):
        if self.isNumber():
            return self.value
        else:
            return None

    def typeOf(self, symbol):
        types = {
            '+': TokenType.Plus,
            '−': TokenType.Minus,
            '×': TokenType.Mult,
            '=': TokenType.Equals,
            '?': TokenType.Conditional,
            'λ': TokenType.Lambda,
            '≜': TokenType.Let,
            '(': TokenType.Lparen,
            ')': TokenType.Rparen,
        }
        return types.get(symbol, ExpressionException())

    def __str__(self):
        strings = {
            TokenType.Number: self.value,
            TokenType.Identifier: self.value,
            TokenType.Plus: "PLUS",
            TokenType.Minus: "MINUS",
            TokenType.Mult: "MULT",
            TokenType.Equals: "EQUALS",
            TokenType.Conditional: "CONDITIONAL",
            TokenType.Lambda: "LAMBDA",
            TokenType.Let: "LET",
            TokenType.Lparen: "LPAREN",
            TokenType.Rparen: "RPAREN",
        }
        return strings.get(self.type, None)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        if self.isNumber():
            if other.isNumber():
                return int(self.value) == int(other.value)
            else:
                return False
        else:
            if other.isNumber():
                return False
            else:
                return self.type == other.type

    def __ne__(self, other):
        return not self == other

class LexicalAnalyser:
    states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6'}
    alphabets = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+', '-', '×', '=', '?', 'λ', '≜', '(', ')', ' '}

    transition_0 = {'q0': 'q1', 'q1': 'q6', 'q2': 'q1', 'q3': 'q3', 'q4': 'q4', 'q5': 'q6', 'q6': 'q6'}
    transition_1_9 = {'q0': 'q3', 'q1': 'q6', 'q2': 'q3', 'q3': 'q3', 'q4': 'q4', 'q5': 'q6', 'q6': 'q6'}
    transition_op = {'q0': 'q5', 'q1': 'q6', 'q2': 'q5', 'q3': 'q6', 'q4': 'q6', 'q5': 'q6', 'q6': 'q6'}
    transition_space = {'q0': 'q0', 'q1': 'q0', 'q2': 'q2', 'q3': 'q0', 'q4': 'q0', 'q5': 'q0', 'q6': 'q6'}
    transition_a_z_A_Z = {'q0': 'q4', 'q1': 'q6', 'q2': 'q4', 'q3': 'q6', 'q4': 'q4', 'q5': 'q6', 'q6': 'q6'}
    transition_paren = {'q0': 'q2', 'q1': 'q2', 'q2': 'q2', 'q3': 'q2', 'q4': 'q2', 'q5': 'q2', 'q6': 'q6'}

    start_state = 'q0'
    accepting_state = ['q1', 'q3', 'q4', 'q5', 'q2', 'q0']

    @classmethod
    def analyse(cls, input):
        current_state = cls.start_state
        token_list = []

        for char in input:
            if current_state == 'q6':
                raise ExpressionException(f'Invalid expression,the input is "{input}"')

            if char.isdigit():
                if char in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    if current_state in ('q0', 'q2'):
                        token_buffer = Token(char)
                        token_list.append(token_buffer)
                    else:
                        token_buffer.value += char
                    current_state = cls.transition_1_9[current_state]
                elif char == '0':
                    if current_state in ('q0', 'q2'):
                        token_buffer = Token(char)
                        token_list.append(token_buffer)
                    else:
                        token_buffer.value += char
                    current_state = cls.transition_0[current_state]
            elif char.isalpha() and char != 'λ':
                if current_state in ('q0', 'q2'):
                    token_buffer = Token(char)
                    token_list.append(token_buffer)
                else:
                    token_buffer.value += char
                current_state = cls.transition_a_z_A_Z[current_state]
            elif char == ' ':
                current_state = cls.transition_space[current_state]
            elif char in ['+', '−', '×', '=', '?', 'λ', '≜']:
                token_buffer = Token(char)
                token_list.append(token_buffer)
                current_state = cls.transition_op[current_state]
            elif char in ['(', ')']:
                token_buffer = Token(char)
                token_list.append(token_buffer)
                current_state = cls.transition_paren[current_state]
            else:
                current_state = 'q6'

        if current_state in cls.accepting_state:
            return token_list
        elif current_state in ['q1', 'q3']:
            raise NumberException(f'Wrong, the input is "{input}"')
        elif current_state in ['q6', 'q5', 'q2']:
            raise ExpressionException(f'Wrong, the input is "{input}"')
        elif current_state == 'q4':
            raise IdentifierException(f'Wrong, the input is "{input}"')

class LL1():
    @staticmethod
    def paren2list(tokenize_input):
        stack_convert = [[]]
        for tok in tokenize_input:
            if tok == "LPAREN":
                new_list = []
                stack_convert[-1].append(new_list)
                stack_convert.append(new_list)
            elif tok == "RPAREN":
                stack_convert.pop()
            else:
                stack_convert[-1].append(tok)
        return stack_convert[0][0] if len(stack_convert[0]) == 1 else stack_convert[0]

    @staticmethod
    def list2json(output):
        return [int(n.value) if n.type == TokenType.Number else str(n) for n in output]

    @classmethod
    def parsing_algorithm(cls, input_str):
        try:
            input = LexicalAnalyser.analyse(input_str)
        except Exception as e:
            return str(e)

        stack = []
        stack.append("S")
        input_index = 0

        def paren_expr():
            nonlocal input_index
            if input[input_index].type in [TokenType.Plus, TokenType.Minus, TokenType.Mult, TokenType.Equals]:
                stack.append('S')
                stack.append('S')
                stack.append(input[input_index].type)
            elif input[input_index].type == TokenType.Conditional:
                stack.append('S')
                stack.append('S')
                stack.append('S')
                stack.append(input[input_index].type)
            elif input[input_index].type == TokenType.Lambda:
                stack.append('S')
                stack.append(TokenType.Identifier)
                stack.append(TokenType.Lambda)
            elif input[input_index].type == TokenType.Let:
                stack.append('S')
                stack.append('S')
                stack.append(TokenType.Identifier)
                stack.append(TokenType.Let)
            elif input[input_index].type in [TokenType.Lparen, TokenType.Number, TokenType.Identifier]:
                stack.append('D')
                stack.append('S')
            elif input[input_index].type == TokenType.Rparen:
                stack.append("wrong number of arguments")
                input_index = len(input)

        def expr_star():
            nonlocal input_index
            if input[input_index].type in [TokenType.Lparen, TokenType.Number, TokenType.Identifier]:
                stack.append('D')
                stack.append('S')
            elif input[input_index].type == TokenType.Rparen:
                return
            else:
                stack.append("Wrong argument format")
                input_index = len(input)

        def expr():
            nonlocal input_index
            if input[input_index].type == TokenType.Lparen:
                stack.append(TokenType.Rparen)
                stack.append('M')
                stack.append(TokenType.Lparen)
            elif input[input_index].type == TokenType.Number or input[input_index].type == TokenType.Identifier:
                stack.append(input[input_index].type)
            elif input[input_index].type == TokenType.Rparen:
                stack.append("wrong number of arguments")
                input_index = len(input)
            else:
                stack.append("Wrong argument format")
                input_index = len(input)

        while input_index < len(input):
            if not stack:
                tok = input[input_index]
                if tok.type == TokenType.Lparen:
                    return "missing closing paren"
                elif tok.type == TokenType.Rparen:
                    return "unmatched paren"
                else:
                    return "wrong number of arguments"
            elif stack[-1] == "S":
                stack.pop()
                expr()
            elif stack[-1] == 'M':
                stack.pop()
                paren_expr()
            elif stack[-1] == 'D':
                stack.pop()
                expr_star()
            elif isinstance(stack[-1], TokenType) and stack[-1] == input[input_index].type:
                stack.pop()
                input_index += 1
            elif isinstance(stack[-1], TokenType) and stack[-1] != input[input_index].type:
                return "wrong number of arguments"

        if input_index == len(input) and not stack:
            new_input = cls.list2json(input)
            new_input_json = cls.paren2list(new_input)
            return new_input_json
        elif input_index == len(input) and stack:
            while stack:
                if isinstance(stack[-1], str):
                    if stack[-1] in ["S", "M", "D"]:
                        stack.pop()
                    else:
                        return stack[-1]
                elif stack[-1] == TokenType.Lparen:
                    return "Unmatch paren"
                elif stack[-1] == TokenType.Rparen:
                    return "Missing closing paren"
                else:
                    return "unmatch expression"

# Test cases with expected errors
def main():
    print("=" * 60)
    print("Test Cases - Error Detection")
    print("=" * 60)
    print()

    # Error test cases matching the image
    error_test_cases = [
        ("(+ 2", "missing closing paren"),
        (")", "unmatched paren"),
        ("(+ 2 3 4)", "wrong number of arguments"),
    ]

    # Additional random error test cases
    additional_tests = [
        ("(× 5", "missing closing paren"),
        ("(− 10 20 30)", "wrong number of arguments"),
        (")))", "unmatched paren"),
        ("((+ 1 2)", "missing closing paren"),
        ("(+ )", "wrong number of arguments"),
        ("(λ)", "wrong number of arguments"),
        ("(= 1 2 3)", "wrong number of arguments"),
        ("(? x)", "wrong number of arguments"),
        ("(≜ x)", "wrong number of arguments"),
        ("((", "missing closing paren"),
        ("(+ 1 2 3 4 5)", "wrong number of arguments"),
        (")+ 2 3(", "unmatched paren"),
        ("(× (+ 2 3)", "missing closing paren"),
        ("(− 5 (× 2 3 4))", "wrong number of arguments"),
        ("(+ 1 (− 2)", "missing closing paren"),
    ]

    all_tests = error_test_cases + additional_tests

    for i, (test_input, expected_error) in enumerate(all_tests, 1):
        result = LL1.parsing_algorithm(test_input)
        status = "✓" if expected_error in str(result).lower() else "✗"

        print(f"{test_input:<25} // {result}")

    print()
    print("=" * 60)
    print(f"Total tests run: {len(all_tests)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
