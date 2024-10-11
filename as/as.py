import socket
import logging

AS_HOST = "0.0.0.0"
AS_PORT = 53533
DNS_RECORDS_FILE = "dns_records.txt"

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_record_to_file(record):
    with open(DNS_RECORDS_FILE, "a") as file:
        file.write(record + "\n")
    logging.info(f"Record saved: {record}")

def load_records_from_file():
    records = {}
    try:
        with open(DNS_RECORDS_FILE, "r") as file:
            for line in file:
                record = line.strip().split(',')
                if len(record) == 4:  # NAME, VALUE, TYPE, TTL
                    name, value, _type, ttl = record
                    records[name] = (value, _type, ttl)
    except FileNotFoundError:
        logging.warning("DNS records file not found. Starting with an empty record set.")
    return records

def handle_registration(data):
    logging.info(f"Received registration request: {data}")
    lines = data.split("\n")
    record_type = lines[0].split("=")[1]  # TYPE=A
    name = lines[1].split("=")[1]  # NAME=fibonacci.com
    value = lines[2].split("=")[1]  # VALUE=IP_ADDRESS
    ttl = lines[3].split("=")[1]  # TTL=10

    record = f"{name},{value},{record_type},{ttl}"
    save_record_to_file(record)
    return "Registration successful"

def handle_dns_query(data, records):
    logging.info(f"Received DNS query: {data}")
    lines = data.split("\n")
    record_type = lines[0].split("=")[1]  # TYPE=A
    name = lines[1].split("=")[1]  # NAME=fibonacci.com

    if name in records:
        value, _type, ttl = records[name]
        response = f"TYPE={_type}\nNAME={name}\nVALUE={value}\nTTL={ttl}\n"
        return response
    else:
        logging.error(f"Record not found for name: {name}")
        return "Record not found"

def start_as_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((AS_HOST, AS_PORT))

    logging.info(f"Authoritative Server running on {AS_HOST}:{AS_PORT}")

    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()

        logging.info(f"Received message from {addr}: {message}")
        
        # Load existing DNS records from the file
        records = load_records_from_file()

        if "VALUE" in message:
            # Handle registration request
            response = handle_registration(message)
        else:
            # Handle DNS query request
            response = handle_dns_query(message, records)

        # Send response
        sock.sendto(response.encode(), addr)
        logging.info(f"Sent response to {addr}: {response.strip()}")

if __name__ == "__main__":
    start_as_server()
