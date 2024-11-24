from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets, permissions
from .models import CustomUser
from .serializers import CustomUserSerializer

class TestUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        try:
            user_data = CustomUserSerializer(request.user).data
            return Response({
                'message': 'Вы успешно аутентифицированы!',
                'user': user_data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=user.id)

    def perform_update(self, serializer):
        user = self.request.user
        if 'role' in self.request.data and user.role != 'admin':
            raise PermissionError("Только администратор может изменять роли.")
        serializer.save()