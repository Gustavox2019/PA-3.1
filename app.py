import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="IA en Gestión de Inventarios",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL Real de tu GitHub
GITHUB_CSV_URL = "https://raw.githubusercontent.com/Gustavox2019/PA-3.1/refs/heads/main/PA4.csv"

# --- FUNCIÓN PARA GENERAR DATA DE DEMOSTRACIÓN (PLANTILLA MOCK) ---
def generar_data_demo():
    data_demo = {
        'year': [2020, 2021, 2021, 2022, 2022, 2023, 2023, 2024, 2024, 2025, 2025, 2026],
        'title': [
            'Predictive AI for Commercial Inventory Optimization',
            'Machine Learning Models in Retail Supply Chains',
            'Deep Learning for Demand Forecasting in Warehouses',
            'Automated Stock Replenishment using Neural Networks',
            'AI-Driven Multi-Echelon Inventory Systems',
            'Reinforcement Learning for Dynamic Safety Stock',
            'IoT and AI Integration for Real-Time Logistics',
            'Big Data Analytics in Commercial Distribution',
            'Heuristic Algorithms for Stockout Prevention',
            'Generative AI for Smart Warehouse Management',
            'Transformers Models applied to Inventory Planning',
            'Next-Gen AI Architectures for Global Supply Chains'
        ],
        'authors': [
            'Smith, J.', 'Taylor, M.', 'Wang, L.', 'Garcia, A.', 'Li, Y.', 
            'Kim, D.', 'Martinez, R.', 'Chen, H.', 'Smith, J.', 'Taylor, M.',
            'Wang, L.', 'Garcia, A.'
        ],
        'source title': [
            'Journal of Logistics and AI', 'International Retail Review', 
            'IEEE Transactions on Automation', 'Supply Chain Management Journal',
            'Journal of Logistics and AI', 'International Retail Review',
            'IEEE Transactions on Automation', 'Supply Chain Management Journal',
            'Journal of Logistics and AI', 'International Retail Review',
            'IEEE Transactions on Automation', 'Supply Chain Management Journal'
        ],
        'cited by': [120, 85, 95, 110, 45, 60, 30, 25, 15, 10, 5, 1],
        'document type': ['Article', 'Article', 'Conference Paper', 'Article', 'Conference Paper', 'Article', 'Article', 'Book Chapter', 'Article', 'Article', 'Conference Paper', 'Article']
    }
    return pd.DataFrame(data_demo)

# 2. BARRA LATERAL (Sidebar) - Simplificada a solo 2 Opciones
st.sidebar.header("⚙️ Configuración del Sistema")

# ==============================================================================
# BLOQUE CORREGIDO: REEMPLAZA ESTA SECCIÓN EN TU APP.PY (Líneas 55 a 76 aprox.)
# ==============================================================================

# Lógica inteligente de flujo de datos
if origen_datos == "Consumir automáticamente desde GitHub":
    try:
        # AQUÍ ESTÁ LA CORRECCIÓN: Cerramos correctamente el paréntesis al final
        df = pd.read_csv(GITHUB_CSV_URL)
        st.sidebar.success("✅ Conectado a GitHub exitosamente.")
    except Exception as e:
        # Si falla GitHub por red, muestra la plantilla interactiva en lugar de romperse
        st.sidebar.error("⚠️ Error al conectar con GitHub. Mostrando plantilla de previsualización.")
        df = generar_data_demo()
        es_demo = True
else:
    # Sección manual de carga
    archivo_cargado = st.sidebar.file_uploader("Sube tu archivo Scopus CSV aquí", type=["csv"])
    if archivo_cargado is not None:
        df = pd.read_csv(archivo_cargado)
        st.sidebar.success("✅ Archivo local cargado con éxito.")
    else:
        # Mientras no cargue el archivo, se inyecta la plantilla de muestra automáticamente
        df = generar_data_demo()
        es_demo = True
        st.sidebar.warning("📌 A la espera del archivo Scopus. Visualizando plantilla guía abajo.")
