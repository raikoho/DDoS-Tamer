A flexible tool for monitoring and protecting against DDoS attacks with many options
![DDoS Tamer Banner](ddos-tamer.gif) 

**DDoS Tamer** is a powerful tool for monitoring and protecting against DDoS attacks, which allows you to check the availability of websites, monitor page size changes and ensure effective protection of your network.

---
## Contents

- [Review](#review)
- [Functions](#functions)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Configuration](#configuration)
- [Contribution](#contribution)

---

## Overview

DDoS Tamer helps detect suspicious activity on your websites, such as changes in page size and response to requests. You can configure monitoring to receive alerts about potential DDoS attacks.

## Functions

- **Response Monitoring**: Checks server response time.
- **Page Size Monitoring**: Tracks changes in the size of web pages.
- **Aviability Monitoring**: Checks web pages aviamility and status code.
- **Flexible configuration**: Customization of check intervals and notification options.
- **Logging**: Writing the results of checks to a file or outputting them to the terminal.

## Requirements

- Python 3.7 or later
- Libraries: `requests`, `argparse`, `colorama`

## Installation

1. Clone the repository:
 ```bash
 git clone https://github.com/yourusername/ddos-tamer.git
 ```

2. Go to the project directory:
 ```bash
 cd ddos-tamer
 ```

3. Install the necessary libraries:
 ```bash
 pip install -r requirements.txt
 ```

## Usage

-at, --answer-time : Maximum allowable response time (in seconds).
-rs, --resize : Check for page size changes (in kilobytes).
-ps, --page-size : Minimum page size for notification.
-i, --interval : Check interval (in seconds).
-o, --output : Output of results (success, error, all).
-f, --file : File with URL to monitor.
-l, --log : Log file.
-c, --count : Number of checks to complete.
-h, --help : Show help.

## Examples

python main.py -at 2 -i 10
python main.py -rs 500 -l log.txt
python main.py -ps 50 -i 10 -o success -f urls.txt -c 5

## Configuration

By default, the program uses "sites.txt" as a database of sites to be monitored.
There you should enter the URLs of the sites. For examples:
 ```bash
https://google.com
https://facebook.com
https://instagram.com
```
Or use the -f flag to specify your text file.

## Contribution

Contribution to the project is welcome! To make changes, please open a Pull Request or create an Issue if you have suggestions or problems.
