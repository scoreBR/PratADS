from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Usuario
from . import db
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

auth = Blueprint('auth', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('views.AdotePet'))
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
        imagem = request.files.get('imagem')
        imagem_url = None
        if imagem and allowed_file(imagem.filename):
            filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(UPLOAD_FOLDER, filename))
            imagem_url = f'static/uploads/{filename}'

        existing_usuario = Usuario.query.filter_by(email=email).first()
        if existing_usuario:
            flash('Email já cadastrado.', 'danger')
        else:
            novo_usuario = Usuario(
                nome=nome,
                email=email,
                senha=generate_password_hash(senha, method='sha256'),
                tipo_usuario=tipo_usuario,
                cidade=cidade,
                contato=contato,
                imagem_url=imagem_url
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