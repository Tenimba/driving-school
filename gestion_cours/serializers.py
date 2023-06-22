from rest_framework import serializers, viewsets
from .models import Inspecteur

class InspecteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspecteur
        fields = '__all__'

class EleveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspecteur
        fields = '__all__'

class CoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspecteur
        fields = '__all__'

class SecretaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspecteur
        fields = '__all__'

class InspecteurViewSet(viewsets.ModelViewSet):
    queryset = Inspecteur.objects.all()
    serializer_class = InspecteurSerializer

class ElevesViewSet(viewsets.ModelViewSet):
    queryset = Inspecteur.objects.all()
    serializer_class = InspecteurSerializer

class RendezVousViewSet(viewsets.ModelViewSet):
    queryset = Inspecteur.objects.all()
    serializer_class = InspecteurSerializer

class HeurePayeeViewSet(viewsets.ModelViewSet):
    queryset = Inspecteur.objects.all()
    serializer_class = InspecteurSerializer