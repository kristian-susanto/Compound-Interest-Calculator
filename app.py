import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io

st.set_page_config(page_title="Compound Interest Calculator", page_icon="🪄")

st.title("🧮 Compound Interest Calculator")

# Helper function to format numbers to IDR-style or standard international (adjusted to standard English for this version)
def format_currency(number):
    # Using standard international format for English version: 1,000,000.00
    return "{:,.2f}".format(number)

# --- INPUT ---
with st.sidebar:
    st.header("Investment Parameters")

    currency_choice = st.selectbox("Select Currency", options=["Yuan (¥)", "US Dollar ($)", "Rupiah (Rp)"])
    symbol = "¥" if currency_choice == "Yuan (¥)" else ("$" if currency_choice == "US Dollar ($)" else "Rp")
    
    # 1. Initial Investment Input
    principal = st.number_input(
        f"Initial Investment ({symbol})", 
        value=1000.0, 
        step=100.0, 
        format="%.2f" 
    )
    st.caption(f"Value: **{symbol} {format_currency(principal)}**")
    
    # 2. Monthly Contribution Input
    monthly_contribution = st.number_input(
        f"Monthly Contribution ({symbol})", 
        value=100.0, 
        step=100.0, 
        format="%.2f"
    )
    st.caption(f"Value: **{symbol} {format_currency(monthly_contribution)}**")

    years = st.number_input("Investment Period (Years)", min_value=1, value=20)
    annual_rate = st.number_input("Estimated Annual Interest Rate (%)", value=7.0, step=0.5)
    
    compounding_freq = st.selectbox(
        "Compounding Frequency",
        options=[
            "Annually", 
            "Semiannually", 
            "Quarterly", 
            "Monthly", 
            "Daily"
        ],
        index=0 # Defaulted to Annually for convenience
    )

# --- CALCULATION LOGIC ---
r = annual_rate / 100
current_balance = principal
total_contributions = principal

# Mapping frequency to periods per year
freq_map = {
    "Annually": 1,
    "Semiannually": 2,
    "Quarterly": 4,
    "Monthly": 12,
    "Daily": 365
}

n = freq_map[compounding_freq]

data = []
data.append({"Year": 0, "Future Value": current_balance, "Total Contributions": total_contributions})

for year in range(1, int(years) + 1):
    yearly_contribution = monthly_contribution * 12
    
    if compounding_freq == "Annually":
        interest_earned = current_balance * r
        current_balance = current_balance + interest_earned + yearly_contribution
    else:
        periods_in_year = n
        contribution_per_period = yearly_contribution / periods_in_year
        
        for _ in range(int(periods_in_year)):
            # Interest is calculated on the balance before the period's contribution
            interest_this_period = current_balance * (r / n)
            current_balance += contribution_per_period + interest_this_period
            
    total_contributions += yearly_contribution

    data.append({
        "Year": year,
        "Future Value": round(current_balance, 2),
        "Total Contributions": round(total_contributions, 2)
    })

df = pd.DataFrame(data)
df["Year_Label"] = df["Year"].apply(lambda x: f"Year {x}")

# --- CHART ---
st.subheader("Savings Projection")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["Year_Label"], 
    y=df["Future Value"],
    mode='lines+markers',
    name=f'Future Value ({annual_rate:.2f}%)',
    line=dict(color='#B22222', width=2),
    marker=dict(size=8, symbol='circle'),
    hovertemplate=f'Future Value: {symbol} %{{y:,.2f}}<extra></extra>'
))

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
    yaxis_title=f"Value ({symbol})",
    legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
    hovermode="x unified",
    margin=dict(l=120, r=20, t=50, b=100), 
    yaxis=dict(
        tickprefix=symbol + " ", 
        tickformat=",.0f",
        exponentformat="none",
        automargin=True,
        separatethousands=True
    )
)

fig.update_xaxes(showgrid=False, tickangle=-45)

st.plotly_chart(fig, use_container_width=True)

# --- DOWNLOAD BUTTON ---
st.write("### 📥 Download Report")

### If you want PDF and Excel options, activate this comment
# dl_col1, dl_col2 = st.columns(2)

# with dl_col1:
#     try:
#         pdf_data = create_pdf(df, fig, symbol)
#         st.download_button(
#             label="Download Laporan Lengkap (PDF)",
#             data=pdf_data,
#             file_name="compound_interest_calculator.pdf",
#             mime="application/pdf"
#         )
#     except Exception as e:
#         st.error(f"Gagal membuat PDF: {e}")

# with dl_col2:
#     buffer = io.BytesIO()
#     with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
#         df.drop(columns=['Year_Label']).to_excel(writer, index=False)
#     st.download_button(
#         label="Download Tabel (Excel)",
#         data=buffer.getvalue(),
#         file_name="compound_interest_calculator.xlsx",
#         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     )

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    df.drop(columns=['Year_Label'], errors='ignore').to_excel(writer, index=False)

st.download_button(
    label="Download Table (Excel)",
    data=buffer.getvalue(),
    file_name="compound_interest_calculator.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

st.markdown("---")

# --- SUMMARY & TABLE ---
col1, col2 = st.columns(2)
col1.metric("End Balance", f"{symbol} {current_balance:,.2f}")
col2.metric("Total Contributions", f"{symbol} {total_contributions:,.2f}")

st.write("### Annual Growth Table")
df_display = df[["Year", "Future Value", "Total Contributions"]].copy()
df_display["Year"] = df_display["Year"].apply(lambda x: f"Year {x}")
df_display["Future Value"] = df_display["Future Value"].map(f"{symbol} {{:,.2f}}".format)
df_display["Total Contributions"] = df_display["Total Contributions"].map(f"{symbol} {{:,.2f}}".format)

st.table(df_display)