import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class ClerkJWTAuthentication(BaseAuthentication):
  def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')
        print("Auth Header:", auth_header)  # Debug: Vérifier le header reçu

        if not auth_header.startswith('Bearer '):
            print("No Bearer token found")
            return None

        token = auth_header.split(' ')[1]
        print("Token:", token)  # Debug: Voir le JWT

        try:
            decoded = jwt.decode(token, settings.CLERK_SECRET_KEY, algorithms=['HS256'])
            print("Decoded JWT:", decoded)  # Debug: Vérifier le contenu décodé
            user_id = decoded['sub']
            print("User ID:", user_id)  # Debug: Vérifier l'ID utilisateur
            return (user_id, None)  # Retourne user_id comme request.user
        except jwt.InvalidTokenError as e:
            print("JWT Error:", str(e))  # Debug: Voir l'erreur spécifique
            raise AuthenticationFailed('Token invalide ou expiré')
        except Exception as e:
            print("Unexpected Error:", str(e))
            raise AuthenticationFailed('Erreur d\'authentification')