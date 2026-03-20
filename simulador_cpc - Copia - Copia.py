# ENADE
st.subheader("Nota do ENADE (20%)")
st.markdown("<div class='sub'>Desempenho dos estudantes</div>", unsafe_allow_html=True)

nc = st.number_input(
    "", min_value=0.0, max_value=5.0,
    value=None, placeholder="Digite", format="%.2f",
    key="enade"
)

# IDD
st.subheader("Nota do IDD (35%)")
st.markdown("<div class='sub'>Valor agregado pelo processo formativo</div>", unsafe_allow_html=True)

nidd = st.number_input(
    "", min_value=0.0, max_value=5.0,
    value=None, placeholder="Digite", format="%.2f",
    key="idd"
)

# QUESTIONÁRIO
no = st.number_input(
    "Nota Organização Didático Pedagógica",
    0.0, 5.0, value=None, placeholder="Digite", format="%.2f",
    key="org"
)

nf = st.number_input(
    "Nota da Infraestrutura",
    0.0, 5.0, value=None, placeholder="Digite", format="%.2f",
    key="infra"
)

na = st.number_input(
    "Nota de Oportunidades de Ampliação da Formação",
    0.0, 5.0, value=None, placeholder="Digite", format="%.2f",
    key="oport"
)

# DOCENTE
total = st.number_input("Total de professores", value=None, key="total")
dout = st.number_input("Quantidade de doutores", value=None, key="dout")
mest = st.number_input("Quantidade de mestres", value=None, key="mest")
regi = st.number_input("Regime de trabalho (TI/TP)", value=None, key="regi")
