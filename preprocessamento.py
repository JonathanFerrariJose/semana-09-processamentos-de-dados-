import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import (
    StandardScaler,
    OrdinalEncoder,
    OneHotEncoder
)


def limpar_imoveis(caminho):
    """Limpa e trata valores ausentes."""

    df = pd.read_csv(
        caminho,
        na_values=["N/D", "?", "s/i"]
    )

    df["area_m2"] = pd.to_numeric(
        df["area_m2"],
        errors="coerce"
    )

    df["idade_anos"] = pd.to_numeric(
        df["idade_anos"],
        errors="coerce"
    )

    df.loc[
        df["idade_anos"] == -1,
        "idade_anos"
    ] = pd.NA

    df["idade_ausente"] = df["idade_anos"].isna()

    df["area_m2"] = (
        df.groupby("tipo")["area_m2"]
        .transform(lambda x: x.fillna(x.median()))
    )

    df["idade_anos"] = (
        df.groupby("tipo")["idade_anos"]
        .transform(lambda x: x.fillna(x.median()))
    )

    df["distancia_praia_km"] = (
        df.groupby("bairro")["distancia_praia_km"]
        .transform(lambda x: x.fillna(x.median()))
    )

    df["condicao"] = (
        df["condicao"]
        .fillna(df["condicao"].mode()[0])
    )

    df["bairro"] = (
        df["bairro"]
        .str.strip()
        .str.title()
    )

    df = df.drop_duplicates()

    return df


def tratar_erros(df):
    """Remove erros e sinaliza preços atípicos."""

    erros = (
        (df["area_m2"] > 600)
        | (df["preco"] < 50000)
        | (df["quartos"] > 10)
    )

    df = df.loc[~erros].copy()

    q1 = df["preco"].quantile(0.25)
    q3 = df["preco"].quantile(0.75)

    iqr = q3 - q1

    li = q1 - 1.5 * iqr
    ls = q3 + 1.5 * iqr

    df["preco_atipico"] = (
        (df["preco"] < li)
        | (df["preco"] > ls)
    )

    return df


def montar_pipeline(df):
    """Divide os dados e aplica o pipeline."""

    # binárias para números
    mapa = {
        "Não": 0,
        "Sim": 1
    }

    df["aceita_pet"] = df["aceita_pet"].map(mapa)
    df["mobiliado"] = df["mobiliado"].map(mapa)

    X = df.drop(
        columns=[
            "preco",
            "id_anuncio",
            "preco_atipico"
        ]
    )

    y = np.log1p(df["preco"])

    X_treino, X_teste, y_treino, y_teste = (
        train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )
    )

    preprocessador = ColumnTransformer(
        transformers=[
            (
                "numericas",
                StandardScaler(),
                [
                    "area_m2",
                    "quartos",
                    "idade_anos"
                ]
            ),
            (
                "ordinal",
                OrdinalEncoder(
                    categories=[[
                        "Ruim",
                        "Regular",
                        "Bom",
                        "Ótimo"
                    ]]
                ),
                ["condicao"]
            ),
            (
                "nominais",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                [
                    "tipo",
                    "bairro"
                ]
            ),
            (
                "binarias",
                "passthrough",
                [
                    "aceita_pet",
                    "mobiliado"
                ]
            )
        ]
    )

    X_treino = preprocessador.fit_transform(
        X_treino
    )

    X_teste = preprocessador.transform(
        X_teste
    )

    return (
        X_treino,
        X_teste,
        y_treino,
        y_teste
    )


# ===== EXECUÇÃO =====

df = limpar_imoveis(
    "imoveis_bruto.csv"
)

df = tratar_erros(df)

df.to_csv(
    "imoveis_tratado.csv",
    index=False
)

X_treino, X_teste, y_treino, y_teste = (
    montar_pipeline(df)
)

print("Shape entrada treino:")
print(X_treino.shape)

print("\nShape entrada teste:")
print(X_teste.shape)

print("\nShape saída treino:")
print(y_treino.shape)

print("\nShape saída teste:")
print(y_teste.shape)