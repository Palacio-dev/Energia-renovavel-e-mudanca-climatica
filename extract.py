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


def load_mudanca_temperatura(cursor):
    # 1) carrega apenas o necessário
    anos = list(range(1961, 2020))
    cols_anos = [f"Y{ano}" for ano in anos]
    df = pd.read_csv("Datasets/temperature_change.csv", encoding="ISO-8859-1",
                     usecols=["Area", "Months", "Element"] + cols_anos)

    # 2) melt para long: cada linha vira um único ano
    df_long = df.melt(
        id_vars=["Area", "Months", "Element"],
        value_vars=cols_anos,
        var_name="Year",        # ex: "Y1961"
        value_name="Value"      # o valor naquele ano
    )

    # 3) pivota para ter colunas separadas para os dois elementos
    df_pivot = (
        df_long
        .pivot_table(
            index=["Area", "Months", "Year"],
            columns="Element",
            values="Value"
        )
        .reset_index()
        # opcional: renomeia as colunas pro padrão do seu banco
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

    # 1.1) mapa nome_area -> id
    cursor.execute('SELECT id,nome FROM "AREA"')
    area_map = {nome: id_ for id_, nome in cursor.fetchall()}

    # 1.2) mapa (numero_mes, ano) -> id_mes
    cursor.execute('SELECT id, numero, id_ano FROM "MES"')
    month_map = {
        (numero, id_ano): id_
        for id_, numero, id_ano in cursor.fetchall()
    }
    for _, row in df_pivot.iterrows():
        mes_nome = row["mes"]
        if mes_nome not in month_name_to_num:
            continue  # pula trimestres ou categorias desconhecidas
        area_nome = row['area']
        if area_nome not in area_map:  
            continue
        id_area = area_map[area_nome]
        numero_mes = month_name_to_num[mes_nome]
        id_area = area_map[row['area']]
        numero_mes = month_name_to_num[row['mes']]
        ano = int(row["ano"][1:])
        id_mes = month_map[(numero_mes, ano)]

        cursor.execute('INSERT INTO "MUD_TEMP" (mud_value, desvio_padrao, id_area, id_mes, id_ano) VALUES (%s, %s, %s, %s, %s)',
                       (row['mud_value'], row['desvio_padrao'], id_area, id_mes, ano))
        


def load_geracao_energia(cursor):
    # 1) lê só as colunas que interessam
    usecols = [
        "Area", "Year", "Category", "Variable",
        "Unit", "Value"
    ]
    df = pd.read_csv(
        "Datasets/energia.csv",
        usecols=usecols,
        encoding="ISO-8859-1"
    )

    # 2) filtra só Electricity generation e Power sector emissions
    categorias = ["Electricity generation", "Power sector emissions"]
    df = df[df["Category"].isin(categorias)]
    # descarta linhas de porcentagem
    df = df[~df["Unit"].str.contains("%", na=False)]

    # 3) carrega os mapas de lookup em memória
    cursor.execute('SELECT id, nome FROM "AREA"')
    area_map = {nome: id_ for id_, nome in cursor.fetchall()}

    cursor.execute('SELECT id, valor FROM "TIPO_ENERGIA"')
    tipo_map = {valor: id_ for id_, valor in cursor.fetchall()}

    # 4) prepara o INSERT
    sql = """
    INSERT INTO "GERACAO_ENERGIA"
      (unidade_geracao, valor_geracao,
       unidade_emissao,  valor_emissao,
       id_area,          id_ano,
       id_tipo)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        area = row["Area"]
        ano  = int(row["Year"])
        var  = row["Variable"]
        unit = row["Unit"]
        val  = float(row["Value"])

        # pula áreas não cadastradas
        if area not in area_map:
            continue
        # pula tipos não cadastrados
        if var not in tipo_map:
            continue

        id_area = area_map[area]
        id_ano  = ano
        id_tipo = tipo_map[var]

        # decide onde vai o valor: geração ou emissão
        if row["Category"] == "Electricity generation":
            unidade_ger = unit
            valor_ger   = val
            unidade_emi = None
            valor_emi   = None
        else:  # Power sector emissions
            unidade_ger = None
            valor_ger   = None
            unidade_emi = unit
            valor_emi   = val

        cursor.execute(
            sql,
            (
                unidade_ger,
                valor_ger,
                unidade_emi,
                valor_emi,
                id_area,
                id_ano,
                id_tipo
            )
        )


def load_pais_grupo(cursor):
    # 1) lê só as colunas relevantes
    usecols = ["Area", "EU", "OECD", "G20", "G7", "ASEAN"]
    df = pd.read_csv(
        "Datasets/energia.csv",
        usecols=usecols,
        encoding="ISO-8859-1"
    )

    # 2) monta lookup de países
    cursor.execute('SELECT id, nome FROM "AREA"')
    area_map = {nome: id_ for id_, nome in cursor.fetchall()}

    # 3) monta lookup de grupos
    cursor.execute('SELECT id, nome FROM "GRUPO"')
    # aqui assumimos que na tabela GRUPO a coluna 'valor' guarda strings como 'EU','G20',...
    grupo_map = {nome: id_ for id_, nome in cursor.fetchall()}

    # 4) prepara o INSERT
    sql = """
    INSERT INTO "PAIS_GRUPO" ("Pais_id", "Grupo_id")
    VALUES (%s, %s)
    """

    # 5) para cada linha, associa a cada grupo ativo
    grupos = ["EU", "OECD", "G20", "G7", "ASEAN"]
    inseridos = set()
    for _, row in df.iterrows():
        pais = row["Area"]
        if pais not in area_map:
            continue
        Pais_id = area_map[pais]

        for grp in grupos:
            # pode ser 0.0 / 1.0 ou 0/1 — trata tudo como float
            flag = float(row[grp]) if pd.notna(row[grp]) else 0.0
            if flag > 0:
                # se o grupo existir no mapa, insere
                Grupo_id = grupo_map.get(grp)
                if Grupo_id is not None:
                    par = (Pais_id, Grupo_id)
                    if par not in inseridos:
                        cursor.execute(sql, (Pais_id, Grupo_id))
                        inseridos.add(par)
