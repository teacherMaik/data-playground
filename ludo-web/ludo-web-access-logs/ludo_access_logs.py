import os
import glob
import gzip
import re
import hashlib
from user_agents import parse
import pandas as pd
from datetime import datetime

CACHE_FILE = 'access_cache.csv'
REFRESH = False

if os.path.exists(CACHE_FILE) and not REFRESH:
    print("loading data from cache")
    df = pd.read_csv(CACHE_FILE)

else:
    # Path to the directory containing the log files
    log_dir = 'logs'  # adjust as needed

    # Get all access.log files in the directory
    log_files = glob.glob(os.path.join(log_dir, '*.gz'))
    print(log_files)

    # Define the regex pattern
    pattern = re.compile(
        r'(?P<ip>\S+) - - \[(?P<timestamp>[^\]]+)\] '
        r'"(?P<method>\S+) (?P<path>\S+) (?P<protocol>[^"]+)" '
        r'(?P<status>\d{3}) (?P<size>\d+) (?P<host>\S+) '
        r'"(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)" "(?P<extra>[^"]*)"'
    )

    # Function to generate ua_hash
    def ua_hash(user_agent_string):
        return hashlib.sha256(user_agent_string.encode('utf-8')).hexdigest()

    # Function to extract user agent details
    def extract_user_agent_info(user_agent_string):
        ua = parse(user_agent_string)
        device = 'Mobile' if ua.is_mobile else 'Tablet' if ua.is_tablet else 'PC' if ua.is_pc else 'Other'
        os = ua.os.family + ' ' + ua.os.version_string
        browser = ua.browser.family + ' ' + ua.browser.version_string
        is_bot = ua.is_bot
        return device, os, browser, is_bot

    # Initialize an empty list to hold the parsed data
    log_data = []

    for log_file in log_files:
        print(f"reading {log_file}")
        with gzip.open(log_file, 'rt', encoding='utf-8') as file:

            for line in file:
                
                match = pattern.match(line)
                if match:
                    print("match found")
                    # Extract the basic data from the regex match
                    data = match.groupdict()
                    dt = datetime.strptime(data['timestamp'], "%d/%b/%Y:%H:%M:%S %z")
                    data['date'] = dt.strftime('%Y-%m-%d')

                    user_agent_string = data['user_agent']
                    
                    # Extract information from the user-agent string
                    device, os, browser, is_bot = extract_user_agent_info(user_agent_string)
                    
                    # Hash the user-agent
                    data['ua_hash'] = ua_hash(user_agent_string)
                    
                    # Add additional info
                    data['full_device_type'] = device
                    data['os_family_version'] = os
                    data['browser_family_version'] = browser
                    data['is_bot'] = is_bot
                    
                    # Add the data to the list
                    log_data.append(data)
                elif not match:
                    print("no match")

    # Create a DataFrame from the accumulated list of log data

    df = pd.DataFrame(log_data, columns=[
        'date', 'ip', 'method', 'path', 'protocol',
        'status', 'referer', 'ua_hash', 'full_device_type', 'os_family_version',
        'browser_family_version', 'is_bot', 'host'
    ])
    df.to_csv(CACHE_FILE, index=False)


print(df)
df = df.drop(columns = ['path'])
df = df.drop(columns=['protocol'])


print(df.groupby('referer'))
