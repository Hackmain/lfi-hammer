
# LFI-Hammer

LFI-Hammer is a powerful Local File Inclusion (LFI) vulnerability scanner that crawls web pages and tests URLs with parameters for LFI vulnerabilities using a wordlist of payloads. It automates the process of detecting vulnerable URLs on a target site by scanning all links, detecting URLs with query parameters, and injecting potential LFI payloads.

## Features

- **Crawling:** Recursively crawls web pages to gather all links.
- **Link Detection:** Filters links that have query parameters for LFI testing.
- **Payload Injection:** Injects potential LFI payloads into URL parameters to identify vulnerabilities.
- **Wordlist Support:** Uses a customizable wordlist for LFI payload injection.
- **Command-Line Interface:** Simple CLI with arguments to specify target URL and wordlist.

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/hackmain/lfi-hammer.git
    ```

2. Navigate to the project directory:
    ```bash
    cd lfi-hammer
    ```

3. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

    **Requirements**:
    - `requests`
    - `BeautifulSoup4`
    - `tqdm`
    - `pyfiglet`
    - `termcolor`

4. (Optional) You can create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

## Usage

Run the tool by specifying the target URL (`-u`) and the LFI payload wordlist file (`-w`):

```bash
python lfi_hammer.py -u <target_url> -w <path_to_wordlist>
 ```
**Example:**
```bash
python lfi_hammer.py -u http://example.com -w wordlists/lfi.txt
 ```
## Arguments
-u, --url: The target URL you want to scan for LFI vulnerabilities.
-w, --wordlist: The path to the file containing LFI payloads to be used in the scan.

**Output:**
The tool will crawl the provided URL to gather links and check for parameters.
It will attempt to inject LFI payloads into URL parameters.
Vulnerable URLs will be marked as [VULNERABLE], and non-vulnerable URLs will be marked as [NOT VULNERABLE].

**Example Output**

 ```bash 
Crawling: http://example.com
Testing URL with parameters: http://example.com/index.php?file=test
[VULNERABLE] http://example.com/index.php?file=../../../../etc/passwd
[NOT VULNERABLE] http://example.com/index.php?file=invalid_payload
Customizing Wordlist
You can use your own wordlist for LFI payloads. The wordlist should be a plain text file with each payload on a new line. Example wordlist (wordlists/lfi.txt):
../../../../etc/passwd
../../../../etc/hosts
../../../../proc/self/environ
 ```
**Disclaimer**
This tool is intended for educational purposes only. Use it responsibly and only on targets you have permission to test.

Authors
@esefkh740_ on Instagram
Cyberhex.tech_


---

