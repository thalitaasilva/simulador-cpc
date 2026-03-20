import streamlit as st
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Simulador CPC | PUCPR", layout="centered")

# -------------------------
# ESTILO GLOBAL
# -------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #ffffff, #f3e8ff);
}

div.stButton > button {
    background: linear-gradient(90deg, #8a0538, #9654FF);
    color: white;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.markdown("""
<div style='background: linear-gradient(90deg, #8a0538, #9654FF);
            padding:20px;
            border-radius:12px;
            text-align:center;
            margin-bottom:20px'>
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


def gerar_pdf(ncpc, faixa, nc, nidd, no, nf, na, total, dout, mest, regi, nd, nm, nr):
    doc = SimpleDocTemplate("relatorio_cpc.pdf")
    styles = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("Relatório CPC - PUCPR", styles['Title']))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph(f"CPC Contínuo: {ncpc:.4f}", styles['Normal']))
    elementos.append(Paragraph(f"Conceito: {faixa}", styles['Normal']))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("Indicadores", styles['Heading2']))
    elementos.append(Paragraph(f"Enade: {nc}", styles['Normal']))
    elementos.append(Paragraph(f"IDD: {nidd}", styles['Normal']))
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

    elementos.append(Paragraph("Simulação Docente", styles['Heading2']))
    elementos.append(Paragraph(f"Doutores: {nd:.2f}", styles['Normal']))
    elementos.append(Paragraph(f"Mestres: {nm:.2f}", styles['Normal']))
    elementos.append(Paragraph(f"Regime: {nr:.2f}", styles['Normal']))

    doc.build(elementos)
    return "relatorio_cpc.pdf"


# -------------------------
# CARD 1 - INDICADORES
# -------------------------
st.markdown("<div style='background:white;padding:20px;border-radius:12px;box-shadow:0px 4px 12px rgba(0,0,0,0.1);margin-bottom:15px'>", unsafe_allow_html=True)

st.subheader("📊 Indicadores de Qualidade")

nc = st.number_input("Nota Enade", 0.0, 5.0, value=None, placeholder="Digite")
nidd = st.number_input("Nota IDD", 0.0, 5.0, value=None, placeholder="Digite")
no = st.number_input("Org. Didática", 0.0, 5.0, value=None, placeholder="Digite")
nf = st.number_input("Infraestrutura", 0.0, 5.0, value=None, placeholder="Digite")
na = st.number_input("Oportunidades", 0.0, 5.0, value=None, placeholder="Digite")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# CARD 2 - DOCENTE
# -------------------------
st.markdown("<div style='background:white;padding:20px;border-radius:12px;box-shadow:0px 4px 12px rgba(0,0,0,0.1);margin-bottom:15px'>", unsafe_allow_html=True)

st.subheader("👨‍🏫 Corpo Docente")

total = st.number_input("Total Professores", 0.0, value=None, placeholder="Digite")
dout = st.number_input("Doutores", 0.0, value=None, placeholder="Digite")
mest = st.number_input("Mestres", 0.0, value=None, placeholder="Digite")
regi = st.number_input("TI/TP", 0.0, value=None, placeholder="Digite")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# BOTÃO
# -------------------------
if st.button("CALCULAR CPC"):

    if None in [nc, nidd, no, nf, na, total, dout, mest, regi]:
        st.error("Preencha todos os campos.")
    elif total <= 0:
        st.error("Total inválido.")
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
            faixa, cor = 3, "#d4a017"
        else:
            faixa, cor = 2, "#ff0040"

        # RESULTADO CARD
        st.markdown(f"""
        <div style='background:white;padding:30px;border-radius:15px;text-align:center;
                    box-shadow:0px 6px 20px rgba(0,0,0,0.15)'>
            <h1 style='color:{cor}; font-size:50px'>{ncpc:.4f}</h1>
            <h3 style='color:{cor};'>CONCEITO {faixa}</h3>
        </div>
        """, unsafe_allow_html=True)

        # PROGRESSO
        st.progress(min(ncpc / 5, 1.0))

        # MENSAGEM
        if faixa < 4:
            st.warning("⚠️ Curso abaixo do ideal para CPC 4")
        else:
            st.success("🎯 Curso com bom desempenho!")

        # GRÁFICO
        df = pd.DataFrame({
            "Indicadores": ["Enade", "IDD", "Org.", "Infra", "Oport."],
            "Notas": [nc, nidd, no, nf, na]
        })
        st.bar_chart(df.set_index("Indicadores"))

        # PDF
        arquivo_pdf = gerar_pdf(ncpc, faixa, nc, nidd, no, nf, na, total, dout, mest, regi, nd, nm, nr)

        with open(arquivo_pdf, "rb") as f:
            st.download_button("📥 Salvar em PDF", f, "relatorio_cpc.pdf")
