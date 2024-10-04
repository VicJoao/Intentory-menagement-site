from app import db
from datetime import datetime

class User(db.Model):
    """Class representing a user in the system."""
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    @property
    def is_active(self):
        """Return True if the user is active."""
        return True

    @property
    def is_anonymous(self):
        """Return True if the user is anonymous."""
        return False

    def get_id(self):
        """Return the user id."""
        return str(self.id)

    def __init__(self, login, password, is_admin=False):
        """Initialize a new user."""
        self.login = login
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        """Return a string representation of the User object."""
        return f'<User id={self.id}, admin={self.is_admin}>'

class Product(db.Model):
    """Class representing an available product."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float)
    code = db.Column(db.String(80), unique=True)
    quantity = db.Column(db.Integer, default=0)
    description = db.Column(db.String(120))

    def __init__(self, name, price, code, quantity):
        """Initialize a new product."""
        self.name = name
        self.price = price
        self.code = code
        self.quantity = quantity

    def __repr__(self):
        """Return a string representation of the Product object."""
        return f'<Product id={self.id}, name={self.name}>'

class Client(db.Model):
    """Class representing a client."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    address = db.Column(db.String(120))
    cpf = db.Column(db.String(120), unique=True)

    def __init__(self, name, email, address, cpf):
        """Initialize a new client."""
        self.name = name
        self.email = email
        self.address = address
        self.cpf = cpf

    def __repr__(self):
        """Return a string representation of the Client object."""
        return f'<Client id={self.id}, name={self.name}>'

class Kart(db.Model):
    """Class representing a shopping cart."""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship('Client', backref='karts')
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, client_id, total):
        """Initialize a new shopping cart."""
        self.client_id = client_id
        self.total = total

    def __repr__(self):
        """Return a string representation of the Kart object."""
        return f'<Kart id={self.id}, total={self.total}>'

class KartItem(db.Model):
    """Class representing an item in a shopping cart."""
    id = db.Column(db.Integer, primary_key=True)
    kart_id = db.Column(db.Integer, db.ForeignKey('kart.id'))
    kart = db.relationship('Kart', backref='kart_items')
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', backref='kart_items')
    quantity = db.Column(db.Integer)
    total = db.Column(db.Float)

    def __init__(self, kart_id, product_id, quantity, total):
        """Initialize a new item in a shopping cart."""
        self.kart_id = kart_id
        self.product_id = product_id
        self.quantity = quantity
        self.total = total

    def __repr__(self):
        """Return a string representation of the KartItem object."""
        return f'<KartItem id={self.id}, quantity={self.quantity}>'

class Car(db.Model):
    """Class representing a car associated with a client."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship('Client', backref='cars')

    def __init__(self, name, client_id):
        """Initialize a new car associated with a client."""
        self.name = name
        self.client_id = client_id

    def __repr__(self):
        """Return a string representation of the Car object."""
        return f'<Car id={self.id}, name={self.name}>'

class Phone(db.Model):
    """Class representing a phone associated with a client."""
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(80))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship('Client', backref='phones')

    def __init__(self, number, client_id):
        """Initialize a new phone associated with a client."""
        self.number = number
        self.client_id = client_id

    def __repr__(self):
        """Return a string representation of the Phone object."""
        return f'<Phone id={self.id}, number={self.number}>'