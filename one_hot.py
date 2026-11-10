import pandas as pd

from sklearn.preprocessing import OneHotEncoder

# Ler arquivo
df = pd.read_csv("arquivos/imoveis_tratado.csv")

# Shape antes
print("Shape original:")
print(df.shape)

# get_dummies com drop_first
df_dummies = pd.get_dummies(
    df,
    columns=["tipo", "bairro"],
    drop_first=True,
    dtype=int
)

print("\nShape depois:")
print(df_dummies.shape)

# Dummies sem drop_first
tipo_dummies = pd.get_dummies(
    df["tipo"],
    dtype=int
)

print("\nSoma das dummies por linha:")
print(tipo_dummies.sum(axis=1))

print(
    "\nTodas as linhas somam 1?",
    (tipo_dummies.sum(axis=1) == 1).all()
)

# OneHotEncoder
encoder = OneHotEncoder(
    handle_unknown="ignore"
)

encoder.fit(df[["tipo"]])

nova_linha = pd.DataFrame({
    "tipo": ["Galpão"]
})

resultado = encoder.transform(
    nova_linha
)

print("\nTransformação para tipo='Galpão':")
print(resultado.toarray())

# Em produção eu usaria OneHotEncoder,
# pois ele pode ser ajustado no treino e reutilizado
# no teste e em novos dados. Além disso,
# handle_unknown='ignore' permite tratar categorias
# não vistas sem gerar erro.
