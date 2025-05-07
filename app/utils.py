import pandas as pd

def analyze_meta_csv(df):
    # Seleciona e renomeia as colunas relevantes
    df = df[[
        "Nome do anúncio", "Impressões", "Alcance", "Frequência",
        "Custo por resultado", "Valor usado (BRL)", "Resultados",
        "CPC (todos)", "CTR (todos)"
    ]].copy()

    df.columns = [
        "Ad Name", "Impressions", "Reach", "Frequency",
        "Cost per Result", "Amount Spent (BRL)", "Results",
        "CPC", "CTR"
    ]

    # Converte colunas numéricas
    for col in ["Impressions", "Reach", "Frequency", "Cost per Result", "Amount Spent (BRL)", "Results", "CPC", "CTR"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove valores inválidos
    df.dropna(subset=["Ad Name", "Impressions", "CTR", "CPC"], inplace=True)
    df = df[df["Impressions"] > 0]

    # Cálculo das médias
    avg_ctr = df["CTR"].mean()
    avg_cpc = df["CPC"].mean()

    # Classificação
    def classify(row):
        if row["CTR"] >= avg_ctr and row["CPC"] <= avg_cpc:
            return "Alta"
        elif row["CTR"] >= avg_ctr or row["CPC"] <= avg_cpc:
            return "Média"
        else:
            return "Baixa"

    df["Performance"] = df.apply(classify, axis=1)

    # Gera resumo
    summary = {
        "CTR médio (%)": round(avg_ctr, 2),
        "CPC médio (R$)": round(avg_cpc, 2),
        "Total investido (R$)": round(df["Amount Spent (BRL)"].sum(), 2)
    }

    return df, summary
