import pandas as pd
import yaml
import sys

def carregar_contrato(path="contracts/pedidos.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)

def validar_schema(df, contrato):
    erros = []
    colunas_esperadas = set(contrato["schema"].keys())
    colunas_atuais = set(df.columns)
    ausentes = colunas_esperadas - colunas_atuais
    if ausentes:
        erros.append(f"Colunas ausentes: {ausentes}")
    inesperadas = colunas_atuais - colunas_esperadas
    if inesperadas:
        erros.append(f"Colunas inesperadas: {inesperadas}")
    return erros

def validar_dominio(df, contrato):
    erros = []
    for coluna, regras in contrato.get("domain", {}).items():
        permitidos = set(regras["allowed_values"])
        atuais = set(df[coluna].dropna().unique())
        invalidos = atuais - permitidos
        if invalidos:
            erros.append(f"Valores invalidos em '{coluna}': {invalidos}")
    return erros

def validar_formato(df, contrato):
    erros = []
    for coluna, regras in contrato.get("format", {}).items():
        if regras.get("decimal_separator") == ".":
            try:
                pd.to_numeric(df[coluna], errors="raise")
            except (ValueError, TypeError):
                erros.append(f"Formato numerico invalido em '{coluna}'")
    return erros

def validar_obrigatorios(df, contrato):
    erros = []
    for coluna in contrato.get("required", []):
        nulos = df[coluna].isna().sum()
        if nulos > 0:
            erros.append(f"Nulos em '{coluna}': {nulos}")
    return erros

def validar_unicidade(df, contrato):
    erros = []
    for coluna in contrato.get("unique", []):
        duplicatas = df[coluna].duplicated().sum()
        if duplicatas > 0:
            erros.append(f"Duplicatas em '{coluna}': {duplicatas}")
    return erros

def validar(csv_path, contrato_path="contracts/pedidos.yaml"):
    contrato = carregar_contrato(contrato_path)
    df = pd.read_csv(csv_path)
    erros = []
    erros.extend(validar_schema(df, contrato))
    erros.extend(validar_dominio(df, contrato))
    erros.extend(validar_formato(df, contrato))
    erros.extend(validar_obrigatorios(df, contrato))
    erros.extend(validar_unicidade(df, contrato))
    if erros:
        print("FALHOU - Pipeline bloqueado")
        for e in erros:
            print(f"  - {e}")
        return False
    print("PASSOU - Dados liberados")
    return True

if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/raw/pedidos.csv"
    ok = validar(csv_path)
    sys.exit(0 if ok else 1)