import streamlit as st
import pandas as pd
import random
import requests

st.set_page_config(page_title="Lotofácil Inteligente", page_icon="🎲", layout="centered")
st.title("🎯 Gerador Inteligente de Jogos da Lotofácil")

st.markdown("""
Este app **NÃO garante prêmio**.  
Ele apenas utiliza **estatísticas dos últimos concursos** para montar combinações.
""")

# --- 1. Baixar últimos resultados (exemplo usando um CSV público) ---
@st.cache_data(ttl=3600)
def carregar_resultados():
    try:
        # Fonte pública (planilha não-oficial com resultados da Caixa)
        url = "https://raw.githubusercontent.com/danilotestelotofacil/dados/main/lotofacil.csv"
        # Formato esperado: Concurso;Data;B1;B2;...;B15
        df = pd.read_csv(url, sep=";")
        return df
    except Exception as e:
        st.error("Não foi possível carregar os últimos resultados.")
        return None

df = carregar_resultados()

if df is not None:
    st.success(f"Resultados carregados: {len(df)} concursos")
else:
    st.warning("Usando apenas geração aleatória por falta de dados.")

# --- 2. Estatísticas básicas ---
def calcular_estatisticas(df):
    freq = {}
    for i in range(1,16):
        col = f"B{i}"
        for n in df[col]:
            freq[n] = freq.get(n,0)+1
    freq_sorted = dict(sorted(freq.items()))
    return freq_sorted

if df is not None:
    freq = calcular_estatisticas(df)
    st.subheader("📊 Frequência das dezenas (últimos concursos)")
    st.bar_chart(pd.DataFrame.from_dict(freq, orient='index', columns=['Frequência']))

# --- 3. Configurações do usuário ---
st.subheader("⚙️ Configurações do Gerador")
qtd_jogos = st.slider("Quantidade de jogos", 1, 10, 5)
repetir_ult = st.slider("Repetir dezenas do último concurso", 0, 10, 5)
usar_quentes = st.checkbox("Dar prioridade para dezenas mais frequentes", True)
usar_balanceamento = st.checkbox("Balancear pares/ímpares", True)

# --- 4. Função para gerar jogo ---
def gerar_jogo():
    numeros = list(range(1,26))

    if df is not None:
        ultimo = [int(df.iloc[-1][f"B{i}"]) for i in range(1,16)]

        # Dezenas quentes
        if usar_quentes:
            ordenados = sorted(freq.items(), key=lambda x: x[1], reverse=True)
            quentes = [x[0] for x in ordenados[:13]]  # 13 mais frequentes
            base = quentes
        else:
            base = numeros

        jogo = set(random.sample(base, 15 - repetir_ult))
        if repetir_ult > 0:
            jogo.update(random.sample(ultimo, repetir_ult))
        jogo = list(jogo)
    else:
        jogo = random.sample(numeros, 15)

    # Balancear pares/ímpares
    if usar_balanceamento:
        for _ in range(100):
            pares = [n for n in jogo if n % 2 == 0]
            impares = [n for n in jogo if n % 2 != 0]
            if 6 <= len(pares) <= 9:
                break
            jogo = random.sample(numeros, 15)

    return sorted(jogo)

# --- 5. Gerar jogos ---
if st.button("🎲 Gerar Jogos"):
    for i in range(qtd_jogos):
        jogo = gerar_jogo()
        st.write(f"Jogo {i+1}: **{' - '.join(f'{n:02d}' for n in jogo)}**")
