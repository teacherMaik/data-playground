import os
import glob
import gzip
import re
import pandas as pd

# Path to the directory containing the log files
log_dir = 'logs'  # adjust as needed

# Get all access.log files in the directory
log_files = glob.glob(os.path.join(log_dir, '*.gz'))

print(log_files)
# Iterate and perform operations

# Custom log pattern based on your sample
log_pattern = re.compile(
    r'(?P<ip>\S+) - - \[(?P<datetime>[^\]]+)\] '
    r'"(?P<method>\S+)\s(?P<url>\S+)\s(?P<protocol>[^"]+)" '
    r'(?P<status>\d{3}) (?P<size>\S+) (?P<host>\S+) '
    r'"(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)" "[^"]*"'
)

all_lines = 0
i = 0
entries = []

for log_file in log_files:
    print(f"Processing: {log_file}")
    with gzip.open(log_file, 'rt', encoding='utf-8') as f:
        count = 0

        if i == 0:
            for line in f:
                match = log_pattern.match(line)
                if match:
                    data = match.groupdict()
                    data['size'] = int(data['size']) if data['size'].isdigit() else 0
                    entries.append(data)
            i += 1
        else:           
            for line in f:
                # Perform your operations here
                count += 1  # Example operation
        
    print(f"{log_file} has {count} lines")
    all_lines += count

print(all_lines)

# Create DataFrame
df = pd.DataFrame(entries)

# Convert datetime field
df['datetime'] = pd.to_datetime(df['datetime'], format='%d/%b/%Y:%H:%M:%S %z')
df['date'] = df['datetime'].dt.date

# Optional: convert status to int
df['status'] = df['status'].astype(int)


# Preview
print(df.nunique())
print(df[df['method'] == 'POST'])
print(df[df['method'] == 'POST'].nunique())
print(df.groupby('method')[['method']].count())



print(df[df['method'] == 'POST']['user_agent'].value_counts())
