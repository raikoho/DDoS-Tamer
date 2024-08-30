import time
import requests
from datetime import datetime
import os
import argparse
from termcolor import colored
import signal
import sys


# Function for processing the interrupt signal (Ctrl+C)
def signal_handler(sig, frame):
    print(colored("\nProgram interrupted. Exiting gracefully...", "yellow"))
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def print_banner():
    banner = """
  ________________________________
 /         DDoS Tamper           /|
|   _______  _______  _______   | |
|  |  site || site  || site  |  | |
|  |_______||_______||_______|  | |
|                               | |
|  [#######]  [#####]           | |
| version 1.0 by Bohdan Misonh  | |
|_______________________________|/
    """
    print(colored(banner, "cyan", attrs=["bold"]))
    print(colored("Welcome to the DDoS Tamper - powerful DDoS Monitoring Tool!\n", "magenta", attrs=["bold"]))


def read_sites(file_path):
    """Reads website URLs from a text file."""
    with open(file_path, 'r') as file:
        sites = [line.strip() for line in file.readlines()]
    return sites


def check_response_time(site, threshold):
    """Tests site response time."""
    try:
        response = requests.get(site, timeout=10)
        response_time = response.elapsed.total_seconds()
        if response_time > threshold:
            return False, f"{response_time} seconds"
        return True, response_time
    except requests.exceptions.RequestException:
        return False, "No response"


def check_page_size_diff(site, previous_size, diff_threshold=1000):
    """Checks for page resizing with diff_threshold tolerance in bytes."""
    try:
        response = requests.get(site, timeout=10)
        current_size = len(response.content)
        if previous_size is not None:
            size_diff = abs(current_size - previous_size)
            if size_diff > diff_threshold:
                return False, f"Significant page size change: {current_size} bytes (diff: {size_diff} bytes)"
        return True, current_size
    except requests.exceptions.RequestException:
        return False, None


def check_page_size_threshold(site, size_threshold_kb):
    """Checks if the page size exceeds the specified threshold (in kilobytes)."""
    try:
        response = requests.get(site, timeout=10)
        current_size_kb = len(response.content) / 1024  # from bytes to KB
        if current_size_kb > size_threshold_kb:
            return False, f"Page size: {current_size_kb:.2f} KB"
        return True, f"Page size: {current_size_kb:.2f} KB"
    except requests.exceptions.RequestException:
        return False, None


def check_status_code(site, expected_code):
    """Status code check:"""
    try:
        response = requests.get(site, timeout=10)
        if response.status_code != expected_code:
            return False, f"Unexpected status code: {response.status_code}"
        return True, response.status_code
    except requests.exceptions.RequestException:
        return False, None


def log_ddos_attack(site, issue, log_file, output_mode, success):
    """Writes information about suspicious activity to a log file."""
    message = f"{datetime.now()} - {issue} detected on {site}\n"

    # Logging or logging depending on the mode
    if output_mode == "error" and not success:
        write_log(log_file, message)
    elif output_mode == "success" and success:
        write_log(log_file, message)
    elif output_mode == "all":
        write_log(log_file, message)


def write_log(log_file, message):
    """Writes a message to the log file."""
    with open(log_file, 'a') as file:
        file.write(message)
    print(colored(message, "red") if "detected" in message else colored(message, "green"))


def main(file_path, log_file, check_interval, method, threshold, output_mode, max_checks):
    print_banner()
    sites = read_sites(file_path)
    page_sizes = {}
    checks_done = 0

    while True:
        for site in sites:
            if method == 'response_time':
                success, result = check_response_time(site, threshold)
            elif method == 'page_size_diff':
                success, result = check_page_size_diff(site, page_sizes.get(site), threshold)
                page_sizes[site] = result
            elif method == 'page_size_threshold':
                success, result = check_page_size_threshold(site, threshold)
            elif method == 'status_code':
                success, result = check_status_code(site, threshold)

            # We check whether the result meets the conditions for success or error
            if (output_mode == "success" and success) or \
                    (output_mode == "error" and not success) or \
                    output_mode == "all":
                log_ddos_attack(site, result, log_file, output_mode, success)

        checks_done += 1
        if max_checks and checks_done >= max_checks:
            print(colored(f"Max checks reached ({max_checks}). Exiting...", "yellow"))
            break

        print(colored(f"Waiting for {check_interval} seconds...", "cyan"))
        time.sleep(check_interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=colored("DDoS Attack Monitoring Tool", "green", attrs=["bold"]))

    # main options
    parser.add_argument("-f", "--file", type=str, default="sites.txt", help="Path to the file with list of sites")
    parser.add_argument("-l", "--log", type=str, default="ddos_log.txt", help="Path to the log file")

    # Inspection methods
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-at", "--answer-time", type=float, help="Threshold for response time (in seconds)")
    group.add_argument("-rs", "--page-size-diff", nargs="?", const=True, type=int,
                       help="Enable page size change monitoring. Optionally, specify the difference threshold in KB.")
    group.add_argument("-ps", "--page-size-threshold", type=int,
                       help="Specify the threshold in KB. Alerts if page size is above this threshold.")
    group.add_argument("-sc", "--status-code", type=int, help="Expected HTTP status code")

    # Additional options
    parser.add_argument("-i", "--interval", type=int, default=300, help="Interval between checks (in seconds)")
    parser.add_argument("-o", "--output", choices=["success", "error", "all"], default="error",
                        help="Output mode: 'success' for successful checks, 'error' for failed checks, 'all' for both")
    parser.add_argument("-c", "--count", type=int, help="Number of checks to perform before stopping")

    args = parser.parse_args()

    # Definition of the verification method
    if args.answer_time:
        method = 'response_time'
        threshold = args.answer_time
    elif args.page_size_diff is not None:
        method = 'page_size_diff'
        threshold = args.page_size_diff * 1024 if isinstance(args.page_size_diff,
                                                             int) else 1000  # Standard deviation 1 kilobyte
    elif args.page_size_threshold:
        method = 'page_size_threshold'
        threshold = args.page_size_threshold
    elif args.status_code:
        method = 'status_code'
        threshold = args.status_code

    # Starting the main monitoring
    main(args.file, args.log, args.interval, method, threshold, args.output, args.count)
