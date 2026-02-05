import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Compound Interest Calculator", page_icon="🪄")

st.title("🧮 Kalkulator Bunga Majemuk")

# --- INPUT ---
with st.sidebar:
    st.header("Parameter Investasi")

    currency_choice = st.selectbox("Pilih Mata Uang", options=["Yuan (¥)", "US Dollar ($)", "Rupiah (Rp)"])
    symbol = "¥" if currency_choice == "Yuan (¥)" else ("$" if currency_choice == "US Dollar ($)" else "Rp")

    principal = st.number_input(f"Investasi Awal ({symbol})", value=1000000.0, step=100000.0)
    monthly_contribution = st.number_input(f"Kontribusi Bulanan ({symbol})", value=1000000.0, step=100000.0)
    years = st.number_input("Jangka Waktu (Tahun)", min_value=1, value=20)
    annual_rate = st.number_input("Estimasi Bunga Tahunan (%)", value=20.0, step=0.5)

    compounding_freq = st.selectbox(
        "Frekuensi Bunga Majemuk",
        options=["Annually (Tahunan)", "Monthly (Bulanan)"],
        index=0
    )

# --- LOGIKA PERHITUNGAN ---
r = annual_rate / 100
current_balance = principal
total_contributions = principal

data = []
data.append({"Year": 0, "Future Value": current_balance, "Total Contributions": total_contributions})

for year in range(1, int(years) + 1):
    if compounding_freq == "Annually (Tahunan)":
        interest_earned = current_balance * r
        yearly_contribution = monthly_contribution * 12
        current_balance = current_balance + interest_earned + yearly_contribution
        total_contributions += yearly_contribution
    else:
        for _ in range(12):
            current_balance += monthly_contribution
            total_contributions += monthly_contribution
            current_balance *= (1 + r/12)

    data.append({
        "Year": year,
        "Future Value": round(current_balance, 2),
        "Total Contributions": round(total_contributions, 2)
    })

df = pd.DataFrame(data)

# Membuat label untuk Sumbu X agar muncul tulisan "Year X"
df["Year_Label"] = df["Year"].apply(lambda x: f"Year {x}")

# --- GRAFIK DENGAN MARKERS (PLOTLY) ---
st.subheader("Total Savings")

fig = go.Figure()

# Trace untuk Future Value
fig.add_trace(go.Scatter(
    x=df["Year_Label"], 
    y=df["Future Value"],
    mode='lines+markers',
    name=f'Future Value ({annual_rate:.2f}%)',
    line=dict(color='#B22222', width=2),
    marker=dict(size=8, symbol='circle'),
    hovertemplate=f'Future Value ({annual_rate:.2f}%): {symbol} %{{y:,.2f}}<extra></extra>'
))

# Trace untuk Total Contributions
fig.add_trace(go.Scatter(
    x=df["Year_Label"], 
    y=df["Total Contributions"],
    mode='lines+markers',
    name='Total Contributions',
    line=dict(color='#20B2AA', width=2),
    marker=dict(size=8, symbol='diamond'),
    hovertemplate=f'Total Contributions: {symbol} %{{y:,.2f}}<extra></extra>'
))

fig.update_layout(
    xaxis_title="Years",
    yaxis_title=f"Value ({symbol})",
    legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor="white",
        font_size=13,
        font_family="Arial, sans-serif",
        font_color="#333333",
        bordercolor="#cccccc"
    ),
    margin=dict(l=0, r=0, t=20, b=100), # Menambah margin bawah agar label x yang miring tidak terpotong
    yaxis=dict(tickprefix=symbol + " ", tickformat=",.0f")
)

# Rotasi sumbu X
fig.update_xaxes(showgrid=False, tickangle=-45)

# Menggunakan width="stretch" sebagai pengganti use_container_width
st.plotly_chart(fig, width="stretch")

# --- RINGKASAN & TABEL ---
col1, col2 = st.columns(2)
col1.metric("Saldo Akhir", f"{symbol} {current_balance:,.2f}")
col2.metric("Total Kontribusi", f"{symbol} {total_contributions:,.2f}")

st.write("### Tabel Pertumbuhan Tahunan")
df_display = df[["Year", "Future Value", "Total Contributions"]].copy()
df_display["Year"] = df_display["Year"].apply(lambda x: f"Year {x}")
df_display["Future Value"] = df_display["Future Value"].map(f"{symbol} {{:,.2f}}".format)
df_display["Total Contributions"] = df_display["Total Contributions"].map(f"{symbol} {{:,.2f}}".format)

st.table(df_display)