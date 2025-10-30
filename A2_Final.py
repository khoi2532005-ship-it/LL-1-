from enum import Enum, auto
import json

# Exception classes for error handling
class NumberException(Exception):
    def __init__(self, message="Wrong number formatting style, error !"):
        super().__init__(message)

class ExpressionException(Exception):
    def __init__(self, message="This expression are illegal to have!!!"):
        super().__init__(message)

class IdentifierException(Exception):
    def __init__(self, message="This is not an identifier!"):
        super().__init__(message)

# Token type enumeration for all language tokens
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

# Token class representing individual lexical units
class Token:
    def __init__(self, valueOrType):
        # Determine token type based on input string
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
        # Check if token is a number
        return self.type == TokenType.Number
    
    def getType(self):
        # Return the token type
        return self.type
    
    def getValue(self):
        # Return the token value (for numbers only)
        if self.isNumber():
            return self.value
        else:
            return None
    
    def typeOf(self, symbol):
        # Map symbol characters to token types
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
        # Convert token to string representation
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
        # Compare two tokens for equality
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

# Lexical analyzer implementing a 7-state DFA
class LexicalAnalyser:
    # DFA state definitions
    states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6'}
    alphabets = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+', '-', '×', '=', '?', 'λ', '≜', '(', ')', ' '}
    
    # Transition table for digit '0' (handles leading zero detection)
    transition_0 = {
        'q0': 'q1',
        'q1': 'q6',
        'q2': 'q1',
        'q3': 'q3',
        'q4': 'q4',
        'q5': 'q6',
        'q6': 'q6'
    }
    
    # Transition table for digits 1-9
    transition_0_9 = {
        'q0': 'q3',
        'q2': 'q3',
        'q3': 'q3',
        'q4': 'q4',
        'q5': 'q3',
        'q6': 'q6'
    }
    
    # Transition table for operators
    transition_op = {
        'q0': 'q5',
        'q2': 'q5',
        'q3': 'q6',
        'q4': 'q6',
        'q5': 'q6',
        'q6': 'q6'
    }
    
    # Transition table for whitespace (token separator)
    transition_space = {
        'q0': 'q0',
        'q2': 'q2',
        'q3': 'q0',
        'q4': 'q0',
        'q5': 'q0',
        'q6': 'q6'
    }
    
    # Transition table for letters
    transition_a_z_A_Z = {
        'q0': 'q4',
        'q2': 'q4',
        'q3': 'q6',
        'q4': 'q4',
        'q5': 'q4',
        'q6': 'q6'
    }
    
    # Transition table for parentheses
    transition_paren = {
        'q0': 'q2',
        'q2': 'q2',
        'q3': 'q2',
        'q4': 'q2',
        'q5': 'q2',
        'q6': 'q6'
    }
    
    # DFA configuration
    start_state = 'q0'
    accepting_state = ['q3', 'q4', 'q5', 'q2', 'q0']
    error_state = 'q6'
    
    @classmethod
    def analyse(cls, input):
        # Main DFA processing - converts input string to token list
        current_state = cls.start_state
        token_list = []
        
        for char in input:
            # Reject if in error state
            if current_state == cls.error_state:
                raise ExpressionException(f'Invalid expression, the input is "{input}"')
            
            # Process digits
            if char.isdigit():
                if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    # Create new token or extend existing
                    if current_state in ('q0', 'q2', 'q5'):
                        token_buffer = Token(char)
                        token_list.append(token_buffer)
                    else:
                        token_buffer.value += char
                    
                    # Transition to next state
                    current_state = cls.transition_0_9[current_state]
                    print(token_list)
            
            # Process letters
            elif char.isalpha() and char != 'λ':
                # Create new identifier or extend existing
                if current_state in ('q0', 'q2', 'q5'):
                    token_buffer = Token(char)
                    token_list.append(token_buffer)
                else:
                    token_buffer.value += char
                current_state = cls.transition_a_z_A_Z[current_state]
            
            # Process whitespace (token separator)
            elif char == ' ':
                current_state = cls.transition_space[current_state]
            
            # Process operators
            elif char in ['+', '−', '×', '=', '?', 'λ', '≜']:
                token_buffer = Token(char)
                token_list.append(token_buffer)
                current_state = cls.transition_op[current_state]
            
            # Process parentheses
            elif char in ['(', ')']:
                token_buffer = Token(char)
                token_list.append(token_buffer)
                current_state = cls.transition_paren[current_state]
            
            # Invalid character - go to error state
            else:
                print(char)
                current_state = cls.error_state
        
        # Return tokens if final state is accepting
        if current_state in cls.accepting_state:
            return token_list

# LL(1) parser implementing pushdown automaton
class LL1():
    @staticmethod
    def paren2list(tokenize_input):
        # Convert flat token list to nested list structure using stack
        stack_convert = [[]]
        
        for tok in tokenize_input:
            if tok == "LPAREN":
                # Start new nested level
                new_list = []
                stack_convert[-1].append(new_list)
                stack_convert.append(new_list)
            elif tok == "RPAREN":
                # Close current nested level
                stack_convert.pop()
            else:
                # Add token to current level
                stack_convert[-1].append(tok)
        
        return stack_convert[0][0] if len(stack_convert[0]) == 1 else stack_convert[0]
    
    @staticmethod
    def list2json(output):
        # Convert Token objects to JSON-serializable format
        return [int(n.value) if n.type == TokenType.Number else str(n) for n in output]
    
    @classmethod
    def parsing_algorithm(cls, pre_input):
        # Main LL(1) parsing algorithm
        input = LexicalAnalyser.analyse(pre_input)
        stack = []
        stack.append("P")  # Start with program symbol
        input_index = 0
        
        print(input)
        
        # Helper function: expand M production (parenthesized expression content)
        def paren_expr():
            nonlocal input_index
            
            # Binary operators: +, −, ×, =
            if input[input_index].type in [TokenType.Plus, TokenType.Minus, TokenType.Mult, TokenType.Equals]:
                stack.append('S')
                stack.append('S')
                stack.append(input[input_index].type)
                print(stack)
                print(input_index)
            
            # Conditional operator: ?
            elif input[input_index].type == TokenType.Conditional:
                stack.append('S')
                stack.append('S')
                stack.append('S')
                stack.append(input[input_index].type)
                print(stack)
                print(input_index)
            
            # Lambda abstraction: λ
            elif input[input_index].type == TokenType.Lambda:
                stack.append('S')
                stack.append(TokenType.Identifier)
                stack.append(TokenType.Lambda)
                print(stack)
                print(input_index)
            
            # Let binding: ≜
            elif input[input_index].type == TokenType.Let:
                stack.append('S')
                stack.append('S')
                stack.append(TokenType.Identifier)
                stack.append(TokenType.Let)
                print(stack)
                print(input_index)
            
            # Function application
            elif input[input_index].type in [TokenType.Lparen, TokenType.Number, TokenType.Identifier]:
                stack.append('D')
                stack.append('S')
                print(stack)
                print(input_index)
            
            # Error: empty parentheses
            elif input[input_index].type == TokenType.Rparen:
                stack.append(f"There is no argument between parentheses. Checked parted: {input[0:input_index]}. Error in remaining: {input[input_index:]}")
                input_index = len(input)
        
        # Helper function: expand D production (additional arguments)
        def expr_star():
            nonlocal input_index
            
            # More arguments coming
            if input[input_index].type in [TokenType.Lparen, TokenType.Number, TokenType.Identifier]:
                stack.append('D')
                stack.append('S')
                print(stack)
                print(input_index)
            
            # End of arguments (epsilon production)
            elif input[input_index].type == TokenType.Rparen:
                return
            
            # Error: invalid argument
            else:
                stack.append(f"Wrong argument format. Checked parted: {input[0:input_index]}. Error in remaining: {input[input_index:]}")
                input_index = len(input)
        
        # Helper function: expand P production (program start)
        def prog():
            nonlocal input_index
            print(input[input_index])
            
            # Valid expression starts
            if input[input_index].type in [TokenType.Lparen, TokenType.Number, TokenType.Identifier]:
                stack.append('S')
                print(stack)
                print(input_index)
            
            # Error: starts with closing paren
            elif input[input_index].type == TokenType.Rparen:
                stack.append(f"Should be left parenthesis, number, or identifier instead of closing parenthesis. Checked parted: {input[0:input_index]}. Error in remaining: {input[input_index:]}")
                input_index = len(input)
            
            # Error: invalid start
            else:
                stack.append(f"Wrong argument format. Checked parted: {input[0:input_index]}. Error in remaining: {input[input_index:]}")
                input_index = len(input)
        
        # Helper function: expand S production (expression)
        def expr():
            nonlocal input_index
            print(input[input_index])
            
            # Parenthesized expression
            if input[input_index].type == TokenType.Lparen:
                stack.append(TokenType.Rparen)
                stack.append('M')
                stack.append(TokenType.Lparen)
                print(stack)
                print(input_index)
            
            # Literal (number or identifier)
            elif input[input_index].type in [TokenType.Number, TokenType.Identifier]:
                stack.append(input[input_index].type)
                print(stack)
                print(input_index)
            
            # Error: found closing paren
            elif input[input_index].type == TokenType.Rparen:
                stack.append(f"wrong number of arguments. Checked parted: {input[0:input_index]}. Error in remaining: {input[input_index:]}")
                input_index = len(input)
            
            # Error: invalid expression start
            else:
                stack.append(f"Wrong argument format. Checked parted: {input[0:input_index]}. Error in remaining: {input[input_index:]}")
                input_index = len(input)
        
        # Main parsing loop
        while input_index < len(input):
            # Case 1: Stack empty but input remains (error)
            if not stack:
                tok = input[input_index]
                if tok.type == TokenType.Lparen:
                    return (f"Shouldn't have opening parenthesis for any argument. Checked parted: {input[0:input_index]}. Error in this part: {input[input_index:]}")
                elif tok.type == TokenType.Rparen:
                    return (f"unmatched paren. Checked parted: {input[0:input_index]}. Error in remaining: {input[input_index:]}")
                else:
                    return (f"wrong number of arguments. Checked parted: {input[0:input_index]}. Error in remaining: {input[input_index:]}")
            
            # Case 2: Expand non-terminals
            elif stack[-1] == "P":
                stack.pop()
                prog()
                print(stack)
                print(input_index)
            
            elif stack[-1] == "S":
                stack.pop()
                expr()
                print(stack)
                print(input_index)
            
            elif stack[-1] == 'M':
                stack.pop()
                paren_expr()
                print(stack)
                print(input_index)
            
            elif stack[-1] == 'D':
                stack.pop()
                print(stack)
                expr_star()
            
            # Case 3: Match terminal
            elif isinstance(stack[-1], TokenType) and stack[-1] == input[input_index].type:
                stack.pop()
                input_index += 1
                print(stack)
                print(input_index)
            
            # Case 4: Terminal mismatch (error)
            elif isinstance(stack[-1], TokenType) and stack[-1] != input[input_index].type:
                if input[input_index].type == TokenType.Lparen:
                    return (f"Open another parenthesis instead of finishing old argument. Checked parted: {input[0:input_index]}. Error remaining: {input[input_index:]}")
                elif input[input_index].type == TokenType.Rparen:
                    return (f"Wrong number of arguments. Checked part: {input[0:input_index]}. Error in remaining: {input[input_index:]}")
                else:
                    return (f"wrong arguments format. Checked part: {input[0:input_index]}. Error remaining: {input[input_index:]}")
        
        # Success: both stack and input empty
        if input_index == len(input) and not stack:
            new_input = cls.list2json(input)
            new_input_json = cls.paren2list(new_input)
            print("String accepted")
            return new_input_json
        
        # Error: input exhausted but stack not empty
        elif input_index == len(input) and stack:
            while stack:
                if isinstance(stack[-1], str):
                    if stack[-1] == "P":
                        return "Empty expression"
                    elif stack[-1] == "S":
                        return "Wrong number of arguments"
                    elif stack[-1] == "M":
                        return "Incomplete argument. Only open parenthesis for the last argument"
                    elif stack[-1] == "D":
                        return "Missing closing parenthesis"
                    else:
                        return stack[-1]
                elif stack[-1] == TokenType.Lparen:
                    return "Unmatch paren"
                elif stack[-1] == TokenType.Rparen:
                    return "Missing closing paren"
                else:
                    return "unmatch expression"

# Test suite with 138 comprehensive test cases
def main():
    test_cases = [
        # Basic valid cases
        '42', 'x ', '(+ 2 3)', '(× x 5)', '(+ (× 2 3) 4)', 
        '(? (= x 0) 1 0)', '(λ x x)', '(≜ y 10 y)', '((λ x (+ x 1)) 5)', 
        
        # Error cases
        '(+ 2', ') ', '(+ 2 3 4)',
        
        # Numbers
        "42", "0", "123", "99999",
        
        # Identifiers
        "x", "y", "var", "abc", "XYZ", "longid",
        
        # Binary operations
        "(+ 1 2)", "(− 5 3)", "(× 2 3)", "(= 4 4)",
        "(+ 12 34)", "(× 9 8)", "(− 10 7)", "(= 99 99)",
        
        # Conditionals
        "(? (= 1 1) 2 3)", "(? (= 2 3) 4 5)",
        "(? (= x 0) 1 0)", "(? (= x y) x y)",
        
        # Lambda abstractions
        "(λ x x)", "(λ y (+ y 1))", "(λ z (× z z))", "(λ f (λ x (f x)))",
        "(λ x (+ x 2))", "(λ x (− x 2))", "(λ x (× x 2))", "(λ x (= x 2))",
        "(λ a (λ b (+ a b)))", "(λ x (? (= x 0) 1 (× x x)))",
        "(λ f (λ x (f (f x))))", "(λ f (λ x (f (f (f x)))))",
        
        # Let bindings
        "(≜ y 10 y)", "(≜ a 1 (+ a 2))", "(≜ b (λ x (+ x 1)) (b 5))",
        "(≜ id (λ x x) (id 5))", "(≜ const (λ x (λ y x)) ((const 1) 2))",
        "(≜ inc (λ n (+ n 1)) (inc 10))", "(≜ dbl (λ n (× n 2)) (dbl 7))",
        "(≜ sq (λ n (× n n)) (sq 9))", "(≜ add (λ a (λ b (+ a b))) ((add 3) 4))",
        "(≜ f (λ x (+ x 1)) (f (f 5)))", "(≜ f (λ x (× x x)) (f (f 2)))",
        "(≜ triple (λ n (+ n (+ n n))) (triple 5))",
        "(≜ a 1 (≜ b 2 (+ a b)))", "(≜ a (≜ b 2 b) a)",
        "(≜ f (λ x (+ x 1)) (≜ g (λ y (+ y 2)) (g (f 3))))",
        
        # Function applications
        "((λ x (+ x 1)) 5)", "((λ y (× y y)) 4)", "((λ z (− z 1)) 10)",
        "((λ f (f 10)) (λ x (+ x 2)))", "((λ f (λ x (f x))) (λ n (+ n 1)))",
        "((λ f (f 5)) (λ n (+ n 1)))", "((λ a (λ b (+ a b))) 3 4)",
        "((λ a (λ b (+ a b))) 3)", "(((λ x (λ y (+ x y))) 2) 3)",
        "((λ x (+ x 1)) ((λ x (+ x 1)) 0))",
        
        # Nested expressions
        "(+ (+ 1 2) 3)", "(× (× 2 3) 4)", "(= (= 1 1) (= 2 2))",
        "(+ (× 2 3) 4)", "(− (× 2 5) (× 3 3))", "(× (+ 2 3) (− 7 2))",
        "(= (+ 1 2) 3)", "(= (× 2 3) 6)", "(+ (× 2 (+ 3 4)) (− 10 1))",
        "(= (+ 1 2) (+ 3 0))", "(= (× 2 3) (× 1 6))", "(+ (λ x x) 3)",
        "(? (= 1 1) (= 2 2) (= 3 3))", "(? (= 1 2) (+ 2 2) (× 3 3))",
        "(? (= x x) (? (= y y) (? (= z z) 1 2) 3) 4)",
        
        # Advanced/complex
        "(≜ sum2 (λ a (λ b (+ a b))) (sum2 3 4))",
        "(≜ sum2 (λ a (λ b (+ a b))) ((sum2 3) 4))",
        "((λ f (λ x (f (f x)))) (λ n (+ n 1)))",
        "((λ f (λ x (f (f (f x))))) (λ n (+ n 1)))",
        "((λ x (x x)) (λ x (x x)))",
        "(≜ omega (λ x (x x)) (omega omega))",
        "((λ x (λ x (λ x x))) 1 2 3)",
        "(≜ F (λ fact (λ n (? (= n 0) 1 (× n (fact (− n 1)))))))",
        "(≜ bool (λ x (λ y x)) bool)",
        "(≜ apply (λ f (λ x (f x))) (apply (λ y (+ y 1)) 3))",
        
        # Church numerals
        "(≜ church1 (λ f (λ x (f x))))",
        "(≜ church2 (λ f (λ x (f (f x)))))",
        
        # Error cases
        '(+ 2 3 ) (4 5)', '( ( + 1 2 ) (3 4 (', ' (λ x x) 5', ')',
        '(+ 2 3)) )', ' (λ x x)) )', '(+ (× 2 3) ( + 4 5))',
        '(= 1 ( ) )', '(? 1 2 ( 3))', '(+ 2', ' (λ x', '(≜ y 10',
        '(+ 2 )', '(? 1 2 )', '(≜ x 10 )', '( )', '(+ )', '(× ( ) )',
        ' (λ 1 x)', '(≜ y ? 10 20)', '( f )', '(+ 2 x', ') 2 3', ')',
        ') (+ 1 2)', '(+', '(× 1', '(λ x', '(≜ y 10', '((λ x (+ x 1))',
        '(+ 2 3', '(? (= x 0) 1 0', '( f x y', '(', '((λ x x)',
        '(+ (× 2 3) 4', "", " "
    ]
    
    # Run all tests (commented out for development)
    # test_cases_results = [LL1.parsing_algorithm(n) for n in test_cases]
    # results = dict(zip(test_cases, test_cases_results))
    # with open("results.json", "w", encoding='utf-8') as f:
    #     json.dump(results, f, ensure_ascii=False, indent=4)
    
    # Individual test for debugging
    print(LexicalAnalyser.analyse('((+c0 0 00'))

if __name__ == "__main__":
    main()
