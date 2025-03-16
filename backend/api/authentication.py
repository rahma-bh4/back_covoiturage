from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
import requests
from django.conf import settings

from django.contrib.auth.models import AnonymousUser

class ClerkUser:
    """A simple user-like object for Django authentication"""
    def __init__(self, decoded_token):
        self.id = decoded_token.get("sub")  # Clerk User ID
        self.email = decoded_token.get("email", "")
        self.decoded_token = decoded_token
        self.is_authenticated = True  # ✅ Required for DRF authentication

    def __str__(self):
        return f"ClerkUser(id={self.id}, email={self.email})"

class ClerkJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        try:
            # Fetch JWKS
            jwks_url = f'https://{settings.CLERK_DOMAIN}/.well-known/jwks.json'
            response = requests.get(jwks_url)
            response.raise_for_status()
            jwks = response.json()

            # Get public key
            header = jwt.get_unverified_header(token)
            kid = header.get('kid')
            public_key = next((key for key in jwks['keys'] if key['kid'] == kid), None)
            if not public_key:
                raise AuthenticationFailed('Invalid token: kid not found')

            pem_key = jwt.algorithms.RSAAlgorithm.from_jwk(public_key)

            # Decode token
            decoded = jwt.decode(
                token,
                pem_key,
                algorithms=['RS256'],
                issuer=f'https://{settings.CLERK_DOMAIN}',
                options={'verify_exp': True}
            )

            # ✅ Return a user-like object instead of a dictionary
            return (ClerkUser(decoded), None)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Invalid token: Token has expired')
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')
    
