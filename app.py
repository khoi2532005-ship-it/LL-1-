from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import sys
import os

# Import your parser
sys.path.append(os.path.dirname(__file__))
from A2_Final import LL1

app = Flask(__name__)
CORS(app)

# Read the HTML template
with open('index.html', 'r', encoding='utf-8') as f:
    HTML_TEMPLATE = f.read()

@app.route('/')
def index():
    """Serve the main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/parse', methods=['POST'])
def parse():
    """Parse a single expression"""
    try:
        data = request.get_json()
        expression = data.get('expression', '').strip()

        if not expression:
            return jsonify({
                'success': False,
                'error': 'Empty input'
            }), 400

        # Call YOUR actual parser
        result = LL1.parsing_algorithm(expression)

        # Check if result is an error (string) or success (list/int)
        is_error = isinstance(result, str)

        return jsonify({
            'success': not is_error,
            'input': expression,
            'result': result
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/parse_batch', methods=['POST'])
def parse_batch():
    """Parse multiple expressions at once"""
    try:
        data = request.get_json()
        expressions = data.get('expressions', [])

        results = {}
        for expr in expressions:
            expr = expr.strip()
            if expr:
                try:
                    result = LL1.parsing_algorithm(expr)
                    is_error = isinstance(result, str)
                    results[expr] = {
                        'success': not is_error,
                        'result': result
                    }
                except Exception as e:
                    results[expr] = {
                        'success': False,
                        'error': str(e)
                    }

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 70)
    print("🐍 LL(1) Parser Web Application")
    print("=" * 70)
    print("Server running at: http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 70)
    app.run(debug=True, host='0.0.0.0', port=5000)
