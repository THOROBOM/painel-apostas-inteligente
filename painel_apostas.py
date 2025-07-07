import streamlit as st
import pandas as pd
import plotly.express as px

# App Configuration
st.set_page_config(layout="wide", page_title="Smart Betting Panel")
st.markdown(
    """
    <style>
    body {
        background-color: black;
    }
    .main {
        background-color: black;
        color: #39FF14 !important;
    }
    .css-1d391kg, .css-ffhzg2, .st-bk {
        color: #39FF14 !important;
        text-shadow: 0 0 6px yellow;
    }
    .st-cd, .st-bb, .st-ag {
        background-color: #111;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Smart Betting Panel")

# Upload
file = st.file_uploader("📁 Upload your betting CSV file:", type=["csv"])

if file:
    df = pd.read_csv(file)
    df["Lucro"] = df.apply(lambda row: (row["Odd"] * row["Valor_apostado"] - row["Valor_apostado"]) if row["Resultado"] == "Ganhou" else -row["Valor_apostado"], axis=1)

    st.subheader("📌 Betting Table")
    st.dataframe(df, use_container_width=True)

    # Bot stats
    st.subheader("🤖 Bot Performance")
    bot_stats = df.groupby("Bot").agg(
        Total_Apostas=("Bot", "count"),
        Acertos=("Resultado", lambda x: (x == "Ganhou").sum()),
        ROI_total=("Lucro", "sum"),
        Valor_Total_Apostado=("Valor_apostado", "sum")
    )
    bot_stats["Taxa_Acerto (%)"] = (bot_stats["Acertos"] / bot_stats["Total_Apostas"]) * 100
    bot_stats["ROI (%)"] = (bot_stats["ROI_total"] / bot_stats["Valor_Total_Apostado"]) * 100
    st.dataframe(bot_stats.style.format({"ROI_total": "R${:.2f}", "ROI (%)": "{:.2f}%", "Taxa_Acerto (%)": "{:.1f}%"}))

    # Accuracy Chart
    fig1 = px.bar(bot_stats, x=bot_stats.index, y="Taxa_Acerto (%)", title="📈 Bot Accuracy", color="Taxa_Acerto (%)", color_continuous_scale="greens")
    st.plotly_chart(fig1, use_container_width=True)

    # ROI Chart
    fig2 = px.bar(bot_stats, x=bot_stats.index, y="ROI (%)", title="💰 ROI by Bot", color="ROI (%)", color_continuous_scale="blues")
    st.plotly_chart(fig2, use_container_width=True)

    # Export Report
    st.subheader("📤 Export Results")
    st.download_button(
        label="⬇️ Download CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name="relatorio_apostas.csv",
        mime="text/csv"
    )
else:
    st.warning("📌 Please upload a CSV file to view the dashboard.")
