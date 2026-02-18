from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Company, Candidate, CandidatePayment, CompanyPayment,
    CandidateVisaTracking, CandidateDocument, CandidateChecklist, Notification
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

class CompanyPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyPayment
        fields = "__all__"

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = "__all__"

class CandidatePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidatePayment
        fields = "__all__"

class CandidateVisaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateVisaTracking
        fields = "__all__"

class CandidateDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateDocument
        fields = ["id","candidate","doc_type","file","uploaded_at"]

class CandidateChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateChecklist
        fields = "__all__"

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
