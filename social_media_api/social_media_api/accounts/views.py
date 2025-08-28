from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from notifications.models import Notification
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from .models import CustomUser

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
	permission_classes = [permissions.IsAuthenticated]

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

class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        try:
            to_follow = self.get_queryset().get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        if to_follow == request.user:
            return Response({'error': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        request.user.followers.add(to_follow)
        # Create notification for the user being followed
        Notification.objects.create(
            recipient=to_follow,
            actor=request.user,
            verb='started following',
            target=to_follow
        )
        return Response({'success': f'You are now following {to_follow.username}.'})

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        try:
            to_unfollow = self.get_queryset().get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        request.user.followers.remove(to_unfollow)
        return Response({'success': f'You have unfollowed {to_unfollow.username}.'})