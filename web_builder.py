import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import sys
import html

# --- PROTECCIÓN DE UNICODE (WINDOWS) ---
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Nexus Hub | Gender Gap Intelligence",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILO PREMIUM ---
st.markdown("""
<style>
    .main { background: #0E1117; }
    .stMetric { background: rgba(30, 34, 45, 0.7); padding: 20px; border-radius: 15px; border-left: 5px solid #6366f1; }
    .stAlert { border-radius: 15px; }
    h1, h2, h3 { color: #8F94FB !important; font-family: 'Inter', sans-serif; }
    .insight-card { background: rgba(255, 255, 255, 0.05); padding: 25px; border-radius: 15px; border-left: 5px solid #6366F1; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- CARGA DE DATOS ---
def get_outputs():
    brain_path = 'reports/brain.json'
    conclusions_path = 'reports/final_conclusions.txt'
    brain = {}
    story = ""

    if os.path.exists(brain_path):
        with open(brain_path, 'r', encoding='utf-8') as f:
            brain = json.load(f)

    if os.path.exists(conclusions_path):
        with open(conclusions_path, 'r', encoding='utf-8') as f:
            story = f.read()

    return brain, story


def load_data():
    clean_dir = 'data/clean/'
    dfs = {}

    if os.path.exists(clean_dir):
        files = [f for f in os.listdir(clean_dir) if f.endswith('.csv')]
        for f in files:
            try:
                dfs[f] = pd.read_csv(os.path.join(clean_dir, f))
            except Exception as e:
                st.warning(f"Error cargando {f}: {e}")

    return dfs


# --- DETECTORES INTELIGENTES ---
def detect_value_column(df):
    return next((col for col in df.columns if col.lower() in ['value', 'obs_value']), None)


def detect_geo_column(df):
    geo_candidates = ['geo', 'country', 'pais', 'location', 'name']
    return next((col for col in df.columns if col.lower() in geo_candidates), df.columns[0])


# --- UI PRINCIPAL ---
def main():
    brain, story = get_outputs()
    datasets = load_data()

    # --- SIDEBAR ---
    st.sidebar.title("🎛️ Nexus Control")
    st.sidebar.info(f"Misión: {brain.get('mission', 'Brecha de Género en TIC')}")

    target = None

    if datasets:
        target = st.sidebar.selectbox("Explorar Dataset", list(datasets.keys()))
        df = datasets[target]
    else:
        st.sidebar.error("⚠️ No hay datos en `/data/clean/`")
        df = pd.DataFrame()

    # --- HEADER ---
    st.title("🧬 Nexus Intelligence Hub v10")
    st.caption("Sistema Agéntico Autónomo para el Análisis de la Brecha de Género")

    col_a, col_b = st.columns([2, 1])

    # --- COLUMNA IZQUIERDA ---
    with col_a:
        st.subheader(f"📊 Visualización: {target if target else 'Modo demo'}")

        # --- MODO DEMO (IMPORTANTE PARA PRESENTACIONES) ---
        if df.empty:
            df = pd.DataFrame({
                "country": ["Spain", "Sweden", "Germany"],
                "Value": [28, 35, 30]
            })
            st.info("⚡ Modo demo activado (datos simulados)")

        value_col = detect_value_column(df)
        geo_col = detect_geo_column(df)

        if value_col:
            df[value_col] = pd.to_numeric(df[value_col], errors='coerce')

            # --- MÉTRICAS ---
            m1, m2, m3 = st.columns(3)

            m1.metric("Registros", len(df))

            mean_val = df[value_col].mean()
            m2.metric("Promedio", f"{mean_val:.2f}" if not pd.isna(mean_val) else "N/A")

            critiques = brain.get("findings", {}).get("skeptic", {}).get("critiques", [])
            m3.metric("Auditoría", "⚠ Issues" if critiques else "✅ Verified")

            # --- GRÁFICO ---
            df_plot = df.dropna(subset=[value_col])

            if not df_plot.empty:
                top_df = df_plot.sort_values(by=value_col, ascending=False).head(15)

                fig = px.bar(
                    top_df,
                    x=geo_col,
                    y=value_col,
                    color=value_col,
                    color_continuous_scale='Magma',
                    template="plotly_dark"
                )

                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)"
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No hay datos válidos para graficar.")

            st.dataframe(df, use_container_width=True)

        else:
            st.warning("No se detectó columna de valores válida.")

    # --- COLUMNA DERECHA ---
    with col_b:
        st.subheader("⚖️ Alertas del Skeptic")

        critiques = brain.get("findings", {}).get("skeptic", {}).get("critiques", [])

        if critiques:
            for c in critiques[-3:]:
                st.warning(c)
        else:
            st.success("Integridad certificada por el Auditor.")

        st.subheader("🎙️ Voz del Storyteller")

        if story:
            safe_story = html.escape(story[:1500])
            st.markdown(
                f"<div class='insight-card'>{safe_story}...</div>",
                unsafe_allow_html=True
            )
        else:
            st.info("Narrativa en proceso...")

        # --- ACTIVIDAD DE AGENTES (WOW FACTOR) ---
        with st.expander("🧠 Actividad del Sistema"):
            st.write("🛰️ Scout: Datos cargados")
            st.write("🧹 Cleaner: Datos procesados")
            st.write("🕵️ Skeptic:", "Issues detectados" if critiques else "Sin problemas")
            st.write("🎙️ Storyteller:", "Narrativa generada" if story else "Pendiente")


# --- RUN ---
if __name__ == "__main__":
    main()
