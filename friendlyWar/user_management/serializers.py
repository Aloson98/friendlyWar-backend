
from django.contrib.auth import get_user_model, authenticate
from django.forms.models import model_to_dict
from rest_framework import serializers
from django_eventstream import send_event
from .models import CustomUser, Matches



class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser model."""
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ["username", "email", "date_joined", "password"]
        read_only_fields = ["date_joined"]
        
    def create(self, validated_data):
        """Create a new user."""
        user = CustomUser.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for login."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """Validate the data."""
        if not data.get("username") or not data.get("password"):
            raise serializers.ValidationError("Username and password are required.")
        
        user = authenticate(username=data.get("username"), password=data.get("password"))
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        
        return user
 
 
class MatchesSerializer(serializers.ModelSerializer):
    """Serializer for Matches model."""
    update_by = serializers.SlugRelatedField(slug_field="username", queryset=CustomUser.objects.all(), required=False)
    team1 = serializers.SlugRelatedField(slug_field="username", queryset=CustomUser.objects.all(), required=False)
    team2 = serializers.SlugRelatedField(slug_field="username", queryset=CustomUser.objects.all())
    winner = serializers.SlugRelatedField(slug_field="username", read_only=True)
    
    class Meta:
        model = Matches
        fields = ["match_id", "team1", "team2", "winner", "update_by", "date"]
        read_only_fields = ["date"]
    
    def validate(self, attrs):
        """Validate the data."""
        winner_username = attrs["team2"]
        user = self.context["request"].user
        
        if user.username == str(winner_username):
            print("You can't win a match against yourself.")
            raise serializers.ValidationError("You can't win a match against yourself.")
        
        return attrs
    
    def create(self, validated_data):
        """Create a new match."""
        winner_username = validated_data.get("team2")
        winner = CustomUser.objects.get(username=winner_username)
        match = Matches.objects.create(winner=winner, **validated_data)
        
        #sending signal to the event stream
        match_data = model_to_dict(match)
        send_event("events", "match_result", match_data)
        
        return match
