import pandas as pd
import psycopg2


df = pd.read_csv('Datasets/temperature_change.csv', encoding='ISO-8859-1')
print(df['Area'].unique())


# anos = list(range(1961, 2020))
# cols_anos = [f"Y{ano}" for ano in anos]
# df = pd.read_csv("Datasets/temperature_change.csv", encoding="ISO-8859-1",
#                     usecols=["Area", "Months", "Element"] + cols_anos)

# # 2) melt para long: cada linha vira um único ano
# df_long = df.melt(
#     id_vars=["Area", "Months", "Element"],
#     value_vars=cols_anos,
#     var_name="Year",        # ex: "Y1961"
#     value_name="Value"      # o valor naquele ano
# )

# df_pivot = (
#     df_long
#     .pivot_table(
#         index=["Area", "Months", "Year"],
#         columns="Element",
#         values="Value"
#     )
#     .reset_index()
#     # opcional: renomeia as colunas pro padrão do seu banco
#     .rename(columns={
#         "Temperature change": "mud_value",
#         "Standard Deviation": "desvio_padrao",
#         "Area": "area",
#         "Months": "mes",
#         "Year": "ano"
#     })
# )
# print(df_pivot)

# df = pd.read_csv('Datasets/temperature_change.csv', usecols=['Y1961'], encoding='ISO-8859-1')
#variables = df['Variable'].unique()
# tipos_energia = list(df[df['Category'] == 'Electricity generation']['Variable'].unique())
# tipos_energia.remove('Total Generation')
# print(tipos_energia)

# df
