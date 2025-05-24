from django.urls import include, path
from rest_framework.routers import SimpleRouter

from habits.apps import HabitsConfig
from habits.views import HabitsViewSet

app_name = HabitsConfig.name

router = SimpleRouter()
router.register("", HabitsViewSet, basename="habit")


urlpatterns = [
    path("", include(router.urls)),
]
