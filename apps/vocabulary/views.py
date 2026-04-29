from rest_framework.viewsets import ModelViewSet

from .models import Vocabulary
from .serializers import VocabularySerializer


class VocabularyViewSet(ModelViewSet):
    queryset = Vocabulary.objects.all()
    serializer_class = VocabularySerializer
