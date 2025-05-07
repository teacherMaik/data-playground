import os
import paramiko
from pathlib import Path
from stat import S_ISREG

def load_env(filepath="../.env"):

    with open(filepath) as f:

        for line in f:

            if line.strip() and not line.startswith("#"):

                key, _, value = line.strip().partition("=")
                os.environ[key] = value

load_env()

HOST = os.getenv("LUDO_SSH_HOST")
USER = os.getenv("LUDO_SSH_USER")
PASS = os.getenv("LUDO_SSH_PASS")

REMOTE_LOGS_DIR = '/logs'
LOCAL_LOGS_DIR = Path('ludo-web-access-logs') / "logs"
SCRIPT_DIR = Path(__file__).resolve().parent
LOCAL_TRAFFIC_DIR = SCRIPT_DIR.parent

print(f"connecting to {HOST}...")

transport = paramiko.Transport((HOST, 22))
transport.connect(username=USER, password=PASS)
sftp = paramiko.SFTPClient.from_transport(transport)

print(f"listing files from {REMOTE_LOGS_DIR}")
sftp.chdir(REMOTE_LOGS_DIR)
files = sftp.listdir_attr()

for file_attr in files:
    filename = file_attr.filename
    remote_mtime = file_attr.st_mtime
    remote_path = f"{REMOTE_LOGS_DIR}/{filename}"
    local_path = LOCAL_LOGS_DIR / filename

    if filename.startswith("access.log"):

        if local_path.exists():

            local_mtime = local_path.stat().st_mtime
            if abs(local_mtime - remote_mtime) < 1:

                print(f"skipping up-to-date {filename}")
                continue

        print(f"downloading {filename}")
        sftp.get(remote_path, str(local_path))
        local_path.touch()
        os.utime(local_path, (remote_mtime, remote_mtime))

    elif filename == "traffic.db":

        local_traffic_path = LOCAL_TRAFFIC_DIR / "traffic_berk.db"

        if local_traffic_path.exists():

            local_mtime = local_traffic_path.stat().st_mtime
            if abs(local_mtime - remote_mtime) < 1:

                print(f"skipping up-to-date {filename}")
                continue

        print(f"downloading {filename}")
        sftp.get(remote_path, str(local_traffic_path))
        local_traffic_path.touch()
        os.utime(local_traffic_path, (remote_mtime, remote_mtime))


sftp.close()
transport.close()
print("✅ SFTP connection closed.")
