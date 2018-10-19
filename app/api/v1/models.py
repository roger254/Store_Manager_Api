# get the database
from app import db
from flask import current_app
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta


class User(db.Model):
    """Represents the User"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    user_name = db.Column(
        db.String(256),
        nullable=False,
        unique=True
    )
    password = db.Column(
        db.String(256),
        nullable=False
    )
    user_status = db.Column(
        db.String(256),
        nullable=False
    )
    sales = db.relationship(
        'Sale',
        order_by='Sale.id'
    )

    def __init__(self, user_name, password, user_status):
        """Initialize User"""
        self.user_name = user_name
        self.user_status = user_status
        self.password = Bcrypt().generate_password_hash(password).decode()

    def is_password_valid(self, password):
        """Validate user password"""
        return Bcrypt().check_password_hash(self.password, password)

    def generate_user_token(self, user_id):
        """Generates user token"""
        try:
            # set up payload with expiration
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=10),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            jwt_token = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'

            )
            return jwt_token
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_user_token(token):
        """Decode user token"""
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid
            return "Invalid token. Please register or login"

    def save(self):
        """Save user to database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete this user"""
        db.session.delete(self)
        db.session.commit()


class Product(db.Model):
    """Represents the products table"""

    __tablename__ = "products"

    # products columns
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    product_name = db.Column(
        db.String(255),
        nullable=False
    )
    product_price = db.Column(
        db.Float,
        nullable=False
    )
    product_quantity = db.Column(
        db.Integer,
        nullable=False
    )
    product_entry_date = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp()
    )

    def __init__(self, product_name, product_price, product_quantity):
        self.product_name = product_name
        self.product_price = product_price
        self.product_quantity = product_quantity

    def save(self):
        """Save to the database"""
        db.session.add(self)
        db.session.commit()

    # method to get all products
    @staticmethod
    def get_all():
        """Get all products"""
        return Product.query.all()

    def delete(self):
        """Delete this product"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Return Current Instance"""
        return "[Product: {} - Price {} - Amount {}]".format(
            self.product_name, self.product_price, self.product_quantity)


class Sale(db.Model):
    """Represents the products table"""

    __tablename__ = "sales"

    # sales columns
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    sales_name = db.Column(
        db.String(255)
    )
    sales_price = db.Column(
        db.Float
    )
    sales_quantity = db.Column(
        db.Integer
    )
    sales_date = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )
    sold_by = db.Column(
        db.Integer,
        db.ForeignKey(User.id)
    )

    def __init__(self, sales_name, sales_price, sales_quantity, sold_by):
        self.sales_name = sales_name
        self.sales_price = sales_price
        self.sales_quantity = sales_quantity
        self.sold_by = sold_by

    def save(self):
        """Save to the database"""
        db.session.add(self)
        db.session.commit()

    # method to get all products
    @staticmethod
    def get_all(user_id):
        """Get all sales for specific user"""
        return Sale.query.filter_by(sold_by=user_id)

    def delete(self):
        """Delete this product"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Return Current Instance"""
        return "[Sale: {} - Price {} - Amount {} - Data {} - Sold by {}]".format(
            self.sales_name,
            self.sales_price,
            self.sales_quantity,
            self.sales_date,
            self.sold_by
        )
