from rest_framework import serializers

from django.contrib.auth.hashers import check_password

from .models import Player, Game

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'thumbnail']
 
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'email', 'balance']

class PlayerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Player
        fields = ['email', 'password']

    def create(self, validated_data):
        player = Player(email=validated_data['email'])
        player.set_password(validated_data['password'])
        player.save()
        return player

class PlayerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            player = Player.objects.get(email=email)
        except Player.DoesNotExist:
            raise serializers.ValidationError("Player not found")

        if not check_password(password, player.password):
            raise serializers.ValidationError("Incorrect password")

        return player       