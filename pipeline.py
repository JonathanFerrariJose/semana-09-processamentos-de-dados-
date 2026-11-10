import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import (
    StandardScaler,
    OrdinalEncoder,
    OneHotEncoder
)

# Ler arquivo
df = pd.read_csv("arquivos/imoveis_tratado.csv")

# X e y
X = df.drop(
    columns=[
        "preco",
        "id_anuncio",
        "preco_atipico"
    ]
)

y = np.log1p(df["preco"])

# Treino e teste
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Grupos de colunas
numericas = [
    "area_m2",
    "quartos",
    "idade_anos"
]

ordinal = [
    "condicao"
]

nominais = [
    "tipo",
    "bairro"
]

binarias = [
    "aceita_pet",
    "mobiliado"
]

# Pipeline
preprocessador = ColumnTransformer(
    transformers=[
        (
            "numericas",
            StandardScaler(),
            numericas
        ),
        (
            "ordinal",
            OrdinalEncoder(
                categories=[
                    [
                        "Ruim",
                        "Regular",
                        "Bom",
                        "Ótimo"
                    ]
                ]
            ),
            ordinal
        ),
        (
            "nominais",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            nominais
        ),
        (
            "binarias",
            "passthrough",
            binarias
        )
    ]
)

# Ajustar somente no treino
X_treino_transf = preprocessador.fit_transform(
    X_treino
)

X_teste_transf = preprocessador.transform(
    X_teste
)

# Shapes
print("Shape treino:")
print(X_treino_transf.shape)

print("\nShape teste:")
print(X_teste_transf.shape)

# Nomes das colunas geradas
nomes_colunas = preprocessador.get_feature_names_out()

print("\nPrimeiras colunas:")
print(nomes_colunas[:10])