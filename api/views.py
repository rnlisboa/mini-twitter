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


class ProfileUserViewSet(viewsets.ModelViewSet):
    queryset = ProfileUserModel.objects.all()
    serializer_class = ProfileUserSerializer
    
    @action(detail=False, methods=['get'])
    def get_profile(self, *args, **kwargs):
        user_id = self.request.query_params.get('user_id', None)

        if not user_id:
            return Response(data="Erro ao buscar usuário", status=status.HTTP_400_BAD_REQUEST)
        try:
            user_profile = self.queryset.get(user=user_id)
        except Exception as e:
            return Response(data={
                "message":"Perfil de usuário não encontrado.",
                "error": f"{e}"
            }, status=status.HTTP_400_BAD_REQUEST) 
        
        serializer = self.serializer_class(user_profile)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def register_profile(self, *args, **kwargs):
        req = self.request.data

        user_id = req['user_id'] if 'user_id' in req else None
        if not user_id:
            return Response(data="Erro ao buscar usuário", status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(pk=user_id)
        
        profile_image = req['profile_image'] if 'profile_image' in req else None

        try:
            new_profile = ProfileUserModel(
                photo=profile_image,
                user = user
            )
            new_profile.save()

        except Exception as e:
            return Response(data={
                'message': 'Erro ao adicionar ao criar perfil',
                'error': f"{e}"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response('Perfil criado com sucesso', status=status.HTTP_201_CREATED)