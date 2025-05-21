import pandas as pd

df = pd.read_csv('Datasets/energia.csv', usecols=['Category', 'Subcategory', 'Variable'])

tipos_energia = df[(df['Category'] == 'Electricity generation') & (df['Subcategory'] == 'Fuel')]['Variable'].unique()

ren = [t not in ['Coal', 'Gas', 'Other Fossil', 'Nuclear'] for t in tipos_energia]
tabela = zip(tipos_energia, ren)
pd.DataFrame(tabela).to_csv('Datasets/tipos_energia.csv', index=False, header=['Tipo', 'Renovavel'])
