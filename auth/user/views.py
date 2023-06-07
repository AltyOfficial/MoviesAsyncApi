from flask import Response
from flask_restful import Resource
from flask import request, make_response
from user.service import create_user, login_user


class RegisterApi(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for creating user.
        :return: JSON object
        """
        input_data = request.get_json()
        response, status = create_user(request, input_data)
        return make_response(response, status)


class LoginApi(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for login user.
        :return: JSON object
        """
        input_data = request.get_json()
        response, status = login_user(request, input_data)
        return make_response(response, status)
    

class LogoutApi(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method to log user out.
        :return: JSON object
        """
        input_data = request.get_json()
        response, status = logout_user(request, input_data)
        return make_response(response, status)
