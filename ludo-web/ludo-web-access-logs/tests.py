import re

pattern = re.compile(
    r'(?P<ip>\S+) - - \[(?P<timestamp>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) (?P<protocol>[^"]+)" '
    r'(?P<status>\d{3}) (?P<size>\d+) (?P<host>\S+) '
    r'"(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)" "(?P<extra>[^"]*)"'
)

log_line = '43.155.195.0 - - [12/May/2025:23:04:17 +0200] "GET / HTTP/1.1" 200 24155 www.ludotecaenlanube.com "http://www.ludotecaenlanube.com" "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1" "-"'

# Try to match the regex to the log line
match = pattern.match(log_line)

if match:
    print("match found")
    print(match.groupdict())  # Print the matched groups (data)
else:
    print("No match")

print(f"Raw log line: {repr(log_line)}")