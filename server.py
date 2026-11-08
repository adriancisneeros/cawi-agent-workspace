import streamlit as st
import pandas as pd
import os
import subprocess
import json

st.set_page_config(page_title="CAWI - Kowey Agent Hub", layout="wide", initial_sidebar_state="expanded")

st.title("CAWI - Kowey Agent Hub")
st.caption("Monitoreo de rendimiento, métricas estructuradas y persistencia local")

csv_path = "metricas_cawi.csv"

# Panel lateral: controles de ejecución
st.sidebar.header("Acciones del Agente")

if st.sidebar.button("Ejecutar Evaluador de Métricas", use_container_width=True):
    with st.spinner("Llamando a Gemini 3.8 Flash..."):
        try:
            res = subprocess.run(["python", "evaluador_metricas.py"], capture_output=True, text=True, check=True)
            st.sidebar.success("Evaluación completada")
        except subprocess.CalledProcessError as e:
            st.sidebar.error(f"Error en ejecución: {e.stderr}")

if st.sidebar.button("Recargar Métricas", use_container_width=True):
    st.rerun()

# Vista principal: visualización del CSV
st.subheader("Registro Histórico de Métricas")

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    
    # Métricas clave en tarjetas superiores
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Evaluaciones", len(df))
    col2.metric("Nodos Exitosos", int(df["nodos_exitosos"].sum()))
    col3.metric("Nodos Fallidos", int(df["nodos_fallidos"].sum()))
    col4.metric("Tokens Acumulados", int(df["tokens_totales"].sum()))
    
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No se encontró el archivo metricas_cawi.csv. Ejecuta una evaluación para crearlo.")
