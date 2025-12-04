from rest_framework import serializers
from .models import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"

class UpdateSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['score', 'status', 'exec_time_ms', 'test_results']