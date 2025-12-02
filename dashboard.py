import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px

# --- CONFIGURACIÓN ---
API_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="Monitor", layout="wide", page_icon="🎛️")

# Estilos CSS para que se vea más "Hacker/Pro"
st.markdown("""
    <style>
    .metric-card {background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #4CAF50;}
    </style>
    """, unsafe_allow_html=True)

st.title("🎛️ Centro de Comando Autonómico ")

# --- BARRA LATERAL (CONTROLES) ---
st.sidebar.header("🕹️ Panel de Control")

# SECCIÓN 1: CAOS (SIMULACIÓN)
st.sidebar.subheader("1. Generar Caos")
if st.sidebar.button("🔥 Simular Tráfico Alto (+30%)"):
    try:
        requests.post(f"{API_URL}/simulate_load?intensity=30")
        st.toast("⚠️ Carga inyectada al servidor", icon="🔥")
    except:
        st.error("Error conectando con Backend")

if st.sidebar.button("🧹 Resetear Todo"):
    try:
        requests.post(f"{API_URL}/reset_simulation")
        st.session_state.history = [] # Limpiar gráfica visual
        st.toast("Sistema reiniciado a estado base", icon="✅")
    except:
        st.error("Error al resetear")

st.sidebar.markdown("---")

# SECCIÓN 2: CURA (ACCIONES MANUALES)
st.sidebar.subheader("2. Acciones Manuales (Actuator)")

col_btn1, col_btn2 = st.sidebar.columns(2)

with col_btn1:
    if st.button("➕ Escalar (Up)"):
        # Llamada a tu endpoint /execute_action
        payload = {"action": "scale_up", "source": "Dashboard Manual"}
        requests.post(f"{API_URL}/execute_action", json=payload)
        st.toast("🚀 Servidor Escalado (Instancia +1)", icon="📈")

with col_btn2:
    if st.button("➖ Reducir (Down)"):
        payload = {"action": "scale_down", "source": "Dashboard Manual"}
        requests.post(f"{API_URL}/execute_action", json=payload)
        st.toast("📉 Servidor Reducido (Instancia -1)", icon="📉")

if st.sidebar.button("🔄 Reinicio de Emergencia"):
    payload = {"action": "restart_service", "source": "Dashboard Manual"}
    requests.post(f"{API_URL}/execute_action", json=payload)
    st.toast("♻️ Servicio Reiniciado (RAM liberada)", icon="🔄")


# --- PANEL PRINCIPAL (VISUALIZACIÓN) ---

# Contenedores para métricas
col1, col2, col3, col4 = st.columns(4)
metric_cpu = col1.empty()
metric_ram = col2.empty()
metric_inst = col3.empty()
metric_resp = col4.empty()

# Espacio para el gráfico
st.subheader("📊 Monitoreo en Tiempo Real")
chart_placeholder = st.empty()

# Tabla de logs recientes (Opcional, para ver qué pasa)
st.subheader("📝 Logs de Acciones")
log_placeholder = st.empty()

# Historial local para el gráfico
if "history" not in st.session_state:
    st.session_state.history = []

def fetch_data():
    try:
        return requests.get(f"{API_URL}/metrics").json()
    except:
        return None

# --- BUCLE DE ACTUALIZACIÓN ---
while True:
    data = fetch_data()
    
    if data:
        # 1. Actualizar Tarjetas con colores dinámicos
        cpu_val = data['cpu']
        cpu_delta = "Normal"
        if cpu_val > 80: cpu_delta = "CRÍTICO"
        
        metric_cpu.metric("CPU Load", f"{cpu_val}%", delta=cpu_delta, delta_color="inverse")
        metric_ram.metric("RAM Usage", f"{data['ram']}%")
        metric_inst.metric("Nodos Activos", f"{data['instances']}")
        metric_resp.metric("Latencia", f"{data['response_time']} ms")

        # 2. Guardar en historial
        st.session_state.history.append(data)
        if len(st.session_state.history) > 60:
            st.session_state.history.pop(0)

        # 3. Dibujar gráfico
        df = pd.DataFrame(st.session_state.history)
        if not df.empty:
            # Crear gráfico con Plotly
            fig = px.line(df, y=["cpu", "ram"], title="Rendimiento del Cluster")
            fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20))
            # Línea roja de peligro
            fig.add_hline(y=80, line_dash="dash", line_color="red")
            chart_placeholder.plotly_chart(fig, use_container_width=True)

    time.sleep(1) # Refresco cada 1 segundo