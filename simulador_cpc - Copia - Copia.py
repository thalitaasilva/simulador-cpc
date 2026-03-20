import streamlit as st
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Simulador CPC | PUCPR", layout="centered")

# -------------------------
# ESTILO
# -------------------------
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

div.stButton > button {
    background: linear-gradient(90deg, #8a0538, #ff0040);
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-weight: bold;
}

.spacer {
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.markdown("""
<div class='header'>
    <h1 style='color:white;'>Simulador CPC | PUCPR</h1>
</div>
""", unsafe_allow_html=True)

# -------------------------
# FUNÇÕES
# -------------------------
def calcular_nota_docente(p, tipo):
    metas = {"doutores": 0.80, "mestres": 1.00, "regime": 0.90}
    return min(5.0, (p / metas.get(tipo, 0.8)) * 5)


def gerar_pdf(ncpc, faixa, nc, nidd, no, nf, na, total, dout, mest, regi, nd, nm, nr):
    doc = SimpleDocTemplate("relatorio_cpc.pdf")
    styles = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("Relatório de Simulação CPC - PUCPR", styles['Title']))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph(f"CPC Contínuo: {ncpc:.4f}", styles['Normal']))
    elementos.append(Paragraph(f"Conceito: {faixa}", styles['Normal']))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("Indicadores", styles['Heading2']))
    elementos.append(Paragraph(f"Nota ENADE: {nc}", styles['Normal']))
    elementos.append(Paragraph(f"Nota IDD: {nidd}", styles['Normal']))
    elementos.append(Paragraph(f"Org. Didática: {no}", styles['Normal']))
    elementos.append(Paragraph(f"Infraestrutura: {nf}", styles['Normal']))
    elementos.append(Paragraph(f"Oportunidades: {na}", styles['Normal']))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("Corpo Docente", styles['Heading2']))
    elementos.append(Paragraph(f"Total: {total}", styles['Normal']))
    elementos.append(Paragraph(f"Doutores: {dout}", styles['Normal']))
    elementos.append(Paragraph(f"Mestres: {mest}", styles['Normal']))
    elementos.append(Paragraph(f"Regime: {regi}", styles['Normal']))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("Notas Calculadas", styles['Heading2']))
    elementos.append(Paragraph(f"Doutores: {nd:.2f}", styles['Normal']))
    elementos.append(Paragraph(f"Mestres: {nm:.2f}", styles['Normal']))
    elementos.append(Paragraph(f"Regime: {nr:.2f}", styles['Normal']))

    doc.build(elementos)
    return "relatorio_cpc.pdf"

# -------------------------
# ENADE
# -------------------------
st.subheader("Nota do ENADE (20%)")
st.markdown("<div class='sub'>Desempenho dos estudantes</div>", unsafe_allow_html=True)

nc = st.number_input("", 0.0, 5.0, value=None, placeholder="Digite aqui", format="%.2f", key="enade")

# -------------------------
# IDD
# -------------------------
st.subheader("Nota do IDD (35%)")
st.markdown("<div class='sub'>Valor agregado pelo processo formativo</div>", unsafe_allow_html=True)

nidd = st.number_input("", 0.0, 5.0, value=None, placeholder="Digite aqui", format="%.2f", key="idd")

st.markdown("---")

# -------------------------
# QUESTIONÁRIO
# -------------------------
st.subheader("Questionário do Estudante (15%)")

no = st.number_input("Nota Organização Didático Pedagógica", 0.0, 5.0, value=None, placeholder="Digite aqui", format="%.2f", key="org")
nf = st.number_input("Nota da Infraestrutura", 0.0, 5.0, value=None, placeholder="Digite aqui", format="%.2f", key="infra")
na = st.number_input("Nota de Oportunidades de Ampliação da Formação", 0.0, 5.0, value=None, placeholder="Digite aqui", format="%.2f", key="oport")

st.markdown("---")

# -------------------------
# DOCENTE
# -------------------------
st.subheader("Corpo docente (30%)")

total = st.number_input("Total de professores", min_value=0, value=None, step=1, format="%d", placeholder="Digite aqui", key="total")
dout = st.number_input("Quantidade de doutores", min_value=0, value=None, step=1, format="%d", placeholder="Digite aqui", key="dout")
mest = st.number_input("Quantidade de mestres", min_value=0, value=None, step=1, format="%d", placeholder="Digite aqui", key="mest")
regi = st.number_input("Regime de trabalho (TI/TP)", min_value=0, value=None, step=1, format="%d", placeholder="Digite aqui", key="regi")

# -------------------------
# ESPAÇO
# -------------------------
st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

# -------------------------
# BOTÃO
# -------------------------
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

        # RESULTADO BONITO
        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, #8a0538, #ff0040);
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            color: white;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.3);
            margin-top: 20px;
        ">
            <h1 style="font-size:60px; margin:0;">{ncpc:.4f}</h1>
            <p style="margin:5px 0 15px 0; font-size:18px;">CPC Contínuo</p>

            <div style="
                display:inline-block;
                padding:10px 25px;
                background:white;
                color:#8a0538;
                border-radius:30px;
                font-weight:bold;
                font-size:20px;
            ">
                CONCEITO {faixa}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # PDF
        arquivo_pdf = gerar_pdf(
            ncpc, faixa,
            nc, nidd, no, nf, na,
            total, dout, mest, regi,
            nd, nm, nr
        )

        with open(arquivo_pdf, "rb") as f:
            st.download_button("📥 Baixar Relatório Completo", f, "relatorio_cpc.pdf")
