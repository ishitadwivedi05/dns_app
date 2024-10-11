#ishita dwivedi (id2380)
from flask import Flask, request, jsonify
import socket
import logging

app = Flask(__name__)

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)

def register_with_as(hostname, ip, as_ip, as_port):
    message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(message.encode(), (as_ip, as_port))
    logging.info(f"Registered with AS: {message.strip()}")

@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    if not all([hostname, ip, as_ip, as_port]):
        logging.error("Missing parameters in registration")
        return jsonify({'error': 'Bad Request'}), 400
    
    register_with_as(hostname, ip, as_ip, as_port)
    return jsonify({'message': 'Registered successfully'}), 201

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    number = request.args.get('number')
    
    if not number.isdigit():
        return jsonify({'error': 'Bad format'}), 400
    
    x = int(number)
    fib_value = fibonacci_number(x)
    logging.info(f"Fibonacci calculated for {x}: {fib_value}")
    
    return jsonify({'fibonacci': fib_value}), 200

def fibonacci_number(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)  # Allow external access
