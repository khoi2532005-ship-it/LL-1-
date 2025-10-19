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
        return types.get(symbol,ExpressionException())

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
                return int(self).value == int(other).value
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
    states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6'}  # define just to clarify group of states in total we are going to have
    alphabets = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+', '-', '×', '=', '?', 'λ', '≜', '(', ')', ' '}  # just define for the group of alphabets that we are going to include
    # transition = {('q0', [1,2,3,4,5,6,7,8,9]):'q1', ('q0', [0]): 'q2', ('q1', ['.']): 'q3', ('q2', ['.']): 'q3',('q3', [for i in range(10)]):'q3', ('q3', [' ']): 'q4', ('q4', ' '): 'q4',   }
    transition_0 = {'q0': 'q1', 'q1': 'q6', 'q2': 'q1', 'q3': 'q3', 'q4': 'q4', 'q5': 'q6', 'q6': 'q6'}  # checked
    transition_1_9 = {'q0': 'q3', 'q1': 'q6', 'q2': 'q3', 'q3': 'q3', 'q4': 'q4', 'q5': 'q6', 'q6': 'q6'}  # checked
    transition_op = {'q0': 'q5', 'q1': 'q6', 'q2': 'q5', 'q3': 'q6', 'q4': 'q6', 'q5': 'q6', 'q6': 'q6'}  # checked
    transition_space = {'q0': 'q0', 'q1': 'q0', 'q2': 'q2', 'q3': 'q0', 'q4': 'q0', 'q5': 'q0', 'q6': 'q6'}  # checked
    # transition_dot = {'q0':'q6', 'q1':'q6','q2':'q8','q3': 'q8', 'q4': 'q7', 'q5':'q7' ,'q6':'q6','q7':'q7', 'q8': 'q6'} #checked
    transition_a_z_A_Z = {'q0': 'q4', 'q1': 'q6', 'q2': 'q4', 'q3': 'q6', 'q4': 'q4', 'q5': 'q6', 'q6': 'q6'}
    transition_paren = {'q0': 'q2', 'q1': 'q2', 'q2': 'q2', 'q3': 'q2', 'q4': 'q2', 'q5': 'q2', 'q6': 'q6'}
    start_state = 'q0'
    accepting_state = ['q1', 'q3', 'q4', 'q5', 'q2', 'q0']  # list of accepting state where state of taking final movement should be landed in
    # error_state = ['q6', 'q7']# list of rejecting state

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
                    print(token_list)
                elif char == '0':
                    if current_state in ('q0', 'q2'):
                        
                        token_buffer = Token(char)
                        token_list.append(token_buffer)
                    else:
                        token_buffer.value += char
                    # print(token_list)
                    current_state = cls.transition_0[current_state]

            # elif char == '.':
            #     numlist += char
            #     prev_state = current_state
            #     current_state = cls.transition_dot[current_state]
            elif char.isalpha() and char != 'λ':
                # print(current_state)
                # print(char)
                if current_state in ('q0', 'q2'):
                    token_buffer = Token(char)
                    token_list.append(token_buffer)
                else:
                    token_buffer.value += char
                   
                current_state = cls.transition_a_z_A_Z[current_state]
                # print(token_list)

            elif char == ' ':
                
                current_state = cls.transition_space[current_state]
                # print(token_list)
            # Progress

            elif char in ['+', '−', '×', '=', '?', 'λ', '≜' ]:
                

                token_buffer = Token(char)
                token_list.append(token_buffer)
                current_state = cls.transition_op[current_state]
                # print(token_list)

            elif char in ['(', ')']:
                
                token_buffer = Token(char)
                token_list.append(token_buffer)
                current_state = cls.transition_paren[current_state]
                # print(token_list)
            else:
                print(char)
                current_state = 'q6'
            # Progress
            # else:
            #     raise NumberException()

            # Error states because we want to reject immediately when it reaches to dead state

            # if current_state == 'q6':
            #     raise ExpressionException(f'Wrong, the input is "{input}"')

        # Accept or reject the entire string when it end traversing or moving to see which states that the last symbol will end
        if current_state in cls.accepting_state:
            return token_list
        elif current_state in ['q1', 'q3']:
            raise NumberException(f'Wrong, the input is "{input}"')
        elif current_state in ['q6', 'q5', 'q2']:
            raise ExpressionException(f'Wrong, the input is "{input}"')
        elif current_state == 'q4':
            raise IdentifierException(f'Wrong, the input is "{input}"')

        # Complete this method.
        # You will probably need to add more to this class.


class LL1():
    # def __init__(self):
    #     self.token = LexicalAnalyser.analyse(token_input)
    #     self.new_token = self.parsing_algorithm(self.token)
    #     self.work = self.paren2list(self.new_token)
    
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
    
    def list2json(output):
        return [int(n.value) if n.type == TokenType.Number else str(n) for n in output]
        
    @classmethod    
    def parsing_algorithm(cls, input):
        input = LexicalAnalyser.analyse(input)      
        stack = []
        # stack.append("$")
        stack.append("S")
        empty = False
        input_index = 0
        print(input)
        def paren_expr():
            nonlocal input_index
            if input[input_index].type in [TokenType.Plus, TokenType.Minus, TokenType.Mult, TokenType.Equals]:
                stack.append('S')
                stack.append('S')
                stack.append(input[input_index].type)
                print(stack)
                print(input_index)
            elif input[input_index].type == TokenType.Conditional:
                stack.append('S')
                stack.append('S')
                stack.append('S')
                stack.append(input[input_index].type)
                print(stack)
                print(input_index)
            elif input[input_index].type == TokenType.Lambda:
                stack.append('S')
                stack.append(TokenType.Identifier)
                stack.append(TokenType.Lambda)
                print(stack)
                print(input_index)
            elif input[input_index].type == TokenType.Let:
                stack.append('S')
                stack.append('S')
                stack.append(TokenType.Identifier)
                stack.append(TokenType.Let)
                print(stack)
                print(input_index)
            elif input[input_index].type in [TokenType.Lparen, TokenType.Number, TokenType.Identifier]:
                stack.append('D')
                stack.append('S')
                print(stack)
                print(input_index)
            elif input[input_index].type == TokenType.Rparen:
                stack.append("wrong number of arguments")
                input_index = len(input)
        
        def expr_star():
            nonlocal input_index
            if input[input_index].type in [TokenType.Lparen, TokenType.Number, TokenType.Identifier]:
                stack.append('D')
                stack.append('S')
                print(stack)
                print(input_index)
            elif input[input_index].type ==TokenType.Rparen:
                return
                print(stack)
                print(input_index)
            else:
                stack.append("Wrong argument format")
                input_index = len(input)
                
                
                
            
        
        def expr():
            nonlocal input_index
            print(input[input_index])
            if input[input_index].type == TokenType.Lparen:
                stack.append(TokenType.Rparen)
                stack.append('M')
                stack.append(TokenType.Lparen)
                print(stack)
                print(input_index)
            elif input[input_index].type == TokenType.Number or input[input_index].type == TokenType.Identifier:
                stack.append(input[input_index].type)
                print(stack)
                print(input_index)
            elif input[input_index].type == TokenType.Rparen:
                stack.append("wrong number of arguments")
                input_index = len(input)
                print(stack)
                
                
                print(input_index)
            else:
                stack.append("Wrong argument format")
                input_index = len(input)
                
                print(stack)
                print(input_index)

                
            # elif input[input_index].type == TokenType.Rparen:
            #     raise Exception("Unmatch paren")
            # # def expr(input_index):
            # else:
            #     raise Exception("wrong format of arguments")
        
        # print(stack)
        while input_index < len(input):
            # print(input_index)
            if not stack:
                tok = input[input_index]
                if tok.type == TokenType.Lparen:
                    return ("missing closing paren")
                elif tok.type == TokenType.Rparen:
                    return ("unmatched paren")
                else:
                    return ("wrong number of arguments")
     
            elif stack[-1] == "S":
                # print(input_index)
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
                print()
                expr_star()
            # elif stack[-1] == "$":
            #     stack.pop()
            #     print(stack)
            elif isinstance(stack[-1], TokenType) and stack[-1] == input[input_index].type:
                stack.pop()
                input_index += 1
                print(stack)
                print(input_index)
            elif isinstance(stack[-1], TokenType) and stack[-1] != input[input_index].type :
                return("wrong number of arguments")
            
            
            
        print(stack)

        if input_index == len(input) and not stack:
            new_input = cls.list2json(input)
            
            new_input_json = cls.paren2list(new_input)
            print("String accepted")
            return new_input_json
        elif input_index == len(input) and stack:
            while stack:
                if isinstance(stack[-1], str):
                    if stack[-1] in ["S", "M","D"]:
                        stack.pop()
                        print(stack)
                    else:
                        return stack[-1]
                elif stack[-1] == TokenType.Lparen:
                    return("Unmatch paren")
                elif stack[-1] == TokenType.Rparen:
                    return("Missing closing paren")
                else:
                    return("unmatch expression")

        
        
        
            

    # def paren_expr(self, lookahead, lookahead_index):
    #     if isinstance(lookahead[lookahead_index], list):
    #         parsing_algorithm(lookahead[lookahead_index])
    #     elif lookahead[lookahead_index].type in [TokenType.Plus, TokenType.Minus, TokenType.Mult, TokenType.Equals]:
    #         stack.push(expr(lookahead, lookahead_index))
    #         stack.push(expr(lookahead, lookahead_index))
    #         stack.push(lookahead[lookahead_index].type)

    #     elif lookahead[lookahead_index].type == TokenType.Conditional:
    #         stack.push(expr(lookahead, lookahead_index))
    #         stack.push(expr(lookahead, lookahead_index))
    #         stack.push(expr(lookahead, lookahead_index))
    #         stack.push(TokenType.Conditional)

    #     elif lookahead.type == TokenType.Lambda:
    #         stack.push(expr(lookahead, lookahead_index))
    #         stack.push(expr(lookahead, lookahead_index))
    #         stack.push(TokenType.Identifier)
    #         stack.push(TokenType.Lambda)

    #     elif lookahead.type == TokenType.Let:
    #         stack.push(expr(lookahead, lookahead_index))
    #         stack.push(expr(lookahead, lookahead_index))
    #         stack.push(TokenType.Identifier)
    #         stack.push(TokenType.Let)

    #     elif lookahead.type in [TokenType.Number, TokenType.Identifier]:
    #         stack.push(expr(lookahead))

    # def expr(self, lookahead, lookahead_index):
    #     if isinstance(lookahead[lookahead_index], list):
    #         stack.append(paren_expr(lookahead, lookahead_index))
    #     elif lookahead[lookahead_index].type == TokenType.Number or lookahead[lookahead_index].type == TokenType.Identifier:
    #         stack.append(lookahead[lookahead_index].type)

    # def parsing_algorithm(self, token_list):
    #     token_list_tracker = 0
    #     stack = []
    #     stack.append('expr')
    #     while not token_list_tracker == len(token_list[token_list_tracker]):
    #         if (stack.peek()) == 'expr':
    #             expr(token_list, token_list_tracker)
    #         elif (stack.peek()).type() in TokenType:
    #             stack.pop()
    #             token_list_tracker + 1
    #         elif (stack.peek()) == 'paren_expr':
    #             paren_expr(token_list[token_list_tracker])


def main():
    test_cases = ['42', 'x  ', '(+ 2 3)', '(× x 5)', '(+ (× 2 3) 4)', '(? (= x 0) 1 0)', '(λ x x)', '(≜ y 10 y)', '((λ x (+ x 1)) 5)', '(+ 2',')  ', '(+ 2 3 4)', "42", "0", "123", "99999", "x", "y", "var", "abc", "XYZ", "longid", "(+ 1 2)", "(− 5 3)", "(× 2 3)", "(= 4 4)", "(+ 12 34)", "(× 9 8)", "(− 10 7)", "(= 99 99)", "(? (= 1 1) 2 3)", "(? (= 2 3) 4 5)", "(λ x x)", "(λ y (+ y 1))", "(λ z (× z z))", "(λ f (λ x (f x)))", "(≜ y 10 y)", "(≜ a 1 (+ a 2))", "(≜ b (λ x (+ x 1)) (b 5))", "((λ x (+ x 1)) 5)", "((λ y (× y y)) 4)", "((λ z (− z 1)) 10)", "(+ (× 2 3) 4)", "(− (× 2 5) (× 3 3))", "(× (+ 2 3) (− 7 2))", "(= (+ 1 2) 3)", "(= (× 2 3) 6)", "(? (= x 0) 1 0)", "(? (= x 1) 2 3)", "(? (= x y) x y)", "(? (= 1 2) 3 4)", "(λ x (+ x 2))", "(λ x (− x 2))", "(λ x (× x 2))", "(λ x (= x 2))", "(≜ id (λ x x) (id 5))", "(≜ const (λ x (λ y x)) ((const 1) 2))", "(≜ inc (λ n (+ n 1)) (inc 10))", "(≜ dbl (λ n (× n 2)) (dbl 7))", "(≜ fact (λ n (? (= n 0) 1 (× n fact (− n 1)))))", "(≜ sq (λ n (× n n)) (sq 9))", "(≜ add (λ a (λ b (+ a b))) ((add 3) 4))", "(≜ f (λ x (+ x 1)) (f (f 5)))", "(≜ f (λ x (× x x)) (f (f 2)))", "((λ f (f 10)) (λ x (+ x 2)))", "((λ f (λ x (f x))) (λ n (+ n 1)))", "((λ f (f 5)) (λ n (+ n 1)))", "(λ a (λ b (+ a b)))", "((λ a (λ b (+ a b))) 3 4)", "((λ a (λ b (+ a b))) 3)", "(+ (+ 1 2) 3)", "(× (× 2 3) 4)", "(= (= 1 1) (= 2 2))", "(+ (λ x x) 3)", "(? (= 1 1) (= 2 2) (= 3 3))", "(? (= 1 2) (+ 2 2) (× 3 3))", "(((λ x (λ y (+ x y))) 2) 3)", "(≜ sum2 (λ a (λ b (+ a b))) (sum2 3 4))", "(≜ sum2 (λ a (λ b (+ a b))) ((sum2 3) 4))", "(≜ a 1 (≜ b 2 (+ a b)))", "(≜ a (≜ b 2 b) a)", "(≜ f (λ x (+ x 1)) (≜ g (λ y (+ y 2)) (g (f 3))))", "(λ x (? (= x 0) 1 (× x x)))", "((λ x (? (= x 0) 1 (× x x))) 5)", "(λ f (λ x (f (f x))))", "((λ f (λ x (f (f x)))) (λ n (+ n 1)))", "((λ f (λ x (f (f (f x))))) (λ n (+ n 1)))", "((λ x (+ x 1)) ((λ x (+ x 1)) 0))", "(+ (× 2 (+ 3 4)) (− 10 1))", "(= (+ 1 2) (+ 3 0))", "(= (× 2 3) (× 1 6))", "(≜ triple (λ n (+ n (+ n n))) (triple 5))", "(? (= x x) (? (= y y) (? (= z z) 1 2) 3) 4)", "((λ x (x x)) (λ x (x x)))", "(≜ omega (λ x (x x)) (omega omega))", "((λ x (λ x (λ x x))) 1 2 3)", "(≜ F (λ fact (λ n (? (= n 0) 1 (× n (fact (− n 1)))))))", "(≜ id (λ x x) (= (id 5) 5))", "(≜ bool (λ x (λ y x)) bool)", "(≜ apply (λ f (λ x (f x))) (apply (λ y (+ y 1)) 3))", "(≜ comp (λ f (λ g (λ x (f (g x))))) ((comp (λ x (+ x 1))) (λ y (× y 2))) 10)", "(≜ church1 (λ f (λ x (f x))))", "(≜ church2 (λ f (λ x (f (f x)))))",]
    test_cases_results = [LL1.parsing_algorithm(n) for n in test_cases]
    # print(LexicalAnalyser.analyse('(≜ fact (λ n (? (= n 0) 1 (× n fact (− n 1)))))'))
    # print(LexicalAnalyser.analyse('x   '))
    # print(LexicalAnalyser.analyse('(+ 2 3)'))
    # print(LexicalAnalyser.analyse('(× x 5)'))
    # print(LexicalAnalyser.analyse('(+ (× 2 3) 4)'))
    # print(LexicalAnalyser.analyse('(? (= x 0) 1 0)'))
    # print(LexicalAnalyser.analyse('(λ x x)'))
    # print(LexicalAnalyser.analyse('(≜ y 10 y)'))
    # print(LexicalAnalyser.analyse('((λ x (+ x 1)) 5)'))
    # print(LL1.parsing_algorithm('(((- 2 3))(+ 2))('))
    #(≜ church1 (λ f (λ x (f x))))
    results = dict(zip(test_cases, test_cases_results))
    with open("results.json", "w", encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)



    # print(LL1.parsing_algorithm('(+ 2'))
    # print(LL1.parsing_algorithm(')'))
    # print(LL1.parsing_algorithm('(+ 2 3 4)'))


if __name__ == "__main__":
    main()