from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Pet, Usuario
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html', user=current_user)

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
        raca = request.form.get('raca')
        porte = request.form.get('porte')
        vacinacao = request.form.get('vacinacao')
        localizacao = request.form.get('localizacao')

        novo_pet = Pet(
            nome=nome,
            idade=idade,
            raca=raca,
            porte=porte,
            vacinacao=vacinacao,
            localizacao=localizacao,
            doador_id=current_user.id
        )
        db.session.add(novo_pet)
        db.session.commit()
        flash('Pet adicionado com sucesso!', 'success')
        return redirect(url_for('views.index'))

    return render_template('adicionar_pet.html', user=current_user)