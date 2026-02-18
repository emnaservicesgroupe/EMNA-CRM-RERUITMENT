from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Sum
from .models import (
    Company, Candidate, CandidatePayment, CompanyPayment,
    CandidateVisaTracking, CandidateDocument, CandidateChecklist
)
from .serializers import (
    CompanySerializer, CandidateSerializer,
    CandidatePaymentSerializer, CompanyPaymentSerializer,
    CandidateVisaSerializer, CandidateDocumentSerializer, CandidateChecklistSerializer
)

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by("-created_at")
    serializer_class = CompanySerializer

    @action(detail=True, methods=["get"])
    def payments(self, request, pk=None):
        company = self.get_object()
        qs = company.payments.all().order_by("-created_at")
        return Response(CompanyPaymentSerializer(qs, many=True).data)

    @action(detail=True, methods=["get"])
    def candidates(self, request, pk=None):
        company = self.get_object()
        qs = company.candidates.all().order_by("-created_at")
        return Response(CandidateSerializer(qs, many=True).data)

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all().order_by("-created_at")
    serializer_class = CandidateSerializer

    @action(detail=True, methods=["get","post"])
    def payments(self, request, pk=None):
        cand = self.get_object()
        if request.method == "POST":
            ser = CandidatePaymentSerializer(data=request.data)
            ser.is_valid(raise_exception=True)
            ser.save()
            # recompute totals
            total = cand.payments.aggregate(s=Sum("amount"))["s"] or 0
            cand.total_paid = total
            cand.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(CandidatePaymentSerializer(cand.payments.all().order_by("installment_number"), many=True).data)

    @action(detail=True, methods=["get","post"])
    def visa(self, request, pk=None):
        cand = self.get_object()
        if request.method == "POST":
            ser = CandidateVisaSerializer(data=request.data)
            ser.is_valid(raise_exception=True)
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(CandidateVisaSerializer(cand.visa_tracks.all().order_by("-created_at"), many=True).data)

    @action(detail=True, methods=["get","post"])
    def documents(self, request, pk=None):
        cand = self.get_object()
        if request.method == "POST":
            # multipart/form-data
            data = request.data.copy()
            data["candidate"] = cand.id
            ser = CandidateDocumentSerializer(data=data)
            ser.is_valid(raise_exception=True)
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(CandidateDocumentSerializer(cand.documents.all().order_by("-uploaded_at"), many=True).data)

    @action(detail=True, methods=["get","post"])
    def checklist(self, request, pk=None):
        cand = self.get_object()
        obj, _ = CandidateChecklist.objects.get_or_create(candidate=cand)
        if request.method == "POST":
            ser = CandidateChecklistSerializer(obj, data=request.data, partial=True)
            ser.is_valid(raise_exception=True)
            ser.save()
            return Response(ser.data)
        return Response(CandidateChecklistSerializer(obj).data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    total_candidates = Candidate.objects.count()
    in_embassy = Candidate.objects.filter(status="embassy").count()
    approved = Candidate.objects.filter(status="visa_approved").count()
    rejected = Candidate.objects.filter(status="visa_rejected").count()
    under_process = Candidate.objects.filter(status="under_process").count()

    paid_total = Candidate.objects.aggregate(s=Sum("total_paid"))["s"] or 0
    remaining_total = Candidate.objects.aggregate(s=Sum("remaining_balance"))["s"] or 0

    companies = Company.objects.count()

    return Response({
        "companies": companies,
        "total_candidates": total_candidates,
        "under_process": under_process,
        "in_embassy": in_embassy,
        "visa_approved": approved,
        "visa_rejected": rejected,
        "total_paid_tnd": float(paid_total),
        "total_remaining_tnd": float(remaining_total),
    })
