import pandas as pd
import random
from datetime import datetime, timedelta

STATUS_VALIDOS = ["pendente", "aprovado", "enviado", "entregue", "cancelado"]
STATUS_INVALIDOS = STATUS_VALIDOS + ["em_analise_manual", "bloqueado_fraude"]

def gerar_pedidos(n=1000, corrompido=False):
    status_disponiveis = STATUS_INVALIDOS if corrompido else STATUS_VALIDOS
    linhas = []
    for i in range(n):
        valor = round(random.uniform(10, 5000), 2)
        if corrompido and random.random() < 0.3:
            valor_str = str(valor).replace(".", ",")
        else:
            valor_str = str(valor)
        linhas.append({
            "order_id": f"ORD-{i:06d}",
            "customer_id": f"CUST-{random.randint(1, 200):04d}",
            "status": random.choice(status_disponiveis),
            "valor_total": valor_str,
            "data_pedido": (datetime.now() - timedelta(days=random.randint(0, 90))).strftime("%Y-%m-%d"),
            "updated_at": datetime.now().isoformat(),
        })
    return pd.DataFrame(linhas)

if __name__ == "__main__":
    df_bom = gerar_pedidos(1000, corrompido=False)
    df_bom.to_csv("data/raw/pedidos.csv", index=False)
    print(f"OK pedidos.csv gerado: {len(df_bom)} linhas")
    df_corrompido = gerar_pedidos(1000, corrompido=True)
    df_corrompido.to_csv("data/raw/pedidos_corrompido.csv", index=False)
    print(f"OK pedidos_corrompido.csv gerado: {len(df_corrompido)} linhas")