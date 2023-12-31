from auth_app.models import User
from .serializer import UsersSerializerReturn, UserInformationSerializer
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
# views.py

class BaseSelectUserViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializerReturn
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class SelectUserViewSet(BaseSelectUserViewSet):
    def get_queryset(self):
        users = User.objects.all()
        if self.request.query_params.get('onlyPosts') == 'true':
            self.serializer_class.Meta.fields = ['posts']
        else:
            self.serializer_class.Meta.fields = ['email', 'username', 'last_name', 'id', 'posts']
        return users

class SelectCurrentlyUserViewSet(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializerReturn
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        query_params = self.request.query_params

        if query_params.get('onlyPosts') == 'true':
            self.serializer_class.Meta.fields = ['posts']

        elif query_params.get('onlyInformation') == 'true':
            self.serializer_class.Meta.fields = ['username', 'last_name', 'posts']

        else:
            self.serializer_class.Meta.fields = ['email', 'username', 'last_name', 'id', 'posts']    
                
        return self.request.user
    
class CurrentUserInfomation(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated] 

    def get(self, request):
        user = self.request.user
        user_serializer = UserInformationSerializer(user, many=False)
        return Response(user_serializer.data)
    
    def patch(self, request):
        user_serializer = UserInformationSerializer(data=request.data, fields=[self.request.query_params.get('changeField')])
        if user_serializer.is_valid():
            user_serializer.update(instance=request.user, validated_data=user_serializer.validated_data)
            return Response({
                'message': 'Actualizacion con exito'
            }, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)