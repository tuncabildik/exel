import streamlit as st
import pandas as pd
from datetime import datetime
from io import StringIO
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from streamlit_autorefresh import st_autorefresh

# Sayfa ayarları
st.set_page_config(page_title="Fiyat Takip Paneli", page_icon="🚖", layout="wide")

# Otomatik yenileme (her 60 saniyede bir)
st_autorefresh(interval=60000, key="data_refresh")

# Başlık
st.markdown("""
    <h1 style='text-align: center;'>🚖 Fiyat Takip Paneli</h1>
""", unsafe_allow_html=True)

# Veriyi oku
@st.cache_data
def load_data():
    df = pd.read_csv("veriler.csv", names=["tarih", "rota", "saat_araligi", "fiyat", "tedarikçi", "arac"])
    df = df.dropna()
    df = df[df["fiyat"].astype(str).str.startswith("€")]
    df["fiyat"] = df["fiyat"].replace("€", "", regex=True).astype(float)
    df["tarih"] = pd.to_datetime(df["tarih"], errors='coerce')
    return df

df = load_data()

# Bugünün verileri öncelikli
bugun = datetime.now().date()
df = df.sort_values(by=["tarih"], ascending=False)
df = pd.concat([
    df[df["tarih"].dt.date == bugun],
    df[df["tarih"].dt.date != bugun]
])

# Önceki yüklemeden farklıysa uyarı göster
@st.cache_data
def get_latest_fiyat():
    return df.iloc[0]["fiyat"] if not df.empty else None

onceki_fiyat = st.session_state.get("onceki_fiyat")
mevcut_fiyat = get_latest_fiyat()

if onceki_fiyat and mevcut_fiyat and mevcut_fiyat != onceki_fiyat:
    if mevcut_fiyat < onceki_fiyat:
        st.success(f"📉 Yeni fiyat bulundu: €{mevcut_fiyat:.2f} (önceki: €{onceki_fiyat:.2f})")
    elif mevcut_fiyat > onceki_fiyat:
        st.warning(f"📈 Fiyat arttı: €{mevcut_fiyat:.2f} (önceki: €{onceki_fiyat:.2f})")

st.session_state["onceki_fiyat"] = mevcut_fiyat

# Filtre paneli
with st.sidebar:
    st.markdown("## 🔍 Filtrele")
    sadece_bugun = st.checkbox("🗓️ Sadece bugünün verileri", value=False)
    tarih_secim = st.multiselect("📅 Tarih", sorted(df["tarih"].dt.strftime("%Y-%m-%d %H:%M:%S").unique(), reverse=True))
    rota_secim = st.multiselect("🚏 Rota", sorted(df["rota"].unique()))
    saat_aralik_secim = st.multiselect("⏰ Saat Aralığı", sorted(df["saat_araligi"].unique()))
    grafik_mod = st.toggle("📊 Grafik Modu")

# Sadece bugünün verileri filtresi
if sadece_bugun:
    df = df[df["tarih"].dt.date == bugun]

# Filtre uygula
if tarih_secim:
    df = df[df["tarih"].dt.strftime("%Y-%m-%d %H:%M:%S").isin(tarih_secim)]
if rota_secim:
    df = df[df["rota"].isin(rota_secim)]
if saat_aralik_secim:
    df = df[df["saat_araligi"].isin(saat_aralik_secim)]

# Bilgi kutusu
son_veri = df["tarih"].max() if not df.empty else "Bilinmiyor"
st.success(f"✅ {len(df)} sonuç bulundu | 🕒 Son veri: {son_veri}")

# Grafik mod
if grafik_mod and not df.empty:
    st.markdown("### 📊 Rotalara Göre Ortalama Fiyatlar")
    fiyat_grafik = df.groupby("rota")["fiyat"].mean().sort_values(ascending=False)
    st.bar_chart(fiyat_grafik.to_frame())

# AgGrid tablosu
st.markdown("### 📋 Sonuçlar")
if not df.empty:
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection(selection_mode="single", use_checkbox=True)
    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        theme="streamlit",
        fit_columns_on_grid_load=True,
        enable_enterprise_modules=False
    )

    selected = grid_response["selected_rows"]
else:
    selected = []

# 📌 Fiyat Hesaplayıcı
st.markdown("---")
st.markdown("### 💸 Fiyat Hesaplayıcı")

if selected is not None and len(selected) > 0:
    selected_row = pd.DataFrame(selected)
    st.write("Seçilen satır:")
    st.dataframe(selected_row)

    try:
        secili_fiyat = selected_row.iloc[0]["fiyat"]
        tercih_edilir_fiyat = ((secili_fiyat - 0.01) / 1.23) * 0.95
        st.markdown(f"#### 💰 %10 Tercih Edilir Fiyat: **€{tercih_edilir_fiyat:.2f}**")
    except Exception as e:
        st.warning(f"Hesaplama yapılamadı: {e}")
else:
    st.info("Lütfen tablodan bir satır seçin.")
