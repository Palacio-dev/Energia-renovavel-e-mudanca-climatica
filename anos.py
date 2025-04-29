import pandas as pd
import psycopg2


conn = psycopg2.connect(
    dbname="EnergiaTempDB",
    user="postgres",
    password="",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

'''
df = pd.read_csv('Datasets/teste.csv')
years = df['Year']
for year in years:
    cursor.execute('INSERT INTO "ANO" (id) VALUES (%s) ON CONFLICT (id) DO NOTHING', (year,))
'''

''' Os datasets contém dados de anos entre 1960 e 2024 '''
for x in range(1960, 2025):
    cursor.execute(f'INSERT INTO "ANO" (id) VALUES ({x}) ON CONFLICT (id) DO NOTHING')


conn.commit()
cursor.close()
conn.close()
