from datetime import datetime

from django.utils import timezone
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView

from Application.User.models import User
from Application.User.serializer import LoginSerializer

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class CustomJSONWebTokenAPIView(JSONWebTokenAPIView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        result = serializer.is_valid()
        user = serializer.validated_data['user']
        token = serializer.validated_data['token']
        response_data = jwt_response_payload_handler(token, user, request)
        response = Response(response_data)
        if api_settings.JWT_AUTH_COOKIE:
            expiration = (datetime.utcnow() +
                          api_settings.JWT_EXPIRATION_DELTA)
            response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                token,
                                expires=expiration,
                                httponly=True)
            user.objects.update(last_login=timezone.now())
        return response


        # if serializer.is_valid():
        #     user = serializer.object.get('user') or request.user
        #     token = serializer.object.get('token')
        #     response_data = jwt_response_payload_handler(token, user, request)
        #     response = Response(response_data)
        #     if api_settings.JWT_AUTH_COOKIE:
        #         expiration = (datetime.utcnow() +
        #                       api_settings.JWT_EXPIRATION_DELTA)
        #         response.set_cookie(api_settings.JWT_AUTH_COOKIE,
        #                             token,
        #                             expires=expiration,
        #                             httponly=True)
        #     return response

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomObtainJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = LoginSerializer


custom_obtain_jwt_token = CustomObtainJSONWebToken.as_view()