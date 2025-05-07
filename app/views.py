from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask import jsonify
from werkzeug.utils import secure_filename
import os
from .models import Pet, Usuario, Produto

from . import db

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def AdotePet():
    pets = Pet.query.all()
    return render_template('AdotePet.html', pets=pets, user=current_user)

@views.route('/loja')
@login_required
def Loja():
    produtos = Produto.query.all()
    return render_template('Loja.html', produtos=produtos, user=current_user)

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
        imagem = request.files.get('imagem')
        imagem_url = None
        if imagem and allowed_file(imagem.filename):
            filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(UPLOAD_FOLDER, filename))
            imagem_url = f'static/uploads/{filename}'

        novo_pet = Pet(
            nome=nome,
            idade=idade,
            tipo=tipo,
            raca=raca,
            porte=porte,
            vacinacao=vacinacao,
            localizacao=localizacao,
            doador_id=current_user.id,
            imagem_url=imagem_url
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
        imagem = request.files.get('imagem')
        imagem_url = None
        if imagem and allowed_file(imagem.filename):
            filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(UPLOAD_FOLDER, filename))
            imagem_url = f'static/uploads/{filename}'

        novo_produto = Produto(
            titulo=titulo,
            descricao=descricao,
            preco=preco,
            categoria=categoria,
            imagem_url=imagem_url,
            usuario_id=current_user.id
        )
        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto adicionado com sucesso!', 'success')
        return redirect(url_for('views.Loja'))

    return render_template('adicionar_produto.html', user=current_user)

@views.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        cidade = request.form.get('cidade')
        contato = request.form.get('contato')
        descricao = request.form.get('descricao')

        # Atualiza os dados do usuário
        current_user.cidade = cidade
        current_user.contato = contato

        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('views.perfil'))

    return render_template('perfil.html', user=current_user)

@views.route('/api/pets', methods=['GET'])
def get_pets():
    pets = Pet.query.all()
    pets_list = [{
        'id': pet.id,
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
        'id': produto.id,
        'titulo': produto.titulo,
        'descricao': produto.descricao,
        'preco': produto.preco,
        'categoria': produto.categoria,
    } for produto in produtos]
    return jsonify(produtos_list)

@views.route('/pet/<int:pet_id>', methods=['GET'])
@login_required
def detalhes_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    return render_template('DetalhesPet.html', pet=pet, user=current_user)

@views.route('/produto/<int:produto_id>', methods=['GET'])
@login_required
def detalhes_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    return render_template('DetalhesProduto.html', produto=produto, user=current_user)

@views.route('/atualizar_descricao', methods=['POST'])
@login_required
def atualizar_descricao():
    descricao = request.form.get('descricao')
    if descricao:
        current_user.descricao = descricao
        db.session.commit()
        flash('Descrição atualizada com sucesso!', 'success')
    else:
        flash('A descrição não pode estar vazia.', 'danger')
    return redirect(url_for('views.Perfil'))

@views.route('/excluir_pet/<int:pet_id>', methods=['POST', 'GET'])
@login_required
def excluir_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    if pet.doador_id != current_user.id:
        flash('Você não tem permissão para excluir este pet.', 'danger')
        return redirect(url_for('views.perfil'))
    db.session.delete(pet)
    db.session.commit()
    flash('Pet excluído com sucesso!', 'success')
    return redirect(url_for('views.perfil'))

@views.route('/excluir_produto/<int:produto_id>', methods=['POST', 'GET'])
@login_required
def excluir_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    if produto.usuario_id != current_user.id:
        flash('Você não tem permissão para excluir este produto.', 'danger')
        return redirect(url_for('views.perfil'))
    db.session.delete(produto)
    db.session.commit()
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('views.perfil'))