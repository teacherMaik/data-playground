import pandas as pd
from load_data import get_sheet_by_gid

GID = 191174433

spreadsheet = get_sheet_by_gid(GID)
data = spreadsheet.get_all_values()
df = pd.DataFrame(data)
print(df)