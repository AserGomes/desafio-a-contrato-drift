import pandas as pd

df = pd.read_csv("data/raw/pedidos.csv")
df.head(100).to_csv("data/sample/pedidos_sample.csv", index=False)
print("OK amostra criada: data/sample/pedidos_sample.csv")