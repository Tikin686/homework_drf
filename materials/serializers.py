from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from materials.models import Course, Lesson, Subscription
from materials.validators import video_url_validator


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()

    def get_subscription(self, obj):
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, course=obj).exists()

    def get_lessons_count(self, course):
        return course.lessons.count()


    class Meta:
        model = Course
        fields = ("id", "title", "lessons_count")


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField(validators=[video_url_validator])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ("title", "lessons_count", "lessons")
