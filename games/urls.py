from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView 
from .views import GameViewSet, PlayerRegistrationView, PlayerLoginView

router = DefaultRouter()
router.register(r'games', GameViewSet)

urlpatterns = [
    # Games routes
    path('', include(router.urls)),

    # Player registration
    path('register/', PlayerRegistrationView.as_view(), name='player_register'),

    # Player login (TokenObtainPairView customized for Player)
    path('login/', PlayerLoginView.as_view(), name='player_login'),

    # Token refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
