import streamlit as st

# Função docente (mantida)
def calcular_nota_docente(proporcao_real, tipo):
    metas = {"doutores": 0.80, "mestres": 0.95, "regime": 0.80}
    meta = metas.get(tipo, 0.80)
    nota = (proporcao_real / meta) * 5
    return min(5.0, max(0.0, nota))

st.set_page_config(page_title="Simulador CPC", layout="centered")

st.title("🎓 Simulador de CPC - CAIQ")

# ------------------------
# Indicadores
# ------------------------
st.subheader("Indicadores de Qualidade (0-5)")

nc = st.number_input("Nota Enade", min_value=0.0, max_value=5.0)
nidd = st.number_input("Nota IDD", min_value=0.0, max_value=5.0)
no = st.number_input("Org. Didática", min_value=0.0, max_value=5.0)
nf = st.number_input("Infraestrutura", min_value=0.0, max_value=5.0)
na = st.number_input("Oportunidades", min_value=0.0, max_value=5.0)

# ------------------------
# Corpo docente
# ------------------------
st.subheader("Corpo Docente")

total = st.number_input("Total de Professores", min_value=0.0)
dout = st.number_input("Qtd Doutores", min_value=0.0)
mest = st.number_input("Qtd Mestres", min_value=0.0)
regi = st.number_input("Qtd TI/TP", min_value=0.0)

# ------------------------
# Botão calcular
# ------------------------
if st.button("CALCULAR"):
    try:
        if total <= 0:
            st.error("Total de professores inválido.")
        else:
            pd = dout / total
            pm = (dout + mest) / total
            pr = regi / total

            nd = calcular_nota_docente(pd, "doutores")
            nm = calcular_nota_docente(pm, "mestres")
            nr = calcular_nota_docente(pr, "regime")

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

            st.markdown(f"## Resultado: **{ncpc:.4f}**")
            st.markdown(f"### Conceito: :{cor}[{faixa}]")

    except:
        st.error("Preencha todos os campos corretamente.")