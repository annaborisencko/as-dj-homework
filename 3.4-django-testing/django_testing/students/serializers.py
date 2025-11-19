from rest_framework import serializers
from django.forms import ValidationError
from django.conf import settings

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        if self.context["request"].method in ['POST', 'PUT', 'PATCH']:
            if data.get('students'):
                students_per_course_count = len(data['students'])
                if students_per_course_count > settings.MAX_STUDENTS_PER_COURSE:
                    raise ValidationError({
                        'limit_error': "Превышен лимит по студентам на курсе (не более 5)"
                    })

        return data