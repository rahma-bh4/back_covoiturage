from django.db import IntegrityError
from django.shortcuts import render

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from api.models import User
from .authentication import ClerkJWTAuthentication
from rest_framework.permissions import IsAuthenticated
# from .serializers import TestSerializer  # Uncomment if using serializer

class TestAuthView(APIView):
    authentication_classes = [ClerkJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user  # Clerk user_id from JWT
        email = request.data.get('email')  # Récupéré depuis le frontend
        first_name = request.data.get('first_name')  # Récupéré depuis le frontend

        try:
            user, created = User.objects.get_or_create(
                clerk_user_id=user_id,
                defaults={'email': email, 'first_name': first_name}
            )
        except IntegrityError:
            return Response({'error': 'Erreur lors de la création de l\'utilisateur'}, status=500)

        return Response({
            'message': 'Authentification réussie',
            'user_id': user_id,
            'created': created,
            'email': user.email,
            'first_name': user.first_name
        }, status=status.HTTP_200_OK)