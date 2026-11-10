import pandas as pd

from sklearn.preprocessing import OrdinalEncoder

# Ler arquivo
df = pd.read_csv("arquivos/imoveis_tratado.csv")

# Colunas de texto
print("Colunas de texto:")
print(
    df.select_dtypes(include="object").columns
)

# Binárias com map
mapa_binario = {
    "Não": 0,
    "Sim": 1
}

df["aceita_pet_num"] = df["aceita_pet"].map(
    mapa_binario
)

df["mobiliado_num"] = df["mobiliado"].map(
    mapa_binario
)

# Conferir valores sem correspondência
print("\nAceita pet sem correspondência:")
print(
    df["aceita_pet_num"].isna().sum()
)

print("\nMobiliado sem correspondência:")
print(
    df["mobiliado_num"].isna().sum()
)

# Codificação ordinal manual
ordem = {
    "Ruim": 0,
    "Regular": 1,
    "Bom": 2,
    "Ótimo": 3
}

df["condicao_num"] = df["condicao"].map(
    ordem
)

# Reproduzir com OrdinalEncoder
encoder = OrdinalEncoder(
    categories=[[
        "Ruim",
        "Regular",
        "Bom",
        "Ótimo"
    ]]
)

df["condicao_encoder"] = encoder.fit_transform(
    df[["condicao"]]
)

# Verificar se coincidem
print("\nValores coincidem?")
print(
    (
        df["condicao_num"]
        == df["condicao_encoder"]
    ).all()
)