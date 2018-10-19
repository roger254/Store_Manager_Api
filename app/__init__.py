from flask import request, jsonify, abort, make_response
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

# init the sql-SQLAlchemy\
db = SQLAlchemy()


# create the flask app
def create_app(config_name):
    from app.api.v1.models import Product, Sale, User
    app = FlaskAPI(__name__, instance_relative_config=True)
    # load the configs
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # connect to db
    db.init_app(app)

    @app.route('/products/', methods=['POST', 'GET'])
    def product():

        # Get the access_token
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(' ')[1]

        if access_token:
            # decode user
            user_id = User.decode_user_token(access_token)

            if not isinstance(user_id, str):
                if request.method == 'POST':
                    # get products details
                    product_name = str(request.data.get('product_name'))
                    product_price = str(request.data.get('product_price'))
                    product_quantity = str(
                        request.data.get('product_quantity'))
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
                        return make_response(response), 201
                else:
                    # GET req
                    products = Product.get_all()
                    results = []

                    for productItem in products:
                        data = {
                            'id': productItem.id,
                            'product_name': productItem.product_name,
                            'product_price': productItem.product_price,
                            'product_quantity': productItem.product_quantity,
                            'product_entry_date': productItem.product_entry_date
                        }
                        results.append(data)

                    return make_response(jsonify(results)), 200
            else:
                # if user is invalid
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/products/<int:id>', methods=['GET'])
    def product_edit(id, **kwargs):
        auth_header = request.headers.get('Authorization')

        access_token = auth_header.split(" ")[1]

        if access_token:
            # decode user
            user_id = User.decode_user_token(access_token)

            if not isinstance(user_id, str):
                productItem = Product.query.filter_by(id=id).first()
                if not productItem:
                    abort(404)

                response = jsonify({
                    'id': productItem.id,
                    'product_name': productItem.product_name,
                    'product_price': productItem.product_price,
                    'product_quantity': productItem.product_quantity,
                    'product_entry_date': productItem.product_entry_date
                })

                return make_response(response), 200

    @app.route('/sales/', methods=['POST', 'GET'])
    def sale():

        # Get the access_token
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(' ')[1]
        print(access_token)
        if access_token:
            # decode user
            user_id = User.decode_user_token(access_token)

            if not isinstance(user_id, str):
                if request.method == 'POST':

                    # get sales details
                    sales_name = str(request.data.get('sales_name'))
                    sales_price = str(request.data.get('sales_price'))
                    sales_quantity = str(request.data.get('sales_quantity'))
                    if sales_name is not None and sales_price is not None and sales_quantity is not None:
                        salesItem = Sale(
                            sales_name=sales_name,
                            sales_price=sales_price,
                            sales_quantity=sales_quantity,
                            sold_by=user_id
                        )
                        salesItem.save()
                        response = jsonify({
                            'id': salesItem.id,
                            'sales_name': salesItem.sales_name,
                            'sales_price': salesItem.sales_price,
                            'sales_quantity': salesItem.sales_quantity,
                            'sales_date': salesItem.sales_date,
                            'sold_by': salesItem.sold_by
                        })

                        return make_response(response), 201
                else:
                    sales = Sale.get_all(user_id)
                    results = []

                    for sale in sales:
                        data = {
                            'id': sale.id,
                            'sales_name': sale.sales_name,
                            'sales_price': sale.sales_price,
                            'sales_quantity': sale.sales_quantity,
                            'sales_date': sale.sales_date,
                            'sold_by': sale.sold_by
                        }
                        results.append(data)

                    return make_response(jsonify(results)), 200
            else:
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/sales/<int:id>', methods=['GET'])
    def sales_edit(id, **kwargs):

        # Get the access_token
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(' ')[1]

        if access_token:
            # decode user
            user_id = User.decode_user_token(access_token)

            if not isinstance(user_id, str):
                sale = Sale.query.filter_by(id=id).first()
                if not sale:
                    abort(404)

                response = jsonify({
                    'id': sale.id,
                    'sales_name': sale.sales_name,
                    'sales_price': sale.sales_price,
                    'sales_quantity': sale.sales_quantity,
                    'sales_date': sale.sales_date,
                    'sold_by': sale.sold_by
                })

                return make_response(response), 200

    # auth Blueprint
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
