from django.shortcuts import render

from rest_framework.response                    import Response
from rest_framework.decorators                  import action
from rest_framework                             import status, viewsets
from rest_framework.permissions                 import IsAuthenticated
from rest_framework_simplejwt.authentication    import JWTAuthentication
from django.contrib.auth.models import User
from .serializers import *
from .models import *
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def create_user(self, *args, **kwargs):
        req = self.request.data

        first_name = req['first_name'] if 'first_name' in req else None
        last_name = req['last_name'] if 'last_name' in req else None
        username = req['username'] if 'username' in req else None
        email = req['email'] if 'email' in req else None
        password = req.get('password')

        if not (username and first_name and last_name and email and password):
            return Response(f'Preencha todos os campos.', status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=req)
        if serializer.is_valid():
            try:
                user = User(
                    username=username,
                    first_name=first_name,
                    email=email,
                    last_name=last_name,
                    is_active=True,
                    is_superuser=False
                )
                user.set_password(password)
                user.save()
                return Response(data={'message': 'Usuário cadastrado!'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(data={'error': f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "Houveram erros de validação",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)