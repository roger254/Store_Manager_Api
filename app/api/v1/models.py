# get the database
from app import db


class Product(db.Model):
    """Represents the products table"""

    __tablename__ = "products"

    # products columns
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    product_name = db.Column(
        db.String(255)
    )
    product_price = db.Column(
        db.Float
    )
    product_quantity = db.Column(
        db.Integer
    )
    product_entry_date = db.Column(
        db.DateTime,
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
