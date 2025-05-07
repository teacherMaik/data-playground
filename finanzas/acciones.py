import pandas as pd
from load_data import get_sheet_by_gid

GID = 350985506

spreadsheet = get_sheet_by_gid(GID)
data = spreadsheet.get_all_values()
df_full = pd.DataFrame(data[1:], columns=data[0])
# print(df_full)

operation_cols = [
    "Miembro",
    "Valor",
    "Tipo",
    "Fecha",
    "Después de Gastos",
    "Titulos",
    "Precio ",
    "Gasto bolsa",
    "Impuestos",
    "Comisión Cambio Moneda"
    ]
df_operations = df_full[operation_cols]

# print(df_operations)

print(df_operations.groupby("Tipo")[["Tipo"]].count())



# print(df_operations)

num_cols_to_clean = ["Después de Gastos", "Precio ", "Gasto bolsa", "Comisión Cambio Moneda"]
df_operations[num_cols_to_clean] = df_operations[num_cols_to_clean].apply(
    lambda col: col.str.replace(r"[\s€]", "", regex = True)
    )

df_operations[num_cols_to_clean] = df_operations[num_cols_to_clean].apply(
    lambda col: col.str.replace(r".", "")
    )
df_operations[num_cols_to_clean] = df_operations[num_cols_to_clean].apply(
    lambda col: col.str.replace(r",", ".").astype(float)
    )

df_operations["Gastos Totales"] = df_operations["Gasto bolsa"] + df_operations["Comisión Cambio Moneda"]
print(df_operations)

