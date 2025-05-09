# URL Status Checker

A simple CLI tool to check the status codes, redirections, and load times for a list of URLs.

## Features

- Check the HTTP status code for each URL.
- Detect if the URL is redirected and where it redirects.
- Measure the load time for the URL to fully load.

## Testing

```bash
$ python3 url_status_checker.py https://www.google.com https://www.nonexistentdomain.abc --verbose --json-output --output results.json
```

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/BaseMax/url-status-checker.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script with one or more URLs as arguments:

```bash
python url_status_checker.py https://www.google.com https://www.example.com
```

## Example Output

```bash
Checking: https://www.google.com
Status Code: 200
Redirection: No redirection
Load Time: 0.58 seconds

Checking: https://www.example.com
Status Code: 301
Redirection: Redirected to: https://example.com/
Load Time: 0.35 seconds
```

### License

MIT License
