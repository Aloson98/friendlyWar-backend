from django.shortcuts import render
from django.contrib.auth import login
from .serializers import *
from rest_framework.generics import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from knox.auth import TokenAuthentication
from knox.views import LoginView as knoxLoginView
from knox.views import LogoutView as knoxLogoutView


class LoginAPIView(knoxLoginView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class= LoginSerializer
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        response = super().post(request, format=None)
        return Response({'data':response.data},status=HTTP_200_OK)
    
    def get_post_response_data(self, request, token, instance):
        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        if self.serializer_class is not None:
            data["user"] = self.serializer_class(
                request.user,
                context=self.get_context()
            ).data
        return data


class LogoutView(knoxLogoutView):
    permission_classes = [IsAuthenticated]


class CustomUserListCreateAPIView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    
class CustomUserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    lookup_field = "username"


#matches views
class MatchesListCreateAPIView(ListCreateAPIView):
    queryset = Matches.objects.all()
    serializer_class = MatchesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(team1=user, update_by=user)
    
    
class MatchesRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Matches.objects.all()
    serializer_class = MatchesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    lookup_field = "match_id"
    
    def perform_update(self, serializer):
        user = self.request.user
        return serializer.save(update_by=user)
    
    def perform_destroy(self, instance):
        user = self.request.user
        return instance.delete()