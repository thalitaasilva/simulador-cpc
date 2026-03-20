import streamlit as st
import pandas as pd
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Simulador CPC | PUCPR", layout="centered")

# -------------------------
# ESTILO PUC
# -------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #ffffff, #f3e8ff);
    font-family: 'Segoe UI', sans-serif;
}

/* HEADER */
.header {
    background: linear-gradient(90deg, #8a0538, #9654FF);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.2);
}

/* CARDS */
.card {
    background: linear-gradient(90deg, #8a0538, #ff0040);
    color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.2);
    margin-bottom: 20px;
}

/* INPUTS */
div[data-baseweb="input"] {
    background-color: white;
    border-radius: 8px;
}

/* BOTÃO */
div.stButton > button {
    background: linear-gradient(90deg, #8a0538, #ff0040);
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
}

/* RESULTADO */
.resultado {
    background: white;
    padding: 35px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.2);
    margin-top: 20px;
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
# LOGO ENADE (SEM ERRO)
# -------------------------
caminho_logo = os.path.join(os.path.dirname(__file__), "enade_logo.png")

if os.path.exists(caminho_logo):
    col1, col2 = st.columns([1, 6])
    with col1:
        st.image(caminho_logo, width=80)
else:
    st.warning("⚠️ Logo ENADE não encontrada. Verifique o arquivo enade_logo.png")

# -------------------------
# FUNÇÕES
# -------------------------
def calcular_nota_docente(proporcao_real, tipo):
    metas = {"doutores": 0.80, "mestres": 1.00, "regime": 0.90}
    meta = metas.get(tipo, 0.80)
    nota = (proporcao_real / meta) * 5
    return min(5.0, max(0.0, nota))


def gerar_pdf(ncpc, faixa):
    doc = SimpleDocTemplate("relatorio_cpc.pdf")
    styles = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("Relatório CPC - PUCPR", styles['Title']))
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph(f"CPC Contínuo: {ncpc:.4f}", styles['Normal']))
    elementos.append(Paragraph(f"Conceito: {faixa}", styles['Normal']))

    doc.build(elementos)
    return "relatorio_cpc.pdf"

# -------------------------
# CARD 1
# -------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📊 Indicadores de Qualidade")

nc = st.number_input("Nota Enade", 0.0, 5.0)
nidd = st.number_input("Nota IDD", 0.0, 5.0)
no = st.number_input("Org. Didática", 0.0, 5.0)
nf = st.number_input("Infraestrutura", 0.0, 5.0)
na = st.number_input("Oportunidades", 0.0, 5.0)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# CARD 2
# -------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("👨‍🏫 Corpo Docente")

total = st.number_input("Total Professores", 0.0)
dout = st.number_input("Doutores", 0.0)
mest = st.number_input("Mestres", 0.0)
regi = st.number_input("TI/TP", 0.0)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# BOTÃO
# -------------------------
if st.button("🚀 CALCULAR CPC"):

    if total <= 0:
        st.error("Preencha corretamente.")
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

        if ncpc >= 3.945:
            faixa, cor = 5, "#9654FF"
        elif ncpc >= 2.945:
            faixa, cor = 4, "#8a0538"
        elif ncpc >= 1.945:
            faixa, cor = 3, "#ff0040"
        else:
            faixa, cor = 2, "#ff0040"

        st.markdown(f"""
        <div class='resultado'>
            <h1 style='color:{cor}; font-size:55px'>{ncpc:.4f}</h1>
            <h3 style='color:{cor};'>CONCEITO {faixa}</h3>
        </div>
        """, unsafe_allow_html=True)

        st.progress(min(ncpc / 5, 1.0))

        if faixa < 4:
            st.warning("⚠️ Abaixo do ideal para CPC 4")
        else:
            st.success("🎯 Excelente desempenho!")

        df = pd.DataFrame({
            "Indicadores": ["Enade", "IDD", "Org.", "Infra", "Oport."],
            "Notas": [nc, nidd, no, nf, na]
        })
        st.bar_chart(df.set_index("Indicadores"))

        arquivo_pdf = gerar_pdf(ncpc, faixa)

        with open(arquivo_pdf, "rb") as f:
            st.download_button("📥 Baixar Relatório", f, "relatorio_cpc.pdf")
