from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class CriarContaForm(FlaskForm):
    nome = StringField(
        "Nome completo",
        validators=[DataRequired(message="Informe seu nome."), Length(max=150)],
    )
    email = StringField(
        "E-mail",
        validators=[
            DataRequired(message="Informe seu e-mail."),
            Email(message="Informe um e-mail válido."),
            Length(max=180),
        ],
    )
    senha = PasswordField(
        "Senha",
        validators=[
            DataRequired(message="Crie uma senha."),
            Length(min=8, message="A senha deve ter pelo menos 8 caracteres."),
        ],
    )
    confirmar_senha = PasswordField(
        "Confirmar senha",
        validators=[
            DataRequired(message="Confirme sua senha."),
            EqualTo("senha", message="As senhas não conferem."),
        ],
    )
    submit = SubmitField("Criar conta")


class LoginForm(FlaskForm):
    email = StringField(
        "E-mail",
        validators=[
            DataRequired(message="Informe seu e-mail."),
            Email(message="Informe um e-mail válido."),
            Length(max=180),
        ],
    )
    senha = PasswordField(
        "Senha",
        validators=[DataRequired(message="Informe sua senha.")],
    )
    submit = SubmitField("Entrar")


class RecuperarSenhaForm(FlaskForm):
    email = StringField(
        "E-mail",
        validators=[
            DataRequired(message="Informe seu e-mail."),
            Email(message="Informe um e-mail válido."),
            Length(max=180),
        ],
    )
    submit = SubmitField("Enviar link de recuperação")


class RedefinirSenhaForm(FlaskForm):
    senha = PasswordField(
        "Nova senha",
        validators=[
            DataRequired(message="Informe uma nova senha."),
            Length(min=8, message="A senha deve ter pelo menos 8 caracteres."),
        ],
    )
    confirmar_senha = PasswordField(
        "Confirmar nova senha",
        validators=[
            DataRequired(message="Confirme a nova senha."),
            EqualTo("senha", message="As senhas não conferem."),
        ],
    )
    submit = SubmitField("Salvar nova senha")
