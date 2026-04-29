from rest_framework.routers import DefaultRouter
from .views import VocabularyViewSet

router = DefaultRouter()
router.register("vocabulary", VocabularyViewSet, basename="vocabulary")

urlpatterns = router.urls
