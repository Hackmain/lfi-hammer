import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from tqdm import tqdm
import argparse
import os
from pyfiglet import Figlet
from termcolor import colored

# Function to print the title in big size and yellow color
def print_banner():
    # Create large ASCII art for "LFI-HAMMER"
    fig = Figlet(font='slant')
    lfi_hammer_title = fig.renderText('LFI-HAMMER')

    # Clear terminal
    os.system('clear')

    # Print title in yellow
    print(colored(lfi_hammer_title, 'yellow'))

    # Print "by man sec" below
    print(colored("by @esefkh740_ (instagram) @cyberhex.tech_", 'yellow'))


# Function to read the wordlist from a file
def load_wordlist(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file]
    except Exception as e:
        print(f"Error reading wordlist file: {e}")
        return []


# Function to crawl and gather all links from a page
def get_all_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()

        # Find all links in anchor tags
        for anchor in soup.find_all('a', href=True):
            link = anchor['href']
            # Resolve relative links
            full_link = urljoin(url, link)
            links.add(full_link)

        return links
    except Exception as e:
        print(f"Error crawling {url}: {e}")
        return set()


# Function to detect URLs with parameters
def detect_urls_with_parameters(links):
    param_urls = []
    for link in links:
        parsed_url = urlparse(link)
        if parsed_url.query:  # URL contains query parameters
            param_urls.append(link)
    return param_urls


# Function to detect LFI by injecting payloads from wordlist
def test_lfi_with_wordlist(url, wordlist):
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)

    # Only test URLs with parameters
    if params:
        for param in params:
            for payload in tqdm(wordlist, desc="Scanning LFI Payloads"):
                # Build the URL with the LFI payload
                vulnerable_url = url.replace(params[param][0], payload)
                try:
                    response = requests.get(vulnerable_url)
                    if "root:x:" in response.text or "127.0.0.1" in response.text or "localhost" in response.text:
                        print(f"[VULNERABLE] {vulnerable_url}")
                    else:
                        print(f"[NOT VULNERABLE] {vulnerable_url}")
                except Exception as e:
                    print(f"Error testing {vulnerable_url}: {e}")


# Function to recursively crawl and test for LFI using a wordlist
def crawl_and_test_lfi_with_wordlist(base_url, wordlist):
    visited = set()
    to_crawl = {base_url}

    while to_crawl:
        url = to_crawl.pop()
        if url not in visited:
            print(f"Crawling: {url}")
            visited.add(url)

            links = get_all_links(url)

            # Filter out external links
            links = {link for link in links if urlparse(link).netloc == urlparse(base_url).netloc}

            # Add new links to crawl
            to_crawl.update(links - visited)

            # Detect URLs with parameters
            param_urls = detect_urls_with_parameters(links)

            # Test the parameterized URLs for LFI using the wordlist
            for param_url in param_urls:
                print(f"Testing URL with parameters: {param_url}")
                test_lfi_with_wordlist(param_url, wordlist)


# Main function to parse command-line arguments and execute the scan
def main():
    # Print banner at the start
    print_banner()

    parser = argparse.ArgumentParser(description="LFI Scanner")
    parser.add_argument('-u', '--url', required=True, help='Target URL to scan')
    parser.add_argument('-w', '--wordlist', required=True, help='Path to the LFI payload wordlist')

    args = parser.parse_args()

    # Load the wordlist
    wordlist = load_wordlist(args.wordlist)

    if wordlist:
        # Start crawling and testing for LFI
        crawl_and_test_lfi_with_wordlist(args.url, wordlist)
    else:
        print("Failed to load the wordlist. Exiting...")


if __name__ == "__main__":
    main()
