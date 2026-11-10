import pandas as pd
from scipy.stats import zscore

# Ler arquivo
df = pd.read_csv("arquivos/imoveis_limpo.csv")

# Describe
print(df[["area_m2", "quartos", "idade_anos", "preco"]].describe())


# Função IQR
def limites_iqr(serie, k=1.5):
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)

    iqr = q3 - q1

    limite_inferior = q1 - k * iqr
    limite_superior = q3 + k * iqr

    return limite_inferior, limite_superior


# Suspeitos por IQR
for coluna in ["area_m2", "quartos", "idade_anos", "preco"]:

    li, ls = limites_iqr(df[coluna])

    suspeitos = (
        (df[coluna] < li)
        | (df[coluna] > ls)
    )

    print(
        f"\n{coluna}: {suspeitos.sum()} suspeitos"
    )


# Z-score da área
z_com = zscore(df["area_m2"])

print("\nÁrea com maior valor:")
print((abs(z_com) > 3).sum())

# Removendo o maior valor
area_sem_maior = df["area_m2"].drop(
    df["area_m2"].idxmax()
)

z_sem = zscore(area_sem_maior)

print("\nÁrea sem o maior valor:")
print((abs(z_sem) > 3).sum())


# Preço por m²
df["preco_m2"] = df["preco"] / df["area_m2"]

# Regra de negócio
suspeitos_negocio = df[
    (df["area_m2"] > 600)
    | (df["preco"] < 50000)
    | (df["quartos"] > 10)
]

print("\nSuspeitos pela regra de negócio:")
print(
    suspeitos_negocio[
        ["id_anuncio", "area_m2", "preco", "quartos", "preco_m2"]
    ]
)