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

origen_datos = st.sidebar.radio(
    "Selecciona la fuente de datos:",
    ("Consumir automáticamente desde GitHub", "Cargar archivo CSV manualmente")
)

df = None
es_demo = False

# Lógica inteligente de flujo de datos
if origen_datos == "Consumir automáticamente desde GitHub":
    try:
        df = pd.read_csv(GITHUB_CSV_URL
