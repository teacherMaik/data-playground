import os
import glob
import gzip

# Path to the directory containing the log files
log_dir = 'logs'  # adjust as needed

# Get all access.log files in the directory
log_files = glob.glob(os.path.join(log_dir, '*.gz'))

print(log_files)
# Iterate and perform operations

all_lines = 0
for log_file in log_files:
    print(f"Processing: {log_file}")
    with gzip.open(log_file, 'rt') as f:
        count = 0
        for line in f:
            # Perform your operations here
            count += 1  # Example operation

    print(f"{log_file} has {count} lines")
    all_lines += count

print(all_lines)

