
import streamlit as st
import pandas as pd
import plotly.express as px

# Configurações visuais
st.set_page_config(layout="wide", page_title="Painel Apostas Inteligentes")
st.markdown(
    '''
    <style>
    body {
        background-color: black;
        color: #00ff88;
    }
    .stApp {
        background-color: black;
    }
    h1, h2, h3, h4, h5, h6, .stMarkdown {
        color: #00ff88;
        text-shadow: 1px 1px 2px yellow;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# Dados fictícios de exemplo
dados = pd.DataFrame({
    "Jogo": ["Fluminense x Al Ahly", "Palmeiras x Chelsea"],
    "Mercado": ["Ambos Marcam", "Mais de 2.5 Gols"],
    "Status": ["✅ GREEN", "❌ RED"],
    "Odd": [1.85, 1.75],
    "Valor Apostado": [100, 100],
    "Retorno": [185, 0]
})

st.title("📊 Painel de Apostas Inteligentes")

# Seções
st.header("📌 Resumo das Apostas")
st.dataframe(dados, use_container_width=True)

st.header("📈 Gráfico de ROI")
dados["ROI"] = dados["Retorno"] - dados["Valor Apostado"]
fig = px.bar(dados, x="Jogo", y="ROI", color="Status", text="ROI", color_discrete_map={"✅ GREEN":"green", "❌ RED":"red"})
st.plotly_chart(fig, use_container_width=True)

st.header("✅ Taxa de Acerto")
taxa = (dados["Status"] == "✅ GREEN").sum() / len(dados) * 100
st.metric("Taxa de Acerto", f"{taxa:.2f}%")

st.markdown("---")
st.caption("Desenvolvido por THOROBOM | Painel com análise de gols, cantos, ROI e bots inteligentes via Streamlit")
