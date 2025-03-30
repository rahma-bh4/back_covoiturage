from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api.models import User, Trajet
from api.serializers import TrajetSerializer

class TestAuthView(APIView):
    def post(self, request):
        """
        API pour enregistrer un utilisateur sans authentification requise.
        """
        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        clerk_user_id = request.data.get("clerk_user_id")  # Optionnel

        if not email or not first_name or not last_name:
            return Response({"error": "Tous les champs sont requis"}, status=400)

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "clerk_user_id": clerk_user_id if clerk_user_id else None,
            },
        )

        if created:
            return Response({"message": "Utilisateur créé avec succès"}, status=201)
        return Response({"message": "Utilisateur déjà existant"}, status=200)

class CreateTrajetView(APIView):
    def post(self, request):
        """
        API pour ajouter un trajet à la base de données.
        """
        serializer = TrajetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteTrajetView(APIView):
    def delete(self, request, pk):
        """
        API pour supprimer un trajet par son ID.
        """
        try:
            trajet = Trajet.objects.get(pk=pk)
            trajet.delete()
            return Response({"message": "Trajet supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
        except Trajet.DoesNotExist:
            return Response({"error": "Trajet non trouvé"}, status=status.HTTP_404_NOT_FOUND)

