from rest_framework.response import Response
from rest_framework.views import APIView
import jwt
import requests
from rest_framework.permissions import IsAuthenticated
from api.models import User

class TestAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Fetch JWKS from Clerk
        jwks_url = 'https://fun-grub-51.clerk.accounts.dev/.well-known/jwks.json'
        jwks = requests.get(jwks_url).json()

        # Extract the token from the Authorization header
        token = request.headers.get('Authorization').split(' ')[1]

        # Function to get public key from JWK
        def get_public_key_from_jwk(jwks, kid):
            for key in jwks['keys']:
                if key['kid'] == kid:
                    return jwt.algorithms.RSAAlgorithm.from_jwk(key)

        # Decode JWT and extract Clerk user ID
        try:
            unverified_header = jwt.get_unverified_header(token)
            if unverified_header is None:
                return Response({"error": "Token does not have a valid header"}, status=400)

            kid = unverified_header['kid']
            public_key = get_public_key_from_jwk(jwks, kid)

            decoded_token = jwt.decode(token, public_key, algorithms=["RS256"])
            clerk_user_id = decoded_token.get('sub')  # Clerk's user ID from the decoded token

            if not clerk_user_id:
                return Response({"error": "Failed to retrieve Clerk user ID"}, status=400)

            print("Clerk User ID:", clerk_user_id)
            
            # Save the user to the database (make sure 'clerk_user_id' field exists in User model)
            user = User.objects.create(
                email=request.data.get('email'),
                first_name=request.data.get('first_name'),
                last_name=request.data.get('last_name'),
                clerk_user_id=clerk_user_id  # Ensure Clerk's user ID is saved
            )

            return Response({"message": "User saved successfully"}, status=201)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=401)
        except Exception as e:
            return Response({"error": f"Error: {str(e)}"}, status=500)
