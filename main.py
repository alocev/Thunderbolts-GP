import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

#carregamento de dados
if "df" not in st.session_state:
    st.session_state.df = df = pd.read_csv('database/membros_gp_fakes.csv', sep = ',')

#configuração da página
st.set_page_config(
    page_title= "Gestão de Equipes",
    page_icon= "🗃️",
    layout= "wide")

#configuração sidebar
st.sidebar.title("Navegação")
aba = st.sidebar.radio("Ir para:", ["👤 Visualizar Membros", "➕ Adicionar Novo", "⚙️ Configurações Extras"])

#visualizar membros
if aba == "👤 Visualizar Membros":
    st.subheader("Lista de Membros")
    equipes = sorted(st.session_state.df["EQUIPE DE PROJETO"].dropna().unique())
    equipe_select = st.selectbox("Filtrar por Equipe:", ["Todas"] + equipes)
    #busca por nome
    busca_nome = st.text_input("Buscar por nome:").strip()
    df_filtrado = st.session_state.df.copy()
    if equipe_select != "Todas":
        df_filtrado = df_filtrado[df_filtrado["EQUIPE DE PROJETO"] == equipe_select]
    if busca_nome:
        df_filtrado = df_filtrado[df_filtrado["NOME"].str.contains(busca_nome, case = False, na = False)]
    #exibir cards
    st.subheader(f"Resultados encontrados: {len(df_filtrado)}")
    for _, membro in df_filtrado.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                try:
                    response = requests.get(membro["IMAGEM_USUÁRIO"])
                    avatar = Image.open(BytesIO(response.content))
                    st.image(avatar, width=195)
                except:
                    st.write("[sem avatar]")
            with col2:
                status_key = f"status_{membro['MATRÍCULA']}"
                status_ativo = st.toggle("Ativo", value=(membro["STATUS"].strip().lower() == "ativo"), key=status_key)
                cor_status = "limegreen" if status_ativo else "tomato"
                texto_status = "Ativo" if status_ativo else "Inativo"
                st.markdown(f"""
                <div style="background-color:#2c2c2c;padding:20px;border-radius:12px">
                    <h3 style="margin-bottom:5px;">{membro["NOME"]}</h3>
                    <p><strong>Curso:</strong> {membro["CURSO"]} &nbsp;|&nbsp;
                    <strong>Equipe:</strong> {membro["EQUIPE DE PROJETO"]} &nbsp;|&nbsp;
                    <strong>Status:</strong> <span style="color:{cor_status}; font-weight:bold">{texto_status}</span></p>
                    <hr style="margin:10px 0;"> <p>
                    <strong>Email:</strong> {membro["EMAIL"]}<br>
                    <strong>Contato:</strong> {membro["CONTATO"]}<br>
                    <strong>CPF:</strong> {membro["CPF"]}<br>
                    <strong>Lattes:</strong> {membro["LATTES"]}<br>
                    <strong>Nascimento:</strong> {membro["DATA NASCIMENTO"]}<br>
                    <strong>Matrícula:</strong> {membro["MATRÍCULA"]}<br>
                    <strong>Série:</strong> {membro["SÉRIE"]} &nbsp;|&nbsp;
                    <strong>Tam. Camiseta:</strong> {membro["TAMANHO CAMISETA"]}<br>
                    <strong>Escolaridade:</strong> {membro["NÍVEL ESCOLARIDADE"]}<br>
                    <strong>Status Curso:</strong> {membro["STATUS CURSO"]}<br>
                    <strong>Tipo:</strong> {membro["TIPO MEMBRO"]}<br>
                    <strong>Rank GP:</strong> {membro["RANK GP"]}<br>
                    <strong>Orientador:</strong> {membro["ORIENTADOR"]}
                    </p>
                </div> """, unsafe_allow_html=True)
        st.divider()

#adicionar novo
elif aba == "➕ Adicionar Novo":
    st.title("Adicionar novo")
    options = st.radio("O que deseja adicionar?", ["Membro", "Equipe"], horizontal=True)
    if options == "Membro":
        with st.form("form_membro"):
            st.subheader("Novo Membro")
            nome = st.text_input("Nome completo")
            id = st.text_input("ID")
            cpf = st.text_input("CPF")
            email = st.text_input("Email")
            contato = st.text_input("Telefone de contato")
            lattes = st.text_input("Lattes")
            matricula = st.text_input("Matrícula")
            tamanho_camiseta = st.selectbox("Tamanho da camiseta", ["PP", "P", "M", "G", "GG", "XGG"])
            data_nascimento = st.date_input("Data de nascimento")
            equipe_projeto = st.selectbox("Equipe do projeto", options=st.session_state.df["EQUIPE DE PROJETO"].unique())
            orientador = st.text_input("Orientador")
            serie = st.selectbox("Série", ["1º ano", "2º ano", "3º ano"])
            ano = st.number_input("Ano", min_value=2020, max_value=2030, step=1, value=2025)
            nivel_escolaridade = st.selectbox("Nível de escolaridade", ["Ensino Fundamental", "Ensino Médio", "Ensino Superior", "Pós-Graduação"])
            curso = st.text_input("Curso")
            status_curso = st.selectbox("Status no curso", ["Cursando", "Concluído", "Trancado"])
            areas_interesse = st.text_input("Áreas de interesse (separadas por vírgula)")
            tipo_membro = st.selectbox("Tipo de membro", ["Discente", "Docente", "Técnico"])
            rank_gp = st.selectbox("Rank GP", ["Iniciante", "Intermediário", "Avançado"])
            status = st.selectbox("Status de atividade", ["Ativo", "Inativo"])
            enviado = st.form_submit_button("Adicionar membro")
            if enviado:
                novo_membro = {
                    "ID": id,
                    "NOME": nome,
                    "CPF": cpf,
                    "EMAIL": email,
                    "CONTATO": contato,
                    "LATTES": lattes,
                    "MATRÍCULA": matricula,
                    "TAMANHO CAMISETA": tamanho_camiseta,
                    "DATA NASCIMENTO": data_nascimento.strftime("%Y-%m-%d"),
                    "EQUIPE DE PROJETO": equipe_projeto,
                    "ORIENTADOR": orientador,
                    "SÉRIE": serie,
                    "ANO": ano,
                    "NÍVEL ESCOLARIDADE": nivel_escolaridade,
                    "CURSO": curso,
                    "STATUS CURSO": status_curso,
                    "ÁREAS DE INTERESSE": areas_interesse,
                    "TIPO MEMBRO": tipo_membro,
                    "RANK GP": rank_gp,
                    "STATUS": status}
                st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([novo_membro])], ignore_index=True)
                st.success(f"Membro {nome} adicionado com sucesso!")
    elif options == "Equipe":
        with st.form("form_equipe"):
            st.subheader("Nova Equipe")
            nome_equipe = st.text_input("Nome da equipe")
            descricao = st.text_area("Descrição (opcional)")
            orientador = st.text_input("Orientador responsável")
            status_equipe = st.selectbox("Status da equipe", ["Ativa", "Inativa", "Parcialmente Ativa"])
            enviado_equipe = st.form_submit_button("Adicionar equipe")
            if enviado_equipe:
                if nome_equipe in st.session_state.df["EQUIPE DE PROJETO"].unique():
                    st.warning("Essa equipe já está cadastrada.")
                else:
                    nova_linha = {
                    "ID": "",
                    "NOME": "",
                    "EQUIPE DE PROJETO": nome_equipe,
                    "ORIENTADOR": orientador,
                    "STATUS": status_equipe,
                    "CURSO": "",
                    "EMAIL": "",
                    "CPF": "",
                    "CONTATO": "",
                    "LATTES": "",
                    "MATRÍCULA": "",
                    "tamanho_camiseta": "",
                    "DATA NASCIMENTO": "",
                    "SÉRIE": "",
                    "ANO": "",
                    "NÍVEL ESCOLARIDADE": "",
                    "STATUS CURSO": "",
                    "ÁREAS DE INTERESSE": "",
                    "TIPO MEMBRO": "",
                    "RANK GP": ""}
                st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([nova_linha])], ignore_index=True)
                st.success(f"Equipe '{nome_equipe}' adicionada com sucesso!")

#configurações extras