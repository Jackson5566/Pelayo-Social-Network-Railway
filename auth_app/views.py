from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str  
from django.template.loader import render_to_string
from rest_framework import generics, permissions, viewsets, status
from auth_app.models import User
from rest_framework.response import Response
from django.core.signing import TimestampSigner, BadSignature
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import UsersSerializer
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication

class UserExpirationLink:
    frontEnd_site = 'localhost:4200'
    subject = 'Password Reset Request'
    signer = TimestampSigner()
    user = None
    email = ""

    def send_link(self, template: str) -> None:
        if self.user:
            token = self.signer.sign(str(self.user.id))
            encoded_token = urlsafe_base64_encode(token.encode())
            # Preparar el correo electrónico de restablecimiento
            message = render_to_string(template, {
                'user': self.user,
                'domain': self.frontEnd_site,
                'token': encoded_token,
            })
            # Enviar el correo electrónico de restablecimiento
            send_mail(self.subject, None, None, [self.email], fail_silently=False, html_message=message)

    def set_user(self, token: str) -> None:
        decode_token = urlsafe_base64_decode(token)
        decoded_token_str = force_str(decode_token)
        user_id = self.signer.unsign(decoded_token_str, max_age=3600)  # Verificar y decodificar el token, máximo 1 hora de validez
        try:
            self.user = User.objects.get(id=int(user_id))
        except User.DoesNotExist:
            pass

class PasswordChangeRequestView(generics.GenericAPIView, UserExpirationLink):
    def post(self, request):
        self.email = request.data.get('email')
        self.user = User.objects.get(email=self.email)
        self.send_link(template='password_reset_email.html')
        # Siempre devolver éxito para evitar adivinación de correo electrónico
        return Response({'message': 'Se ha enviado un email que te permitirá cambiar tu contraseña.'}, status=status.HTTP_200_OK)


class PasswordChangeConfirmView(generics.GenericAPIView, UserExpirationLink):
    def post(self, request, token):
        try:
            self.set_user(token)

            password = request.data.get('password')
            confirm_password = request.data.get('confirm_password')

            if password == confirm_password:
                self.user.set_password(password)
                self.user.save()

                return Response({'message': 'Contraseña cambiada correctamente.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Las contraseñas no coinciden.'}, status=status.HTTP_400_BAD_REQUEST)
            
        except BadSignature:
            return Response({'error': 'Link de reseto inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Usario no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

class CreateUser(generics.GenericAPIView, UserExpirationLink):
    def post(self, request):
        users_serializer = UsersSerializer(data=request.data)

        if users_serializer.is_valid():
            self.email = request.data['email']

            self.user = users_serializer.create(validated_data=users_serializer.data)
            self.user.is_active = False
            self.user.save()
            
            self.subject = 'Confirmación de cuenta'
            self.send_link(template='user_confirmation_email.html')

            return Response({
                'message': 'Mail de ocnfirmacion enviado'
            }, status=200)
        
        return Response(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateUserConfirmation(generics.GenericAPIView, UserExpirationLink):
    def get(self, request, token):
        self.set_user(token=token)

        self.user.is_active = True
        self.user.save()

        refresh = RefreshToken.for_user(self.user)

        return Response({'refresh': str(refresh), 'access': str(refresh.access_token),}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def denunciate(request):
    try:
      user_id = request.data['id']
      user = User.objects.filter(id=user_id).first()

      if user not in user.denunciations.all():
        if user != request.user:
          user.denunciations.add(request.user)

          user_denuncations = len(user.denunciations.all())
          if user_denuncations >= 20:
              send_mail("Exceso de denuncias", f"El usuario ha sido denunciado {user_denuncations} veces", None,  ["jackson0102almeida@gmail.com"])

          return Response({
              'message': 'Usuario denunciado'
          }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'No te puedes denunciar a ti mismo'
            })
      else:
          return Response({
              'message': 'Usuario ya denunciado'
          })
    
    except User.DoesNotExist:
        return Response({
            'message': 'Usuario no encontrado'
        })

class UsersView(viewsets.ModelViewSet):
    serializer_class  = UsersSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]