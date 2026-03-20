import streamlit as st
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

h1 a, h2 a, h3 a, h4 a {
    display: none !important;
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
    border-radius: 15px;
    height: 4em;
    width: 100%;
    font-weight: bold;
    font-size: 18px;
}

.spacer {
    margin-top: 40px;
}

.resultado {
    background: white;
    padding: 35px;
    border-radius: 20px;
    margin-top: 25px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.resultado h1 {
    font-size: 48px;
    color: #8a0538;
    margin-bottom: 10px;
    text-align: center;
}

.badge {
    display:inline-block;
    padding:12px 30px;
    background:linear-gradient(90deg, #8a0538, #ff0040);
    color:white;
    border-radius:30px;
    font-weight:bold;
    font-size:18px;
    margin-top:10px;
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

def gerar_pdf(ncpc, faixa, dados):
    doc = SimpleDocTemplate("relatorio_cpc.pdf")
    styles = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("SIMULAÇÃO CPC - RELATÓRIO COMPLETO", styles['Title']))
    elementos.append(Spacer(1, 16))

    elementos.append(Paragraph("1. DESEMPENHO DOS ESTUDANTES", styles['Heading2']))
    elementos.append(Spacer(1, 8))
    elementos.append(Paragraph(f"Nota ENADE: {dados['Nota ENADE']}", styles['Normal']))
    elementos.append(Paragraph(f"Nota IDD: {dados['Nota IDD']}", styles['Normal']))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("2. QUESTIONÁRIO DO ESTUDANTE", styles['Heading2']))
    elementos.append(Spacer(1, 8))
    elementos.append(Paragraph(f"Org. Didático Pedagógica: {dados['Org. Didático Pedagógica']}", styles['Normal']))
    elementos.append(Paragraph(f"Infraestrutura: {dados['Infraestrutura']}", styles['Normal']))
    elementos.append(Paragraph(f"Oportunidades: {dados['Oportunidades']}", styles['Normal']))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("3. CORPO DOCENTE", styles['Heading2']))
    elementos.append(Spacer(1, 8))
    elementos.append(Paragraph(f"Total: {dados['Total Docentes']}", styles['Normal']))
    elementos.append(Paragraph(f"Doutores: {dados['Doutores']} ({dados['Proporção Doutores']})", styles['Normal']))
    elementos.append(Paragraph(f"Mestres: {dados['Mestres']} ({dados['Proporção Mestres']})", styles['Normal']))
    elementos.append(Paragraph(f"Regime: {dados['Regime']} ({dados['Proporção Regime']})", styles['Normal']))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("4. RESULTADO FINAL", styles['Heading2']))
    elementos.append(Spacer(1, 8))
    elementos.append(Paragraph(f"CPC Contínuo: {ncpc}", styles['Normal']))
    elementos.append(Paragraph(f"Conceito: {faixa}", styles['Normal']))

    doc.build(elementos)
    return "relatorio_cpc.pdf"

# ==========================
# FUNÇÃO AUXILIAR PARA INTEIROS
# ==========================
def parse_int(valor):
    try:
        return int(valor.replace(".", ""))
    except:
        return None

# ==========================
# INPUTS DO USUÁRIO
# ==========================
st.subheader("Nota do ENADE (20%)")
st.markdown("<div class='sub'>Desempenho dos estudantes</div>", unsafe_allow_html=True)
nc_input = st.text_input("", placeholder="Digite aqui")
try:
    nc = float(nc_input)
except:
    nc = None

st.subheader("Nota do IDD (35%)")
st.markdown("<div class='sub'>Valor agregado pelo processo formativo</div>", unsafe_allow_html=True)
nidd_input = st.text_input("", placeholder="Digite aqui")
try:
    nidd = float(nidd_input)
except:
    nidd = None

st.markdown("---")

st.subheader("Questionário do Estudante (15%)")
no_input = st.text_input("Nota Organização Didático Pedagógica", placeholder="Digite aqui")
nf_input = st.text_input("Nota da Infraestrutura", placeholder="Digite aqui")
na_input = st.text_input("Nota de Oportunidades de Ampliação da Formação", placeholder="Digite aqui")
try:
    no = float(no_input)
except:
    no = None
try:
    nf = float(nf_input)
except:
    nf = None
try:
    na = float(na_input)
except:
    na = None

st.markdown("---")

st.subheader("Corpo docente (30%)")
total_input = st.text_input("Total de professores", placeholder="Digite aqui")
dout_input = st.text_input("Quantidade de doutores", placeholder="Digite aqui")
mest_input = st.text_input("Quantidade de mestres", placeholder="Digite aqui")
regi_input = st.text_input("Regime de trabalho (TI/TP)", placeholder="Digite aqui")

total = parse_int(total_input)
dout = parse_int(dout_input)
mest = parse_int(mest_input)
regi = parse_int(regi_input)

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

# ==========================
# BOTÃO CALCULAR
# ==========================
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
        ncpc_str = str(ncpc)  # mantém o número completo, ex: 3.409

        st.markdown(f"""
        <div class='resultado'>
            <h1>{ncpc_str}</h1>
            <h3>CONCEITO {faixa}</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

        dados_simulacao = {
            "Nota ENADE": nc,
            "Nota IDD": nidd,
            "Org. Didático Pedagógica": no,
            "Infraestrutura": nf,
            "Oportunidades": na,
            "Total Docentes": total,
            "Doutores": dout,
            "Mestres": mest,
            "Regime": regi,
            "Proporção Doutores": round(pd, 3),
            "Proporção Mestres": round(pm, 3),
            "Proporção Regime": round(pr, 3),
        }

        with open(gerar_pdf(ncpc_str, faixa, dados_simulacao), "rb") as f:
            st.download_button("📥 Baixar PDF", f, "relatorio_cpc.pdf")
