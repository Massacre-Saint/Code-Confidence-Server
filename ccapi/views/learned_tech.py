"""Module sets up Django Viewset for the class of LearnedTech"""
from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ccapi.models import Tech, User, LearnedTech

class LearnedTechView(ViewSet):
    """Class creates viewset for LeanredTech"""
    def retrieve(self, request, pk):
        """Get method retrieves single LearnedTech instance"""
        try:
            learned_tech = LearnedTech.objects.get(pk=pk)
            serializer = LearnedTechSerializer(learned_tech)

            return Response(serializer.data)

        except LearnedTech.DoesNotExist as ex:

            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Get method lists all LearnedTech instances"""
        uid = request.META['HTTP_AUTHORIZATION']

        learned_tech = LearnedTech.objects.all()
        last_updated_tech = learned_tech.filter(uid__uid = uid).order_by('-last_updated')
        serializer = LearnedTechSerializer(last_updated_tech, many=True)

        return Response(serializer.data)

    def create(self, request):
        """Post Method creates an instance of LearnedTech"""
        payload = request.data
        uid = request.META['HTTP_AUTHORIZATION']
        user = User.objects.get(uid=uid)
        tech = Tech.objects.get(pk=payload['tech'])

        learned_tech = LearnedTech.objects.create(
          uid = user,
          tech = tech,
          last_updated = date.today()
        )

        serializer = LearnedTechSerializer(learned_tech)
        return Response(serializer.data)

class LearnedTechSerializer(serializers.ModelSerializer):
    """Class creates the serializer for LearnedTech class"""

    class Meta:
        depth = 1
        model = LearnedTech
        fields = (
          'uid',
          'tech',
          'last_updated'
        )
