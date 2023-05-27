from django.shortcuts import render

from rest_framework.response                    import Response
from rest_framework.decorators                  import action
from rest_framework                             import status, viewsets
from rest_framework.permissions                 import IsAuthenticated
from rest_framework_simplejwt.authentication    import JWTAuthentication
from django.contrib.auth.models import User
from django.db.models import Q
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
    
    @action(detail=False, methods=['post'])
    def add_follower(self, *args, **kwargs):
        req = self.request.data

        user_id = req['user_id'] if 'user_id' in req else None 
        follower_id = req['follower_id'] if 'follower_id' in req else None

        if not user_id or not follower_id:
            return Response(data="Erro ao buscar usuário ou seguidor", status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
            user_to_follow_instace = User.objects.get(pk=follower_id)

            existing_follow = FollowModel.objects.filter(user=user, following=user_to_follow_instace).exists()
            if existing_follow:
                return Response(data="Você já está seguindo o usuário", status=status.HTTP_400_BAD_REQUEST)

            follow = FollowModel(user=user, following=user_to_follow_instace)
            follow.save()
            return Response(data="Seguidor adicionado com sucesso", status=status.HTTP_201_CREATED)

        except ProfileUserModel.DoesNotExist:
            return Response(data="Perfil de usuário não encontrado", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={
                'message': 'Erro ao adicionar seguidor',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserPostViewSet(viewsets.ModelViewSet):
    queryset = UserPostModel.objects.all()
    serializer_class = UserPostSerializer

    @action(detail=False, methods=['get'])
    def get_my_posts(self, *args, **kwargs):
        user_id = self.request.query_params.get('user_id', None)

        try:
            posts = self.queryset.filter(user=user_id)
        except Exception as e:
            return Response(data={
                "message":"Não há publicações para este usuário.",
                "error": f"{e}"
            }, status=status.HTTP_400_BAD_REQUEST) 
        
        serializer = serializer_class(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def get_followers_posts(self, *args, **kwargs):
        user_id = self.request.query_params.get('user_id', None)

        try:
            following_ids = FollowModel.objects.filter(user=user_id).values_list('following', flat=True)

            posts = self.queryset.filter(Q(user__in=following_ids)).exclude(user=user_id)

            serializer = self.serializer_class(posts, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data={
                "message": "Erro ao obter os posts dos seguidores",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def register_publication(self, *args, **kwargs):
        req = self.request.data
        user_id = req['user_id'] if 'user_id' in req else None 
        user = User.objects.get(pk=user_id)
        
        twitt = req['twitt'] if 'twitt' in req else None
        photo = req['photo'] if 'photo' in req else None

        if not (twitt and photo):
            return  Response(data="Não é possível publicações vazias.", status=status.HTTP_400_BAD_REQUEST)  

        try:
            publi = UserPostModel(
                user=user,
                photo=photo,
                twitt=twitt
            )   

            publi.save()
            serializer = self.serializer_class(publi)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={
                "message": "Erro ao publicar",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)