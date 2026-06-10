import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN DE LA PÁGINA (Diseño limpio y profesional)
st.set_page_config(
    page_title="IA en Gestión de Inventarios",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ENLACE REAL AL CSV EN GITHUB (Consumo Automatizado)
GITHUB_CSV_URL = "https://raw.githubusercontent.com/Gustavox2019/PA-3.1/refs/heads/main/PA4.csv"

# 3. BARRA LATERAL (Sidebar) - Control de Fuentes de Datos y Filtros
st.sidebar.header("⚙️ Configuración del Sistema")

origen_datos = st.sidebar.radio(
    "Selecciona la fuente de datos:",
    ("Consumir automáticamente desde GitHub", "Cargar archivo CSV manualmente")
)

df = None

if origen_datos == "Consumir automáticamente desde GitHub":
    try:
        df = pd.read_csv(GITHUB_CSV_URL)
        st.sidebar.success("✅ Conectado a GitHub exitosamente.")
    except Exception as e:
        st.sidebar.error("⚠️ No se pudo conectar automáticamente. Revisa la URL o carga el archivo manual.")
else:
    archivo_cargado = st.sidebar.file_uploader("Sube tu archivo Scopus CSV aquí", type=["csv"])
    if archivo_cargado is not None:
        df = pd.read_csv(archivo_cargado)
        st.sidebar.success("✅ Archivo local cargado con éxito.")

# 4. PROCESAMIENTO Y RENDERIZADO DEL DASHBOARD
if df is not None:
    # Estandarizar nombres de columnas a minúsculas para evitar conflictos
    df.columns = df.columns.str.lower().str.strip()
    
    # Asegurar formato numérico para las citas
    if 'cited by' in df.columns:
        df['cited by'] = pd.to_numeric(df['cited by'], errors='coerce').fillna(0)

    # --- SECCIÓN DE CABECERA (Pregunta de Investigación y Keywords) ---
    st.title("📦 Inteligencia Artificial para la Optimización de Inventarios")
    st.markdown("### **Pregunta de Investigación:**")
    st.info("¿Cómo se utiliza la Inteligencia Artificial para optimizar la gestión de inventarios en empresas comerciales?")
    
    st.markdown("**Palabras Clave (Keywords) de Búsqueda:**")
    cols_kw = st.columns(4)
    keywords = ["Artificial Intelligence", "Inventory Management", "Supply Chain", "Demand Forecasting"]
    for i, kw in enumerate(keywords):
        cols_kw[i].markdown(f"🔍 `{kw}`")
    
    st.markdown("---")

    # --- BLOQUE DE MÉTRICAS CLAVE (KPIs) ---
    total_articulos = len(df)
    total_citas = int(df['cited by'].sum()) if 'cited by' in df.columns else 0
    total_revistas = df['source title'].nunique() if 'source title' in df.columns else 0
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(label="📚 Artículos Totales", value=total_articulos)
    kpi2.metric(label="⭐ Citas Globales Acumuladas", value=total_citas)
    kpi3.metric(label="🏢 Revistas / Fuentes Indexadas", value=total_revistas)

    st.markdown("---")

    # --- CONTROL DE FILTROS LATERALES ---
    if 'year' in df.columns:
        anios_disponibles = sorted(df['year'].dropna().unique().astype(int))
        st.sidebar.subheader("🎯 Filtrar Resultados")
        anios_seleccionados = st.sidebar.multiselect(
            "Selecciona los años de publicación:",
            options=anios_disponibles,
            default=anios_disponibles
        )
        df_filtrado = df[df['year'].isin(anios_seleccionados)]
    else:
        df_filtrado = df

    # --- ORGANIZACIÓN POR PESTAÑAS (Tabs) ---
    tab1, tab2, tab3 = st.tabs(["📊 Tendencias e Impacto", "🔬 Análisis de Autores y Fuentes", "📋 Vista de Datos Crudos"])

    with tab1:
        st.subheader("Análisis de Tendencias Temporales e Impacto Metodológico")
        
        # Gráfico 1: Ocupa toda la fila superior de la pestaña (100% de ancho)
        if 'year' in df_filtrado.columns:
            df_year = df_filtrado['year'].value_counts().reset_index()
            df_year.columns = ['Año', 'Cantidad de Publicaciones']
            df_year = df_year.sort_values(by='Año')
            
            fig_line = px.line(df_year, x='Año', y='Cantidad de Publicaciones', 
                               title='Madurez Tecnológica: Publicaciones por Año',
                               markers=True, template='plotly_white')
            fig_line.update_layout(xaxis=dict(tickmode='linear', dtick=1))
            st.plotly_chart(fig_line, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True) # Espaciador estético

        # Gráfico 2: Ocupa toda la fila inferior de la pestaña (100% de ancho)
        if 'cited by' in df_filtrado.columns and 'title' in df_filtrado.columns:
            top_cited = df_filtrado.sort_values(by='cited by', ascending=False).head(10)
            # El texto se amplía para un ancho de fila completo
            top_cited['titulo_corto'] = top_cited['title'].str.slice(0, 85) + "..."
            
            fig_cited = px.bar(top_cited, x='cited by', y='titulo_corto', orientation='h',
                               title='Top 10 Artículos con Mayor Impacto (Citas)',
                               labels={'cited by': 'Número de Citas', 'titulo_corto': 'Artículo'},
                               color='cited by', color_continuous_scale='Blues')
            fig_cited.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_cited, use_container_width=True)

    with tab2:
        st.subheader("Análisis de Actores Científicos y Canales de Difusión")
        
        # Gráfico 3: Ocupa toda la fila superior en Tab 2 (100% de ancho)
        if 'authors' in df_filtrado.columns:
            authors_series = df_filtrado['authors'].dropna().str.split(',').explode().str.strip()
            authors_series = authors_series[authors_series != ""]
            top_authors = authors_series.value_counts().head(10).reset_index()
            top_authors.columns = ['Autor', 'Documentos']
            top_authors = top_authors.sort_values(by='Documentos', ascending=True)

            fig_author = px.bar(top_authors, x='Documentos', y='Autor', orientation='h',
                                title='Top 10 Autores con Mayor Producción Científica',
                                text_auto=True, color='Documentos', color_continuous_scale='Cividis')
            st.plotly_chart(fig_author, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Gráfico 4: Ocupa toda la fila inferior en Tab 2 (100% de ancho)
        if 'source title' in df_filtrado.columns:
            top_sources = df_filtrado['source title'].value_counts().head(10).reset_index()
            top_sources.columns = ['Revista / Fuente', 'Artículos']
            top_sources = top_sources.sort_values(by='Artículos', ascending=True)

            fig_source = px.bar(top_sources, x='Artículos', y='Revista / Fuente', orientation='h',
                                title='Top 10 Revistas donde se Publica sobre IA e Inventarios',
                                text_auto=True, color='Artículos', color_continuous_scale='Viridis')
            st.plotly_chart(fig_source, use_container_width=True)

    with tab3:
        st.subheader("Dataset Completo Extraído de Scopus")
        st.markdown("A continuación se presentan los metadatos esenciales limpios utilizados para el análisis estadístico:")
        columnas_visibles = [c for c in ['authors', 'title', 'year', 'source title', 'cited by', 'document type'] if c in df_filtrado.columns]
        st.dataframe(df_filtrado[columnas_visibles], use_container_width=True)

    # --- SECCIÓN FINAL DE EMPATÍA ---
    st.markdown("---")
    st.subheader("💡 Conclusiones del Análisis de Datos")
    st.success(
        f"El análisis de los **{total_articulos}** artículos científicos indexados en Scopus demuestra una fuerte tendencia creciente hacia la automatización logística. "
        "Las publicaciones se concentran estratégicamente en revistas de ingeniería de sistemas y ciencias de decisiones, evidenciando que el **Demand Forecasting (Predicción de la Demanda)** "
        "es el enfoque metodológico de Inteligencia Artificial que más impacto genera para mitigar el sobrestock y optimizar las cadenas de suministro en empresas comerciales modernas."
    )

else:
    st.info("👋 ¡Bienvenido! Selecciona un método de obtención de datos en la barra lateral izquierda para comenzar a analizar la metadata científica.")
