import os
import streamlit as st
from groq import Groq

# Tenta carregar a API_KEY a partir do secrets
api_key = "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"

if not api_key:
    st.error("⚠️ API_KEY não carregada. Verifique se ela está configurada no secrets do Streamlit Cloud.")
    st.stop()

# Função para obter resposta do Groq
def get_groq_completions(user_content):
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=[
            {
                "role": "system",
                "content": "Você é um assistente especialista em criar ideias para projetos de feira de ciências. Responda sempre em português do Brasil e siga estritamente as instruções de formatação do usuário."
            },
            {
                "role": "user",
                "content": user_content
            }
        ],
        temperature=0.7,
        max_tokens=8000,
        top_p=1,
        stream=True,
        stop=None,
    )

    result = ""
    for chunk in completion:
        result += chunk.choices[0].delta.content or ""

    return result

def gerar_ideias(dados_usuario):
    prompt = criar_prompt(dados_usuario)
    try:
        response = get_groq_completions(prompt)
        return response.strip() if response else None
    except Exception as e:
        st.error(f"Erro ao tentar gerar ideias: {e}")
        return None

# Prompt com instruções de formatação extremamente claras
def criar_prompt(dados_usuario):
    metodologia = dados_usuario.get('metodologia')
    
    prompt_template = """
    Como estudante do ensino {ano_serie}, estou empolgado em criar um projeto {preferencia_projeto} para participar de uma feira de ciência. 
    Meu objetivo é desenvolver um projeto utilizando a metodologia {metodologia}, que envolve {detalhes_metodologia}. 
    Gostaria de abordar um problema ou investigação da subárea {especialidade} que faz parte da grande área {area_conhecimento}, com preferência por temas relacionados à {tema_especifico}, pois tenho interesse no {motivacao}. 
    Sobre o conhecimento prévio sobre esse tema minha resposta é {conhecimento_previo}. 
    Para desenvolver esse projeto pretendo fazer uso das minhas habilidades de {habilidades} e dos seguintes recursos {recursos}. 
    Espero que ao final do projeto possa {impacto}. 
    Gostaria ainda de acrescentar que {informacao_adicional}. 

    Com base em todas as informações fornecidas, gere uma lista com 5 ideias de projetos de feira de ciência em português do Brasil.
    A resposta DEVE começar diretamente com a primeira ideia, sem qualquer introdução, saudação ou preâmbulo.
    
    Use estritamente o seguinte formato de Markdown para CADA uma das 5 ideias. 
    É CRUCIAL que cada seção (**Título**, **Objetivo**, **Materiais**) comece em uma NOVA LINHA para garantir a clareza.

    **Título:** [Aqui vai o título da ideia]

    **Objetivo:** [Aqui vai o objetivo da ideia]

    **Materiais:** 
    * Item 1
    * Item 2
    * Item 3

    ---

    Ao final de TODAS as 5 ideias, ofereça uma seção chamada **Recursos Adicionais** com links para artigos ou vídeos.
    """

    detalhes_metodologia = "o teste de uma hipótese, coleta e processamento de dados para chegar a uma conclusão" if metodologia == "Científica" else "a criação ou aperfeiçoamento de um dispositivo, procedimento, programa de computador ou algoritmo"

    return prompt_template.format(
        ano_serie=dados_usuario['ano_serie'],
        preferencia_projeto=dados_usuario['preferencia_projeto'],
        metodologia=dados_usuario['metodologia'],
        detalhes_metodologia=detalhes_metodologia,
        especialidade=dados_usuario['especialidade'],
        area_conhecimento=dados_usuario['area_conhecimento'],
        tema_especifico=dados_usuario['tema_especifico'],
        motivacao=dados_usuario['motivacao'],
        conhecimento_previo=dados_usuario['conhecimento_previo'],
        habilidades=dados_usuario['habilidades'],
        recursos=dados_usuario['recursos'],
        impacto=dados_usuario['impacto'],
        informacao_adicional=dados_usuario.get('informacao_adicional', 'Nenhuma.')
    )


# --- CONFIGURAÇÃO DA APLICAÇÃO STREAMLIT ---
st.set_page_config(page_title="Faísca - Gerador de Ideias", page_icon="✨", layout="centered")

st.title("Tenha ideias incríveis de projetos com o Faísca!")
st.subheader("Seu assistente virtual para feiras de ciência")

# --- IMAGEM ADICIONADA AQUI ---
col1, col2, col3 = st.columns([0.2, 1, 0.2])
with col2:
    st.image("faísca.png")
# --- FIM DA SEÇÃO DA IMAGEM ---

st.write("""
Faísca é um chatbot de inteligência artificial feito sob medida para alunos da educação básica como você. Ele não é apenas um assistente; é uma fonte de inspiração que irá acender sua criatividade e ajudá-lo a gerar ideias para seus projetos.
""")

st.info("Para que o Faísca possa te oferecer as melhores sugestões, é fundamental que você responda a todas as perguntas.")

# Coletando informações do usuário
ano_serie = st.selectbox("Qual ano/série você está cursando?", [
    "", "4º Ano do Ensino Fundamental", "5º Ano do Ensino Fundamental", "6º Ano do Ensino Fundamental", "7º Ano do Ensino Fundamental", "8º Ano do Ensino Fundamental", "9º Ano do Ensino Fundamental", "1º Ano do Ensino Médio",
    "2º Ano do Ensino Médio", "3º Ano do Ensino Médio"], key="ano_serie")

preferencia_projeto = st.radio("Prefere realizar o projeto sozinho ou em equipe?", ["Sozinho", "Em equipe"],
                               key="preferencia_projeto")

metodologia = st.selectbox("Qual metodologia você pretende utilizar para o seu projeto?",
                           ["", "Científica", "Engenharia"], key="metodologia")

area_conhecimento = st.selectbox("Em qual área do conhecimento você tem mais interesse?", [
    "", "Ciências Agrárias", "Ciências Biológicas", "Ciências da Saúde",
    "Ciências Exatas e da Terra", "Engenharias", "Ciências Humanas",
    "Ciências Sociais Aplicadas", "Lingüística, Letras e Artes"], key="area_conhecimento")

especialidade = ""
especialidades_map = {
    "Ciências Agrárias": ["Agronomia", "Ciência e Tecnologia de Alimentos", "Medicina Veterinária", "Recursos Florestais e Engenharia Florestal", "Zootecnia"],
    "Ciências Biológicas": ["Biotecnologia", "Genética", "Microbiologia", "Imunologia", "Botânica", "Ecologia"],
    "Ciências da Saúde": ["Farmácia", "Enfermagem", "Medicina", "Nutrição", "Odontologia", "Saúde Pública"],
    "Ciências Exatas e da Terra": ["Astronomia", "Ciência da Computação", "Geociências", "Matemática", "Oceanografia", "Química", "Física", "Estatística"],
    "Engenharias": ["Engenharia Aeroespacial", "Engenharia Ambiental", "Engenharia Biomédica", "Engenharia Civil", "Engenharia Elétrica", "Engenharia de Controle e Automação", "Engenharia de Materiais e Metalúrgica", "Engenharia de Produção", "Engenharia Mecânica", "Engenharia Química"],
    "Ciências Humanas": ["Antropologia", "Arqueologia", "Ciência Política", "Educação", "Filosofia", "Geografia", "História", "Psicologia", "Sociologia"],
    "Ciências Sociais Aplicadas": ["Administração", "Arquitetura e Urbanismo", "Comunicação", "Direito", "Economia", "Planejamento Urbano e Regional", "Turismo"],
    "Lingüística, Letras e Artes": ["Artes", "Letras", "Linguística", "Música", "Design"]
}

if area_conhecimento in especialidades_map:
    opcoes = [""] + especialidades_map[area_conhecimento]
    especialidade = st.selectbox("Dentro da área escolhida, qual especialidade te interessa mais?", opcoes)

tema_especifico = st.text_input("Informe o tema específico que você deseja explorar:", placeholder="Ex: Impacto das redes sociais na saúde mental", key="tema_especifico")
motivacao = st.text_input("O que te motivou a escolher esse tema?", placeholder="Ex: Tenho curiosidade sobre como a tecnologia nos afeta.", key="motivacao")
conhecimento_previo = st.selectbox("Qual seu conhecimento prévio sobre esse tema?", ["", "Nenhum", "Básico", "Intermediário", "Avançado"], key="conhecimento_previo")
habilidades = st.text_area("Quais habilidades você tem que podem ajudar?", placeholder="Ex: Sou bom em pesquisa, programação básica, desenho...", key="habilidades")
recursos = st.text_area("Quais recursos você tem disponível?", placeholder="Ex: Acesso à internet, laboratório da escola, livros...", key="recursos")
impacto = st.text_area("Qual impacto você espera alcançar com o projeto?", placeholder="Ex: Conscientizar meus colegas, criar uma solução para um problema local...", key="impacto")
informacao_adicional = st.text_area("Deseja adicionar alguma informação adicional? (Opcional)", key="informacao_adicional")

dados_usuario = {
    'ano_serie': ano_serie,
    'preferencia_projeto': preferencia_projeto,
    'metodologia': metodologia,
    'area_conhecimento': area_conhecimento,
    'especialidade': especialidade,
    'tema_especifico': tema_especifico,
    'motivacao': motivacao,
    'conhecimento_previo': conhecimento_previo,
    'habilidades': habilidades,
    'recursos': recursos,
    'impacto': impacto,
    'informacao_adicional': informacao_adicional or "Nenhuma informação adicional a ser considerada."
}

if st.button("Gerar Ideias de Projetos", type="primary"):
    campos_obrigatorios = [ano_serie, preferencia_projeto, metodologia, area_conhecimento, especialidade, tema_especifico, motivacao, conhecimento_previo, habilidades, recursos, impacto]
    
    if not all(campos_obrigatorios):
        st.error("Por favor, preencha todos os campos obrigatórios antes de continuar.")
    else:
        with st.spinner("Faísca está pensando nas melhores ideias para você... aguarde! ✨"):
            response = gerar_ideias(dados_usuario)
        
        st.success("Pronto! Aqui estão algumas ideias de projetos para você:")
        if response:
            st.markdown(response)
        else:
            st.warning("Não foi possível gerar ideias. Tente refinar suas respostas ou tente novamente mais tarde.")




