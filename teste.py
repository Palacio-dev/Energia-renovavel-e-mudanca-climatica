import pandas as pd
import psycopg2


df = pd.read_csv('Datasets/energia.csv')
tipos = df['Area type'].unique()
print(tipos)
