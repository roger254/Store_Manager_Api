from . import auth_blueprint
from flask import make_response, request, jsonify
from flask.views import MethodView
from app.api.v1.models import User


class UserRegistrationView(MethodView):
    """Registers new User."""

    def post(self):
        """POST req for /auth/register"""

        user = User.query.filter_by(
            user_name=request.data['user_name']).first()

        # if user does not exist
        if not user:
            try:
                user_data = request.data
                user_name = user_data['user_name']
                password = user_data['password']
                user = User(user_name=user_name, password=password)
                # save User
                user.save()

                response = {
                    'message': 'Registration Successful. Login!'
                }
                return make_response(jsonify(response)), 201
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            # user already exists
            response = {
                'message': 'User already exists. Login!'
            }
            return make_response(jsonify(response)), 202


class UserLoginView(MethodView):
    """Handles user login"""

    def post(self):
        """POST req for /auth/login"""

        try:
            user = User.query.filter_by(
                user_name=request.data['user_name']).first()

            # check for valid details
            if user and user.is_password_valid(request.data['password']):
                # Generate access token
                access_token = user.generate_user_token(user.id)
                if access_token:
                    response = {
                        "message": "You've logged in successfully.",
                        "access_token": access_token.decode()
                    }
                    # return response
                    return make_response(jsonify(response)), 201
            else:
                response = {
                    'message': 'Invalid User, Please try again'
                }
                return make_response(jsonify(response)), 401
        except Exception as e:
            # return error as string
            response = {
                'message': str(e)
            }
            # send Internal Server Error
            return make_response(jsonify(response)), 500


user_registration_view = UserRegistrationView.as_view('user_registration_view')
user_login_view = UserLoginView.as_view('user_login_view')
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=user_registration_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=user_login_view,
    methods=['POST']
)
