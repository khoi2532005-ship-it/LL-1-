import random
import json

# Random Test Case Generator for LL(1) Parser
# Generates valid and invalid expressions with Unicode operators

class TestCaseGenerator:
    """
    Generates random test cases for the LL(1) parser with Unicode operators:
    + (plus), − (minus), × (multiply), = (equals), ? (conditional), λ (lambda), ≜ (let)
    """

    def __init__(self):
        self.operators = {
            'binary': ['+', '−', '×', '='],  # Need exactly 2 arguments
            'conditional': '?',               # Needs exactly 3 arguments
            'lambda': 'λ',                    # Needs identifier and expression
            'let': '≜'                        # Needs identifier, value, and expression
        }
        self.identifiers = ['x', 'y', 'z', 'a', 'b', 'c', 'n', 'f', 'val', 'sum']

    def random_number(self):
        """Generate a random number (0-999)"""
        return str(random.randint(0, 999))

    def random_identifier(self):
        """Generate a random identifier"""
        return random.choice(self.identifiers)

    def random_binary_op(self):
        """Generate a random binary operator"""
        return random.choice(self.operators['binary'])

    def generate_valid_expression(self, depth=0, max_depth=3):
        """Generate a valid expression"""
        if depth >= max_depth or random.random() < 0.3:
            # Base case: return number or identifier
            if random.random() < 0.5:
                return self.random_number()
            else:
                return self.random_identifier()

        expr_type = random.choice(['binary', 'conditional', 'lambda', 'let', 'simple'])

        if expr_type == 'binary':
            op = self.random_binary_op()
            arg1 = self.generate_valid_expression(depth + 1, max_depth)
            arg2 = self.generate_valid_expression(depth + 1, max_depth)
            return f"({op} {arg1} {arg2})"

        elif expr_type == 'conditional':
            cond = self.generate_valid_expression(depth + 1, max_depth)
            then_expr = self.generate_valid_expression(depth + 1, max_depth)
            else_expr = self.generate_valid_expression(depth + 1, max_depth)
            return f"(? {cond} {then_expr} {else_expr})"

        elif expr_type == 'lambda':
            param = self.random_identifier()
            body = self.generate_valid_expression(depth + 1, max_depth)
            return f"(λ {param} {body})"

        elif expr_type == 'let':
            var = self.random_identifier()
            val = self.generate_valid_expression(depth + 1, max_depth)
            body = self.generate_valid_expression(depth + 1, max_depth)
            return f"(≜ {var} {val} {body})"

        else:  # simple
            if random.random() < 0.5:
                return self.random_number()
            else:
                return self.random_identifier()

    def generate_error_missing_paren(self):
        """Generate expression with missing closing parenthesis"""
        expr = self.generate_valid_expression(max_depth=2)
        # Remove random closing paren
        if ')' in expr:
            pos = expr.rfind(')')
            return expr[:pos]
        return "(+ 2 3"

    def generate_error_unmatched_paren(self):
        """Generate expression with unmatched parenthesis"""
        options = [
            ")",
            "))",
            ")))",
            f"){self.random_number()}",
            f") {self.random_identifier()}",
            f"){self.generate_valid_expression(max_depth=1)}("
        ]
        return random.choice(options)

    def generate_error_wrong_args(self):
        """Generate expression with wrong number of arguments"""
        op_type = random.choice(['binary', 'conditional', 'lambda', 'let'])

        if op_type == 'binary':
            op = self.random_binary_op()
            num_args = random.choice([0, 1, 3, 4])
            args = ' '.join([self.generate_valid_expression(max_depth=1) for _ in range(num_args)])
            return f"({op} {args})" if args else f"({op})"

        elif op_type == 'conditional':
            num_args = random.choice([0, 1, 2, 4])
            args = ' '.join([self.generate_valid_expression(max_depth=1) for _ in range(num_args)])
            return f"(? {args})" if args else "(?)"

        elif op_type == 'lambda':
            if random.random() < 0.5:
                return "(λ)"  # No args
            else:
                return f"(λ {self.random_identifier()})"  # Missing body

        else:  # let
            choices = [
                "(≜)",
                f"(≜ {self.random_identifier()})",
                f"(≜ {self.random_identifier()} {self.random_number()})",
            ]
            return random.choice(choices)

    def generate_test_cases(self, num_valid=20, num_errors=20):
        """Generate a mix of valid and error test cases"""
        test_cases = []

        # Generate valid cases
        print("Generating valid test cases...")
        for i in range(num_valid):
            expr = self.generate_valid_expression(max_depth=random.randint(1, 4))
            test_cases.append({
                'input': expr,
                'type': 'valid',
                'description': f'Valid expression {i+1}'
            })

        # Generate error cases
        print("Generating error test cases...")
        error_types = ['missing_paren', 'unmatched_paren', 'wrong_args']

        for i in range(num_errors):
            error_type = random.choice(error_types)

            if error_type == 'missing_paren':
                expr = self.generate_error_missing_paren()
                desc = 'Missing closing parenthesis'
            elif error_type == 'unmatched_paren':
                expr = self.generate_error_unmatched_paren()
                desc = 'Unmatched parenthesis'
            else:
                expr = self.generate_error_wrong_args()
                desc = 'Wrong number of arguments'

            test_cases.append({
                'input': expr,
                'type': 'error',
                'description': desc
            })

        # Shuffle the test cases
        random.shuffle(test_cases)
        return test_cases

    def save_test_cases(self, test_cases, filename='random_test_cases.txt'):
        """Save test cases to a file"""
        with open(filename, 'w', encoding='utf-8') as f:
            for i, tc in enumerate(test_cases, 1):
                f.write(f"# Test {i}: {tc['description']} ({tc['type']})\n")
                f.write(f"{tc['input']}\n\n")
        print(f"Saved {len(test_cases)} test cases to {filename}")

    def save_test_cases_json(self, test_cases, filename='random_test_cases.json'):
        """Save test cases to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(test_cases, f, indent=4, ensure_ascii=False)
        print(f"Saved {len(test_cases)} test cases to {filename}")

def main():
    print("="*60)
    print("Random Test Case Generator for LL(1) Parser")
    print("="*60)
    print()

    generator = TestCaseGenerator()

    # Generate test cases
    test_cases = generator.generate_test_cases(num_valid=30, num_errors=30)

    print()
    print("Sample generated test cases:")
    print("-"*60)
    for i, tc in enumerate(test_cases[:10], 1):
        print(f"{i}. [{tc['type'].upper()}] {tc['input']}")
    print(f"... and {len(test_cases) - 10} more")
    print()

    # Save to files
    generator.save_test_cases(test_cases, 'random_test_cases.txt')
    generator.save_test_cases_json(test_cases, 'random_test_cases.json')

    print()
    print("="*60)
    print(f"Total: {len(test_cases)} test cases generated")
    print("Files created:")
    print("  - random_test_cases.txt (readable format)")
    print("  - random_test_cases.json (JSON format)")
    print("="*60)

if __name__ == "__main__":
    main()
