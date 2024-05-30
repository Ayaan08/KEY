from flask import Flask, jsonify
import random
import string

app = Flask(__name__)

codes = {}

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

@app.route('/generate-code', methods=['GET'])
def get_code():
    code = generate_code()
    while code in codes:
        code = generate_code()
    codes[code] = False  # Code is not used
    return jsonify({'code': code})

@app.route('/check-code/<code>', methods=['GET'])
def check_code(code):
    if code in codes and not codes[code]:
        codes[code] = True  # Mark as used
        return jsonify({'valid': True})
    return jsonify({'valid': False})

if __name__ == '__main__':
    app.run(port=5000)
