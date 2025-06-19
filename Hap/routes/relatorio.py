from flask import Blueprint, send_file
from utils.google_sheets import obter_dados_alunos
import matplotlib.pyplot as plt
import pandas as pd
import io

relatorio_bp = Blueprint('relatorio', __name__)

@relatorio_bp.route("/relatorio/faixas-etarias")
def relatorio_faixas_etarias():
    dados = obter_dados_alunos()
    df = pd.DataFrame(dados)

    if "idade" in df.columns:
        df["idade"] = pd.to_numeric(df["idade"], errors="coerce")
    else:
        return "Coluna 'idade' não encontrada na planilha", 400

    bins = [0, 7, 12, 17, 25, 40, 60, 120]
    labels = ['0-7', '8-12', '13-17', '18-25', '26-40', '41-60', '60+']
    df["faixa"] = pd.cut(df["idade"], bins=bins, labels=labels)

    contagem = df["faixa"].value_counts().sort_index()
    fig, ax = plt.subplots()
    contagem.plot(kind="bar", color="#ffd93b", edgecolor="#001a41", ax=ax)
    ax.set_title("Distribuição por Faixa Etária")
    ax.set_xlabel("Faixa Etária")
    ax.set_ylabel("Quantidade de Alunos")
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    return send_file(img, mimetype="image/png")