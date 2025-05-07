import pandas as pd

def classify_ads_performance(df):
    # Renomeia colunas caso venham com nomes diferentes
    if 'CTR (todos)' in df.columns:
        df['CTR'] = df['CTR (todos)']
    if 'CPC (todos)' in df.columns:
        df['CPC'] = df['CPC (todos)']

    df["CTR"] = pd.to_numeric(df["CTR"], errors="coerce")
    df["CPC"] = pd.to_numeric(df["CPC"], errors="coerce")

    avg_ctr = df["CTR"].mean()
    avg_cpc = df["CPC"].mean()

    def classify(row):
        if row["CTR"] >= avg_ctr and row["CPC"] <= avg_cpc:
            return "High Performing"
        elif row["CTR"] >= avg_ctr or row["CPC"] <= avg_cpc:
            return "Medium Performing"
        else:
            return "Low Performing"

    df["Performance"] = df.apply(classify, axis=1)

    return df, round(avg_ctr, 4), round(avg_cpc, 4)
