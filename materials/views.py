from rest_framework import generics, viewsets
from materials.models import Course, Lesson, Subscription
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailSerializer,
)
from users.permissions import IsModer, IsOwner
from rest_framework.permissions import IsAuthenticated
from materials.paginators import MaterialsPaginator
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from materials.tasks import send_info
from rest_framework.generics import (CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView)
from rest_framework.viewsets import ModelViewSet


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MaterialsPaginator

    def get_serializer_class(self):

        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        """Этот метод срабатывает, когда пользователь создает новый курс через API."""
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner, )
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

    def perform_update(self, serializer):
        course = serializer.save()

        emails = []
        subscriptions = Subscription.objects.filter(course=course)
        for s in subscriptions:
            emails.append(s.user.email)

        send_info.delay(course.id, emails, f'Изменен курс {course.title}')


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        """ Этот метод срабатывает, когда пользователь создает новый урок через API."""

        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = MaterialsPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)


class SubscriptionView(APIView):

    def post(self, request, course_id, *args, **kwargs):
        user = request.user  # Получаем текущего пользователя

        course_item = get_object_or_404(
            Course, id=course_id
        )  # Получаем объект курса или 404

        # Проверяем, есть ли уже подписка
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(
                user=user, course=course_item
            )  # Создаем подписку
            message = "Подписка добавлена"

        return Response({"message": message})