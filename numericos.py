import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def limites_iqr(serie, k=1.5):
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)

    iqr = q3 - q1

    return (
        q1 - k * iqr,
        q3 + k * iqr
    )


def preparar_numericos(caminho):

    df = pd.read_csv(caminho)

    # remover erros pelas regras de negócio
    erros = (
        (df["area_m2"] > 600)
        | (df["preco"] < 50000)
        | (df["quartos"] > 10)
    )

    df = df.loc[~erros].copy()

    # criar preco_atipico
    li, ls = limites_iqr(df["preco"])

    df["preco_atipico"] = (
        (df["preco"] < li)
        | (df["preco"] > ls)
    )

    # salvar antes de escalar
    df.to_csv(
        "arquivos/imoveis_tratado.csv",
        index=False
    )

    # treino e teste
    treino, teste = train_test_split(
        df,
        test_size=0.2,
        random_state=42
    )

    colunas = [
        "area_m2",
        "quartos",
        "idade_anos"
    ]

    scaler = StandardScaler()

    treino[colunas] = scaler.fit_transform(
        treino[colunas]
    )

    teste[colunas] = scaler.transform(
        teste[colunas]
    )

    return treino, teste


treino, teste = preparar_numericos(
    "arquivos/imoveis_limpo.csv"
)

print("Tamanho treino:")
print(treino.shape)

print("\nTamanho teste:")
print(teste.shape)

print("\nMédia das colunas escaladas (treino):")
print(
    treino[
        ["area_m2", "quartos", "idade_anos"]
    ].mean()
)

print("\nMédia das colunas escaladas (teste):")
print(
    teste[
        ["area_m2", "quartos", "idade_anos"]
    ].mean()
)