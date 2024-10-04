from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField, HiddenField, TelField, validators

class LoginForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[validators.DataRequired(), validators.Length(min=2, max=20)], render_kw={"autocomplete": "off"})
    password = PasswordField('Senha', validators=[validators.DataRequired(), validators.Length(min=2, max=20)], render_kw={"autocomplete": "off"})
    submit = SubmitField('Login')

class ClientSearchForm(FlaskForm):
    clientName = StringField('Nome do Cliente', validators=[validators.DataRequired(), validators.Length(min=2, max=20)], render_kw={"autocomplete": "off"})
    submit = SubmitField('Buscar')

class ClientAtualizeForm(FlaskForm):
    clientName = StringField('Nome do Cliente', render_kw={"autocomplete": "off"})
    clientAddress = StringField('Endereço do Cliente', render_kw={"autocomplete": "off"})
    clientCPF = StringField('CPF do Cliente', render_kw={"autocomplete": "off"})
    clientEmail = StringField('E-mail do Cliente', render_kw={"autocomplete": "off"})
    submit = SubmitField('Atualizar')

class ProductSearchForm(FlaskForm):
    productName = StringField('Nome do Produto', validators=[validators.DataRequired(), validators.Length(min=2, max=20)], render_kw={"autocomplete": "off"})
    submit = SubmitField('Buscar')

class ProductUpdateForm(FlaskForm):
    productName = StringField('Nome do Produto', render_kw={"autocomplete": "off"})
    productPrice = DecimalField('Preço do Produto', [validators.Optional()])
    productCode = StringField('Código do Produto', render_kw={"autocomplete": "off"})
    productQuantity = IntegerField('Quantidade do Produto', [validators.Optional()])
    productDescription = StringField('Descrição do Produto', render_kw={"autocomplete": "off"})
    submit = SubmitField('Atualizar')

class ProductCreateForm(FlaskForm):
    productName = StringField('Nome do Produto', validators=[validators.DataRequired(), validators.Length(min=2, max=20)], render_kw={"autocomplete": "off"})
    productPrice = DecimalField('Preço do Produto', [validators.Optional()])
    productCode = StringField('Código do Produto', validators=[validators.DataRequired(), validators.Length(min=2, max=20)], render_kw={"autocomplete": "off"})
    productQuantity = IntegerField('Quantidade do Produto', [validators.Optional()])
    submit = SubmitField('Criar')

class ClientCreateForm(FlaskForm):
    clientName = StringField('Nome do Cliente', validators=[validators.DataRequired(), validators.Length(min=2, max=20)], render_kw={"autocomplete": "off"})
    clientAddress = StringField('Endereço do Cliente', validators=[validators.DataRequired(), validators.Length(min=2, max=20)], render_kw={"autocomplete": "off"})
    clientCPF = StringField('CPF do Cliente', validators=[validators.DataRequired(), validators.Length(min=2, max=20)], render_kw={"autocomplete": "off"})
    clientEmail = StringField('E-mail do Cliente', validators=[validators.DataRequired(), validators.Length(min=2, max=20)], render_kw={"autocomplete": "off"})
    submit = SubmitField('Criar')

class CarEditForm(FlaskForm):
    id = HiddenField('ID do Carro')
    modelo = StringField('Modelo do Carro', render_kw={"autocomplete": "off"})
    submit_edit = SubmitField('Editar')
    submit_delete = SubmitField('Excluir')

class CarAddForm(FlaskForm):
    modelo = StringField('Modelo do Carro', render_kw={"autocomplete": "off"})
    submit = SubmitField('Criar')

class PhoneEditForm(FlaskForm):
    id = HiddenField('ID do Telefone')
    number = TelField('Número de Telefone', render_kw={"autocomplete": "off"})
    submit_edit = SubmitField('Editar')
    submit_delete = SubmitField('Excluir')

class PhoneAddForm(FlaskForm):
    number = TelField('Número de Telefone', render_kw={"autocomplete": "off"})
    submit = SubmitField('Criar')

# Formulário do carrinho de compras
class CartForm(FlaskForm):
    id = HiddenField('ID do Produto')
    quantity = IntegerField('Quantidade', [validators.Optional(), validators.NumberRange(min=1, max=100)])
    submit = SubmitField('Atualizar')


