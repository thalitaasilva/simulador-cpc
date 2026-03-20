import streamlit as st
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Simulador CPC | PUCPR", layout="centered")

# ESTILIZAÇÃO CSS OTIMIZADA
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
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.sub {
    font-size: 13px;
    color: #666;
    margin-bottom: 15px;
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
    transition: 0.3s;
}

div.stButton > button:hover {
    opacity: 0.9;
    transform: scale(1.02);
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
    box-shadow: 0 10px 25px rgba(0,0,0,0.05);
}

.resultado h1 {
    font-size: 52px;
    color: #8a0538;
    margin: 10px 0;
}

.badge {
    display:inline-block;
    padding:10px 30px;
    background:linear-gradient(90deg, #8a0538, #ff0040);
    color:white;
    border-radius:30px;
    font-weight:bold;
    font-size:20px;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class='header'>
    <h1 style='color:white; margin:0;'>Simulador CPC | PUCPR</h1>
</div>
""", unsafe_allow_html=True)

# FUNÇÕES DE CÁLCULO E PDF
def calcular_nota_docente(p, tipo):
    metas = {"doutores": 0.80, "mestres": 1.00, "regime": 0.90}
    return min(5.0, (p / metas.get(tipo, 0.8)) * 5)

def gerar_pdf(ncpc, faixa, dados):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("SIMULAÇÃO CPC - RELATÓRIO COMPLETO", styles['Title']))
    elementos.append(Spacer(1, 20))

    secoes = [
        ("1. DESEMPENHO DOS ESTUDANTES", [f"Nota ENADE: {dados['Nota ENADE']}", f"Nota IDD: {dados['Nota IDD']}"]),
        ("2. QUESTIONÁRIO DO ESTUDANTE", [f"Org. Didático Pedagógica: {dados['Org. Didático Pedagógica']}", f"Infraestrutura: {dados['Infraestrutura']}", f"Oportunidades: {dados['Oportunidades']}"]),
        ("3. CORPO DOCENTE", [f"Total: {dados['Total Docentes']}", f"Doutores: {dados['Doutores']} ({dados['Proporção Doutores']:.1%})", f"Mestres: {dados['Mestres']} ({dados['Proporção Mestres']:.1%})", f"Regime: {dados['Regime']} ({dados['Proporção Regime']:.1%})"]),
        ("4. RESULTADO FINAL", [f"CPC Contínuo: {ncpc:.4f}", f"Conceito Faixa: {faixa}"])
    ]

    for titulo, linhas in secoes:
        elementos.append(Paragraph(titulo, styles['Heading2']))
        for linha in linhas:
            elementos.append(Paragraph(linha, styles['Normal']))
        elementos.append(Spacer(1, 12))

    doc.build(elementos)
    return buffer.getvalue()

def parse_int(valor):
    try:
        return int(''.join(filter(str.isdigit, str(valor))))
    except:
        return None

# INPUTS ORGANIZADOS POR COLUNAS
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🎓 Notas Oficiais (Inep)")
    nc = st.number_input("Nota ENADE (20%)", 0.0, 5.0, value=0.0, step=0.01)
    nidd = st.number_input("Nota IDD (35%)", 0.0, 5.0, value=0.0, step=0.01)

with col_b:
    st.subheader("📝 Questionário Estudante")
    no = st.number_input("Org. Didático Pedagógica (7.5%)", 0.0, 5.0, value=0.0)
    nf = st.number_input("Infraestrutura (5.0%)", 0.0, 5.0, value=0.0)
    na = st.number_input("Oportunidades (2.5%)", 0.0, 5.0, value=0.0)

st.markdown("---")

st.subheader("👨‍🏫 Corpo Docente (30%)")
c1, c2, c3, c4 = st.columns(4)
total_input = c1.text_input("Total Profs", placeholder="Ex: 45")
dout_input = c2.text_input("Doutores", placeholder="Ex: 30")
mest_input = c3.text_input("Mestres", placeholder="Ex: 10")
regi_input = c4.text_input("Regime (TI/TP)", placeholder="Ex: 38")

total = parse_int(total_input)
dout = parse_int(dout_input)
mest = parse_int(mest_input)
regi = parse_int(regi_input)

st.markdown("<br>", unsafe_allow_html=True)

# BOTÃO DE CÁLCULO
if st.button("🚀 CALCULAR CONCEITO"):
    
    if not total or total == 0:
        st.error("Insira a quantidade total de professores para realizar o cálculo.")
    else:
        # Cálculo de Proporções e Notas Docentes
        pd = dout / total
        pm = (dout + mest) / total  # Metodologia INEP considera Mestres + Doutores para nota de Mestrado
        pr = regi / total

        nd = calcular_nota_docente(pd, "doutores")
        nm = calcular_nota_docente(pm, "mestres")
        nr = calcular_nota_docente(pr, "regime")

        # Fórmula CPC Contínuo (Pesos Oficiais)
        ncpc = (0.20 * nc) + (0.35 * nidd) + (0.15 * nd) + (0.075 * nm) + (0.075 * nr) + (0.075 * no) + (0.05 * nf) + (0.025 * na)

        # Lógica de Faixa (Conceito Preliminar)
        if ncpc >= 3.945: faixa = 5
        elif ncpc >= 2.945: faixa = 4
        elif ncpc >= 1.945: faixa = 3
        elif ncpc >= 0.945: faixa = 2
        else: faixa = 1

        # EXIBIÇÃO DO RESULTADO
        st.markdown(f"""
        <div class='resultado'>
            <div style='font-size:14px; color:#888; font-weight:bold;'>CPC CONTÍNUO ESTIMADO</div>
            <h1>{ncpc:.4f}</h1>
            <div class='badge'>CONCEITO FAIXA {faixa}</div>
        </div>
        """, unsafe_allow_html=True)

        # GERAÇÃO DO PDF PARA DOWNLOAD
        dados_simulacao = {
            "Nota ENADE": nc, "Nota IDD": nidd, "Org. Didático Pedagógica": no,
            "Infraestrutura": nf, "Oportunidades": na, "Total Docentes": total,
            "Doutores": dout, "Mestres": mest, "Regime": regi,
            "Proporção Doutores": pd, "Proporção Mestres": pm, "Proporção Regime": pr
        }

        pdf_bytes = gerar_pdf(ncpc, faixa, dados_simulacao)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="📥 Baixar Relatório Detalhado (PDF)",
            data=pdf_bytes,
            file_name=f"Relatorio_CPC_{faixa}.pdf",
            mime="application/pdf"
        )
