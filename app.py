import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import re

# ==============================================================================
# 🎨 1. INYECCIÓN DE CSS PERSONALIZADO (Estilo Ejecutivo y Minimalista)
# ==============================================================================
st.markdown("""
    <style>
    /* Fondo limpio y tipografía profesional */
    .stApp {
        background-color: #fcfdfd;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }
    
    /* Título principal con diseño sobrio y elegante */
    .dashboard-title {
        font-size: 2.2rem;
        color: #0F172A; /* Azul oscuro casi negro */
        font-weight: 700;
        letter-spacing: -0.5px;
        border-left: 5px solid #2563EB; /* Línea de acento azul */
        padding-left: 15px;
        margin-bottom: 25px;
        margin-top: 10px;
    }
    
    /* Tarjetas de Métricas (KPI Cards) Tipo Dashboard Corporativo */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    /* Hover sutil sin exagerar */
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
        border-color: #cbd5e1;
    }
    
    /* Color del valor numérico de los investigadores */
    div[data-testid="stMetricSimpleValue"] {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #1E40AF !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título del Dashboard
st.markdown('<div class="dashboard-title">IA en Gestión de Inventarios · Análisis Bibliométrico</div>', unsafe_allow_html=True)

# ==============================================================================
# 📂 CONEXIÓN CON EL DATASET PA3.CSV
# ==============================================================================
if 'df_filtrado' in locals() or 'df_filtrado' in globals():
    df_dashboard = df_filtrado.copy()
else:
    try:
        df_dashboard = pd.read_csv('PA3.csv')
    except FileNotFoundError:
        st.error("❌ No se encontró el archivo 'PA3.csv'. Verifica que esté en la raíz de tu proyecto.")
        st.stop()

# Estandarizar columnas
df_dashboard.columns = df_dashboard.columns.str.lower().str.strip()

# Formatear tipos de datos numéricos
if 'cited by' in df_dashboard.columns:
    df_dashboard['cited by'] = pd.to_numeric(df_dashboard['cited by'], errors='coerce').fillna(0).astype(int)
if 'year' in df_dashboard.columns:
    df_dashboard['year'] = pd.to_numeric(df_dashboard['year'], errors='coerce').fillna(0).astype(int)

# ==============================================================================
# 🛑 FILTRADO SEMÁNTICO Y UNIFICACIÓN (Cero conceptos repetidos)
# ==============================================================================
stopwords_estrictas = {
    'artificial intelligence', 'inventory management', 'supply chain', 'inventory control', 
    'supply chain management', 'optimization', 'management', 'analysis', 'system', 'systems',
    'models', 'model', 'approach', 'research', 'paper', 'results', 'based', 'using', 'applications',
    'case', 'study', 'performance', 'framework', 'industry', 'applied', 'application', 'inventories',
    'intelligent', 'perspective', 'algorithms', 'algorithm', 'review', 'literature review', 'stochastic model'
}

mapeo_conceptos = {
    'machine learning algorithm': 'machine learning',
    'machine-learning': 'machine learning',
    'deep learning neural network': 'deep learning',
    'deep-learning': 'deep learning',
    'demand forecast': 'demand forecasting',
    'forecasting': 'demand forecasting',
    'predictive analytic': 'predictive analytics',
    'neural network': 'neural networks',
    'internet of things (iot)': 'internet of things',
    'iot': 'internet of things',
    'rfid technology': 'rfid',
    'genetic algorithm': 'genetic algorithms'
}

# ==============================================================================
# 🗂️ PESTAÑAS DEL INTERFAZ
# ==============================================================================
sub_tab1, sub_tab2 = st.tabs(["🎯 Enfoques Tecnológicos", "👥 Comparador de Investigadores"])

# ------------------------------------------------------------------------------
# PESTAÑA 1: DISEÑO LIMPIO (BARRAS HORIZONTALES ORDENADAS)
# ------------------------------------------------------------------------------
with sub_tab1:
    st.markdown("### 📊 Tecnologías y Variables Operativas Clave")
    st.caption("Principales sub-técnicas y enfoques extraídos de Scopus que responden cómo la IA optimiza el inventario.")
    
    if 'author keywords' in df_dashboard.columns:
        # Procesamiento de palabras clave
        keywords_crudas = ", ".join(df_dashboard['author keywords'].dropna().astype(str).str.lower())
        lista_kw_procesadas = []
        
        for k in re.split(r'[;,]', keywords_crudas):
            termino = k.strip()
            if len(termino) > 3:
                termino_unificado = mapeo_conceptos.get(termino, termino)
                if termino_unificado not in stopwords_estrictas:
                    lista_kw_procesadas.append(termino_unificado)
                    
        # Dataframe del Top 12 conceptos (más estético que 15 o 20)
        conteo_kw = Counter(lista_kw_procesadas)
        df_g1 = pd.DataFrame(conteo_kw.items(), columns=['Concepto', 'Frecuencia']).sort_values(by='Frecuencia', ascending=True).html_safe().head(12)
        
        # NUEVO GRÁFICO 1: Barras horizontales limpias, ordenadas y monocromáticas
        fig1 = px.bar(df_g1, x='Frecuencia', y='Concepto', orientation='h',
                      text='Frecuencia',
                      title='Frecuencia de Aparición de Conceptos en la Literatura',
                      color_discrete_sequence=['#1E40AF'], # Azul institucional sobrio
                      template='plotly_white')
        
        fig1.update_traces(textposition='outside', cliponaxis=False)
        fig1.update_layout(
            xaxis_title="Número de Artículos",
            yaxis_title="",
            margin=dict(l=15, r=40, t=40, b=10),
            height=450
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        st.markdown("---")
        
        # NUEVO GRÁFICO 2: Evolución Temporal en Formato de Líneas Limpias
        st.markdown("### 📈 Tendencia y Adopción de Tecnologías en el Tiempo")
        
        df_kw_year = df_dashboard[['year', 'author keywords']].dropna()
        df_kw_year['author keywords'] = df_kw_year['author keywords'].str.lower()

        # Reducimos a las 5 tecnologías core más importantes para que no se vea saturado
        tecnologias_rastreo = ['machine learning', 'deep learning', 'demand forecasting', 'predictive analytics', 'internet of things']
        
        registros_tiempo = []
        for idx, row in df_kw_year.iterrows():
            anio = int(row['year'])
            texto_kw = str(row['author keywords'])
            
            for clave_sinonimo, valor_unificado in mapeo_conceptos.items():
                texto_kw = texto_kw.replace(clave_sinonimo, valor_unificado)
                
            for tech in tecnologias_rastreo:
                if tech in texto_kw:
                    registros_tiempo.append({'Año': anio, 'Tecnología': tech})

        if registros_tiempo:
            df_matrix = pd.DataFrame(registros_tiempo)
            df_grouped = df_matrix.value_counts().reset_index(name='Artículos').sort_values(by='Año')
            
            # Filtrar para mostrar solo el rango más moderno y relevante
            df_grouped = df_grouped[(df_grouped['Año'] >= 2018) & (df_grouped['Año'] <= 2026)]
            
            # Gráfico de líneas sofisticado
            fig2 = px.line(df_grouped, x='Año', y='Artículos', color='Tecnología', markers=True,
                           title='Evolución del interés científico anual (2018 - 2026)',
                           color_discrete_sequence=px.colors.qualitative.Slate, # Paleta elegante gris/azul/verde opaco
                           template='plotly_white')
            
            fig2.update_layout(
                xaxis=dict(tickmode='linear', dtick=1),
                xaxis_title="Año de Publicación",
                yaxis_title="Cantidad de Investigaciones",
                margin=dict(l=10, r=10, t=40, b=10),
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("⚠️ La columna 'Author Keywords' no está disponible.")

# ------------------------------------------------------------------------------
# PESTAÑA 2: COMPARADOR INTERACTIVO
# ------------------------------------------------------------------------------
with sub_tab2:
    st.markdown("### 👥 Panel Comparativo de Investigadores")
    st.caption("Busca y selecciona autores específicos para aislar y contrastar sus métricas de rendimiento.")
    
    if 'authors' in df_dashboard.columns:
        todos_autores = df_dashboard['authors'].dropna().str.split(',').explode().str.strip()
        autores_unicos = sorted(todos_autores[todos_autores != ""].unique())
        
        autores_seleccionados = st.multiselect(
            "🔍 Escribe o selecciona los investigadores a comparar:",
            options=autores_unicos,
            default=autores_unicos[:2] if len(autores_unicos) > 1 else autores_unicos[0:1]
        )
        
        if autores_seleccionados:
            patron_busqueda = '|'.join([re.escape(a) for a in autores_seleccionados])
            df_autores_filt = df_dashboard[df_dashboard['authors'].str.contains(patron_busqueda, case=False, na=
