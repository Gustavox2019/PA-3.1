import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import re

# ==============================================================================
# 🎨 1. INYECCIÓN DE CSS PERSONALIZADO (Diseño Interactivo y Elegante)
# ==============================================================================
st.markdown("""
    <style>
    /* Estilización del contenedor de la aplicación */
    .stApp {
        background-color: #fcfdfd;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Título principal con acento corporativo */
    .dashboard-title {
        font-size: 2.4rem;
        color: #1E3A8A;
        font-weight: 800;
        border-bottom: 3px solid #3B82F6;
        padding-bottom: 8px;
        margin-bottom: 20px;
    }
    
    /* Tarjetas de Métricas (KPI Cards) Avanzadas */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 16px 22px;
        border-radius: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: all 0.25s ease-in-out;
    }
    
    /* Efecto Hover para las tarjetas de investigadores */
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: #3B82F6;
    }
    
    /* Ajuste de los valores de las métricas */
    div[data-testid="stMetricSimpleValue"] {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #2563EB !important;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado principal de la sección
st.markdown('<h1 class="dashboard-title">🧠 IA en Gestión de Inventarios · Vigilancia Científica</h1>', unsafe_allow_html=True)

# ==============================================================================
# 📂 CARGA Y CONEXIÓN CON EL DATASET DE SCOPUS
# ==============================================================================
# Intentamos jalar el DataFrame de los filtros globales de tu App, sino cargamos PA3.csv
if 'df_filtrado' in locals() or 'df_filtrado' in globals():
    df_dashboard = df_filtrado.copy()
else:
    try:
        df_dashboard = pd.read_csv('PA3.csv')
    except FileNotFoundError:
        st.error("❌ No se encontró el archivo 'PA3.csv' en el directorio actual. Por favor, verifica la ruta.")
        st.stop()

# Homogeneizar nombres de columnas a minúsculas y quitar espacios en blanco
df_dashboard.columns = df_dashboard.columns.str.lower().str.strip()

# Formatear columnas críticas para prevenir caídas de tipos de datos
if 'cited by' in df_dashboard.columns:
    df_dashboard['cited by'] = pd.to_numeric(df_dashboard['cited by'], errors='coerce').fillna(0).astype(int)
if 'year' in df_dashboard.columns:
    df_dashboard['year'] = pd.to_numeric(df_dashboard['year'], errors='coerce').fillna(0).astype(int)

# ==============================================================================
# 🛑 FILTRADO DE STOPWORDS Y UNIFICACIÓN DE CONCEPTOS DUPLICADOS
# ==============================================================================
# Términos genéricos redundantes que ensucian la respuesta a tu pregunta de investigación
stopwords_estrictas = {
    'artificial intelligence', 'inventory management', 'supply chain', 'inventory control', 
    'supply chain management', 'optimization', 'management', 'analysis', 'system', 'systems',
    'models', 'model', 'approach', 'research', 'paper', 'results', 'based', 'using', 'applications',
    'case', 'study', 'performance', 'framework', 'industry', 'applied', 'application', 'inventories',
    'intelligent', 'perspective', 'algorithms', 'algorithm', 'review', 'literature review'
}

# Diccionario inteligente: Mapea variaciones léxicas hacia un solo concepto estándar
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
# 🗂️ PESTAÑAS DEL DASHBOARD
# ==============================================================================
sub_tab1, sub_tab2 = st.tabs(["🎯 Enfoques Tecnológicos y Tendencias", "👥 Comparador de Investigadores"])

# ------------------------------------------------------------------------------
# PESTAÑA 1: MINERÍA CONCEPTUAL Y TRACCIÓN TEMPORAL
# ------------------------------------------------------------------------------
with sub_tab1:
    st.markdown("### 📊 Tecnologías de IA y Variables de Stock Aplicadas")
    st.caption("Filtra automáticamente los metadatos de Scopus para aislar el 'CÓMO' se optimiza el inventario en las empresas comerciales.")
    
    if 'author keywords' in df_dashboard.columns:
        # Extraer, procesar y unificar términos conceptuales
        keywords_crudas = ", ".join(df_dashboard['author keywords'].dropna().astype(str).str.lower())
        lista_kw_procesadas = []
        
        for k in re.split(r'[;,]', keywords_crudas):
            termino = k.strip()
            if len(termino) > 3:
                # Aplicar unificación semántica
                termino_unificado = mapeo_conceptos.get(termino, termino)
                if termino_unificado not in stopwords_estrictas:
                    lista_kw_procesadas.append(termino_unificado)
                    
        # Construir Top 15 de conceptos limpios
        conteo_kw = Counter(lista_kw_procesadas)
        df_g1 = pd.DataFrame(conteo_kw.items(), columns=['Concepto Clave', 'Frecuencia']).sort_values(by='Frecuencia', ascending=False).head(15)
        
        # Gráfico 1: Burbujas/Dispersión de Conceptos Limpios
        fig1 = px.scatter(df_g1, x='Frecuencia', y='Concepto Clave', size='Frecuencia', color='Frecuencia',
                          title='Top 15 Soluciones de IA y Parámetros de Stock con Mayor Presencia',
                          color_continuous_scale='Cividis', template='plotly_white')
        fig1.update_layout(margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig1, use_container_width=True)
        
        st.markdown("---")
        
        # Gráfico 2: Evolución Temporal Sin Duplicados
        st.markdown("### 📈 Evolución y Tracción Tecnológica en el Tiempo")
        
        df_kw_year = df_dashboard[['year', 'author keywords']].dropna()
        df_kw_year['author keywords'] = df_kw_year['author keywords'].str.lower()

        # Tecnologías objetivo para evaluar su madurez analítica
        tecnologias_rastreo = ['machine learning', 'deep learning', 'demand forecasting', 'predictive analytics', 'neural networks', 'big data', 'reinforcement learning', 'internet of things', 'blockchain']
        
        registros_tiempo = []
        for idx, row in df_kw_year.iterrows():
            anio = int(row['year'])
            texto_kw = str(row['author keywords'])
            
            # Unificar sinónimos en la cadena de texto cruda antes de buscar la presencia tecnológica
            for clave_sinonimo, valor_unificado in mapeo_conceptos.items():
                texto_kw = texto_kw.replace(clave_sinonimo, valor_unificado)
                
            for tech in tecnologias_rastreo:
                if tech in texto_kw:
                    registros_tiempo.append({'Año': anio, 'Técnica / Enfoque': tech})

        if registros_tiempo:
            df_matrix = pd.DataFrame(registros_tiempo)
            df_grouped = df_matrix.value_counts().reset_index(name='Cantidad de Estudios').sort_values(by='Año')
            
            # Filtrar años con histórico relevante para la IA moderna
            df_grouped = df_grouped[df_grouped['Año'] >= 2016]
            
            fig2 = px.scatter(df_grouped, x='Año', y='Técnica / Enfoque', size='Cantidad de Estudios', 
                              color='Cantidad de Estudios', title='Intensidad de Publicaciones Científicas por Año y Enfoque',
                              color_continuous_scale='Viridis', template='plotly_white')
            fig2.update_layout(xaxis=dict(tickmode='linear', dtick=1), margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("⚠️ No se localizó la columna de metadatos 'Author Keywords'.")

# ------------------------------------------------------------------------------
# PESTAÑA 2: COMPARA E AISLA ACTORES / INVESTIGADORES
# ------------------------------------------------------------------------------
with sub_tab2:
    st.markdown("### 👥 Panel de Control e Impacto de Investigadores")
    st.caption("Selecciona y contrasta en tiempo real el volumen de producción científica e impacto de citas acumuladas de los autores.")
    
    if 'authors' in df_dashboard.columns:
        # Extraer autores unitarios limpios eliminando nulos
        todos_autores = df_dashboard['authors'].dropna().str.split(',').explode().str.strip()
        autores_unicos = sorted(todos_autores[todos_autores != ""].unique())
        
        # Selector múltiple interactivo nativo con buscador
        autores_seleccionados = st.multiselect(
            "🔍 Selecciona los autores para aislar su información y comparar:",
            options=autores_unicos,
            default=autores_unicos[:2] if len(autores_unicos) > 1 else autores_unicos[0:1]
        )
        
        if autores_seleccionados:
            # Filtrado exacto por autores usando expresiones regulares seguras
            patron_busqueda = '|'.join([re.escape(a) for a in autores_seleccionados])
            df_autores_filt = df_dashboard[df_dashboard['authors'].str.contains(patron_busqueda, case=False, na=False)]
            
            datos_mapeados = []
            for _, fila in df_autores_filt.iterrows():
                for autor in autores_seleccionados:
                    if autor.lower() in fila['authors'].lower():
                        datos_mapeados.append({
                            'Autor': autor,
                            'Título': fila['title'],
                            'Revista / Fuente': fila.get('source title', 'N/A'),
                            'Año': fila['year'],
                            'Citas': fila['cited by']
                        })
            
            df_comparativa_final = pd.DataFrame(datos_mapeados)
            
            if not df_comparativa_final.empty:
                st.markdown("#### 📊 Tarjetas de Rendimiento Consolidado (Efecto CSS Hover)")
                
                df_resumen = df_comparativa_final.groupby('Autor').agg(
                    Articulos=('Título', 'count'),
                    Citas_Totales=('Citas', 'sum')
                ).reset_index()
                
                # Renderizar KPIs distribuidos dinámicamente en columnas
                cols_tarjetas = st.columns(len(autores_seleccionados))
                for idx, autor in enumerate(autores_seleccionados):
                    sub_df = df_resumen[df_resumen['Autor'] == autor]
                    if not sub_df.empty:
                        arts = sub_df.iloc[0]['Articulos']
                        citas = sub_df.iloc[0]['Citas_Totales']
                        cols_tarjetas[idx].metric(
                            label=f"👤 {autor}", 
                            value=f"{arts} Art. / {int(citas)} Citas"
                        )
                
                st.markdown("---")
                
                # Visualización Gráfica Cruzada
                col_g1, col_g2 = st.columns(2)
                
                with col_g1:
                    fig_bar_citas = px.bar(df_resumen, x='Autor', y='Citas_Totales', color='Autor', text='Articulos',
                                           title='Citas Acumuladas Scopus (Número = Cantidad de Artículos)',
                                           color_discrete_sequence=px.colors.qualitative.Safe, template='plotly_white')
                    st.plotly_chart(fig_bar_citas, use_container_width=True)
                    
                with col_g2:
                    df_linea_tiempo = df_comparativa_final.groupby(['Autor', 'Año']).size().reset_index(name='Artículos')
                    fig_linea_prod = px.line(df_linea_tiempo, x='Año', y='Artículos', color='Autor', markers=True,
                                             title='Historial y Línea de Producción Científica Anual',
                                             color_discrete_sequence=px.colors.qualitative.Safe, template='plotly_white')
                    fig_linea_prod.update_layout(xaxis=dict(tickmode='linear', dtick=1))
                    st.plotly_chart(fig_linea_prod, use_container_width=True)
                
                # Estructura transaccional de los documentos seleccionados
                st.markdown("#### 📋 Producción Científica Detallada de la Selección")
                st.dataframe(df_comparativa_final[['Autor', 'Título', 'Revista / Fuente', 'Año', 'Citas']], use_container_width=True)
            else:
                st.info("No se hallaron coincidencias estructuradas para los autores seleccionados.")
        else:
            st.warning("⚠️ Elige por lo menos un investigador en el cuadro superior para generar la comparación.")
    else:
        st.error("La columna 'Authors' requerida para mapear a los investigadores no existe en el archivo actual.")
