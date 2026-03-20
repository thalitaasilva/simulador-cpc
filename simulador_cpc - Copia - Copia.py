import streamlit as st
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Simulador CPC | PUCPR", layout="centered")

# ESTILIZAÇÃO CSS (Ajustada para o novo layout)
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
    margin-bottom: 40px;
}

/* Espaçamento entre seções */
.section-spacer {
    margin-top: 40px;
}

div.stButton > button {
    background: linear-gradient(90deg, #8a0538, #ff0040);
    color: white;
    border-radius: 12px;
    height: 3.5em;
    width: 100%;
    font-weight: bold;
    font-size: 18px;
    border: none;
    margin-top: 30px;
}

.resultado {
    background: white;
    padding: 30px;
    border-radius: 20px;
    border: 1px solid #e0e0e0;
    margin-top: 25px;
    display: flex;
    flex-direction: column;
    align-items: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.resultado h1 {
    font-size: 52px;
    color: #8a0538;
    margin: 10px 0;
}

.badge {
    display:inline-block;
    padding: 10px 30px;
    background: linear-gradient(90deg, #8a0538, #ff0040);
    color: white;
    border-radius: 30px;
    font-weight: bold;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("<div class='header'><h1 style='color:white; margin:0;'>Simulador CPC | PUCPR</h1></div>", unsafe_allow_html=True)

# --- SEÇÃO 1: NOTA ENADE E IDD (Lado a Lado) ---
col_e, col_i = st.columns(2)
with col_e:
    nc = st.number_input("Nota ENADE (20%)", 0.0, 5.0, value=0.0, step=0.01)
with col_i:
    nidd = st.number_input("Nota IDD (35%)", 0.0, 5.0, value=0.0, step=0.01)

st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

# --- SEÇÃO 2: QUESTIONÁRIO DO ESTUDANTE (Em uma linha só) ---
st.subheader("📝 Questionário Estudante (15%)")
q1, q2, q3 = st.columns(3)

with q1:
    no = st.number_input("Org. Didático Pedagógica", 0.0, 5.0, value=0.0)
with q2:
    nf = st.number_input("Infraestrutura", 0.0, 5.0, value=0.0)
with q3:
    na = st.number_input("Oportunidades", 0.0, 5.0, value=0.0)

st.markdown("---")

# --- SEÇÃO 3: CORPO DOCENTE (30%) ---
st.subheader("👨‍🏫 Corpo Docente")
c1, c2, c3, c4 = st.columns(4)

def parse_int(valor):
    try:
        return int(''.join(filter(str.isdigit, str(valor))))
    except:
        return None

total = parse_int(c1.text_input("Total Profs"))
dout = parse_int(c2.text_input("Doutores"))
mest = parse_int(c3.text_input("Mestres"))
regi = parse_int(c4.text_input("Regime (TI/TP)"))

# FUNÇÕES TÉCNICAS
def calcular_nota_docente(p, tipo):
    metas = {"doutores": 0.80, "mestres": 1.00, "regime": 0.90}
    return min(5.0, (p / metas.get(tipo, 0.8)) * 5)

def gerar_pdf(ncpc, faixa, dados):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elementos = [Paragraph("RELATÓRIO SIMULAÇÃO CPC", styles['Title']), Spacer(1, 20)]
    
    # Detalhes básicos para o relatório
    texto = f"CPC Contínuo: {ncpc:.4f} | Conceito: {faixa}"
    elementos.append(Paragraph(texto, styles['Normal']))
    
    doc.build(elementos)
    return buffer.getvalue()

# BOTÃO CALCULAR
if st.button("CALCULAR"):
    if not total or total == 0:
        st.error("Por favor, preencha o campo 'Total de Professores'.")
    else:
        # Cálculo de Proporções e Notas Insumo
        pd = dout / total
        pm = (dout + mest) / total
        pr = regi / total

        nd = calcular_nota_docente(pd, "doutores")
        nm = calcular_nota_docente(pm, "mestres")
        nr = calcular_nota_docente(pr, "regime")

        # Fórmula CPC Oficial
        ncpc = (0.20 * nc) + (0.35 * nidd) + (0.15 * nd) + (0.075 * nm) + (0.075 * nr) + (0.075 * no) + (0.05 * nf) + (0.025 * na)
        
        # Faixas Inep
        if ncpc >= 3.945: faixa = 5
        elif ncpc >= 2.945: faixa = 4
        elif ncpc >= 1.945: faixa = 3
        elif ncpc >= 0.945: faixa = 2
        else: faixa = 1

        # RESULTADO VISUAL
        st.markdown(f"""
        <div class='resultado'>
            <div style='font-size:14px; color:#888; font-weight:bold;'>CPC CONTÍNUO ESTIMADO</div>
            <h1>{ncpc:.4f}</h1>
            <div class='badge'>CONCEITO {faixa}</div>
        </div>
        """, unsafe_allow_html=True)

        # PDF DOWNLOAD
        dados_simulacao = {
            "Nota ENADE": nc, "Nota IDD": nidd, "Org. Didático Pedagógica": no,
            "Infraestrutura": nf, "Oportunidades": na, "Total Docentes": total,
            "Doutores": dout, "Mestres": mest, "Regime": regi
        }
        pdf_bytes = gerar_pdf(ncpc, faixa, dados_simulacao)
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button("📥 Baixar Relatório (PDF)", pdf_bytes, "relatorio_cpc.pdf", "application/pdf")
