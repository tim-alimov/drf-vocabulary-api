from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from .models import Vocabulary
from .serializers import VocabularySerializer


class VocabularyViewSet(ModelViewSet):
    queryset = Vocabulary.objects.all()
    serializer_class = VocabularySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["cefr", "pos"]
    search_fields = ["headword"]
