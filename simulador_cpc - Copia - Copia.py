import streamlit as st
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Simulador CPC | PUCPR", layout="centered")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #ffffff, #f3e8ff);
    font-family: 'Segoe UI', sans-serif;
}

.header {
    background: linear-gradient(90deg, #8a0538, #ff0040);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 30px;
}

.sub {
    font-size: 13px;
    color: #666;
    margin-bottom: 10px;
}

div[data-baseweb="input"] input {
    background-color: white !important;
}

div.stButton > button {
    background: linear-gradient(90deg, #8a0538, #ff0040);
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-weight: bold;
}

.resultado {
    background: white;
    padding: 35px;
    border-radius: 20px;
    text-align: center;
    margin-top: 25px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='header'>
    <h1 style='color:white;'>Simulador CPC | PUCPR</h1>
</div>
""", unsafe_allow_html=True)

# FUNÇÕES
def calcular_nota_docente(proporcao_real, tipo):
    metas = {"doutores": 0.80, "mestres": 1.00, "regime": 0.90}
    return min(5.0, (proporcao_real / metas.get(tipo, 0.8)) * 5)

def gerar_pdf(ncpc, faixa):
    doc = SimpleDocTemplate("relatorio_cpc.pdf")
    styles = getSampleStyleSheet()
    elementos = []
    elementos.append(Paragraph(f"CPC: {ncpc:.4f}", styles['Normal']))
    elementos.append(Paragraph(f"Conceito: {faixa}", styles['Normal']))
    doc.build(elementos)
    return "relatorio_cpc.pdf"

# ENADE
st.subheader("Nota do ENADE (20%)")
st.markdown("<div class='sub'>Desempenho dos estudantes</div>", unsafe_allow_html=True)
nc = st.number_input("", min_value=0.0, max_value=5.0, value=None, placeholder="Digite", format="%.2f")

# IDD
st.subheader("Nota do IDD (35%)")
st.markdown("<div class='sub'>Valor agregado pelo processo formativo</div>", unsafe_allow_html=True)
nidd = st.number_input("", min_value=0.0, max_value=5.0, value=None, placeholder="Digite", format="%.2f")

st.markdown("---")

# QUESTIONÁRIO
st.subheader("Questionário do Estudante (15%)")

no = st.number_input("Nota Organização Didático Pedagógica", 0.0, 5.0, value=None, placeholder="Digite", format="%.2f")
nf = st.number_input("Nota da Infraestrutura", 0.0, 5.0, value=None, placeholder="Digite", format="%.2f")
na = st.number_input("Nota de Oportunidades de Ampliação da Formação", 0.0, 5.0, value=None, placeholder="Digite", format="%.2f")

st.markdown("---")

# DOCENTE
st.subheader("Corpo docente (30%)")

total = st.number_input("Total de professores", min_value=0.0, value=None, placeholder="Digite")
dout = st.number_input("Quantidade de doutores", min_value=0.0, value=None, placeholder="Digite")
mest = st.number_input("Quantidade de mestres", min_value=0.0, value=None, placeholder="Digite")
regi = st.number_input("Regime de trabalho (TI/TP)", min_value=0.0, value=None, placeholder="Digite")

st.markdown("<br>", unsafe_allow_html=True)

# BOTÃO
if st.button("🚀 CALCULAR CPC"):

    if None in [nc, nidd, no, nf, na, total, dout, mest, regi] or total == 0:
        st.error("Preencha todos os campos corretamente.")
    else:
        pd = dout / total
        pm = (dout + mest) / total
        pr = regi / total

        nd = calcular_nota_docente(pd, "doutores")
        nm = calcular_nota_docente(pm, "mestres")
        nr = calcular_nota_docente(pr, "regime")

        ncpc = (
            0.20 * nc + 0.35 * nidd + 0.15 * nd +
            0.075 * nm + 0.075 * nr +
            0.075 * no + 0.05 * nf + 0.025 * na
        )

        faixa = 5 if ncpc >= 3.945 else 4 if ncpc >= 2.945 else 3 if ncpc >= 1.945 else 2

        st.markdown(f"<div class='resultado'><h1>{ncpc:.4f}</h1><h3>CONCEITO {faixa}</h3></div>", unsafe_allow_html=True)

        arquivo_pdf = gerar_pdf(ncpc, faixa)

        with open(arquivo_pdf, "rb") as f:
            st.download_button("📥 Baixar Relatório", f, "relatorio_cpc.pdf")
