import streamlit as st
import requests
import random

st.set_page_config(page_title="Gerador Lotofácil Automático", page_icon="🎲", layout="centered")

st.title("🎲 Gerador Automático Lotofácil")
st.write("Baseado nos últimos resultados oficiais da Lotofácil (Caixa).")

# Função para buscar os últimos resultados da API da Caixa (via site oficial)
def get_last_results(qtd=10):
    url = f"https://loteriascaixa-api.herokuapp.com/api/lotofacil/latest/{qtd}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except:
        return []

# Função para gerar novo jogo baseado em frequências
def generate_game_from_results(results):
    if not results:
        return sorted(random.sample(range(1, 26), 15))  # se não conseguir pegar nada, gera aleatório
    
    freq = {i: 0 for i in range(1, 26)}
    for r in results:
        for num in r.get("dezenas", []):
            freq[int(num)] += 1
    
    # ordenar por frequência
    sorted_nums = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    
    # pegar os 20 mais frequentes
    top20 = [n for n, _ in sorted_nums[:20]]
    
    # dos 20, sortear 15
    return sorted(random.sample(top20, 15))

# Interface
qtd = st.slider("Quantos últimos concursos usar como base?", 5, 30, 15)
results = get_last_results(qtd)

if st.button("🔮 Gerar Jogo"):
    jogo = generate_game_from_results(results)
    st.success(f"Seu jogo gerado: {jogo}")

st.divider()
st.caption("⚠️ Este app não garante ganhos. É apenas uma ferramenta de geração baseada em estatísticas passadas.")
