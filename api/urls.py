from django.urls import path
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('profile', ProfileUserViewSet)
urlpatterns = router.urls