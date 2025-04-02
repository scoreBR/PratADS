from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask import jsonify
from .models import Pet, Usuario, Produto

from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def AdotePet():
    return render_template('AdotePet.html', user=current_user)

@views.route('/loja')
@login_required
def Loja():
    return render_template('Loja.html', user=current_user)

@views.route('/perfil')
@login_required
def Perfil():
    return render_template('perfil.html', user=current_user)

@views.route('/Chat')
@login_required
def Chat():
    return render_template('Chat.html', user=current_user)

@views.route('/usuarios')
@login_required
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios, user=current_user)

@views.route('/adicionar_pet', methods=['GET', 'POST'])
@login_required
def adicionar_pet():
    if request.method == 'POST':
        nome = request.form.get('nome')
        idade = request.form.get('idade')
        tipo = request.form.get('tipo')
        raca = request.form.get('raca')
        porte = request.form.get('porte')
        vacinacao = request.form.get('vacinacao')
        localizacao = request.form.get('localizacao')

        novo_pet = Pet(
            nome=nome,
            idade=idade,
            tipo=tipo,
            raca=raca,
            porte=porte,
            vacinacao=vacinacao,
            localizacao=localizacao,
            doador_id=current_user.id
        )
        db.session.add(novo_pet)
        db.session.commit()
        flash('Pet adicionado com sucesso!', 'success')
        return redirect(url_for('views.AdotePet'))

    return render_template('adicionar_pet.html', user=current_user)

@views.route('/adicionar_produto', methods=['GET', 'POST'])
@login_required
def adicionar_produto():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        preco = request.form.get('preco')
        categoria = request.form.get('categoria')

        novo_produto = Produto(
            titulo=titulo,
            descricao=descricao,
            preco=preco,
            categoria=categoria
        )
        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto adicionado com sucesso!', 'success')
        return redirect(url_for('views.Loja'))

    return render_template('adicionar_produto.html', user=current_user)

@views.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    
    return render_template('perfil.html', user=current_user)

@views.route('/api/pets', methods=['GET'])
def get_pets():
    pets = Pet.query.all()
    pets_list = [{
        'nome': pet.nome,
        'idade': pet.idade,
        'tipo': pet.tipo,
        'raca': pet.raca,
        'porte': pet.porte,
        'localizacao': pet.localizacao
    } for pet in pets]
    return jsonify(pets_list)

@views.route('/api/produtos', methods=['GET'])
def get_produtos():
    produtos = Produto.query.all()
    produtos_list = [{
        'titulo': produto.titulo,
        'descricao': produto.descricao,
        'preco': produto.preco,
        'categoria': produto.categoria,
    } for produto in produtos]
    return jsonify(produtos_list)