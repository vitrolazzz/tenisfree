"""
forms/tenisfree_forms.py
Formulários Flask-WTF para criação e edição de Produto.
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    DecimalField,
    IntegerField,
    URLField,
    SelectField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
    Optional,
    URL,
)

CATEGORIAS = [
    ("", "Selecione uma categoria"),
    ("Corrida", "Corrida"),
    ("Casual", "Casual"),
    ("Esportivo", "Esportivo"),
    ("Basquete", "Basquete"),
    ("Futebol", "Futebol"),
    ("Skate", "Skate"),
    ("Trilha", "Trilha"),
    ("Outros", "Outros"),
]

TAMANHOS = [(str(n), str(n)) for n in range(33, 46)] + [("Único", "Único")]


class ProdutoForm(FlaskForm):
    """Formulário compartilhado por Create e Update."""

    nome = StringField(
        "Nome do Produto",
        validators=[
            DataRequired(message="O nome é obrigatório."),
            Length(max=150, message="Máximo de 150 caracteres."),
        ],
    )

    marca = StringField(
        "Marca",
        validators=[
            DataRequired(message="A marca é obrigatória."),
            Length(max=100, message="Máximo de 100 caracteres."),
        ],
    )

    categoria = SelectField(
        "Categoria",
        choices=CATEGORIAS,
        validators=[DataRequired(message="Selecione uma categoria.")],
    )

    tamanho = SelectField(
        "Tamanho (BR)",
        choices=TAMANHOS,
        validators=[DataRequired(message="Selecione um tamanho.")],
    )

    cor = StringField(
        "Cor",
        validators=[
            DataRequired(message="A cor é obrigatória."),
            Length(max=60, message="Máximo de 60 caracteres."),
        ],
    )

    preco = DecimalField(
        "Preço (R$)",
        places=2,
        validators=[
            DataRequired(message="O preço é obrigatório."),
            NumberRange(min=0.01, message="O preço deve ser maior que zero."),
        ],
    )

    estoque = IntegerField(
        "Estoque",
        validators=[
            DataRequired(message="Informe a quantidade em estoque."),
            NumberRange(min=0, message="O estoque não pode ser negativo."),
        ],
    )

    descricao = TextAreaField(
        "Descrição",
        validators=[Optional(), Length(max=2000, message="Máximo de 2000 caracteres.")],
    )

    imagem_url = URLField(
        "URL da Imagem",
        validators=[
            Optional(),
            URL(message="Informe uma URL válida para a imagem."),
            Length(max=500),
        ],
    )

    submit = SubmitField("Salvar")
