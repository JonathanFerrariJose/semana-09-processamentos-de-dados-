import pandas as pd

from sklearn.preprocessing import (
    MinMaxScaler,
    StandardScaler,
    RobustScaler
)

# Ler arquivo tratado
df = pd.read_csv("arquivos/imoveis_tratado.csv")

colunas = [
    "area_m2",
    "quartos",
    "idade_anos",
    "preco"
]

# Min e Max
print("Mínimos:")
print(df[colunas].min())

print("\nMáximos:")
print(df[colunas].max())

# Dois imóveis para comparação
imovel1 = df.loc[0, colunas]
imovel2 = df.loc[1, colunas]

# Distância ao quadrado
distancias = (imovel1 - imovel2) ** 2

print("\nDistância ao quadrado por coluna:")
print(distancias)

print("\nColuna dominante:")
print(distancias.idxmax())

# MinMaxScaler
minmax = MinMaxScaler()

df_minmax = pd.DataFrame(
    minmax.fit_transform(df[colunas]),
    columns=colunas
)

print("\nMinMaxScaler")
print(df_minmax.agg(["mean", "std"]))

# StandardScaler
standard = StandardScaler()

df_standard = pd.DataFrame(
    standard.fit_transform(df[colunas]),
    columns=colunas
)

print("\nStandardScaler")
print(df_standard.agg(["mean", "std"]))

# RobustScaler
robust = RobustScaler()

df_robust = pd.DataFrame(
    robust.fit_transform(df[colunas]),
    columns=colunas
)

print("\nRobustScaler")
print(df_robust.agg(["mean", "std"]))

# Conferências
print("\nMinMax - mínimos")
print(df_minmax.min())

print("\nMinMax - máximos")
print(df_minmax.max())

print("\nStandardScaler - médias")
print(df_standard.mean())