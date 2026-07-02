from datetime import datetime
from database.connection import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text

class AnaliseModel(Base):
    __tablename__ = "analises"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    image_path = Column(String(255), nullable=True)
    descricao = Column(Text, nullable=True)
    objetos = Column(Text, nullable=True)
    quantidade_pessoas = Column(Integer, default=0)
    rostos = Column(Integer, default=0)
    idade = Column(String(50), nullable=True)
    emocao = Column(String(50), nullable=True)
    cores = Column(String(100), nullable=True)
    luminosidade = Column(Float, nullable=True)
    nitidez = Column(Float, nullable=True)
    json_resultado = Column(Text, nullable=True)
