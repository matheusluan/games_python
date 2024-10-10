
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_player(player):
    """
    Gera e retorna os tokens de acesso e refresh para o jogador.
    """
    refresh = RefreshToken.for_user(player)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }