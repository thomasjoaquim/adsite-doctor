import pandas as pd

def classify_ads_performance(df):
    df["CTR"] = pd.to_numeric(df["CTR"], errors="coerce")
    df["CPC"] = pd.to_numeric(df["CPC"], errors="coerce")

    avg_ctr = df["CTR"].mean()
    avg_cpc = df["CPC"].mean()

    def classify(row):
        if row["CTR"] >= avg_ctr and row["CPC"] <= avg_cpc:
            return "High Performing"
        else:
            return "Low Performing"

    df["Performance"] = df.apply(classify, axis=1)
    return df, avg_ctr, avg_cpc
