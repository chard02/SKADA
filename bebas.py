import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Konfigurasi halaman
st.set_page_config(
    page_title="Order Data Visualization",
    page_icon="📊",
    layout="wide",
)

# Judul aplikasi
st.title("📦 Order Data Visualization")
st.markdown("Visualisasi interaktif data pesanan untuk menganalisis status, durasi, dan tren waktu.")

# Sidebar untuk upload file
st.sidebar.header("📂 Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type="csv")

# Fungsi untuk membaca dan memproses data
@st.cache_data
def load_data(file):
    data = pd.read_csv(file)
    # Mengonversi kolom waktu ke format datetime
    data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'], errors='coerce')
    data['order_approved_at'] = pd.to_datetime(data['order_approved_at'], errors='coerce')
    data['order_delivered_carrier_date'] = pd.to_datetime(data['order_delivered_carrier_date'], errors='coerce')
    data['order_delivered_customer_date'] = pd.to_datetime(data['order_delivered_customer_date'], errors='coerce')
    data['order_estimated_delivery_date'] = pd.to_datetime(data['order_estimated_delivery_date'], errors='coerce')
    return data

if uploaded_file is not None:
    # Membaca data
    data = load_data(uploaded_file)

    # Menampilkan opsi untuk menampilkan seluruh data
    st.sidebar.subheader("📋 Data Display Options")
    show_full_data = st.sidebar.checkbox("Tampilkan seluruh data")

    # Menampilkan ringkasan data
    st.subheader("📄 Data Overview")
    if show_full_data:
        st.dataframe(data, use_container_width=True)  # Menampilkan seluruh data
    else:
        st.dataframe(data.head(), use_container_width=True)  # Menampilkan sampel data

    # Visualisasi 1: Jumlah pesanan berdasarkan status
    st.subheader("📊 Orders by Status")
    st.markdown("Grafik ini menunjukkan jumlah pesanan berdasarkan statusnya, seperti 'delivered', 'shipped', atau lainnya. Hal ini membantu Anda memahami distribusi status pesanan.")
    status_counts = data['order_status'].value_counts()
    fig1 = px.bar(
        status_counts,
        x=status_counts.index,
        y=status_counts.values,
        labels={'x': 'Order Status', 'y': 'Count'},
        title="Jumlah Pesanan Berdasarkan Status",
        color=status_counts.index,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Visualisasi 2: Distribusi waktu persetujuan
    st.subheader("⏱ Approval Time Distribution")
    st.markdown("Grafik ini menampilkan distribusi waktu yang diperlukan untuk menyetujui pesanan setelah pesanan dilakukan, diukur dalam jam.")
    data['approval_duration'] = (data['order_approved_at'] - data['order_purchase_timestamp']).dt.total_seconds() / 3600
    fig2 = px.histogram(
        data,
        x="approval_duration",
        nbins=30,
        title="Distribusi Durasi Persetujuan Pesanan (dalam Jam)",
        color_discrete_sequence=["#636EFA"],
    )
    fig2.update_layout(xaxis_title="Durasi (Jam)", yaxis_title="Frekuensi")
    st.plotly_chart(fig2, use_container_width=True)

    # Visualisasi 3: Analisis durasi pengiriman
    st.subheader("🚚 Delivery Duration Analysis")
    st.markdown("Boxplot ini membandingkan durasi aktual pengiriman dengan estimasi pengiriman, diukur dalam hari. Data ini membantu Anda menganalisis keakuratan estimasi pengiriman.")
    data['delivery_duration'] = (data['order_delivered_customer_date'] - data['order_delivered_carrier_date']).dt.days
    data['estimated_vs_actual'] = (data['order_estimated_delivery_date'] - data['order_delivered_customer_date']).dt.days
    
    fig3 = px.box(
        data,
        y=["delivery_duration", "estimated_vs_actual"],
        labels={'value': 'Durasi (Hari)', 'variable': 'Tipe Durasi'},
        title="Perbandingan Durasi Pengiriman Aktual vs Estimasi",
        color_discrete_sequence=["#FFA07A", "#00BFFF"],
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Visualisasi 4: Tren pesanan berdasarkan waktu
    st.subheader("📈 Order Trends Over Time")
    st.markdown("Grafik ini menunjukkan tren jumlah pesanan dari waktu ke waktu, membantu Anda memahami pola pesanan pada periode tertentu.")
    order_trends = data.groupby(data['order_purchase_timestamp'].dt.to_period("M")).size()
    order_trends.index = order_trends.index.to_timestamp()

    fig4 = px.line(
        x=order_trends.index,
        y=order_trends.values,
        labels={'x': 'Time', 'y': 'Number of Orders'},
        title="Tren Jumlah Pesanan dari Waktu ke Waktu",
        color_discrete_sequence=["#2CA02C"],
    )
    fig4.update_traces(mode="lines+markers", line=dict(width=3))
    st.plotly_chart(fig4, use_container_width=True)

else:
    st.info("📥 Upload a CSV file from the sidebar to get started.")

# Footer
st.sidebar.markdown("Developed with ❤️ using Streamlit and Plotly.")
