import pandas as pd


def limpar_imoveis(caminho):

    df = pd.read_csv(
        caminho,
        na_values=["N/D", "?", "s/i"]
    )

    # Passo 1: corrigir tipos
    df["area_m2"] = pd.to_numeric(
        df["area_m2"],
        errors="coerce"
    )

    df["idade_anos"] = pd.to_numeric(
        df["idade_anos"],
        errors="coerce"
    )

    # Passo 2: tratar ausentes
    df.loc[df["idade_anos"] == -1, "idade_anos"] = pd.NA

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

    # Passo 3: padronizar texto
    df["bairro"] = (
        df["bairro"]
        .str.strip()
        .str.title()
    )

    # Passo 4: remover duplicatas
    df = df.drop_duplicates()

    # Passo 5: devolver dataframe
    return df


df_original = pd.read_csv("imoveis_bruto.csv")

df_limpo = limpar_imoveis("imoveis_bruto.csv")

print("Linhas antes:", len(df_original))
print("Linhas depois:", len(df_limpo))

print("\nAusentes restantes:")
print(df_limpo.isna().sum().sum())

df_limpo.to_csv(
    "arquivos/imoveis_limpo.csv",
    index=False
)