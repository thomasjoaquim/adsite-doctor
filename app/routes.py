from flask import Blueprint, render_template, request
import os
import pandas as pd
from .analyzer.ads_analysis import classify_ads_performance
from .utils import analyze_meta_csv

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join("uploads", file.filename)
            file.save(filepath)

            try:
                # Leitura com encoding que evita erro de caracteres especiais
                df = pd.read_csv(filepath, encoding="latin1")
                result_df, avg_ctr, avg_cpc = classify_ads_performance(df)
                return render_template("results.html", tables=[result_df.to_html(classes='data')], avg_ctr=avg_ctr, avg_cpc=avg_cpc)
            except Exception as e:
                return render_template("results.html", error=str(e))

    return render_template("index.html")


@main.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    analysis_data = None

    if request.method == "POST":
        file = request.files.get("campaign_file")

        if file:
            filepath = os.path.join("uploads", file.filename)
            file.save(filepath)

            try:
                if file.filename.endswith(".csv"):
                    df = pd.read_csv(filepath, encoding="latin1")
                    result_df, avg_ctr, avg_cpc = classify_ads_performance(df)

                    score = 100
                    if df["CTR"].mean() < 0.04:
                        score -= 10

                    suggestions = []
                    if df["CTR"].mean() < avg_ctr:
                        suggestions.append("Tente criativos com chamadas mais diretas ou imagens mais chamativas.")
                    if df["CPC"].mean() > avg_cpc:
                        suggestions.append("Experimente segmentações de público diferentes para reduzir o CPC.")
                    if result_df["Performance"].value_counts().get("Low Performing", 0) > 1:
                        suggestions.append("Teste novas variações de imagem e texto para os anúncios com baixo desempenho.")

                    analysis_data = {
                        "ads_table": result_df.to_html(classes="data"),
                        "avg_ctr": avg_ctr,
                        "avg_cpc": avg_cpc,
                        "score": score,
                        "suggestions": suggestions
                    }

                elif file.filename.endswith(".xlsx"):
                    df = pd.read_excel(filepath)
                    result_df, summary = analyze_meta_csv(df)

                    analysis_data = {
                        "ads_table": result_df.to_html(classes="data"),
                        "avg_ctr": summary["CTR médio (%)"],
                        "avg_cpc": summary["CPC médio (R$)"],
                        "score": 100,
                        "suggestions": [
                            "Aproveite a performance destacada de criativos com baixo CPC e alta CTR.",
                            "Considere reinvestir em anúncios com classificação Alta."
                        ]
                    }

            except Exception as e:
                return render_template("dashboard.html", error=str(e))

    return render_template("dashboard.html", data=analysis_data)
