import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Painel de Apostas", layout="wide")

# Custom CSS for dark theme and green text
st.markdown(
    """
    <style>
    body {
        background-color: #000000;
        color: #00FF00;
    }
    .stButton > button {
        color: #00FF00;
        background-color: #000000;
        border: 1px solid #00FF00;
    }
    .stDataFrame table, .stTable table {
        background-color: #000000;
        color: #00FF00;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("Painel de Apostas")
st.write("Carregue um arquivo CSV com dados de apostas.")

uploaded_file = st.file_uploader("Upload de arquivo CSV", type=["csv"])
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo CSV: {e}")
        st.stop()

    st.header("Dados Carregados")
    st.dataframe(df)

    expected_cols = ["Data", "Jogo", "Mercado", "Odd", "Valor_apostado", "Resultado", "Tipo_de_aposta", "Bot"]
    missing_cols = [col for col in expected_cols if col not in df.columns]
    if missing_cols:
        st.error(f"Colunas ausentes no CSV: {missing_cols}")
        st.stop()

    def is_win(val):
        if pd.isna(val):
            return False
        try:
            if isinstance(val, (int, float)):
                return val == 1 or val == True
            val_str = str(val).strip().lower()
            if val_str in ["1", "v", "ganhou", "sim", "true", "win", "acerto"]:
                return True
            return False
        except:
            return False

    df['Win'] = df['Resultado'].apply(is_win)
    df['Profit'] = df.apply(lambda row: row['Odd'] * row['Valor_apostado'] - row['Valor_apostado'] if row['Win'] else -row['Valor_apostado'], axis=1)

    bot_stats = []
    bots = df['Bot'].unique()
    for bot in bots:
        bot_df = df[df['Bot'] == bot]
        total_bets = len(bot_df)
        wins = bot_df['Win'].sum()
        losses = total_bets - wins
        total_profit = bot_df['Profit'].sum()
        total_staked = bot_df['Valor_apostado'].sum()
        roi = (total_profit / total_staked * 100) if total_staked != 0 else 0
        bot_stats.append((bot, total_bets, wins, losses, roi))

    stats_df = pd.DataFrame(bot_stats, columns=['Bot', 'NÃºmero de Apostas', 'Acertos', 'Erros', 'ROI (%)'])
    stats_df['ROI (%)'] = stats_df['ROI (%)'].round(2)
    stats_df = stats_df.sort_values(by='Bot')
    st.header("EstatÃ­sticas dos Bots")
    st.dataframe(stats_df)

    # Success rate chart
    success_rates = []
    for bot, bot_df in df.groupby('Bot'):
        rate = bot_df['Win'].sum() / len(bot_df) * 100 if len(bot_df) > 0 else 0
        success_rates.append((bot, rate))
    success_rates.sort(key=lambda x: x[0])
    bots_names = [x[0] for x in success_rates]
    success_values = [x[1] for x in success_rates]

    fig1, ax1 = plt.subplots()
    fig1.patch.set_facecolor('black')
    ax1.set_facecolor('black')
    ax1.bar(bots_names, success_values, color='green')
    ax1.set_ylim(0, 100)
    ax1.set_ylabel('Percentual de Acertos (%)', color='green')
    ax1.set_title('Percentual de Acertos por Bot', color='green')
    ax1.tick_params(axis='x', colors='green')
    ax1.tick_params(axis='y', colors='green')
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    # Cumulative ROI chart
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    df_sorted = df.sort_values('Data')
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    fig2.patch.set_facecolor('black')
    ax2.set_facecolor('black')
    for bot in bots:
        bot_df = df_sorted[df_sorted['Bot'] == bot]
        if bot_df.empty:
            continue
        bot_df = bot_df.copy()
        bot_df['Cumulative Profit'] = bot_df['Profit'].cumsum()
        bot_df['Cumulative Staked'] = bot_df['Valor_apostado'].cumsum()
        bot_df['Cumulative ROI (%)'] = np.where(bot_df['Cumulative Staked'] > 0,
                                               bot_df['Cumulative Profit'] / bot_df['Cumulative Staked'] * 100, 0)
        ax2.plot(bot_df['Data'], bot_df['Cumulative ROI (%)'], label=f"{bot}")
    ax2.set_ylabel('ROI Acumulado (%)', color='green')
    ax2.set_title('ROI Acumulado por Bot ao longo do tempo', color='green')
    ax2.tick_params(axis='x', colors='green')
    ax2.tick_params(axis='y', colors='green')
    ax2.legend()
    st.pyplot(fig2)
else:
    st.info("Por favor, faÃ§a o upload de um arquivo CSV para visualizar os dados.")