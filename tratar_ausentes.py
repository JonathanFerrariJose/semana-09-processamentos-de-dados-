import pandas as pd
from pathlib import Path

# =====================================================
# LEITURA
# =====================================================

ARQUIVO = Path("imoveis_bruto.csv")

df = pd.read_csv(
    ARQUIVO,
    na_values=["N/D", "?", "s/i"]
)

# =====================================================
# TRATAMENTOS INICIAIS
# =====================================================

df["area_m2"] = pd.to_numeric(
    df["area_m2"],
    errors="coerce"
)

df["idade_anos"] = pd.to_numeric(
    df["idade_anos"],
    errors="coerce"
)

# substituir -1 por ausente
df.loc[df["idade_anos"] == -1, "idade_anos"] = pd.NA

# =====================================================
# CRIAR FLAG DE IDADE AUSENTE
# =====================================================

df["idade_ausente"] = df["idade_anos"].isna()

# =====================================================
# PREENCHER AREA_M2 COM MEDIANA POR TIPO
# =====================================================

df["area_m2"] = (
    df.groupby("tipo")["area_m2"]
    .transform(lambda x: x.fillna(x.median()))
)

# =====================================================
# PREENCHER IDADE_ANOS COM MEDIANA POR TIPO
# =====================================================

df["idade_anos"] = (
    df.groupby("tipo")["idade_anos"]
    .transform(lambda x: x.fillna(x.median()))
)

# =====================================================
# PREENCHER DISTANCIA_PRAIA_KM COM MEDIANA POR BAIRRO
# =====================================================

df["distancia_praia_km"] = (
    df.groupby("bairro")["distancia_praia_km"]
    .transform(lambda x: x.fillna(x.median()))
)

# =====================================================
# PREENCHER CONDICAO COM MODA
# =====================================================

moda_condicao = df["condicao"].mode()[0]

df["condicao"] = df["condicao"].fillna(moda_condicao)

# =====================================================
# RESULTADO FINAL
# =====================================================

print("\nAusentes por coluna:")
print(df.isna().sum())

print("\nTotal de ausentes:")
print(df.isna().sum().sum())

# opcional: salvar arquivo tratado
df.to_csv("imoveis_tratado.csv", index=False)

print("\nArquivo salvo: imoveis_tratado.csv")

# area_m2 -> mediana por tipo porque apartamentos,
# casas e studios possuem tamanhos diferentes.

# idade_anos -> mediana por tipo para preservar
# características semelhantes entre imóveis.

# distancia_praia_km -> mediana por bairro porque
# imóveis do mesmo bairro tendem a ficar em regiões próximas.

# condicao -> moda porque é variável categórica
# e a moda representa a categoria mais frequente.

# idade_ausente -> criada para não perder a informação
# de quais registros tinham idade faltante originalmente.