import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import re

# ==============================================================================
# 🎨 2. INYECCIÓN DE CSS PERSONALIZADO (Look & Feel Moderno)
# ==============================================================================
st.markdown("""
    <style>
    /* Cambiar el fondo global y tipografía */
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Estilizar contenedores de métricas (KPI Cards) */
    [data-testid="stMetricSimpleValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #1E3A8A !important;
    }
    
    .stMetric {
        background-color: #ffffff;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e5e7eb;
        transition: transform 0.2s ease-in-out;
    }
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
    }

    /* Títulos y Subtítulos con diseño limpio */
    h1, h2, h3 {
        color: #0F172A !important;
        font-weight: 700 !important;
    }
    
    .main-title {
        font-size: 2.5rem;
        color: #1E3A8A;
        border-bottom: 3px solid #3B82F6;
        padding-bottom: 10px;
        margin-bottom: 25px;
    }
    
    /* Mensajes informativos y alertas estilizadas */
    .stAlert {
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    /* Ajustes para listas desplegables y inputs */
    .stMultiSelect div {
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título de la sección con clase CSS personalizada
st.markdown('<h1 class="main-title">🧠 Vigilancia Tecnológica: IA en Gestión de Inventarios</h1>', unsafe_allow_html=True)

# ==============================================================================
# 📂 CARGA Y PREPROCESAMIENTO DE DATOS (Usa tu DataFrame ya cargado en la app)
# ==============================================================================
# NOTA: Ajusta esta línea si tu DataFrame principal se llama diferente (ej. st.session_state.df o df)
if 'df_filtrado' in locals() or 'df_filtrado' in globals():
    df_ia = df_filtrado.copy()
else:
    # Carga de respaldo en caso de ejecutar esta pestaña de forma aislada
    try:
        df_ia = pd.read_csv('scopus_export_Jun 10-2026_bf2e31d3-f509-49f3-90cf-3a128f6918b1.csv')
    except FileNotFoundError:
        try:
            df_ia = pd.read_csv('PA4.csv')
        except FileNotFoundError:
            st.error("❌ Archivo de Scopus no detectado. Por favor asegúrate de cargar los datos primero.")
            st.stop()

# Estandarizar columnas
df_ia.columns = df_ia.columns.str.lower().str.strip()

# Asegurar tipos de datos numéricos
if 'cited by' in df_ia.columns:
    df_ia['cited by'] = pd.to_numeric(df_ia['cited by'], errors='coerce').fillna(0).astype(int)
if 'year' in df_ia.columns:
    df_ia['year'] = pd.to_numeric(df_ia['year'], errors='coerce').fillna(0).astype(int)

# ==============================================================================
# 🛑 FILTRADO EVITANDO DUPLICADOS SEMÁNTICOS (STOPWORDS)
# ==============================================================================
# Agrupamos términos repetitivos o genéricos para que los gráficos muestren solo conceptos limpios y de alto valor
stopwords_estrictas = {
    'artificial intelligence', 'inventory management', 'supply chain', 'inventory control', 
    'supply chain management', 'optimization', 'management', 'analysis', 'system', 'systems',
    'models', 'model', 'approach', 'research', 'paper', 'results', 'based', 'using', 'applications',
    'case', 'study', 'performance', 'framework', 'industry', 'applied', 'application', 'inventories',
    'intelligent', 'perspective', 'algorithms', 'algorithm', 'review'
}

# Diccionario para unificar variaciones gramaticales comunes y no repetir conceptos en las barras/burbujas
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
    'rfid technology': 'rfid'
}

# ==============================================================================
# 📊 CREACIÓN DE LOS GRÁFICOS AVANZADOS
# ==============================================================================

# Crear pestañas internas dentro de la sección para una navegación elegante
sub_tab1, sub_tab2 = st.tabs(["🎯 Enfoques y Tendencias IA", "👥 Comparador de Investigadores"])

with sub_tab1:
    st.markdown("### 🔍 Mapeo Semántico de Tecnologías y Variables Operativas")
    st.info("💡 Este análisis responde directamente al **'CÓMO'** y **'QUÉ'** se está investigando, filtrando ruido conceptual y unificando sinónimos tecnológicos.")
    
    if 'author keywords' in df_ia.columns:
        # Extraer, limpiar y unificar palabras clave
        keywords_crudas = ", ".join(df_ia['author keywords'].dropna().astype(str).str.lower())
        lista_kw_limpias = []
        
        for k in re.split(r'[;,]', keywords_crudas):
            termino = k.strip()
            if len(termino) > 3 and termino not in stopwords_estrictas:
                # Aplicar el mapa de unificación para evitar conceptos duplicados
                termino_unificado = mapeo_conceptos.get(termino, termino)
                if termino_unificado not in stopwords_estrictas:
                    lista_kw_limpias.append(termino_unificado)
        
        conteo_kw = Counter(lista_kw_limpias)
        df_g1 = pd.DataFrame(conteo_kw.items(), columns=['Concepto Clave', 'Frecuencia']).sort_values(by='Frecuencia', ascending=False).head(15)
        
        # --- GRÁFICO 1: BURBUJAS DE CONCEPTOS LIMPIOS ---
        fig1 = px.scatter(df_g1, x='Frecuencia', y='Concepto Clave', size='Frecuencia', color='Frecuencia',
                          title='Top 15 Componentes de IA y Variables de Stock más Investigadas',
                          color_continuous_scale='Cividis', template='plotly_white')
        fig1.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig1, use_container_width=True)
        
        st.markdown("---")
        
        # --- GRÁFICO 2: EVOLUCIÓN TEMPORAL DE ENFOQUES CORE ---
        st.markdown("### 📈 Madurez de Soluciones Tecnológicas en la Línea de Tiempo")
        
        df_kw_year = df_ia[['year', 'author keywords']].dropna()
        df_kw_year['author keywords'] = df_kw_year['author keywords'].str.lower()

        # Usamos la lista de conceptos ya unificados
        tecnologias_core = ['machine learning', 'deep learning', 'demand forecasting', 'predictive analytics', 'neural networks', 'big data', 'reinforcement learning', 'internet of things', 'blockchain']
        
        registros_tiempo = []
        for idx, row in df_kw_year.iterrows():
            anio = int(row['year'])
            texto_kw = str(row['author keywords'])
            
            # Reemplazar sinónimos en el texto crudo para un mapeo correcto
            for clave_sinonimo, valor_unificado in mapeo_conceptos.items():
                texto_kw = texto_kw.replace(clave_sinonimo, valor_unificado)
                
            for tech in tecnologias_core:
                if tech in texto_kw:
                    registros_tiempo.append({'Año': anio, 'Técnica / Enfoque': tech})

        if registros_tiempo:
            df_matrix = pd.DataFrame(registros_tiempo)
            df_grouped = df_matrix.value_counts().reset_index(name='Cantidad de Estudios').sort_values(by='Año')
            
            # Filtrar años atípicos o vacíos
            df_grouped = df_grouped[df_grouped['Año'] >= 2015]
            
            fig2 = px.scatter(df_grouped, x='Año', y='Técnica / Enfoque', size='Cantidad de Estudios', 
                              color='Cantidad de Estudios', title='Intensidad y Adopción Tecnológica por Año',
                              color_continuous_scale='Viridis', template='plotly_white')
            fig2.update_layout(xaxis=dict(tickmode='linear', dtick=1), margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("⚠️ La columna 'Author Keywords' no está disponible en este archivo.")

with sub_tab2:
    st.markdown("### 👥 Panel Comparativo e Impacto de Investigadores")
    st.markdown("Selecciona autores específicos de la base de datos de Scopus para aislar sus métricas y realizar una comparación de rendimiento directa.")
    
    if 'authors' in df_ia.columns:
        # Extraer lista limpia de autores únicos para el selector
        todos_autores = df_ia['authors'].dropna().str.split(',').explode().str.strip()
        autores_unicos = sorted(todos_autores[todos_autores != ""].unique())
        
        # Selector múltiple interactivo
        autores_seleccionados = st.multiselect(
            "🔍 Busca y selecciona los investigadores que deseas contrastar:",
            options=autores_unicos,
            default=autores_unicos[:2] if len(autores_unicos) > 1 else autores_unicos[0:1]
        )
        
        if autores_seleccionados:
            patron_busqueda = '|'.join([re.escape(a) for a in autores_seleccionados])
            df_autores_filt = df_ia[df_ia['authors'].str.contains(patron_busqueda, case=False, na=False)]
            
            datos_mapeados = []
            for _, fila in df_autores_filt.iterrows():
                for autor in autores_seleccionados:
                    if autor.lower() in fila['authors'].lower():
                        datos_mapeados.append({
                            'Autor': autor,
                            'Título': fila['title'],
                            'Revista': fila.get('source title', 'N/A'),
                            'Año': fila['year'],
                            'Citas': fila['cited by']
                        })
            
            df_comparativa_final = pd.DataFrame(datos_mapeados)
            
            if not df_comparativa_final.empty:
                # Resumen en tarjetas métricas (Afectadas por el CSS personalizado)
                st.markdown("#### 📊 Desempeño Consolidado")
                df_resumen = df_comparativa_final.groupby('Autor').agg(
                    Articulos=('Título', 'count'),
                    Citas_Totales=('Citas', 'sum')
                ).reset_index()
                
                # Crear columnas dinámicas para las tarjetas de cada autor
                cols_tarjetas = st.columns(len(autores_seleccionados))
                for idx, autor in enumerate(autores_seleccionados):
                    sub_df = df_resumen[df_resumen['Autor'] == autor]
                    if not sub_df.empty:
                        arts = sub_df.iloc[0]['Articulos']
                        citas = sub_df.iloc[0]['Citas_Totales']
                        cols_tarjetas[idx].metric(label=f"👤 {autor}", value=f"{arts} Art. / {int(citas)} Citas")
                
                st.markdown("---")
                
                # Gráficos de comparación lado a lado
                col_g1, col_g2 = st.columns(2)
                
                with col_g1:
                    fig_comp_bar = px.bar(df_resumen, x='Autor', y='Citas_Totales', color='Autor', text='Articulos',
                                         title='Citas Totales Acumuladas (Número = Volumen de Artículos)',
                                         color_discrete_sequence=px.colors.qualitative.Safe, template='plotly_white')
                    st.plotly_chart(fig_comp_bar, use_container_width=True)
                    
                with col_g2:
                    df_linea_tiempo = df_comparativa_final.groupby(['Autor', 'Año']).size().reset_index(name='Artículos')
                    fig_comp_line = px.line(df_linea_tiempo, x='Año', y='Artículos', color='Autor', markers=True,
                                            title='Historial de Producción Científica Anual',
                                            color_discrete_sequence=px.colors.qualitative.Safe, template='plotly_white')
                    fig_comp_line.update_layout(xaxis=dict(tickmode='linear', dtick=1))
                    st.plotly_chart(fig_comp_line, use_container_width=True)
                
                # Tabla detallada con CSS nativo de Streamlit
                st.markdown("#### 📋 Producción Científica Detallada")
                st.dataframe(df_comparativa_final[['Autor', 'Título', 'Revista', 'Año', 'Citas']], use_container_width=True)
            else:
                st.info("Por favor selecciona autores válidos que contengan registros claros en el archivo.")
        else:
            st.warning("⚠️ Selecciona al menos un autor en el buscador superior para desplegar el panel comparativo.")
    else:
        st.error("No se localizó la columna 'Authors' necesaria para la comparación.")
