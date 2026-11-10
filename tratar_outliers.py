import pandas as pd


def limites_iqr(serie, k=1.5):
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)

    iqr = q3 - q1

    return (
        q1 - k * iqr,
        q3 + k * iqr
    )


# Ler arquivo
df = pd.read_csv("arquivos/imoveis_limpo.csv")

# Guardar original para comparações
df_original = df.copy()

# Regras de negócio
erros = (
    (df["area_m2"] > 600)
    | (df["preco"] < 50000)
    | (df["quartos"] > 10)
)

# Remover erros
df = df.loc[~erros].copy()

# IQR para preço
li, ls = limites_iqr(df["preco"])

df["preco_atipico"] = (
    (df["preco"] < li)
    | (df["preco"] > ls)
)

# Mediana do preço nos dois grupos
print("Mediana preço normal:")
print(
    df.loc[~df["preco_atipico"], "preco"].median()
)

print("\nMediana preço atípico:")
print(
    df.loc[df["preco_atipico"], "preco"].median()
)

# Estatísticas da área antes
print("\nÁrea antes:")
print(
    df_original["area_m2"].agg(
        ["mean", "median", "std"]
    )
)

# Estatísticas da área depois
print("\nÁrea depois:")
print(
    df["area_m2"].agg(
        ["mean", "median", "std"]
    )
)

# Correlação antes
print("\nCorrelação antes:")
print(
    df_original["area_m2"].corr(
        df_original["preco"]
    )
)

# Correlação depois
print("\nCorrelação depois:")
print(
    df["area_m2"].corr(
        df["preco"]
    )
)

# Salvar arquivo
df.to_csv(
    "arquivos/imoveis_tratado.csv",
    index=False
)