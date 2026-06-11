import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import re

# 1. CONFIGURACIÓN DE LA PÁGINA (Diseño limpio y profesional)
st.set_page_config(
    page_title="IA en Gestión de Inventarios",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enlace real a tu repositorio de GitHub
GITHUB_CSV_URL = "https://raw.githubusercontent.com/Gustavox2019/PA-3.1/refs/heads/main/PA3.csv"

# --- FUNCIÓN PARA GENERAR DATA DE DEMOSTRACIÓN (PLANTILLA MOCK CON KEYWORDS INCLUIDAS) ---
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
        'document type': ['Article', 'Article', 'Conference Paper', 'Article', 'Conference Paper', 'Article', 'Article', 'Book Chapter', 'Article', 'Article', 'Conference Paper', 'Article'],
        'author keywords': [
            'artificial intelligence; predictive analytics; inventory optimization',
            'machine learning; supply chain; optimization',
            'deep learning; demand forecasting; warehouses',
            'neural networks; automated replenishment; inventory control',
            'artificial intelligence; supply chain management; multi-echelon',
            'reinforcement learning; safety stock; inventory control',
            'internet of things; big data; smart forecasting',
            'big data; warehouse management; commercial distribution',
            'heuristic algorithms; inventory control; stockout prevention',
            'generative ai; smart warehouse; artificial intelligence',
            'deep learning; predictive analytics; demand forecasting',
            'machine learning; inventory control; neural networks'
        ],
        'abstract': [
            'This paper focuses on predictive artificial intelligence models for forecasting...',
            'An analysis of machine learning integration within retail supply chains...',
            'Deep learning architectures applied to demand forecasting across warehouses...',
            'Automated replenishment inventory management using neural network control...',
            'AI frameworks optimizing multi-echelon warehouse and distribution systems...',
            'Reinforcement learning controls dynamic safety stock under inventory uncertainty...',
            'IoT and smart forecasting systems applied to logistics and supply chain analytics...',
            'Big data analysis for warehouse management and commercial distribution networks...',
            'Heuristic algorithms designed for inventory stockout prevention in retail...',
            'Generative architectures for smart warehouse organization and data logistics...',
            'Transformers models for multi-echelon predictive demand planning...',
            'Next-generation logistics management driven by intelligent inventory control...'
        ]
    }
    return pd.DataFrame(data_demo)

# 2. BARRA LATERAL (Sidebar) - Control de Fuentes de Datos
st.sidebar.header("⚙️ Configuración del Sistema")

origen_datos = st.sidebar.radio(
    "Selecciona la fuente de datos:",
    ("Consumir automáticamente desde GitHub", "Cargar archivo CSV manualmente")
)

df = None
es_demo = False

# Lógica inteligente para el flujo de datos
if origen_datos == "Consumir automáticamente desde GitHub":
    try:
        df = pd.read_csv(GITHUB_CSV_URL)
        st.sidebar.success("✅ Conectado a GitHub exitosamente.")
    except Exception as e:
        st.sidebar.error("⚠️ Error al conectar con GitHub. Mostrando plantilla de previsualización.")
        df = generar_data_demo()
        es_demo = True
else:
    archivo_cargado = st.sidebar.file_uploader("Sube tu archivo Scopus CSV aquí", type=["csv"])
    if archivo_cargado is not None:
        df = pd.read_csv(archivo_cargado)
        st.sidebar.success("✅ Archivo local cargado con éxito.")
    else:
        df = generar_data_demo()
        es_demo = True
        st.sidebar.warning("📌 A la espera del archivo Scopus. Visualizando plantilla guía abajo.")

# 3. PROCESAMIENTO Y RENDERIZADO DEL DASHBOARD
if df is not None:
    # Estandarizar nombres de columnas a minúsculas y limpiar espacios para evitar fallos de Scopus
    df.columns = df.columns.str.lower().str.strip()
    
    if 'cited by' in df.columns:
        df['cited by'] = pd.to_numeric(df['cited by'], errors='coerce').fillna(0)

    # --- INDICADOR DE MODO PLANTILLA / DEMO ---
    if es_demo:
        st.warning("📢 **MODO PREVISUALIZACIÓN ACTIVO:** Estás viendo la estructura del dashboard con datos simulados de ejemplo. Cuando subas tu archivo CSV o conectes GitHub correctamente, tus métricas reales de Scopus reemplazarán estos gráficos.")

    # --- SECCIÓN DE CABECERA ---
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

    # --- ORGANIZACIÓN POR PESTAÑAS ---
    tab1, tab2, tab3 = st.tabs(["📊 Tendencias y Tipología", "🔬 Análisis de Autores, Fuentes y Contenido", "📋 Vista de Datos Crudos"])

    with tab1:
        st.subheader("Análisis de Evolución Temporal y Tipología Documental")
        
        # Gráfico Original: Línea de Tiempo
        if 'year' in df_filtrado.columns:
            df_year = df_filtrado['year'].value_counts().reset_index()
            df_year.columns = ['Año', 'Cantidad de Publicaciones']
            df_year = df_year.sort_values(by='Año')
            
            fig_line = px.line(df_year, x='Año', y='Cantidad de Publicaciones', 
                               title='Madurez Tecnológica: Evolución de Publicaciones por Año',
                               markers=True, template='plotly_white')
            fig_line.update_layout(xaxis=dict(tickmode='linear', dtick=1))
            st.plotly_chart(fig_line, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        # 🔄 NUEVO INTEGRADO - GRÁFICO 2: Intensidad Tecnológica por Año (Burbujas Temporales)
        if 'year' in df_filtrado.columns and 'author keywords' in df_filtrado.columns:
            df_kw_year = df_filtrado[['year', 'author keywords']].dropna()
            df_kw_year['author keywords'] = df_kw_year['author keywords'].str.lower()

            tecnologias_rastreo = [
                'machine learning', 'deep learning', 'demand forecasting', 
                'predictive analytics', 'neural networks', 'big data', 
                'reinforcement learning', 'internet of things', 'blockchain'
            ]

            registros_tiempo = []
            for idx, row in df_kw_year.iterrows():
                anio = int(row['year'])
                texto_kw = str(row['author keywords'])
                for tech in tecnologias_rastreo:
                    if tech in texto_kw:
                        registros_tiempo.append({'Año': anio, 'Técnica / Enfoque': tech})

            if registros_tiempo:
                df_matrix = pd.DataFrame(registros_tiempo)
                df_grouped = df_matrix.value_counts().reset_index(name='Cantidad de Estudios').sort_values(by='Año')

                fig2 = px.scatter(
                    df_grouped, x='Año', y='Técnica / Enfoque', size='Cantidad de Estudios',
                    color='Cantidad de Estudios', title='Gráfico de Intensidad Tecnológica (Evolución de Enfoques Core)',
                    color_continuous_scale='Viridis', template='plotly_white'
                )
                fig2.update_layout(xaxis=dict(tickmode='linear', dtick=1))
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("ℹ️ No se detectaron tecnologías core específicas en las palabras clave para los años seleccionados.")
        
        st.markdown("<br>", unsafe_allow_html=True)

        # Gráfico Original: Distribución por Tipo de Documento
        if 'document type' in df_filtrado.columns:
            type_counts = df_filtrado['document type'].value_counts().reset_index()
            type_counts.columns = ['Tipo de Documento', 'Cantidad']

            fig_type = px.pie(type_counts, values='Cantidad', names='Tipo de Documento', hole=0.4,
                              title='Tipología Documental: Preferencia de Canales de Difusión',
                              color_discrete_sequence=px.colors.qualitative.Safe)
            fig_type.update_traces(textinfo='percent+label')
            st.plotly_chart(fig_type, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Gráfico Original: Artículos más citados
        if 'cited by' in df_filtrado.columns and 'title' in df_filtrado.columns:
            top_cited = df_filtrado.sort_values(by='cited by', ascending=False).head(10)
            top_cited['titulo_corto'] = top_cited['title'].str.slice(0, 85) + "..."
            
            fig_cited = px.bar(top_cited, x='cited by', y='titulo_corto', orientation='h',
                               title='Top 10 Artículos con Mayor Impacto Académico (Citas)',
                               labels={'cited by': 'Número de Citas', 'titulo_corto': 'Artículo'},
                               color='cited by', color_continuous_scale='Blues')
            fig_cited.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_cited, use_container_width=True)

    with tab2:
        st.subheader("Análisis de Actores Científicos y Semántica de Contenido")
        
        # Gráfico Original: Top Autores
        if 'authors' in df_filtrado.columns:
            authors_series = df_filtrado['authors'].dropna().str.split(',').explode().str.strip()
            authors_series = authors_series[authors_series != ""]
            top_authors = authors_series.value_counts().head(10).reset_index()
            top_authors.columns = ['Autor', 'Documentos']
            top_authors = top_authors.sort_values(by='Documentos', ascending=True)

            fig_author = px.bar(top_authors, x='Documentos', y='Autor', orientation='h',
                                title='Top 10 Autores con Mayor Production Científica',
                                text_auto=True, color='Documentos', color_continuous_scale='Cividis')
            st.plotly_chart(fig_author, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Gráfico Original: Top Revistas
        if 'source title' in df_filtrado.columns:
            top_sources = df_filtrado['source title'].value_counts().head(10).reset_index()
            top_sources.columns = ['Revista / Fuente', 'Artículos']
            top_sources = top_sources.sort_values(by='Artículos', ascending=True)

            fig_source = px.bar(top_sources, x='Artículos', y='Revista / Fuente', orientation='h',
                                title='Top 10 Revistas donde se Publica sobre IA e Inventarios',
                                text_auto=True, color='Artículos', color_continuous_scale='Viridis')
            st.plotly_chart(fig_source, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 🔄 NUEVO INTEGRADO - GRÁFICO 1: Burbujas de Conceptos Específicos (Keywords de Autor)
        if 'author keywords' in df_filtrado.columns:
            st.markdown("### 🏷️ Minería de Textos: Palabras Clave del Autor")
            keywords_totales = ", ".join(df_filtrado['author keywords'].dropna().astype(str).str.lower())
            lista_kw = [k.strip() for k in re.split(r'[;,]', keywords_totales) if len(k.strip()) > 3]

            conteo_kw = Counter(lista_kw)
            
            # Diccionario de Stopwords de tu código original
            stopwords_keywords = {
                'artificial intelligence', 'inventory management', 'supply chain', 'inventory control',
                'supply chain management', 'optimization', 'management', 'analysis', 'system', 'systems',
                'models', 'model', 'approach', 'research', 'paper', 'results', 'based', 'using', 'applications',
                'case', 'study', 'performance', 'framework', 'industry', 'applied', 'application'
            }

            kw_filtradas = {k: v for k, v in conteo_kw.items() if k not in stopwords_keywords}

            if kw_filtradas:
                df_g1 = pd.DataFrame(kw_filtradas.items(), columns=['Concepto Clave', 'Frecuencia']).sort_values(by='Frecuencia', ascending=False).head(20)

                fig1 = px.scatter(
                    df_g1, x='Frecuencia', y='Concepto Clave', size='Frecuencia', color='Frecuencia',
                    title='Gráfico de Burbujas: Sub-técnicas de IA y Componentes Logísticos más Investigados',
                    color_continuous_scale='Cividis', template='plotly_white'
                )
                fig1.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("ℹ️ No se encontraron suficientes palabras clave para mostrar tras el filtrado.")

        st.markdown("<br>", unsafe_allow_html=True)

        # Gráfico Original: Análisis Semántico en Abstracts (NLP)
        if 'abstract' in df_filtrado.columns:
            st.markdown("### 🔍 Análisis de Palabras Frecuentes en los Abstracts (NLP)")
            
            texto_completo = " ".join(df_filtrado['abstract'].dropna().astype(str).str.lower())
            palabras = re.findall(r'\b[a-z]{4,}\b', texto_completo)
            
            stopwords_abstracts = {
                'this', 'that', 'with', 'from', 'they', 'have', 'were', 'been', 'which',
                'their', 'about', 'paper', 'study', 'research', 'using', 'based', 'used',
                'analysis', 'results', 'proposed', 'method', 'approach', 'system', 'inventory',
                'management', 'supply', 'chain', 'optimization', 'intelligence', 'artificial',
                'application', 'applications', 'control', 'systems', 'models', 'model', 'results',
                'framework', 'efficient', 'performance', 'paper', 'studies', 'presents', 'developed'
            }
            
            palabras_filtradas = [p for p in palabras if p not in stopwords_abstracts]
            conteo_palabras = Counter(palabras_filtradas).most_common(15)
            
            if conteo_palabras:
                df_palabras = pd.DataFrame(conteo_palabras, columns=['Término', 'Frecuencia'])
                df_palabras = df_palabras.sort_values(by='Frecuencia', ascending=True)
                
                fig_words = px.bar(
                    df_palabras, x='Frecuencia', y='Término', orientation='h',
                    title='Top 15 Términos Conceptuales más Frecuentes en los Resúmenes de Scopus',
                    labels={'Frecuencia': 'Conteo de Apariciones', 'Término': 'Palabra Clave'},
                    color='Frecuencia', color_continuous_scale='Teal'
                )
                st.plotly_chart(fig_words, use_container_width=True)

    with tab3:
        st.subheader("Dataset Completo Extraído de Scopus")
        st.markdown("A continuación se presentan los metadatos esenciales limpios utilizados para el análisis estadístico:")
        columnas_visibles = [c for c in ['authors', 'title', 'year', 'source title', 'cited by', 'document type', 'author keywords', 'abstract'] if c in df_filtrado.columns]
        st.dataframe(df_filtrado[columnas_visibles], use_container_width=True)

    # --- SECCIÓN DE CONCLUSIONES ---
    st.markdown("---")
    st.subheader("💡 Conclusiones del Análisis de Datos")
    st.success(
        f"El análisis de los **{total_articulos}** artículos científicos indexados en Scopus demuestra una fuerte tendencia creciente hacia la automatización logística. "
        "Las publicaciones se concentran estratégicamente en revistas de ingeniería de sistemas y ciencias de decisiones, evidenciando que el **Demand Forecasting (Predicción de la Demanda)** "
        "es el enfoque metodológico de Inteligencia Artificial que más impacto genera para mitigar el sobrestock y optimizar las cadenas de suministro en empresas comerciales modernas."
    )
