import pandas as pd

df = pd.read_csv("imoveis_bruto.csv")

print("Duplicatas exatas:")
print(df.duplicated().sum())

print("\nDuplicatas por id_anuncio:")
print(df.duplicated(subset=["id_anuncio"]).sum())

print("\nBairros antes:")
print(df["bairro"].nunique())

df["bairro"] = df["bairro"].str.strip().str.title()

print("\nBairros depois:")
print(df["bairro"].nunique())

# quase duplicatas (ignorando o id)
quase_dup = df.duplicated(
    subset=df.columns.drop("id_anuncio")
)

print("\nQuantidade de quase duplicatas:")
print(quase_dup.sum())

print("\nUm par de quase duplicatas:")
print(
    df[
        df.duplicated(
            subset=df.columns.drop("id_anuncio"),
            keep=False
        )
    ].head(2)
)

# remover duplicatas considerando todas as colunas,
# exceto o id_anuncio
df = df.drop_duplicates(
    subset=df.columns.drop("id_anuncio")
)

print("\nTotal de linhas que sobraram:")
print(len(df))