import requests
import json
import os
from datetime import date
import sys


def dump_database(db_name):

    response = requests.get('https://ludotecaenlanube.com/server/db_ludo_api.php', params={"db": db_name})


    print("STATUS:", response.status_code)
    print("RESPONSE TEXT:")
    print(response.text)

    try:
        data = response.json()
        print("PARSED JSON:", data)
    except Exception as e:
        print("Error parsing JSON:", e)

    if data.get('success'):
        today = date.today().isoformat()
        folder = os.path.join(os.path.dirname(__file__), 'dumps')
        dump_filename = f"dump-{db_name}-{today}.json"
        file_path = os.path.join(folder, dump_filename)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data['data'], f, ensure_ascii = False, indent = 2)

        print(f"saved to {file_path}")
    else:
        print(f"HTTP Error: {response.status_code}")

# Entry Point
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_ludo_databases.py <db_name>")
        print("Example: python get_ludo_databases.py social")
        print("database names: jokes, biblioteca, accesslogs, social")
    else:
        db_name = sys.argv[1]
        dump_database(db_name)