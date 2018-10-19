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


user_registration_view = UserRegistrationView.as_view('user_registration_view')
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=user_registration_view,
    methods=['POST']
)
