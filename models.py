from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    camisetas = db.relationship("Camiseta", backref="user", lazy=True)


class Camiseta(db.Model):
    __tablename__ = "camisetas"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    time = db.Column(db.String(100), nullable=False)
    pais = db.Column(db.String(100), nullable=False)
    modalidade = db.Column(db.String(50), nullable=False)
    temporada = db.Column(db.String(20), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    tamanho = db.Column(db.String(10), nullable=False)
    jogador = db.Column(db.String(100))
    numero = db.Column(db.String(10))
    condicao = db.Column(db.String(50))
    observacoes = db.Column(db.Text)
    imagem = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Favorito(db.Model):
    __tablename__ = "favoritos"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    camiseta_id = db.Column(db.Integer, db.ForeignKey("camisetas.id"), nullable=False)