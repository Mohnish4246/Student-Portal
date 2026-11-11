from rest_framework import serializers
from students.models import Student

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student

        fields = [
            "id",
            "name",
            "age",
            "email",
            "phone",
            "marks",
            "city",
            "course",
            "skills",
        ]

        read_only_fields = ["id"]

# json > serializer > django models