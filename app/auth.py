from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Usuario
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('views.index'))
        else:
            flash('Email ou senha incorretos.', 'danger')

    return render_template('login.html', user=current_user)

@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        tipo_usuario = request.form.get('tipo_usuario')
        cidade = request.form.get('cidade')
        contato = request.form.get('contato')

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            flash('Email já cadastrado.', 'danger')
        else:
            novo_usuario = usuario(
                nome=nome,
                email=email,
                senha=generate_password_hash(senha, method='sha256'),
                tipo_usuario=tipo_usuario,
                cidade=cidade,
                contato=contato
            )
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Conta criada com sucesso!', 'success')
            return redirect(url_for('auth.login'))

    return render_template('registro.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('auth.login'))