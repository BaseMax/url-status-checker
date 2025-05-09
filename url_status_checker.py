import argparse
import requests
import time
from urllib.parse import urlparse

def get_url_status(url):
    """Checks the status code, redirection, and load time of the URL."""
    start_time = time.time()
    try:
        response = requests.get(url, allow_redirects=True)
        load_time = time.time() - start_time
        status_code = response.status_code
        final_url = response.url

        if url != final_url:
            redirection = f"Redirected to: {final_url}"
        else:
            redirection = "No redirection"

        return status_code, redirection, load_time

    except requests.exceptions.RequestException as e:
        return None, str(e), None


def check_urls(urls):
    """Checks a list of URLs."""
    for url in urls:
        print(f"Checking: {url}")
        status_code, redirection, load_time = get_url_status(url)

        if status_code is None:
            print(f"Error: {redirection}")
        else:
            print(f"Status Code: {status_code}")
            print(f"Redirection: {redirection}")
            print(f"Load Time: {load_time:.2f} seconds\n")


def main():
    """Main function to parse arguments and call the check_urls function."""
    parser = argparse.ArgumentParser(description="CLI tool to check status codes, redirections, and load times for a list of URLs.")
    parser.add_argument('urls', nargs='+', help="List of URLs to check.")
    args = parser.parse_args()

    check_urls(args.urls)


if __name__ == "__main__":
    main()
