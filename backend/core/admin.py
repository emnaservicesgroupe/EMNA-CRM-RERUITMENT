from django.contrib import admin
from .models import Company, Candidate, CandidatePayment, CompanyPayment, CandidateVisaTracking, CandidateDocument, CandidateChecklist, Notification

admin.site.register(Company)
admin.site.register(Candidate)
admin.site.register(CandidatePayment)
admin.site.register(CompanyPayment)
admin.site.register(CandidateVisaTracking)
admin.site.register(CandidateDocument)
admin.site.register(CandidateChecklist)
admin.site.register(Notification)
