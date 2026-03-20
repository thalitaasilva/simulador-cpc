import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Simulador CPC | PUCPR", layout="centered")

st.markdown("<h1 style='color:#8a0538;'>Simulador CPC | PUCPR</h1>", unsafe_allow_html=True)

# -------------------------
# FUNÇÃO DOCENTE
# -------------------------
def calcular_nota_docente(proporcao_real, tipo):
    metas = {
        "doutores": 0.80,
        "mestres": 1.00,
        "regime": 0.90
    }
    meta = metas.get(tipo, 0.80)
    nota = (proporcao_real / meta) * 5
    return min(5.0, max(0.0, nota))

# -------------------------
# FUNÇÃO PDF
# -------------------------
def gerar_pdf(ncpc, faixa):
    doc = SimpleDocTemplate("relatorio_cpc.pdf")
    styles = getSampleStyleSheet()

    elementos = []

    elementos.append(Paragraph("Relatório CPC - PUCPR", styles['Title']))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph(f"CPC Contínuo: {ncpc}", styles['Normal']))
    elementos.append(Paragraph(f"Conceito: {faixa}", styles['Normal']))

    doc.build(elementos)

    return "relatorio_cpc.pdf"

# -------------------------
# CONTROLE DE CASAS DECIMAIS
# -------------------------
casas = st.selectbox("Casas decimais", [2, 3, 4], index=2)

# -------------------------
# INPUTS
# -------------------------
st.subheader("📊 Indicadores de Qualidade (0 a 5)")

nc = st.number_input("Nota Enade", min_value=0.0, max_value=5.0, value=None, placeholder="Digite")
nidd = st.number_input("Nota IDD", min_value=0.0, max_value=5.0, value=None, placeholder="Digite")
no = st.number_input("Organização Didático-Pedagógica", min_value=0.0, max_value=5.0, value=None, placeholder="Digite")
nf = st.number_input("Infraestrutura", min_value=0.0, max_value=5.0, value=None, placeholder="Digite")
na = st.number_input("Oportunidades", min_value=0.0, max_value=5.0, value=None, placeholder="Digite")

st.subheader("👨‍🏫 Corpo Docente")

total = st.number_input("Total de Professores", min_value=0.0, value=None, placeholder="Digite")
dout = st.number_input("Qtd Doutores", min_value=0.0, value=None, placeholder="Digite")
mest = st.number_input("Qtd Mestres", min_value=0.0, value=None, placeholder="Digite")
regi = st.number_input("Professores TI/TP", min_value=0.0, value=None, placeholder="Digite")

# -------------------------
# BOTÃO
# -------------------------
if st.button("CALCULAR CPC"):

    # Validação
    if None in [nc, nidd, no, nf, na, total, dout, mest, regi]:
        st.error("Preencha todos os campos.")
    elif total <= 0:
        st.error("Total de professores inválido.")
    else:
        try:
            # Proporções
            pd = dout / total
            pm = (dout + mest) / total
            pr = regi / total

            # Notas docentes
            nd = calcular_nota_docente(pd, "doutores")
            nm = calcular_nota_docente(pm, "mestres")
            nr = calcular_nota_docente(pr, "regime")

            # Cálculo CPC
            ncpc = (
                (0.20 * nc) +
                (0.35 * nidd) +
                (0.15 * nd) +
                (0.075 * nm) +
                (0.075 * nr) +
                (0.075 * no) +
                (0.05 * nf) +
                (0.025 * na)
            )

            # Faixa
            if ncpc >= 3.945:
                faixa = 5
                cor = "#9654FF"
            elif ncpc >= 2.945:
                faixa = 4
                cor = "#8a0538"
            elif ncpc >= 1.945:
                faixa = 3
                cor = "#d4a017"
            else:
                faixa = 2
                cor = "#ff0040"

            valor_formatado = round(ncpc, casas)

            # -------------------------
            # RESULTADO
            # -------------------------
            st.markdown(f"""
            <h1 style='text-align:center; color:{cor};'>
            {valor_formatado}
            </h1>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <h3 style='text-align:center; color:{cor};'>
            CONCEITO {faixa}
            </h3>
            """, unsafe_allow_html=True)

            # -------------------------
            # PDF
            # -------------------------
            arquivo_pdf = gerar_pdf(valor_formatado, faixa)

            with open(arquivo_pdf, "rb") as f:
                st.download_button(
                    label="📥 Baixar Relatório em PDF",
                    data=f,
                    file_name="relatorio_cpc.pdf",
                    mime="application/pdf"
                )

        except:
            st.error("Erro no cálculo. Verifique os dados.")
