import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import re

# 1. CONFIGURACIÓN DE LA PÁGINA (Diseño limpio y profesional)
st.set_page_config(
    page_title="IA en Gestión de Inventarios - Executive Analytics",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enlace real a tu repositorio de GitHub
GITHUB_CSV_URL = "https://raw.githubusercontent.com/Gustavox2019/PA-3.1/refs/heads/main/PA3.csv"

# --- FUNCIÓN PARA GENERAR DATA DE DEMOSTRACIÓN ---
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

# 2. BARRA LATERAL (Sidebar)
st.sidebar.header("⚙️ Configuración del Sistema")

origen_datos = st.sidebar.radio(
    "Selecciona la fuente de datos:",
    ("Consumir automáticamente desde GitHub", "Cargar archivo CSV manualmente")
)

df = None
es_demo = False

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
        st.sidebar.warning("📌 A la espera del archivo Scopus.")

# 3. PROCESAMIENTO Y RENDERIZADO DEL DASHBOARD
if df is not None:
    df.columns = df.columns.str.lower().str.strip()
    if 'cited by' in df.columns:
        df['cited by'] = pd.to_numeric(df['cited by'], errors='coerce').fillna(0)

    if es_demo:
        st.warning("📢 **MODO PREVISUALIZACIÓN ACTIVO:** Viendo estructura con datos simulados.")

    # --- CABECERA ---
    st.title("📦 Inteligencia Artificial para la Optimización de Inventarios")
    st.markdown("### **Pregunta de Investigación:**")
    st.info("¿Cómo se utiliza la Inteligencia Artificial para optimizar la gestión de inventarios en empresas comerciales?")
    
    # --- BLOQUE DE MÉTRICAS CLAVE (KPIs) ---
    total_articulos = len(df)
    total_citas = int(df['cited by'].sum()) if 'cited by' in df.columns else 0
    total_revistas = df['source title'].nunique() if 'source title' in df.columns else 0
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(label="📚 Artículos Totales", value=total_articulos)
    kpi2.metric(label="⭐ Citas Globales Acumuladas", value=total_citas)
    kpi3.metric(label="🏢 Revistas Indexadas", value=total_revistas)

    st.markdown("---")

    # --- FILTROS ---
    if 'year' in df.columns:
        anios_disponibles = sorted(df['year'].dropna().unique().astype(int))
        anios_seleccionados = st.sidebar.multiselect("Selecciona los años:", options=anios_disponibles, default=anios_disponibles)
        df_filtrado = df[df['year'].isin(anios_seleccionados)]
    else:
        df_filtrado = df

    # --- PESTAÑAS ---
    tab1, tab2, tab3 = st.tabs(["📊 Tendencias y Tipología", "🔬 Análisis de Autores y Contenido", "📋 Datos Crudos"])

    with tab1:
        st.subheader("Evolución Temporal y Tipología Documental")
        
        # 1. Gráfico de Línea Temporal
        if 'year' in df_filtrado.columns:
            c1, c2 = st.columns([3, 1])
            with c1:
                df_year = df_filtrado['year'].value_counts().reset_index()
                df_year.columns = ['Año', 'Cantidad de Publicaciones']
                df_year = df_year.sort_values(by='Año')
                fig_line = px.line(df_year, x='Año', y='Cantidad de Publicaciones', markers=True, template='plotly_white', title='Evolución de Publicaciones por Año')
                fig_line.update_layout(xaxis=dict(tickmode='linear', dtick=1))
                st.plotly_chart(fig_line, use_container_width=True)
            with c2:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.info("**¿Para qué sirve?**\n\nMide la **vigencia y adopción** del tema. Valida si la optimización con IA es una tendencia creciente en el mercado.")

        st.markdown("---")

        # 2. Gráfico de Burbujas Temporales
        if 'year' in df_filtrado.columns and 'author keywords' in df_filtrado.columns:
            c3, c4 = st.columns([3, 1])
            with c3:
                df_kw_year = df_filtrado[['year', 'author keywords']].dropna()
                df_kw_year['author keywords'] = df_kw_year['author keywords'].str.lower()
                tecnologias_rastreo = ['machine learning', 'deep learning', 'demand forecasting', 'predictive analytics', 'neural networks', 'big data', 'reinforcement learning', 'internet of things', 'blockchain']
                registros_tiempo = []
                for idx, row in df_kw_year.iterrows():
                    anio = int(row['year'])
                    texto_kw = str(row['author keywords'])
                    for tech in tecnologias_rastreo:
                        if tech in texto_kw: registros_tiempo.append({'Año': anio, 'Técnica': tech})
                
                if registros_tiempo:
                    df_matrix = pd.DataFrame(registros_tiempo)
                    df_grouped = df_matrix.value_counts().reset_index(name='Estudios').sort_values(by='Año')
                    fig2 = px.scatter(df_grouped, x='Año', y='Técnica', size='Estudios', color='Estudios', title='Intensidad Tecnológica (Evolución de Enfoques)', color_continuous_scale='Viridis', template='plotly_white')
                    fig2.update_layout(xaxis=dict(tickmode='linear', dtick=1))
                    st.plotly_chart(fig2, use_container_width=True)
            with c4:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.success("**¿Para qué sirve?**\n\nMuestra la evolución del **'¿Cómo?'**. Explica el paso de analítica simple a modelos complejos (Deep Learning/Transformers) en el tiempo.")

        st.markdown("---")

        # 3. Gráfico de Torta (Document Type)
        if 'document type' in df_filtrado.columns:
            c5, c6 = st.columns([3, 1])
            with c5:
                type_counts = df_filtrado['document type'].value_counts().reset_index()
                type_counts.columns = ['Tipo de Documento', 'Cantidad']
                fig_type = px.pie(type_counts, values='Cantidad', names='Tipo de Documento', hole=0.4, title='Tipología Documental (Canales de Difusión)')
                st.plotly_chart(fig_type, use_container_width=True)
            with c6:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.warning("**¿Para qué sirve?**\n\nMuestra el **nivel de validación**. El dominio de 'Articles' prueba que las soluciones ya pasaron por experimentos rigurosos.")

        st.markdown("---")

        # 4. Gráfico de Impacto (Citas)
        if 'cited by' in df_filtrado.columns and 'title' in df_filtrado.columns:
            c7, c8 = st.columns([3, 1])
            with c7:
                top_cited = df_filtrado.sort_values(by='cited by', ascending=False).head(10)
                top_cited['titulo_corto'] = top_cited['title'].str.slice(0, 85) + "..."
                fig_cited = px.bar(top_cited, x='cited by', y='titulo_corto', orientation='h', title='Top 10 Artículos con Mayor Impacto (Citas)', color='cited by', color_continuous_scale='Blues')
                fig_cited.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig_cited, use_container_width=True)
            with c8:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.error("**¿Para qué sirve?**\n\nIdentifica **casos de éxito de referencia**. Apunta directo a las metodologías más respetadas y validadas por la comunidad científica.")

    with tab2:
        st.subheader("Análisis de Actores Científicos y Semántica")
        
        # 5. Top Autores
        if 'authors' in df_filtrado.columns:
            c9, c10 = st.columns([3, 1])
            with c9:
                authors_series = df_filtrado['authors'].dropna().str.split(',').explode().str.strip()
                authors_series = authors_series[authors_series != ""]
                top_authors = authors_series.value_counts().head(10).reset_index()
                top_authors.columns = ['Autor', 'Documentos']
                fig_author = px.bar(top_authors.sort_values(by='Documentos'), x='Documentos', y='Autor', orientation='h', title='Top 10 Autores más Productivos', text_auto=True, color='Documentos', color_continuous_scale='Cividis')
                st.plotly_chart(fig_author, use_container_width=True)
            with c10:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.info("**¿Para qué sirve?**\n\nUbica a los **líderes de opinión**. Identifica a los expertos clave que lideran la innovación en la optimización de almacenes.")

        st.markdown("---")

        # 6. Top Revistas
        if 'source title' in df_filtrado.columns:
            c11, c12 = st.columns([3, 1])
            with c11:
                top_sources = df_filtrado['source title'].value_counts().head(10).reset_index()
                top_sources.columns = ['Revista', 'Artículos']
                fig_source = px.bar(top_sources.sort_values(by='Artículos'), x='Artículos', y='Revista', orientation='h', title='Top 10 Revistas de Publicación', text_auto=True, color='Artículos', color_continuous_scale='Viridis')
                st.plotly_chart(fig_source, use_container_width=True)
            with c12:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.success("**¿Para qué sirve?**\n\nRevela el **enfoque disciplinario**. Define si el tema se enfoca desde la informática teórica o desde la ingeniería logística aplicada.")

        st.markdown("---")

        # 7. Burbujas de Keywords
        if 'author keywords' in df_filtrado.columns:
            c13, c14 = st.columns([3, 1])
            with c13:
                keywords_totales = ", ".join(df_filtrado['author keywords'].dropna().astype(str).str.lower())
                lista_kw = [k.strip() for k in re.split(r'[;,]', keywords_totales) if len(k.strip()) > 3]
                conteo_kw = Counter(lista_kw)
                stopwords_keywords = {'artificial intelligence', 'inventory management', 'supply chain', 'inventory control', 'supply chain management', 'optimization', 'management', 'analysis', 'system', 'systems', 'models', 'model', 'approach', 'research', 'paper', 'results', 'based', 'using', 'applications', 'case', 'study', 'performance', 'framework', 'industry', 'applied', 'application'}
                kw_filtradas = {k: v for k, v in conteo_kw.items() if k not in stopwords_keywords}
                
                if kw_filtradas:
                    df_g1 = pd.DataFrame(kw_filtradas.items(), columns=['Concepto Clave', 'Frecuencia']).sort_values(by='Frecuencia', ascending=False).head(20)
                    fig1 = px.scatter(df_g1, x='Frecuencia', y='Concepto Clave', size='Frecuencia', color='Frecuencia', title='Sub-técnicas de IA y Componentes Logísticos Comunes', color_continuous_scale='Cividis', template='plotly_white')
                    st.plotly_chart(fig1, use_container_width=True)
            with c14:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.warning("**¿Para qué sirve?**\n\nMuestra las **herramientas exactas**. Identifica los pilares operativos más usados (ej. *demand forecasting*, *safety stock*).")

        st.markdown("---")

        # 8. NLP de Abstracts
        if 'abstract' in df_filtrado.columns:
            c15, c16 = st.columns([3, 1])
            with c15:
                texto_completo = " ".join(df_filtrado['abstract'].dropna().astype(str).str.lower())
                palabras = re.findall(r'\b[a-z]{4,}\b', texto_completo)
                stopwords_abstracts = {'this', 'that', 'with', 'from', 'they', 'have', 'were', 'been', 'which', 'their', 'about', 'paper', 'study', 'research', 'using', 'based', 'used', 'analysis', 'results', 'proposed', 'method', 'approach', 'system', 'inventory', 'management', 'supply', 'chain', 'optimization', 'intelligence', 'artificial', 'application', 'applications', 'control', 'systems', 'models', 'model', 'results', 'framework', 'efficient', 'performance', 'paper', 'studies', 'presents', 'developed'}
                palabras_filtradas = [p for p in palabras if p not in stopwords_abstracts]
                conteo_palabras = Counter(palabras_filtradas).most_common(15)
                
                if conteo_palabras:
                    df_palabras = pd.DataFrame(conteo_palabras, columns=['Término', 'Frecuencia']).sort_values(by='Frecuencia', ascending=True)
                    fig_words = px.bar(df_palabras, x='Frecuencia', y='Término', orientation='h', title='Top 15 Términos Frecuentes en Resúmenes (NLP)', color='Frecuencia', color_continuous_scale='Teal')
                    st.plotly_chart(fig_words, use_container_width=True)
            with c16:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.error("**¿Para qué sirve?**\n\nRevela el **propósito de fondo**. Extrae las necesidades reales de los negocios comerciales (ej. reducir *costos*, mitigar *incertidumbre*).")

    with tab3:
        st.subheader("Dataset Completo Extraído de Scopus")
        columnas_visibles = [c for c in ['authors', 'title', 'year', 'source title', 'cited by', 'document type', 'author keywords', 'abstract'] if c in df_filtrado.columns]
        st.dataframe(df_filtrado[columnas_visibles], use_container_width=True)

    # --- CONCLUSIONES ---
    st.markdown("---")
    st.subheader("💡 Conclusión General")
    st.success(
        f"El análisis de los artículos indexados demuestra que la Inteligencia Artificial se aplica en las empresas comerciales "
        f"principalmente mediante el **Demand Forecasting (Predicción de la Demanda)** para solucionar problemas de sobrestock e incertidumbre, "
        f"evolucionando de analítica tradicional a modelos avanzados de Machine/Deep Learning."
    )
