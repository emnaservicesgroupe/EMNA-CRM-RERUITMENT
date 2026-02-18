from django.db import models

class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    ACCOUNTANT = "accountant", "Accountant"
    RECEPTIONIST = "receptionist", "Receptionist"
    COMMERCIAL = "commercial", "Commercial Agent"
    CANDIDATE = "candidate", "Candidate"
    COMPANY = "company", "Company"

class CandidateStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    UNDER_PROCESS = "under_process", "Under Process"
    EMBASSY = "embassy", "Embassy"
    VISA_APPROVED = "visa_approved", "Visa Approved"
    VISA_REJECTED = "visa_rejected", "Visa Rejected"
    COMPLETED = "completed", "Completed"

class VisaStage(models.TextChoices):
    REGISTRATION = "registration", "Registration"
    DOCS_CHECK = "docs_check", "Docs Check"
    PROGRAMARI = "programari", "Programari"
    AVIS = "avis", "Avis"
    EMBASSY = "embassy", "Embassy"
    VISA = "visa", "Visa"
    TRAVEL = "travel", "Travel"

class PaymentMethod(models.TextChoices):
    CASH = "cash", "Cash"

class Currency(models.TextChoices):
    TND = "tnd", "TND"
    EUR = "eur", "EUR"
