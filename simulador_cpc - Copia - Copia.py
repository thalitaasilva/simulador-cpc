import streamlit as st
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ==========================
# CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(page_title="Simulador CPC | PUCPR", layout="centered")

# ==========================
# ESTILO CSS
# ==========================
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

/* ESPAÇO EXTRA */
.spacer {
    margin-top: 40px;
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

# ==========================
# HEADER
# ==========================
st.markdown("""
<div class='header'>
    <h1 style='color:white;'>Simulador CPC | PUCPR</h1>
</div>
""", unsafe_allow_html=True)

# ==========================
# FUNÇÕES
# ==========================
def calcular_nota_docente(p, tipo):
    metas = {"doutores": 0.80, "mestres": 1.00, "regime": 0.90}
    return min(5.0, (p / metas.get(tipo, 0.8)) * 5)

def gerar_pdf(dados):
    doc = SimpleDocTemplate("relatorio_cpc.pdf")
    styles = getSampleStyleSheet()
    elementos = []

    # Título
    elementos.append(Paragraph("<b>RELATÓRIO DE SIMULAÇÃO CPC</b>", styles['Title']))
    elementos.append(Spacer(1, 20))

    # ENADE e IDD
    elementos.append(Paragraph("<b>ENADE e IDD</b>", styles['Heading2']))
    elementos.append(Paragraph(f"Nota ENADE: {dados['nc']}", styles['Normal']))
    elementos.append(Paragraph(f"Nota IDD: {dados['nidd']}", styles['Normal']))
    elementos.append(Spacer(1, 15))

    # Questionário do Estudante
    elementos.append(Paragraph("<b>Questionário do Estudante</b>", styles['Heading2']))
    elementos.append(Paragraph(f"Organização Didático Pedagógica: {dados['no']}", styles['Normal']))
    elementos.append(Paragraph(f"Infraestrutura: {dados['nf']}", styles['Normal']))
    elementos.append(Paragraph(f"Oportunidades de Formação: {dados['na']}", styles['Normal']))
    elementos.append(Spacer(1, 15))

    # Corpo Docente
    elementos.append(Paragraph("<b>Corpo Docente</b>", styles['Heading2']))
    elementos.append(Paragraph(f"Total de professores: {dados['total']}", styles['Normal']))
    elementos.append(Paragraph(f"Doutores: {dados['dout']}", styles['Normal']))
    elementos.append(Paragraph(f"Mestres: {dados['mest']}", styles['Normal']))
    elementos.append(Paragraph(f"Regime de trabalho: {dados['regi']}", styles['Normal']))
    elementos.append(Spacer(1, 20))

    # Resultado Final
    elementos.append(Paragraph("<b>RESULTADO FINAL</b>", styles['Heading2']))
    elementos.append(Paragraph(f"CPC Contínuo: {dados['ncpc']}", styles['Normal']))
    elementos.append(Paragraph(f"Conceito: {dados['faixa']}", styles['Normal']))

    doc.build(elementos)

    return "relatorio_cpc.pdf"

# ==========================
# ENADE
# ==========================
st.subheader("Nota do ENADE (20%)")
st.markdown("<div class='sub'>Desempenho dos estudantes</div>", unsafe_allow_html=True)
nc = st.number_input("", min_value=0.0, max_value=5.0, value=None, placeholder="Digite aqui", format="%.3f", key="enade")

# ==========================
# IDD
# ==========================
st.subheader("Nota do IDD (35%)")
st.markdown("<div class='sub'>Valor agregado pelo processo formativo</div>", unsafe_allow_html=True)
nidd = st.number_input("", min_value=0.0, max_value=5.0, value=None, placeholder="Digite aqui", format="%.3f", key="idd")

st.markdown("---")

# ==========================
# QUESTIONÁRIO
# ==========================
st.subheader("Questionário do Estudante (15%)")
no = st.number_input("Nota Organização Didático Pedagógica", 0.0, 5.0, value=None, placeholder="Digite aqui", format="%.3f", key="org")
nf = st.number_input("Nota da Infraestrutura", 0.0, 5.0, value=None, placeholder="Digite aqui", format="%.3f", key="infra")
na = st.number_input("Nota de Oportunidades de Ampliação da Formação", 0.0, 5.0, value=None, placeholder="Digite aqui", format="%.3f", key="oport")

st.markdown("---")

# ==========================
# CORPO DOCENTE
# ==========================
st.subheader("Corpo docente (30%)")
total = st.number_input("Total de professores", min_value=0, value=None, step=1, format="%d", placeholder="Digite aqui", key="total")
dout = st.number_input("Quantidade de doutores", min_value=0, value=None, step=1, format="%d", placeholder="Digite aqui", key="dout")
mest = st.number_input("Quantidade de mestres", min_value=0, value=None, step=1, format="%d", placeholder="Digite aqui", key="mest")
regi = st.number_input("Regime de trabalho (TI/TP)", min_value=0, value=None, step=1, format="%d", placeholder="Digite aqui", key="regi")

# ==========================
# ESPAÇO ANTES DO BOTÃO
# ==========================
st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

# ==========================
# BOTÃO DE CALCULAR CPC
# ==========================
if st.button("🚀 CALCULAR CPC"):

    if None in [nc, nidd, no, nf, na, total, dout, mest, regi] or total == 0:
        st.error("Preencha todos os campos.")
    else:
        # Porcentagens docentes
        pd = dout / total
        pm = (dout + mest) / total
        pr = regi / total

        # Notas docentes
        nd = calcular_nota_docente(pd, "doutores")
        nm = calcular_nota_docente(pm, "mestres")
        nr = calcular_nota_docente(pr, "regime")

        # CPC final
        ncpc = (
            0.20 * nc + 0.35 * nidd + 0.15 * nd +
            0.075 * nm + 0.075 * nr +
            0.075 * no + 0.05 * nf + 0.025 * na
        )

        # Faixa conceitual
        faixa = 5 if ncpc >= 3.945 else 4 if ncpc >= 2.945 else 3 if ncpc >= 1.945 else 2

        # Mantém o número completo
        ncpc_str = str(round(ncpc, 4))

        # Mostra resultado na tela
        st.markdown(f"""
        <div class='resultado'>
            <h1>{ncpc_str}</h1>
            <h3>CONCEITO {faixa}</h3>
        </div>
        """, unsafe_allow_html=True)

        # Dados para PDF
        dados = {
            "nc": nc,
            "nidd": nidd,
            "no": no,
            "nf": nf,
            "na": na,
            "total": total,
            "dout": dout,
            "mest": mest,
            "regi": regi,
            "ncpc": ncpc_str,
            "faixa": faixa
        }

        # Botão para baixar PDF
        with open(gerar_pdf(dados), "rb") as f:
            st.download_button("📥 Baixar PDF", f, "relatorio_cpc.pdf")
