import pandas as pd
from pathlib import Path

print("=" * 60)
print("1. LEITURA INICIAL")
print("=" * 60)

# Procura o arquivo automaticamente
possiveis_caminhos = [
    Path("imoveis_bruto.csv"),
    Path("arquivos/imoveis_bruto.csv"),
    Path("dados/imoveis_bruto.csv"),
    Path(__file__).parent / "imoveis_bruto.csv",
    Path(__file__).parent / "arquivos" / "imoveis_bruto.csv",
    Path(__file__).parent / "dados" / "imoveis_bruto.csv",
]

arquivo = None

for caminho in possiveis_caminhos:
    if caminho.exists():
        arquivo = caminho
        break

if arquivo is None:
    print("\nERRO: arquivo imoveis_bruto.csv não encontrado.")
    print("\nArquivos encontrados na pasta atual:")
    for item in Path(".").iterdir():
        print("-", item)
    exit()

print(f"\nArquivo encontrado: {arquivo}")

df = pd.read_csv(arquivo)

print("\nDtypes:")
print(df.dtypes)

print("\nAusentes detectados automaticamente:")
antes = df.isna().sum()
print(antes)

print("\n" + "=" * 60)
print("2. INVESTIGAÇÃO DE VALORES DISFARÇADOS")
print("=" * 60)

for coluna in ["bairro", "condicao", "area_m2", "idade_anos"]:
    if coluna in df.columns:
        print(f"\n--- {coluna} ---")
        print(df[coluna].value_counts(dropna=False).head(20))

print("\nConversão de area_m2 para número:")

df["area_m2_num"] = pd.to_numeric(
    df["area_m2"],
    errors="coerce"
)

print(
    "Valores inválidos encontrados:",
    df["area_m2_num"].isna().sum()
)

print("\nConversão de idade_anos para número:")

df["idade_anos_num"] = pd.to_numeric(
    df["idade_anos"],
    errors="coerce"
)

print(
    "Valores inválidos encontrados:",
    df["idade_anos_num"].isna().sum()
)

print("\n" + "=" * 60)
print("3. RELENDO COM NA_VALUES")
print("=" * 60)

valores_ausentes = [
    "N/D",
    "?",
    "s/i"
]

df_limpo = pd.read_csv(
    arquivo,
    na_values=valores_ausentes
)

df_limpo["area_m2"] = pd.to_numeric(
    df_limpo["area_m2"],
    errors="coerce"
)

df_limpo["idade_anos"] = pd.to_numeric(
    df_limpo["idade_anos"],
    errors="coerce"
)

# idade negativa é erro de qualidade
df_limpo.loc[
    df_limpo["idade_anos"] < 0,
    "idade_anos"
] = pd.NA

depois = df_limpo.isna().sum()

print("\nAusentes ANTES:")
print(antes)

print("\nAusentes DEPOIS:")
print(depois)

print("\nDiferença:")
print(depois - antes)

print("\n" + "=" * 60)
print("4. PROPORÇÃO DE AUSENTES EM idade_anos POR TIPO")
print("=" * 60)

proporcao = (
    df_limpo.groupby("tipo")["idade_anos"]
    .apply(lambda x: x.isna().mean())
    .mul(100)
    .round(2)
    .sort_values(ascending=False)
)

print(proporcao)

print("\nDiagnóstico concluído!")