import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
from fpdf import FPDF # Library untuk membuat PDF kustom

st.set_page_config(page_title="Compound Interest Calculator", page_icon="🪄")

st.title("🧮 Kalkulator Bunga Majemuk")

# Fungsi pembantu untuk konversi teks ke float
def parse_money(text):
    # Menghapus karakter non-digit kecuali titik/koma desimal
    clean_text = ''.join(c for c in text if c.isdigit() or c in '.,')
    try:
        return float(clean_text.replace(',', '')) # Sesuaikan jika menggunakan format IDR
    except:
        return 0.0

# Fungsi pembantu untuk memformat angka ke gaya Indonesia (1.000.000,00)
def format_idr(angka):
    # Menggunakan f-string untuk ribuan dengan koma, lalu ditukar agar sesuai standar IDR
    # Ribuan jadi titik, desimal jadi koma
    formatted = "{:,.2f}".format(angka).replace(",", "X").replace(".", ",").replace("X", ".")
    return formatted

# --- INPUT ---
with st.sidebar:
    st.header("Parameter Investasi")
    
    currency_choice = st.selectbox("Pilih Mata Uang", options=["Yuan (¥)", "US Dollar ($)", "Rupiah (Rp)"])
    symbol = "¥" if currency_choice == "Yuan (¥)" else ("$" if currency_choice == "US Dollar ($)" else "Rp")
    
    # 1. Input Investasi Awal
    # Kita gunakan format="%f" agar input menerima angka desimal
    principal = st.number_input(
        f"Investasi Awal ({symbol})", 
        value=1000000.0, 
        step=100000.0, 
        format="%.2f" 
    )
    # Caption yang diformat khusus agar sama dengan input (titik=ribuan, koma=desimal)
    st.caption(f"Terbaca: **{symbol} {format_idr(principal)}**")
    
    # 2. Input Kontribusi Bulanan
    monthly_contribution = st.number_input(
        f"Kontribusi Bulanan ({symbol})", 
        value=1000000.0, 
        step=100000.0, 
        format="%.2f"
    )
    st.caption(f"Terbaca: **{symbol} {format_idr(monthly_contribution)}**")

    years = st.number_input("Jangka Waktu (Tahun)", min_value=1, value=20)
    annual_rate = st.number_input("Estimasi Bunga Tahunan (%)", value=20.0, step=0.5)
    
    compounding_freq = st.selectbox(
        "Frekuensi Bunga Majemuk",
        options=[
            "Annually (Tahunan)", 
            "Semiannually (6 Bulanan)", 
            "Quarterly (Kuartal)", 
            "Monthly (Bulanan)", 
            "Daily (Harian)"
        ],
        index=0
    )

# --- LOGIKA PERHITUNGAN ---
r = annual_rate / 100
current_balance = principal
total_contributions = principal

# Mapping frekuensi ke jumlah periode per tahun
freq_map = {
    "Annually (Tahunan)": 1,
    "Semiannually (6 Bulanan)": 2,
    "Quarterly (Kuartal)": 4,
    "Monthly (Bulanan)": 12,
    "Daily (Harian)": 365
}

n = freq_map[compounding_freq]

data = []
data.append({"Year": 0, "Future Value": current_balance, "Total Contributions": total_contributions})

for year in range(1, int(years) + 1):
    # Hitung kontribusi tahunan (tetap dijumlahkan per bulan sesuai input awal)
    yearly_contribution = monthly_contribution * 12
    
    # Perhitungan berdasarkan frekuensi yang dipilih
    if compounding_freq == "Annually (Tahunan)":
        interest_earned = current_balance * r
        current_balance = current_balance + interest_earned + yearly_contribution
    else:
        # Untuk frekuensi selain tahunan, kita bagi dalam sub-periode
        # Contoh: Monthly (12x), Quarterly (4x), Semiannually (2x), Daily (365x)
        periods_in_year = n
        contribution_per_period = yearly_contribution / periods_in_year
        
        for _ in range(int(periods_in_year)):
            # Bunga dihitung dari saldo yang ada sebelum kontribusi periode tersebut (standar finansial)
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

# --- GRAFIK ---
st.subheader("Total Savings")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["Year_Label"], 
    y=df["Future Value"],
    mode='lines+markers',
    name=f'Future Value ({annual_rate:.2f}%)',
    line=dict(color='#B22222', width=2),
    marker=dict(size=8, symbol='circle'),
    hovertemplate=f'Future Value ({annual_rate:.2f}%): {symbol} %{{y:,.2f}}<extra></extra>'
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
    # xaxis_title="Years",
    yaxis_title=f"Value ({symbol})",
    legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
    hovermode="x unified",
    # l=120 memberikan ruang yang cukup untuk angka hingga Triliun agar tidak terpotong
    margin=dict(l=120, r=20, t=50, b=100), 
    yaxis=dict(
        tickprefix=symbol + " ", 
        tickformat=",.0f",
        exponentformat="none",
        automargin=True, # Meminta Plotly menghitung margin secara otomatis
        separatethousands=True
    )
)

fig.update_xaxes(showgrid=False, tickangle=-45)

# Menggunakan width="stretch" sebagai pengganti use_container_width
st.plotly_chart(fig, width="stretch")

# def create_pdf(dataframe, figure, symbol_label):
#     pdf = FPDF()
#     pdf.add_page()
    
#     # Judul
#     pdf.set_font("helvetica", "B", 16)
#     pdf.cell(190, 10, "Laporan Investasi Bunga Majemuk", align="C")
#     pdf.ln(10)
    
#     # Gunakan width yang lebih besar saat render agar teks tidak bertumpuk
#     img_bytes = figure.to_image(format="png", width=1200, height=700, scale=2)
#     img_buf = io.BytesIO(img_bytes)

#     # x=5 (melebar ke kiri) dan w=200 (memenuhi lebar kertas A4)
#     pdf.image(img_buf, x=5, y=30, w=200)
    
#     # Pindah ke bawah grafik untuk tabel
#     pdf.set_y(155)
    
#     # ... (bagian tabel tetap sama) ...
#     pdf.set_font("helvetica", "B", 12)
#     pdf.cell(190, 10, "Tabel Pertumbuhan Tahunan")
#     pdf.ln(10)
    
#     # Header Tabel
#     pdf.set_font("helvetica", "B", 10)
#     pdf.set_fill_color(200, 200, 200)
#     pdf.cell(35, 10, "Tahun", border=1, align="C", fill=True)
#     pdf.cell(75, 10, f"Value ({symbol_label})", border=1, align="C", fill=True)
#     pdf.cell(75, 10, f"Kontribusi ({symbol_label})", border=1, align="C", fill=True)
#     pdf.ln()

#     # Isi Tabel
#     pdf.set_font("helvetica", "", 10)
#     for index, row in dataframe.iterrows():
#         if pdf.get_y() > 260: 
#             pdf.add_page()
#         pdf.cell(35, 8, f"Year {int(row['Year'])}", border=1, align="C")
#         pdf.cell(75, 8, f"{row['Future Value']:,.2f}", border=1, align="R")
#         pdf.cell(75, 8, f"{row['Total Contributions']:,.2f}", border=1, align="R")
#         pdf.ln()
        
#     return bytes(pdf.output())

def create_pdf(dataframe, symbol_label):
    pdf = FPDF()
    pdf.add_page()
    
    # Judul Laporan
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(190, 10, "Laporan Investasi Bunga Majemuk", ln=True, align="C")
    pdf.ln(5)
    
    # Subheader Tabel
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(190, 10, "Tabel Pertumbuhan Tahunan", ln=True, align="L")
    pdf.ln(2)
    
    # --- HEADER TABEL ---
    pdf.set_font("helvetica", "B", 10)
    pdf.set_fill_color(200, 200, 200) # Warna abu-abu untuk header
    pdf.cell(35, 10, "Tahun", border=1, align="C", fill=True)
    pdf.cell(75, 10, f"Value ({symbol_label})", border=1, align="C", fill=True)
    pdf.cell(75, 10, f"Kontribusi ({symbol_label})", border=1, align="C", fill=True)
    pdf.ln()

    # --- ISI TABEL ---
    pdf.set_font("helvetica", "", 10)
    for index, row in dataframe.iterrows():
        # Cek jika posisi kursor hampir mencapai batas bawah kertas (A4 sekitar 297mm)
        # Jika ya, tambah halaman baru
        if pdf.get_y() > 270: 
            pdf.add_page()
            # Opsional: Print ulang header di halaman baru jika diinginkan
            pdf.set_font("helvetica", "B", 10)
            pdf.cell(35, 10, "Tahun", border=1, align="C", fill=True)
            pdf.cell(75, 10, f"Value ({symbol_label})", border=1, align="C", fill=True)
            pdf.cell(75, 10, f"Kontribusi ({symbol_label})", border=1, align="C", fill=True)
            pdf.ln()
            pdf.set_font("helvetica", "", 10)

        pdf.cell(35, 8, f"Year {int(row['Year'])}", border=1, align="C")
        pdf.cell(75, 8, f"{row['Future Value']:,.2f}", border=1, align="R")
        pdf.cell(75, 8, f"{row['Total Contributions']:,.2f}", border=1, align="R")
        pdf.ln()
        
    return bytes(pdf.output())

# --- TOMBOL DOWNLOAD ---
st.write("### 📥 Download Laporan")
dl_col1, dl_col2 = st.columns(2)

with dl_col1:
    try:
        # pdf_data = create_pdf(df, fig, symbol)
        pdf_data = create_pdf(df, symbol)
        st.download_button(
            label="Download Laporan Lengkap (PDF)",
            data=pdf_data,
            file_name="laporan_investasi.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Gagal membuat PDF: {e}")

with dl_col2:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.drop(columns=['Year_Label']).to_excel(writer, index=False)
    st.download_button(
        label="Download Tabel (Excel)",
        data=buffer.getvalue(),
        file_name="data_investasi.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.markdown("---")

# --- RINGKASAN & TABEL (Tampilan Web) ---
col1, col2 = st.columns(2)
col1.metric("Saldo Akhir", f"{symbol} {current_balance:,.2f}")
col2.metric("Total Kontribusi", f"{symbol} {total_contributions:,.2f}")

st.write("### Tabel Pertumbuhan Tahunan")
df_display = df[["Year", "Future Value", "Total Contributions"]].copy()
df_display["Year"] = df_display["Year"].apply(lambda x: f"Year {x}")
df_display["Future Value"] = df_display["Future Value"].map(f"{symbol} {{:,.2f}}".format)
df_display["Total Contributions"] = df_display["Total Contributions"].map(f"{symbol} {{:,.2f}}".format)

st.table(df_display)