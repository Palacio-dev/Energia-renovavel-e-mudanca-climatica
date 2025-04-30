import pandas as pd
from psycopg2._psycopg import connection

def load_anos_meses(cursor: connection):
    # Os datasets contém dados de anos entre 1960 e 2024
    for ano in range(1960, 2025):
        cursor.execute(f'INSERT INTO "ANO" (id) VALUES ({ano}) ON CONFLICT (id) DO NOTHING')
        for m in range(1, 13):
            cursor.execute(f'INSERT INTO "MES" (id, numero, id_ano) VALUES (\'{m}/{ano}\', {m}, {ano})')

def load_areas(cursor: connection):
    df = pd.read_csv('Datasets/energia.csv', usecols=['Area', 'Country code', 'Area type'])
    areas = df['Area'].unique()
    for area_nome in areas:
        linha_area = df[df['Area'] == area_nome]
        code = linha_area.iloc[0]['Country code']
        tipo = linha_area.iloc[0]['Area type']

        cursor.execute(f'INSERT INTO "AREA" (nome) VALUES (%s) RETURNING id', (area_nome,))
        area_id = cursor.fetchone()[0]

        if tipo == 'Country':
            cursor.execute('INSERT INTO "PAIS" (id, codigo, nome) VALUES (%s, %s, %s)',
                           (area_id, code, area_nome))
        elif tipo == 'Region':
            cursor.execute('INSERT INTO "GRUPO" (id, codigo, nome) VALUES (%s, %s, %s)',
                           (area_id, code, area_nome))


def load_tipo_energia(cursor: connection):
    df = pd.read_csv('Datasets/tipos_energia.csv', usecols=['Tipo', 'Renovavel'])

    for linha in df.itertuples():
        cursor.execute(f'INSERT INTO "TIPO_ENERGIA" (valor, renovavel) VALUES (%s, %s) RETURNING id', (linha[1], linha[2]))


def load_mudanca_temperatura(cursor: connection):
    pass


def load_geracao_energia(cursor: connection):
    pass


