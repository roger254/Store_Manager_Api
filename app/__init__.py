from flask import request, jsonify
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

# init the sql-SQLAlchemy\
db = SQLAlchemy()


# create the flask app
def create_app(config_name):
    from app.api.v1.models import Product
    app = FlaskAPI(__name__, instance_relative_config=True)
    # load the configs
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # connect to db
    db.init_app(app)

    @app.route('/products/', methods=['POST'])
    def product():
        # get products details
        product_name = str(request.data.get('product_name'))
        product_price = str(request.data.get('product_price'))
        product_quantity = str(request.data.get('product_quantity'))
        if product_name is not None and product_price is not None and product_quantity is not None:
            productItem = Product(
                product_name=product_name,
                product_price=product_price,
                product_quantity=product_quantity
            )
            productItem.save()
            response = jsonify({
                'id': productItem.id,
                'product_name': productItem.product_name,
                'product_price': productItem.product_price,
                'product_quantity': productItem.product_quantity,
                'product_entry_date': productItem.product_entry_date
            })
            response.status_code = 201
            return response
    return app
