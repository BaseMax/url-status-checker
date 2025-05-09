import argparse
import requests
import time
import concurrent.futures
import json
from urllib.parse import urlparse

def get_url_status(url, timeout, headers, proxy, retries, retry_delay):
    """Checks the status code, redirection, and load time of the URL."""
    start_time = time.time()
    attempt = 0

    while attempt < retries:
        try:
            response = requests.get(url, allow_redirects=True, timeout=timeout, headers=headers, proxies=proxy)
            load_time = time.time() - start_time
            status_code = response.status_code
            final_url = response.url

            if url != final_url:
                redirection = f"Redirected to: {final_url}"
            else:
                redirection = "No redirection"

            return status_code, redirection, load_time, response.headers

        except requests.exceptions.RequestException as e:
            attempt += 1
            if attempt < retries:
                time.sleep(retry_delay)
            else:
                return None, str(e), None, None
    return None, "Max retries reached", None, None


def check_urls(urls, timeout, verbose, output_file, user_agent, proxy, status_filter, json_output, retries, retry_delay):
    """Checks a list of URLs."""
    headers = {'User-Agent': user_agent}
    
    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_url_status, url, timeout, headers, proxy, retries, retry_delay): url for url in urls}
        
        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            status_code, redirection, load_time, headers = future.result()

            result = {"URL": url}
            if status_code is None:
                result["Error"] = redirection
            else:
                result["Status Code"] = status_code
                result["Redirection"] = redirection
                result["Load Time"] = f"{load_time:.2f} seconds"
                if verbose and headers:
                    result["Response Headers"] = dict(headers)

            if status_filter and status_code != status_filter:
                continue
            
            results.append(result)
            print(result)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as file:
            if json_output:
                json.dump(results, file, indent=4)
            else:
                for res in results:
                    file.write(f"{res}\n")
        print(f"\nResults saved to {output_file}")


def main():
    """Main function to parse arguments and call the check_urls function."""
    parser = argparse.ArgumentParser(description="CLI tool to check status codes, redirections, and load times for a list of URLs.")
    
    parser.add_argument('urls', nargs='+', help="List of URLs to check.")
    parser.add_argument('--timeout', type=int, default=10, help="Timeout for requests in seconds (default: 10).")
    parser.add_argument('--verbose', action='store_true', help="Show detailed response headers and additional information.")
    parser.add_argument('--output', type=str, help="Save results to a text or JSON file.")
    parser.add_argument('--user-agent', type=str, default="Mozilla/5.0", help="Custom User-Agent for requests.")
    parser.add_argument('--proxy', type=str, help="Proxy server to use (format: http://<proxy>:<port>).")
    parser.add_argument('--status-filter', type=int, help="Only show URLs with a specific status code (e.g., 404).")
    parser.add_argument('--json-output', action='store_true', help="Save output in JSON format.")
    parser.add_argument('--retries', type=int, default=3, help="Number of retries on failure (default: 3).")
    parser.add_argument('--retry-delay', type=int, default=2, help="Delay between retries in seconds (default: 2).")

    args = parser.parse_args()

    proxy = None
    if args.proxy:
        proxy = {"http": args.proxy, "https": args.proxy}

    check_urls(args.urls, args.timeout, args.verbose, args.output, args.user_agent, proxy, args.status_filter, args.json_output, args.retries, args.retry_delay)


if __name__ == "__main__":
    main()
