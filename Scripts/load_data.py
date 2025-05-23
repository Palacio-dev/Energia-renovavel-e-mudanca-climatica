'''
MC536 - Grupo 1
Este arquivo contém todas as funções que usamos para carregar os dados dos datasets para o banco.
'''

import pandas as pd
from psycopg2._psycopg import connection

# Carrega os anos e meses no banco de dados
# def load_anos_meses(cursor: connection):
#     # Os datasets contém dados de anos entre 1961 e 2024
#     # Por questões de simplicidade/performance, optamos por adicionar os anos e meses de forma "hardcoded"
#     # adicionamos o ano de 1960 para entender como se comportaria no DB
#     for ano in range(1960, 2025):
#         cursor.execute(f'INSERT INTO "ANO" (id) VALUES ({ano}) ON CONFLICT (id) DO NOTHING')
#         # pra cada ano, adiciona os 12 meses com id no formato m/yyyy
#         for m in range(1, 13):
#             cursor.execute(f'INSERT INTO "MES" (id, numero, id_ano) VALUES (\'{m}/{ano}\', {m}, {ano})')

# Carrega todas as AREAS, incluindo as heranças: País e Grupo
# OBS: não carrega as relações entre GRUPO e AREA
def load_areas(cursor: connection):
    df = pd.read_csv('Datasets/energia.csv', usecols=['Area', 'Country code', 'Area type'])

    # lista as áreas sem repetições
    areas = df['Area'].unique()

    for area_nome in areas:

        # encontra ocorrências da área
        linha_area = df[df['Area'] == area_nome]

        # separa código e tipo (país ou grupo) da área
        code = linha_area.iloc[0]['Country code']
        tipo = linha_area.iloc[0]['Area type']

        # inserta a área retornando o id
        cursor.execute(f'INSERT INTO "AREA" (nome) VALUES (%s) RETURNING id', (area_nome,))
        area_id = cursor.fetchone()[0]

        # carrega a linha na tabela de herança correspondente
        if tipo == 'Country':
            cursor.execute('INSERT INTO "PAIS" (id, codigo, nome) VALUES (%s, %s, %s)',
                           (area_id, code, area_nome))
        elif tipo == 'Region':
            cursor.execute('INSERT INTO "GRUPO" (id, codigo, nome) VALUES (%s, %s, %s)',
                           (area_id, code, area_nome))


# Carrega a tabela de tipos de energia a partir do dataset simplificado
def load_tipo_energia(cursor: connection):
    df = pd.read_csv('Datasets/tipos_energia.csv', usecols=['Tipo', 'Renovavel'])

    for linha in df.itertuples():
        cursor.execute(f'INSERT INTO "TIPO_ENERGIA" (valor, renovavel) VALUES (%s, %s) RETURNING id', (linha[1], linha[2]))


# Carrega as mudanças de temperatura já com seus respectivos meses/anos além da área
def load_mudanca_temperatura(cursor):
    #carrega apenas o necessário
    anos = list(range(1961, 2020))
    cols_anos = [f"Y{ano}" for ano in anos]
    df = pd.read_csv("Datasets/temperature_change.csv", encoding="ISO-8859-1",
                     usecols=["Area", "Months", "Element"] + cols_anos)

    # melt para long: cada linha vira um único ano
    df_long = df.melt(
        id_vars=["Area", "Months", "Element"],
        value_vars=cols_anos,
        var_name="Year",        # ex: "Y1961"
        value_name="Value"      # o valor naquele ano
    )

    # pivota para ter colunas separadas para os dois elementos
    df_pivot = (
        df_long
        .pivot_table(
            index=["Area", "Months", "Year"],
            columns="Element",
            values="Value"
        )
        .reset_index()
        # renomeia as colunas pro padrão do banco
        .rename(columns={
            "Temperature change": "mud_value",
            "Standard Deviation": "desvio_padrao",
            "Area": "area",
            "Months": "mes",
            "Year": "ano"
        })
    )
    month_name_to_num = {
    "January":   1,  "February":  2,  "March":     3,
    "April":     4,  "May":       5,  "June":      6,
    "July":      7,  "August":    8,  "September": 9,
    "October":  10,  "November": 11,  "December": 12
    }

    #mapa nome_area -> id
    cursor.execute('SELECT id,nome FROM "AREA"')
    area_map = {nome: id_ for id_, nome in cursor.fetchall()}

    for _, row in df_pivot.iterrows():
        mes_nome = row["mes"]
        if mes_nome not in month_name_to_num:
            continue  # pula trimestres ou categorias desconhecidas
        area_nome = row['area']
        if area_nome not in area_map:  
            continue
        id_area = area_map[area_nome]
        id_area = area_map[row['area']]
        mes = month_name_to_num[row['mes']]
        ano = int(row["ano"][1:])

        cursor.execute('INSERT INTO "MUD_TEMP" (mud_value, desvio_padrao, id_area, mes, ano) VALUES (%s, %s, %s, %s, %s)',
                       (row['mud_value'], row['desvio_padrao'], id_area, mes, ano))

# Carrega a tabela GERACAO_ENERGIA
def load_geracao_energia(cursor):

    # lê a tabela das areas para associar os IDs
    cursor.execute('SELECT id, nome FROM "AREA"')
    area_map = {nome: id_ for id_, nome in cursor.fetchall()}

    # lê a tabela de tipos de energia para associar os IDs
    cursor.execute('SELECT id, valor FROM "TIPO_ENERGIA"')
    tipo_map = {valor: id_ for id_, valor in cursor.fetchall()}

    # leitura do dataset
    usecols = [
        "Area", "Year", "Category", "Variable",
        "Unit", "Value"
    ]
    df = pd.read_csv(
        "Datasets/energia.csv",
        usecols=usecols,
        encoding="ISO-8859-1"
    )

    # filtra apenas as linhas de interesse (geração de enrgia e emissão de CO2)
    categorias = ["Electricity generation", "Power sector emissions"]
    df = df[df["Category"].isin(categorias)]

    # Remove as linhas com porcentagens e dados redundantes (como soma total etc.)
    df = df[~df["Unit"].str.contains("%", na=False)]
    df = df[df["Variable"].isin(tipo_map.keys())]

    # adiciona linha por linha no banco
    for _, row in df.iterrows():
        area = row["Area"]
        ano  = int(row["Year"])
        var  = row["Variable"]
        unit = row["Unit"]
        val  = float(row["Value"])

        if area not in area_map:
            continue

        id_area = area_map[area]
        id_tipo = tipo_map[var]

        # se a cetgoria for geração enregia, cria uma linha no banco
        if row["Category"] == "Electricity generation":
            unidade_ger = unit
            valor_ger   = val

            # INSERT
            sql = """
                INSERT INTO "GERACAO_ENERGIA"
                    (unidade_geracao, valor_geracao,
                    id_area,          ano,
                    id_tipo)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(
                sql,
                (
                    unidade_ger,
                    valor_ger,
                    id_area,
                    ano,
                    id_tipo
                )
            )
        # se a categoria for emissão, dá update na linha no banco que já existe para a AREA/ANO
        # obs: o csv do dataset segue o padrão de que a geração vem antes da emissão
        else:
            unidade_emi = unit
            valor_emi   = val

            # encontra o id da linha correspondente (pais e ano)
            cursor.execute('SELECT id FROM "GERACAO_ENERGIA" WHERE id_area = %s AND ano = %s AND id_tipo = %s', 
                           (id_area, ano, id_tipo))
            id_row = cursor.fetchone()[0]

            # UPDATE
            sql = """
                UPDATE "GERACAO_ENERGIA"
                SET "valor_emissao" = %s,
                    "unidade_emissao" = %s
                WHERE id = %s;
            """
            cursor.execute(
                sql,
                (
                    valor_emi,
                    unidade_emi,
                    id_row
                )
            )

# Carrega as relações entre país e grupo a partir do dataset energia.csv
def load_pais_grupo(cursor):
    #lê só as colunas relevantes
    usecols = ["Area", "EU", "OECD", "G20", "G7", "ASEAN"]
    df = pd.read_csv(
        "Datasets/energia.csv",
        usecols=usecols,
        encoding="ISO-8859-1"
    )
    #monta lookup de países
    cursor.execute('SELECT id, nome FROM "AREA"')
    area_map = {nome: id_ for id_, nome in cursor.fetchall()}

    #monta lookup de grupos
    cursor.execute('SELECT id, nome FROM "GRUPO"')
    
    grupo_map = {nome: id_ for id_, nome in cursor.fetchall()}

    sql = """
    INSERT INTO "PAIS_GRUPO" ("Pais_id", "Grupo_id")
    VALUES (%s, %s)
    """
    
    grupos = ["EU", "OECD", "G20", "G7", "ASEAN"]
    inseridos = set()
    for _, row in df.iterrows():
        pais = row["Area"]
        if pais not in area_map:
            continue
        Pais_id = area_map[pais]
        for grp in grupos:
            flag = float(row[grp]) if pd.notna(row[grp]) else 0.0
            if flag > 0:
                #se o grupo existir no mapa, insere
                Grupo_id = grupo_map.get(grp)
                if Grupo_id is not None:
                    par = (Pais_id, Grupo_id)
                    if par not in inseridos:
                        cursor.execute(sql, (Pais_id, Grupo_id))
                        inseridos.add(par)
