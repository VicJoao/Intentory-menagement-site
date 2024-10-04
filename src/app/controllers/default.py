from app import app, db
# Import statements for form classes
from app.models.forms import (
    LoginForm, ClientSearchForm, ClientAtualizeForm,
    ProductSearchForm, ProductUpdateForm, ProductCreateForm,
    ClientCreateForm, CarEditForm, CarAddForm,
    PhoneEditForm, PhoneAddForm, CartForm
)
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app.models.tables import User, Product, Car, Phone, Client, Kart, KartItem
from app import login_manager
from sqlalchemy import or_, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.operators import and_


@login_manager.user_loader
def load_user(user_id):
    # Esta função deve retornar um objeto de usuário ou None
    return User.query.get(int(user_id))

#loads the entry page index.html
@app.route('/index')
def index():
    return render_template('index.html')

#loads the login page login.html
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login = form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Login realizado com sucesso!')
            return redirect(url_for('home'))
        else:
            flash('Login inválido!')
    return render_template('login.html', title='Sign In', form=form)

#loads the home page home.html
@app.route('/home')
@login_required
def home():
    return render_template('home.html')

#loads the logout page logout.html
@app.route('/logout')
@app.route('/')
def logout():
    if current_user.is_authenticated:
        flash('Logout realizado com sucesso!')
        logout_user()
    return render_template('index.html')

#loads the sale first page sale_page1.html
#requires login
@app.route('/sale_page1', methods=['GET', 'POST'])
@login_required
def sale_page1():
    form = ClientSearchForm()
    # retorna todos clientes do banco de dados
    clients = Client.query.all()
    results = []
    id = 0
    for client in clients:
        results.append(client.name)
        results.append(client.cpf)

    #name pode ser ou o id ou o real name tenta achar o cliente pelo name e pelo id caso n ache retorna erro
    if form.validate_on_submit():
        name = form.clientName.data
        if name:
            client = Client.query.filter(or_(Client.name == name, Client.cpf == name)).first()
        if client:
            id = client.id
        else:
            flash('client not found')
        #open a new kart
        kart = Kart(
            client_id=id,
            total = 0
        )
        db.session.add(kart)
        db.session.commit()
        return redirect(url_for('sale_page2', id=id, kart=kart.id))
    return render_template('sale_page1.html', form=form, results=results)

# load the sale page (formerly sale_page2 and sale_page2_no_client)
# requires login
@app.route('/sale_page2/<int:kart>/<int:id>', methods=['GET', 'POST'])
@app.route('/sale_page2/<int:kart>', methods=['GET', 'POST'])
@app.route('/sale_page2', methods=['GET', 'POST'])
@login_required
def sale_page2(kart=None, id=None):
    form = ProductSearchForm()

    # Fetch all products from the database
    products = Product.query.all()
    results = []
    for product in products:
        results.append(product.name)
        results.append(product.code)

    # Check if a valid kart is provided
    if kart is None or not Kart.query.get(kart):
        # If no kart is provided or kart is invalid, create a new one
        new_kart = Kart(client_id=id, total=0)
        db.session.add(new_kart)
        db.session.commit()

        # Set kart to the newly created cart's id
        kart = new_kart.id

    # Retrieve kart items for display
    kartitems = KartItem.query.filter_by(kart_id=kart).all()
    kartinfo = Kart.query.filter_by(id=kart).first()
    if form.validate_on_submit():
        name = form.productName.data
        return redirect(url_for('sale_page3', name=name, id=id, kart=kart))

    return render_template('sale_page2.html', results=results, id=id, kart=kart, form=form, kartitems=kartitems, kartinfo=kartinfo)

#loads the sale third page sale_page3.html
#requires login
@app.route('/sale_page3/<name>/<int:kart>/<int:id>', methods=['GET', 'POST'])
@app.route('/sale_page3/<name>/<int:kart>', methods=['GET', 'POST'])
@login_required
def sale_page3(name, kart, id=None):
    form = CartForm()  # Use o seu formulário CartForm

    # recupera o produto com o nome passado
    product = Product.query.filter_by(name=name).first()

    if form.validate_on_submit():
        quantidade = form.quantity.data
        #checa se a quantidade é maior que a quantidade em estoque
        if quantidade > product.quantity:
            flash('Quantidade maior que a disponível em estoque', 'error')
            return redirect(url_for('sale_page3', name=name, id=id, kart=kart))
        # recupera o kart
        kart_instance = Kart.query.filter_by(id=kart).first()

        # seta o total do kart
        kart_instance.total = kart_instance.total + (quantidade * product.price)

        # cria um novo item no kart
        kartitem = KartItem(
            kart_id=kart_instance.id,
            product_id=product.id,
            quantity=quantidade,
            total=quantidade * product.price
        )

        db.session.add(kartitem)
        db.session.commit()

        flash('Produto adicionado ao carrinho com sucesso!', 'success')
        if id:
            return redirect(url_for('sale_page2', id=id, kart=kart_instance.id))
        else:
            return redirect(url_for('sale_page2', kart=kart_instance.id))

    return render_template('sale_page3.html', product=product, form=form, id=id, kart=kart)

#sele confirm rote
@app.route('/sale_confirm/<int:kart>', methods=['GET', 'POST'])
@login_required
def sale_confirm(kart):
    # recupera o kart
    kart_instance = Kart.query.filter_by(id=kart).first()
    # seta o total do kart
    kart_instance.confirmed = True
    db.session.commit()
    #remove a quantidade de produtos do estoque
    kartitems = KartItem.query.filter_by(kart_id=kart).all()
    for item in kartitems:
        product = Product.query.filter_by(id=item.product_id).first()
        product.quantity = product.quantity - item.quantity
        db.session.commit()

    flash('Compra confirmada com sucesso!', 'success')
    return redirect(url_for('sale_page1'))

@app.route('/sale_cancel/<int:kart>', methods=['GET', 'POST'])
@login_required
def sale_cancel(kart):
    # recupera o kart
    kart_instance = Kart.query.filter_by(id=kart).first()
    #excli o carrinho
    db.session.delete(kart_instance)
    db.session.commit()
    flash('Compra cancelada com sucesso!', 'success')
    return redirect(url_for('sale_page1'))

# Carregue a página de histórico de vendas
@app.route('/sale_history', methods=['GET', 'POST'])
@login_required
def sale_history():
    class Sale:
        def __init__(self, id, date, total, client):
            self.id = id
            self.date = date
            self.items = []  # Alteração aqui para armazenar itens como tuplas (nome do produto, quantidade)
            self.total = total
            self.client = client

    sales = []
    karts = Kart.query.filter_by(confirmed=True).all()

    for kart in karts:
        client = Client.query.get(kart.client_id)

        if client is None:
            client_name = "Nenhum"
        else:
            client_name = client.name

        sale = Sale(kart.id, kart.date, kart.total, client_name)

        kartitems = KartItem.query.filter_by(kart_id=kart.id).all()

        for item in kartitems:
            product = Product.query.get(item.product_id)

            if product is None:
                app.logger.warning(f"Product with ID {item.product_id} not found.")
                continue  # Pule o produto se não for encontrado

            sale.items.append((product.name, item.quantity))  # Adição da quantidade ao item

        sales.append(sale)

    return render_template('sale_history.html', sales=sales)

#loads the search client page search_client.html
#requires login
@app.route('/search_client', methods=['GET', 'POST'])
@login_required
def search_client():
    form = ClientSearchForm()
    # retorna todos clientes do banco de dados
    clients = Client.query.all()
    results = []
    for client in clients:
        results.append(client.name)
        results.append(client.cpf)

    if form.validate_on_submit():
        name = form.clientName.data
        return redirect(url_for('client', name=name))

    return render_template('search_client.html', results=results, form=form)

# Rota para exibir a página do cliente com base no parâmetro 'name'
# ... (import statements and other code)

@app.route('/client/<name>', methods=['GET', 'POST'])
@login_required
def client(name):
    form = ClientAtualizeForm()
    car_form = CarAddForm()
    phone_form = PhoneAddForm()
    client_cars = []
    client_phones = []

    client = Client.query.filter(or_(Client.name == name, Client.cpf == name)).first()
    products = Product.query.all()

    itens = (
        db.session.query(
            Kart.id.label('cart_id'),
            Kart.date.label('cart_date'),
            Kart.total.label('cart_total'),
            Product.name.label('product_name'),
            KartItem.quantity.label('item_quantity'),
            func.sum(KartItem.total).label('item_total')
        )
        .join(KartItem, Kart.id == KartItem.kart_id)
        .join(Product, KartItem.product_id == Product.id)
        .join(Client, Kart.client_id == Client.id)
        .filter(Client.id == client.id)  # Separate filter conditions with a comma
        .group_by(Kart.id, Product.id)
        .all()
    ) if client else []

    client_cars = Car.query.filter_by(client_id=client.id).all() if client else []
    client_phones = Phone.query.filter_by(client_id=client.id).all() if client else []

    if form.validate_on_submit() and form.submit.data:
        # Update client information
        if form.clientName.data:
            client.name = form.clientName.data
        if form.clientAddress.data:
            client.address = form.clientAddress.data
        if form.clientCPF.data:
            client.cpf = form.clientCPF.data
        if form.clientEmail.data:
            client.email = form.clientEmail.data
        db.session.commit()
        flash('Cliente atualizado com sucesso!')
        return redirect(url_for('search_client'))

    return render_template('client.html', cliente=client, form=form, carros=client_cars, car_form=car_form, phone_form=phone_form, phones=client_phones, itens=itens)

#add phone page
@app.route('/client/<name>/add_phone', methods=['POST'])
@login_required
def add_phone(name):
    phone_form = PhoneAddForm()

    client = Client.query.filter(or_(Client.name == name, Client.cpf == name)).first()

    if phone_form.validate_on_submit() and phone_form.submit.data:
        try:
            phone = Phone(
                number=phone_form.number.data,
                client_id=client.id
            )
            db.session.add(phone)
            db.session.commit()
            flash('Telefone adicionado com sucesso!')
            return redirect(url_for('client', name=name))
        except IntegrityError as e:
            db.session.rollback()
            flash(f"Erro ao adicionar telefone: {str(e)}", 'error')

    return redirect(url_for('client', name=name))

#add car page
@app.route('/client/<name>/add_car', methods=['POST'])
@login_required
def add_car(name):
    car_form = CarAddForm()

    client = Client.query.filter(or_(Client.name == name, Client.cpf == name)).first()

    if car_form.validate_on_submit() and car_form.submit.data:
        try:
            carro = Car(
                name=car_form.modelo.data,
                client_id=client.id
            )
            db.session.add(carro)
            db.session.commit()
            flash('Carro adicionado com sucesso!')
            return redirect(url_for('client', name=name))
        except IntegrityError as e:
            db.session.rollback()
            flash(f"Erro ao adicionar carro: {str(e)}", 'error')

    return redirect(url_for('client', name=name))

@app.route('/new_client', methods=['GET', 'POST'])
@login_required
def new_client():
    form = ClientCreateForm()

    if form.validate_on_submit():
        try:
            # Cria um novo cliente com os dados do formulário
            client = Client(
                name=form.clientName.data,
                address=form.clientAddress.data,
                cpf=form.clientCPF.data,
                email=form.clientEmail.data
            )

            # Adiciona o cliente ao banco de dados e comita as mudanças
            db.session.add(client)
            db.session.commit()

            # Redireciona para a página de pesquisa de clientes
            return redirect(url_for('search_client'))
        except IntegrityError:
            # Handle unique constraint violation (CPF already exists)
            db.session.rollback()
            flash("CPF already exists. Please use a different CPF.")
            return render_template('new_client.html', form=form)

    return render_template('new_client.html', form=form)
# new_product
@app.route('/new_product', methods=['GET', 'POST'])
@login_required
def new_product():
    form = ProductUpdateForm()

    if form.validate_on_submit():
        try:
            # Cria um novo produto com os dados do formulário
            product = Product(
                name=form.productName.data,
                price=form.productPrice.data,
                code=form.productCode.data,
                quantity=form.productQuantity.data
            )

            # Adiciona o produto ao banco de dados e comita as mudanças
            db.session.add(product)
            db.session.commit()

            # Redireciona para a página de pesquisa de produtos
            return redirect(url_for('search_product'))
        except IntegrityError:
            # Handle unique constraint violation (CPF already exists)
            db.session.rollback()
            flash("Code already exists. Please use a different code.")
            return render_template('new_product.html', form=form)

    return render_template('new_product.html', form=form)


@app.route('/search_product', methods=['GET', 'POST'])
@login_required
def search_product():
    form = ProductSearchForm()
    products = Product.query.all()
    results = []
    for product in products:
        results.append(product.name)
        results.append(product.code)

    if form.validate_on_submit():
        name = form.productName.data
        return redirect(url_for('product', name=name))

    return render_template('search_product.html',results=results, form=form)


@app.route('/product/<name>', methods=['GET', 'POST'])
@login_required
def product(name):
    product = Product.query.filter_by(name=name).first()
    if product is None:
        product = Product.query.filter_by(code=name).first()
    form = ProductUpdateForm(obj=product)  # Popula o formulário com os dados do produto

    if form.validate_on_submit():
        if form.productQuantity.data:
            product.quantity = form.productQuantity.data
        if form.productPrice.data:
            product.price = form.productPrice.data
        if form.productName.data:
            product.name = form.productName.data
        if form.productCode.data:
            product.code = form.productCode.data
        if form.productDescription.data:
            product.description = form.productDescription.data
        db.session.commit()
        return redirect(url_for('search_product'))

    return render_template('product.html', produto=product, form=form)

#delete client
@app.route('/delete_client/<name>', methods=['GET', 'POST'])
@login_required
def delete_client(name):
    client = Client.query.filter_by(name=name).first()
    if client is None:
        client = Client.query.filter_by(cpf=name).first()
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('search_client'))

#delete product
@app.route('/delete_product/<name>', methods=['GET', 'POST'])
@login_required
def delete_product(name):
    product = Product.query.filter_by(name=name).first()
    if product is None:
        product = Product.query.filter_by(code=name).first()
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('search_product'))

@app.route('/edit_car/<int:car_id>', methods=['GET', 'POST'])
@login_required
def edit_car(car_id):
    form = CarEditForm()
    car_to_edit = Car.query.filter_by(id=car_id).first()
    id = car_to_edit.client_id
    #pega o nome do cliente baseado no id
    client = Client.query.filter_by(id=id).first()
    if form.validate_on_submit():
        if form.submit_edit.data:
            car_to_edit.name = form.modelo.data
            db.session.commit()
        elif form.submit_delete.data:
            db.session.delete(car_to_edit)
            db.session.commit()
        return redirect(url_for('client', name=client.name))
    return render_template('edit_car.html', form=form, car=car_to_edit)

#edit phone
@app.route('/edit_phone/<int:phone_id>', methods=['GET', 'POST'])
@login_required
def edit_phone(phone_id):
    form = PhoneEditForm()
    phone_to_edit = Phone.query.filter_by(id=phone_id).first()
    id = phone_to_edit.client_id
    #pega o nome do cliente baseado no id
    client = Client.query.filter_by(id=id).first()
    if form.validate_on_submit():
        if form.submit_edit.data:
            phone_to_edit.number = form.number.data
            db.session.commit()
        elif form.submit_delete.data:
            db.session.delete(phone_to_edit)
            db.session.commit()
        return redirect(url_for('client', name=client.name))
    return render_template('edit_phone.html', form=form, phone=phone_to_edit)

