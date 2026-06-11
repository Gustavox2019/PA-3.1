# --- NUEVA SECCIÓN: LEYENDA EJECUTIVA Y GLOSARIO DE TÉRMINOS (Estilo ChurnAI Horizon) ---
with st.expander("📖 Leyenda del Dashboard y Glosario Ejecutivo", expanded=False):
    st.markdown("""
    ### 🧭 Guía de Interpretación de Métricas
    Bienvenido al panel analítico. Para garantizar una lectura alineada con los estándares de la industria, consulte el significado y el propósito de los componentes clave evaluados:
    """)
    
    # Creamos 4 columnas para que parezcan tarjetas de leyenda
    leg_col1, leg_col2, leg_col3, leg_col4 = st.columns(4)
    
    with leg_col1:
        st.markdown("#### 🔮 Demand Forecasting")
        st.caption("**Modelos Predictivos**")
        st.info("Uso de IA (ML/DL) para anticipar la demanda futura del mercado basándose en histórico de ventas, estacionalidad y factores externos.")
        
    with leg_col2:
        st.markdown("#### 🛡️ Safety Stock")
        st.caption("**Stock de Seguridad**")
        st.success("Inventario adicional que se mantiene para mitigar el riesgo de desabastecimiento (stockouts) debido a fluctuaciones en la oferta o demanda.")
        
    with leg_col3:
        st.markdown("#### 🔄 Auto-Replenishment")
        st.caption("**Reabastecimiento Automatizado**")
        st.warning("Algoritmos inteligentes que generan órdenes de compra automáticas hacia los proveedores cuando las existencias tocan un punto crítico.")
        
    with leg_col4:
        st.markdown("#### 🏢 Multi-Echelon")
        st.caption("**Sistemas Multicanal**")
        st.error("Optimización conjunta de inventarios distribuidos en múltiples niveles de la cadena (ej. Fábrica -> Centro de Distribución -> Tienda).")

    st.markdown("---")
    st.markdown("""
    💡 **Nota de Uso:** Puedes usar los filtros de la barra lateral para ajustar el rango de años. Los gráficos semánticos (NLP) y de burbujas se actualizarán automáticamente para reflejar las tecnologías predominantes en el periodo seleccionado.
    """)
