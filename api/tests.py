from django.test import TestCase, RequestFactory
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework.response import Response
from .views import *
from . models import *
from django.contrib.auth.models                 import User
from .serializers import UserSerializer

class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = UserViewSet.as_view({'post': 'create_user'})

    def test_create_user_success(self):
        request_data = {
            'first_name': 'user',
            'last_name': 'teste',
            'username': 'usertest',
            'email': 'user@teste.com',
            'password': 'password123'
        }
        request = self.factory.post('/users/create_user', request_data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'usertest')
        self.assertEqual(user.email, 'user@teste.com')

    def test_create_user_missing_fields(self):
        request_data = {
            'first_name': 'user',
            'last_name': 'teste',
            'username': 'usertest',
            'email': 'user@teste.com'
            # password field is missing
        }
        request = self.factory.post('/users/create_user', request_data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(
            response.data,
            {'detail': 'Preencha todos os campos.'}
        )

    def test_create_user_validation_error(self):
        request_data = {
            'first_name': 'user',
            'last_name': 'teste',
            'username': 'usertest',
            'email': 'email invalido',
            'password': 'password123'
        }
        request = self.factory.post('/users/create_user', request_data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(
            response.data,
            {
            "errors": {
                "email": [
                    "Insira um endereço de email válido."
                ]
            },
            "message": "Houveram erros de validação"
        }
        )

class ProfileUserViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user teste',
            password='passwordteste'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):

        profile = ProfileUserModel.objects.create(user=self.user)

        url = '/api/profile/get_profile/'
        response = self.client.get(url, {'user_id': self.user.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data['user'])
        self.assertIsNone(response.data['photo'])
        self.assertEqual(str(profile.photo), '')



    def test_get_profile_invalid_user_id(self):
        url = '/api/profile/get_profile/'
        response = self.client.get(url, {'user_id': 999}) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Perfil de usuário não encontrado.')

    def test_register_profile(self):
        url = '/api/profile/register_profile/'
        profile_image = 'path/to/profile_image.jpg'
        response = self.client.post(url, {'user_id': self.user.id, 'profile_image': profile_image})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 'Perfil criado com sucesso')


    def test_register_profile_missing_user_id(self):
        url = '/api/profile/register_profile/'
        profile_image = 'path/to/profile_image.jpg'
        response = self.client.post(url, {'profile_image': profile_image})  # user_id ausente

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'Erro ao buscar usuário')

    def test_add_follower(self):
 
        user_to_follow = User.objects.create_user(username='testuser2', password='testpassword')
        follower = User.objects.create_user(username='testuser3', password='testpassword')

        url = '/api/profile/add_follower/'
        response = self.client.post(url, {'user_id': user_to_follow.id, 'follower_id': follower.id})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 'Seguidor adicionado com sucesso')


    def test_add_follower_missing_ids(self):
        url = '/api/profile/add_follower/'
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'Erro ao buscar usuário ou seguidor')

    def test_add_follower_already_following(self):
    
        user_to_follow = User.objects.create_user(username='testuser2', password='testpassword')
        follower = User.objects.create_user(username='testuser3', password='testpassword')

        FollowModel.objects.create(user=user_to_follow, following=follower)

        url = '/api/profile/add_follower/'
        response = self.client.post(url, {'user_id': user_to_follow.id, 'follower_id': follower.id})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'Você já está seguindo o usuário')

class UserPostViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UserPostViewSet.as_view({'get': 'list', 'post': 'create'})
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_get_my_posts(self):
        request = self.factory.get('/user-posts/get-my-posts/?user_id={}'.format(self.user.id))
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_followers_posts(self):
        request = self.factory.get('/user-posts/get-followers-posts/?user_id={}'.format(self.user.id))
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_publication(self):
        data = {
            'user': self.user.id,
            'twitt': 'Test twitt',
            'photo': 'test_photo.jpg'
        }
        request = self.factory.post('/user-posts/register-publication/', data)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)