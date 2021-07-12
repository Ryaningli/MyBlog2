from datetime import datetime
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_encode_handler
from rest_framework_jwt.views import ObtainJSONWebToken, jwt_response_payload_handler
from Blog.models import User
from Blog import serializer as serializer_list
from rest_framework import generics
from Blog.serializer import UserSerializer
from Blog.utils.APIResponse import APIResponse


class UserList(generics.ListCreateAPIView):
    authentication_classes = [JSONWebTokenAuthentication]  # 存储到request.user，如果只配置这个，则不登陆也能访问
    # permission_classes = [IsAuthenticated]  # 必须已经登陆，即request.user不能是匿名用户
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Test(APIView):
    authentication_classes = [JSONWebTokenAuthentication]  # 存储到request.user，如果只配置这个，则不登陆也能访问

    def post(self, request):
        print('***********' * 20)
        # token = request.headers.get('token')
        # user = jwt_decode_handler(token)
        user = request.user
        print(user)

        return APIResponse()


class Register(APIView):
    def get(self, request):
        return APIResponse({'method': 'GET'})

    @staticmethod
    def post(request):
        serializer = serializer_list.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(**serializer.data)
            return APIResponse()
        return APIResponse()


class Login(ObtainJSONWebToken):

    def post(self, request, *args, **kwargs):
        serializer = serializer_list.LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            token = jwt_encode_handler(jwt_payload_handler(user))
            response_data = jwt_response_payload_handler(token, user, request)
            response = APIResponse(data=response_data, msg='登录成功')
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE, token, expires=expiration, httponly=True)
            return response

        return APIResponse(serializer=serializer, status=status.HTTP_401_UNAUTHORIZED)
