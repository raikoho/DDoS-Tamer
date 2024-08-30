![DDoS Tamer Banner](ddos-tamer.gif) 

**DDoS Tamer** is a powerful tool for monitoring and protecting against DDoS attacks or checking, which allows you to check the availability of an infinite number of websites, status code, monitor page size changes and ensure effective protection of your network.

This program is designed to use various functions and parameters to make checking the availability or load or changes of many websites at once comfortable and automatic. And also uses a logging and notification system to report a problem.

## 📖 Overview

DDoS Tamer helps detect suspicious activity on your websites, such as changes in page size and response to requests. You can configure monitoring to receive alerts about potential DDoS attacks.

## 🖥️ Functions

- **Response Monitoring**: Checks server response time.
- **Page Size Monitoring**: Tracks changes in the size of web pages.
- **Aviability Monitoring**: Checks web pages aviamility and status code.
- **Flexible configuration**: Customization of check intervals and notification options.
- **Logging**: Writing the results of checks to a file or outputting them to the terminal.

## ⚠️ Requirements

- Python 3.7 or later
- Libraries: `requests`, `argparse`, `colorama`

## 📝 Installation

1. Clone the repository:
 ```bash
 git clone https://github.com/raikoho/DDoS-Tamer.git
 ```

2. Go to the project directory:
 ```bash
 cd DDoS-Tamer
 ```

3. Install the necessary libraries:
 ```bash
 pip install -r requirements.txt
 ```

## 🚀 Usage

### Main options

| Parameter | Description |


| `-h`, `--help` | Show help. |

| `-at`, `--answer-time` | The maximum allowable response time (in seconds). |

| `-rs`, `--resize` | Checking for page size changes (in kilobytes). |

| `-ps`, `--page-size` | Minimum page size for notification. |

| `-sc`, `--status-code` | Page output depending on the status code. For example, 403, 404, 200, etc. |


### Second options

| Parameter | Description |


| `-i`, `--interval` | Check interval (in seconds). |

| `-c`, `--count` | Number of checks to complete. |

### Additional options

| Parameter | Description |


| `-o`, `--output` | Output of results (`success`, `error`, `all`). |

| | `success' - there are fewer responses than the specified number (matches the condition). |

| | `error' - more answers than the specified number (does not meet the condition). |

| | `all' - all answers. |

### Output/Input options

| `-f`, `--file` | File with URL for monitoring. |

| `-l`, `--log` | Log file.


## 🔢 Examples

List websites that take less than 2 seconds to load overall. With regularity every 10 seconds. And the total number of checks - 5 times:
```bash
python ddos-tamer.py -at 2 -i 10 -o success -c 5
```

Display websites with periodic changes with a size difference greater than 400 KB. With regularity every 10 seconds. And the total number of checks - 5 times. With output of results to a text file.
```bash
python ddos-tamer.py -rs 400 -i 10 -o error -c 5 -l log.txt
```

This example will only display pages (websites) that are less than or equal to 50 KB if you use the -o success option. With regularity every 15 seconds. And the total number of checks is 10 times. With reading sites from own text file.
```bash
python ddos-tamer.py -ps 50 -i 15 -o success -f urls.txt -c 10
```

Returns all websites that do not satisfy the condition that the page returns a "200" or "400" code. Instead, it displays all answers except those specified. With regularity every 15 seconds. And the total number of checks - infinity.
```bash
python ddos-tamer.py -f sites.txt -l ddos_log.txt -sc 200 -i 15 -o error
```

## 📏 Configuration

By default, the program uses "sites.txt" as a database of sites to be monitored.
There you should enter the URLs of the sites. For examples:
 ```bash
https://google.com
https://facebook.com
https://instagram.com
```
Or use the -f flag to specify your text file.

## 💡 Contribution

Contribution to the project is welcome! To make changes, please open a Pull Request or create an Issue if you have suggestions or problems.
