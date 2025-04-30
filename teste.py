import pandas as pd
import psycopg2

df = pd.read_csv('Datasets/energia.csv', usecols=['Category', 'Variable'])
#variables = df['Variable'].unique()

tipos_energia = list(df[df['Category'] == 'Electricity generation']['Variable'].unique())
tipos_energia.remove('Total Generation')
print(tipos_energia)
