#ishita dwivedi (id2380)
from flask import Flask, request, jsonify
import socket
import requests
import logging

app = Flask(__name__)

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not all([hostname, fs_port, number, as_ip, as_port]):
        logging.error("Missing parameters in request")
        return jsonify({'error': 'Bad Request'}), 400

    try:
        fs_ip = socket.gethostbyname(hostname)
        logging.debug(f"Resolved {hostname} to {fs_ip}")

        response = requests.get(f'http://{fs_ip}:{fs_port}/fibonacci?number={number}&user_ip={request.remote_addr}')
        return jsonify({'fibonacci': response.json()}), response.status_code
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Allow external access
