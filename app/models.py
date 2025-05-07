from . import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    tipo_usuario = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(100), nullable=True)
    contato = db.Column(db.String(100), nullable=True)
    pets = db.relationship('Pet', backref='doador', lazy=True)
    descricao = db.Column(db.Text, nullable=True)
    imagem_url = db.Column(db.String(255), nullable=True)
    produtos = db.relationship('Produto', backref='usuario', lazy=True)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    raca = db.Column(db.String(100), nullable=False)
    porte = db.Column(db.String(50), nullable=False)
    vacinacao = db.Column(db.String(100), nullable=True)
    localizacao = db.Column(db.String(100), nullable=False)
    doador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    imagem_url = db.Column(db.String(255), nullable=True)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    imagem_url = db.Column(db.String(255), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
