import streamlit as st
import pandas as pd
from datetime import datetime
from database.connection import engine, Base, SessionLocal
from database.models.analise import AnaliseModel
from services.vision_service import VisionService

# Cria a tabela no banco caso ela não exista ainda
Base.metadata.create_all(bind=engine)

st.set_page_config(page_title="Computer Vision Hub", layout="wide")

st.sidebar.title("Menu")
tela = st.sidebar.selectbox("Mudar de tela:", ["Capturar Foto", "Histórico e Gráficos"])

if tela == "Capturar Foto":
    st.title("🧠 Scanner de Visão Computacional")
    
    # Abre o componente de câmera do Streamlit
    foto = st.camera_input("Tire uma foto para análise:")
    
    if foto is not None:
        bytes_foto = foto.getvalue()
        
        if st.button("Analisar Imagem e Salvar"):
            with st.spinner("Analisando..."):
                try:
                    resultado = VisionService.analisar_imagem(bytes_foto)
                    
                    # Salva os dados no banco de dados
                    db = SessionLocal()
                    registro = AnaliseModel(
                        descricao=resultado["descricao"],
                        objetos=resultado["objetos"],
                        cores=resultado["cores"],
                        luminosidade=resultado["luminosidade"],
                        nitidez=resultado["nitidez"],
                        json_resultado=resultado["json_resultado"]
                    )
                    db.add(registro)
                    db.commit()
                    db.close()
                    
                    st.success("Salvo com sucesso no banco de dados!")
                    st.write(resultado)
                except Exception as e:
                    st.error(f"Erro ao processar a análise: {e}")

elif tela == "Histórico e Gráficos":
    st.title("📊 Painel de Histórico")
    
    db = SessionLocal()
    dados_banco = db.query(AnaliseModel).all()
    db.close()
    
    if dados_banco:
        df = pd.DataFrame([{
            "ID": r.id, 
            "Data": r.created_at, 
            "Luminosidade": r.luminosidade, 
            "Nitidez": r.nitidez
        } for r in dados_banco])
        
        st.dataframe(df)
        st.subheader("Evolução dos Índices")
        st.line_chart(df.set_index("Data")["Nitidez"])
    else:
        st.info("Nenhum dado cadastrado no banco ainda.")