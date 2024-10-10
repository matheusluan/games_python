# games/views.py

from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Game, Player
from .serializers import GameSerializer, PlayerRegistrationSerializer, PlayerLoginSerializer, PlayerSerializer
from .utils import get_tokens_for_player 

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()  
    serializer_class = GameSerializer 
    permission_classes = [AllowAny]
    
class PlayerRegistrationView(generics.CreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        player = serializer.save()
        tokens = get_tokens_for_player(player)  
        return Response({
            'player': PlayerSerializer(player).data,
            'tokens': tokens
        }, status=status.HTTP_201_CREATED)

class PlayerLoginView(generics.GenericAPIView):
    serializer_class = PlayerLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        player = serializer.validated_data
        tokens = get_tokens_for_player(player) 
        return Response({
            'player': PlayerSerializer(player).data,
            'tokens': tokens
        })
