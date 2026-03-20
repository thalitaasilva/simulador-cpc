import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Simulador CPC | PUCPR", layout="centered")

st.title("🎓 Simulador CPC | PUCPR")

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
def gerar_pdf(ncpc, faixa, nc, nidd, no, nf, na, total, dout, mest, regi):
    doc = SimpleDocTemplate("relatorio_cpc.pdf")
    styles = getSampleStyleSheet()

    elementos = []

    elementos.append(Paragraph("Relatório CPC - PUCPR", styles['Title']))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph(f"CPC Contínuo: {ncpc:.4f}", styles['Normal']))
    elementos.append(Paragraph(f"Conceito: {faixa}", styles['Normal']))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("Indicadores:", styles['Heading2']))
    elementos.append(Paragraph(f"Enade: {nc}", styles['Normal']))
    elementos.append(Paragraph(f"IDD: {nidd}", styles['Normal']))
    elementos.append(Paragraph(f"Org. Didática: {no}", styles['Normal']))
    elementos.append(Paragraph(f"Infraestrutura: {nf}", styles['Normal']))
    elementos.append(Paragraph(f"Oportunidades: {na}", styles['Normal']))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("Corpo Docente:", styles['Heading2']))
    elementos.append(Paragraph(f"Total: {total}", styles['Normal']))
    elementos.append(Paragraph(f"Doutores: {dout}", styles['Normal']))
    elementos.append(Paragraph(f"Mestres: {mest}", styles['Normal']))
    elementos.append(Paragraph(f"TI/TP: {regi}", styles['Normal']))

    doc.build(elementos)

    return "relatorio_cpc.pdf"

# -------------------------
# INPUTS
# -------------------------
st.subheader("📊 Indicadores de Qualidade (0 a 5)")

nc = st.number_input("Nota Enade", 0.0, 5.0)
nidd = st.number_input("Nota IDD", 0.0, 5.0)
no = st.number_input("Organização Didático-Pedagógica", 0.0, 5.0)
nf = st.number_input("Infraestrutura", 0.0, 5.0)
na = st.number_input("Oportunidades", 0.0, 5.0)

st.subheader("👨‍🏫 Corpo Docente")

total = st.number_input("Total de Professores", 0.0)
dout = st.number_input("Qtd Doutores", 0.0)
mest = st.number_input("Qtd Mestres", 0.0)
regi = st.number_input("Professores TI/TP", 0.0)

st.subheader("📊 Histórico")

cpc_anterior = st.number_input("CPC anterior", 0.0, 5.0)

# -------------------------
# BOTÃO
# -------------------------
if st.button("CALCULAR CPC"):

    if total <= 0:
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
                cor = "green"
            elif ncpc >= 2.945:
                faixa = 4
                cor = "limegreen"
            elif ncpc >= 1.945:
                faixa = 3
                cor = "orange"
            else:
                faixa = 2
                cor = "red"

            # -------------------------
            # RESULTADO
            # -------------------------
            st.markdown(f"## Resultado: **{ncpc:.4f}**")
            st.markdown(f"### Conceito: :{cor}[{faixa}]")

            # -------------------------
            # COMPARAÇÃO
            # -------------------------
            if cpc_anterior > 0:
                diferenca = ncpc - cpc_anterior

                col1, col2, col3 = st.columns(3)

                col1.metric("CPC Atual", f"{ncpc:.4f}")
                col2.metric("CPC Anterior", f"{cpc_anterior:.4f}")
                col3.metric("Evolução", f"{diferenca:.4f}", delta=f"{diferenca:.4f}")

            # -------------------------
            # PDF
            # -------------------------
            arquivo_pdf = gerar_pdf(ncpc, faixa, nc, nidd, no, nf, na, total, dout, mest, regi)

            with open(arquivo_pdf, "rb") as f:
                st.download_button(
                    label="📥 Baixar Relatório em PDF",
                    data=f,
                    file_name="relatorio_cpc.pdf",
                    mime="application/pdf"
                )

        except:
            st.error("Preencha todos os campos corretamente.")
