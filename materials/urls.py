from rest_framework.routers import SimpleRouter
from materials.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, LessonDestroyAPIView
from materials.apps import MaterialsConfig
from django.urls import path

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lesson/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path("lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson_delete")
] + router.urls