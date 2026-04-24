from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Camiseta(db.Model):
    __tablename__ = "camisetas"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(100), nullable=False)
    pais = db.Column(db.String(100), nullable=False)
    modalidade = db.Column(db.String(50), nullable=False)
    temporada = db.Column(db.String(20), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    tamanho = db.Column(db.String(10), nullable=False)
    jogador = db.Column(db.String(100))
    numero = db.Column(db.String(10))
    condicao = db.Column(db.String(50), nullable=False)
    observacoes = db.Column(db.Text)
    imagem = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)