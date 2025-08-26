from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserRegistrationSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		token, created = Token.objects.get_or_create(user=user)
		return Response({
			'user': UserSerializer(user).data,
			'token': token.key
		}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
	def post(self, request):
		serializer = UserLoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data
		token, created = Token.objects.get_or_create(user=user)
		return Response({
			'user': UserSerializer(user).data,
			'token': token.key
		}, status=status.HTTP_200_OK)

class UserDetailView(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class ProfileView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		user = request.user
		serializer = UserSerializer(user)
		return Response(serializer.data)

	def put(self, request):
		user = request.user
		serializer = UserSerializer(user, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)