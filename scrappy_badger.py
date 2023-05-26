import requests
import re
from bs4 import BeautifulSoup
import socks
import socket
import stem
from stem.control import Controller
import time
import json
import urllib3
import argparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
control_port = 9151  # Change this to match your Tor control port
password = 'your-passphrase'  # Change this to match your Tor control password
socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)  # Tor default port is 9150

def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

socket.socket = create_connection

def scrape_onion_url(url, keywords):
    with Controller.from_port(port=control_port) as controller:
        controller.authenticate(password=password)

        response = requests.get(url, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            data = extract_data(soup, keywords)
            output_file = 'output.json'
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            print("Error: Unable to fetch the webpage.")

def extract_data(soup, keywords):
    links = [a['href'] for a in soup.find_all('a', href=True)]
    usernames = [span.text for span in soup.find_all('span', {'class': 'username'})]
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, str(soup))
    ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    ip_addresses = re.findall(ip_pattern, str(soup))
    bitcoin_pattern = r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b'
    bitcoin_addresses = re.findall(bitcoin_pattern, str(soup))
    dates = [time['datetime'] for time in soup.find_all('time', {'datetime': True})]
    found_keywords = [keyword for keyword in keywords if keyword in str(soup).lower()]

    return {
        'Links': links,
        'Usernames': usernames,
        'Email addresses': emails,
        'IP addresses': ip_addresses,
        'Bitcoin addresses': bitcoin_addresses,
        'Dates and timestamps': dates,
        'Found keywords': found_keywords
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tor Onion Scraper')
    parser.add_argument('-u', '--url', help='The onion URL to scrape', default=os.getenv('URL'))
    parser.add_argument('-k', '--keywords', help='A comma-separated list of keywords', default=os.getenv('KEYWORDS'))
    args = parser.parse_args()

    keywords = [keyword.strip() for keyword in args.keywords.split(',')]
    scrape_onion_url(args.url, keywords)
