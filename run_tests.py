# Test runner that imports from A2-lexical.py
# Make sure A2-lexical.py is in the same folder!

# Import everything from A2-lexical.py
# Note: If A2-lexical.py has dashes, we need to import it differently
import importlib.util
import sys

# Load A2-lexical.py as a module
spec = importlib.util.spec_from_file_location("a2_lexical", "A2-lexical.py")
a2_module = importlib.util.module_from_spec(spec)
sys.modules["a2_lexical"] = a2_module
spec.loader.exec_module(a2_module)

# Import the classes we need
LexicalAnalyser = a2_module.LexicalAnalyser
LL1 = a2_module.LL1

# Test cases with expected errors
def main():
    print("=" * 60)
    print("Test Cases - Error Detection")
    print("Using A2-lexical.py")
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
