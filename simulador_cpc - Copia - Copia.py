import streamlit as st
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# CONFIG
st.set_page_config(page_title="Simulador CPC | PUCPR", layout="centered")

# ESTILO
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
}

div[data-baseweb="input"] input {
    background-color: white !important;
}

/* BOTÃO MAIOR */
div.stButton > button {
    background: linear-gradient(90deg, #8a0538, #ff0040);
    color: white;
    border-radius: 12px;
    height: 3.5em;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
}

.resultado {
    background: white;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.15);
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class='header'>
    <h1 style='color:white;'>Simulador CPC | PUCPR</h1>
</div>
""", unsafe_allow_html=True)

# FUNÇÕES
def calcular_nota_docente(p, tipo):
    metas = {"doutores": 0.80, "mestres": 1.00, "regime": 0.90}
    return min(5.0, (p / metas.get(tipo, 0.8)) * 5)

def gerar_pdf(ncpc, faixa, nc, nidd, no, nf, na, total, dout, mest, regi, nd, nm, nr):
    doc = SimpleDocTemplate("relatorio_cpc.pdf")
    styles = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("Relatório de Simulação CPC", styles['Title']))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph(f"<b>CPC:</b> {ncpc:.4f}", styles['Normal']))
    elementos.append(Paragraph(f"<b>Conceito:</b> {faixa}", styles['Normal']))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("<b>Indicadores</b>", styles['Heading2']))
    elementos.append(Paragraph(f"ENADE: {nc}", styles['Normal']))
    elementos.append(Paragraph(f"IDD: {nidd}", styles['Normal']))
    elementos.append(Paragraph(f"Org. Didática: {no}", styles['Normal']))
    elementos.append(Paragraph(f"Infraestrutura: {nf}", styles['Normal']))
    elementos.append(Paragraph(f"Oportunidades: {na}", styles['Normal']))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("<b>Corpo Docente</b>", styles['Heading2']))
    elementos.append(Paragraph(f"Total: {total}", styles['Normal']))
    elementos.append(Paragraph(f"Doutores: {dout}", styles['Normal']))
    elementos.append(Paragraph(f"Mestres: {mest}", styles['Normal']))
    elementos.append(Paragraph(f"Regime: {regi}", styles['Normal']))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("<b>Notas Calculadas</b>", styles['Heading2']))
    elementos.append(Paragraph(f"Doutores: {nd:.2f}", styles['Normal']))
    elementos.append(Paragraph(f"Mestres: {nm:.2f}", styles['Normal']))
    elementos.append(Paragraph(f"Regime: {nr:.2f}", styles['Normal']))

    doc.build(elementos)
    return "relatorio_cpc.pdf"

# INPUTS
st.subheader("Nota do ENADE (20%)")
nc = st.number_input("", 0.0, 5.0, value=None, placeholder="Digite aqui", format="%.3f", key="enade")

st.subheader("Nota do IDD (35%)")
nidd = st.number_input("", 0.0, 5.0, value=None, placeholder="Digite aqui", format="%.3f", key="idd")

st.markdown("---")

st.subheader("Questionário do Estudante (15%)")
no = st.number_input("Org. Didática", 0.0, 5.0, value=None, format="%.3f", key="org")
nf = st.number_input("Infraestrutura", 0.0, 5.0, value=None, format="%.3f", key="infra")
na = st.number_input("Oportunidades", 0.0, 5.0, value=None, format="%.3f", key="oport")

st.markdown("---")

st.subheader("Corpo docente (30%)")
total = st.number_input("Total", min_value=0, value=None, step=1, format="%d", key="total")
dout = st.number_input("Doutores", min_value=0, value=None, step=1, format="%d", key="dout")
mest = st.number_input("Mestres", min_value=0, value=None, step=1, format="%d", key="mest")
regi = st.number_input("Regime", min_value=0, value=None, step=1, format="%d", key="regi")

st.markdown("<br><br>", unsafe_allow_html=True)

# BOTÃO
if st.button("🚀 CALCULAR CPC"):

    if None in [nc, nidd, no, nf, na, total, dout, mest, regi] or total == 0:
        st.error("Preencha todos os campos.")
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

        # RESULTADO LIMPO
        st.markdown(f"""
        <div class='resultado'>
            <h1 style='margin:0;'>{ncpc:.4f}</h1>
            <p style='color:#666;'>CPC Contínuo</p>
            <h3 style='color:#8a0538;'>Conceito {faixa}</h3>
        </div>
        """, unsafe_allow_html=True)

        arquivo_pdf = gerar_pdf(ncpc, faixa, nc, nidd, no, nf, na, total, dout, mest, regi, nd, nm, nr)

        with open(arquivo_pdf, "rb") as f:
            st.download_button("📥 Baixar Relatório", f, "relatorio_cpc.pdf")
