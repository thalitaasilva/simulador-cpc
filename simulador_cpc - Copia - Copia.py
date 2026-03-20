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

/* HEADER */
.header {
    background: linear-gradient(90deg, #8a0538, #ff0040);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.2);
}

/* SUBTITULOS */
.sub {
    font-size: 13px;
    color: #666;
    margin-top: -10px;
    margin-bottom: 10px;
}

/* INPUT */
div[data-baseweb="input"] input {
    background-color: white !important;
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
    margin-top: 25px;
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
# ENADE
# -------------------------
st.subheader("Nota do ENADE")
st.markdown("<div class='sub'>Desempenho dos estudantes (20%)</div>", unsafe_allow_html=True)
nc = st.number_input("", 0.0, 5.0, key="enade")

# -------------------------
# IDD
# -------------------------
st.subheader("Nota do IDD")
st.markdown("<div class='sub'>Valor agregado pelo processo formativo (35%)</div>", unsafe_allow_html=True)
nidd = st.number_input("", 0.0, 5.0, key="idd")

# -------------------------
# SEPARAÇÃO
# -------------------------
st.markdown("---")

# -------------------------
# QUESTIONÁRIO
# -------------------------
st.subheader("Questionário do Estudante (15%)")

no = st.number_input("Nota Organização Didático Pedagógica", 0.0, 5.0)
nf = st.number_input("Nota da Infraestrutura", 0.0, 5.0)
na = st.number_input("Nota de Oportunidades de Ampliação da Formação", 0.0, 5.0)

# -------------------------
# SEPARAÇÃO
# -------------------------
st.markdown("---")

# -------------------------
# CORPO DOCENTE
# -------------------------
st.subheader("Corpo docente (30%)")

total = st.number_input("Total de professores", 0.0)
dout = st.number_input("Quantidade de doutores", 0.0)
mest = st.number_input("Quantidade de mestres", 0.0)
regi = st.number_input("Regime de trabalho (TI/TP)", 0.0)

# -------------------------
# BOTÃO
# -------------------------
st.markdown("<br>", unsafe_allow_html=True)

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
