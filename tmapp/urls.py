# from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter
from tmapp.views import TaskViewSet

# router = DefaultRouter(trailing_slash=False)
router = DefaultRouter()

app_name = "tmappapp"


router.register(
    prefix="tasks",
    viewset=TaskViewSet,
    basename="tasks",
)

urlpatterns = router.urls
