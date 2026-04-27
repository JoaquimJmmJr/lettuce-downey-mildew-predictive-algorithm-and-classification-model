import pandas as pd

df = pd.read_csv("dados_sensores.csv", sep=";", encoding="utf-8-sig")
df.columns = df.columns.str.strip().str.lower()

# --------------- Detecta automaticamente o nome das colunas --------------- #
def encontrar_coluna(df, candidatos):
    for nome in candidatos:
        if nome in df.columns:
            return nome
    raise KeyError(f"Nenhuma dessas colunas foi encontrada: {candidatos}\nColunas disponíveis: {df.columns.tolist()}")

col_temp     = encontrar_coluna(df, ["temp", "temperatura", "temperature", "temp_c", "tmp"])
col_umidade  = encontrar_coluna(df, ["umidade", "humidity", "umid", "hum", "rh"])
col_ts       = encontrar_coluna(df, ["timestamp", "data", "datetime", "data_hora", "date"])

# print(f"Colunas identificadas → tempo: '{col_ts}' | temp: '{col_temp}' | umidade: '{col_umidade}'")

# --------------- Preparo --------------- #
df[col_ts] = pd.to_datetime(df[col_ts], dayfirst=True)
df = df.sort_values(col_ts).reset_index(drop=True)
janela = df[df[col_ts] >= df[col_ts].max() - pd.Timedelta(hours=24)].copy()     # Análise das últimas 24 horas em relação ao último timestamp do CSV

# --------------- Condição de risco --------------- #
janela["condicao"] = (
    (janela[col_umidade] > 90) &
    (janela[col_temp].between(10, 20))
)

# --------------- Blocos contínuos --------------- #
janela["grupo"] = (janela["condicao"] != janela["condicao"].shift()).cumsum()
blocos = janela[janela["condicao"]].groupby("grupo").size()                     # Só entra no groupby quem tem condicao == True

intervalo_min = 30
blocos_horas = blocos * (intervalo_min / 60)
max_horas_continuas = blocos_horas.max() if not blocos_horas.empty else 0       # Pega o maior bloco contínuo de risco nas últimas 24h, ou 0 se não houver blocos de risco

# --------------- Classificação --------------- #
if max_horas_continuas >= 6:
    risco = "ALTO 🔴"
elif max_horas_continuas >= 3:
    risco = "MÉDIO 🟡"
else:
    risco = "BAIXO 🟢"

# # --------------- Diagnóstico da janela analisada --------------- #
# print("=" * 60)
# print("DIAGNÓSTICO")
# print(f"  Total de linhas no CSV:       {len(df)}")
# print(f"  Período completo do CSV:      {df[col_ts].min()} → {df[col_ts].max()}")
# print(f"  Janela analisada (últimas 24h):{janela[col_ts].min()} → {janela[col_ts].max()}")
# print(f"  Linhas na janela:             {len(janela)}")
# print(f"  Intervalo médio entre leituras: {intervalo_min} min (configurado)")
# print(f"  Linhas em condição de risco:  {janela['condicao'].sum()}")
# print("=" * 60)

print(f"Horas contínuas em condição crítica: {max_horas_continuas:.1f}h")
print(f"Nível de risco de Míldio: {risco}")