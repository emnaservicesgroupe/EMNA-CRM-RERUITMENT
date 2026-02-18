from django.db import models
from django.contrib.auth.models import User
from .choices import CandidateStatus, VisaStage, PaymentMethod, Currency
from .validators import validate_pdf

class Company(models.Model):
    name = models.CharField(max_length=255)
    manager_name = models.CharField(max_length=255, blank=True, default="")
    phone = models.CharField(max_length=50, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    address = models.CharField(max_length=255, blank=True, default="")
    sector = models.CharField(max_length=120, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Candidate(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=50, blank=True, default="")
    passport_number = models.CharField(max_length=80, blank=True, default="")
    national_id = models.CharField(max_length=80, blank=True, default="")  # CIN
    city = models.CharField(max_length=120, blank=True, default="")

    assigned_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name="candidates")

    contract_price = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    total_paid = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    remaining_balance = models.DecimalField(max_digits=12, decimal_places=3, default=0)

    status = models.CharField(max_length=30, choices=CandidateStatus.choices, default=CandidateStatus.PENDING)
    visa_result = models.CharField(max_length=30, blank=True, default="")  # Approved/Rejected/Pending text
    application_date = models.DateField(null=True, blank=True)

    programari_date = models.DateField(null=True, blank=True)
    avis_date = models.DateField(null=True, blank=True)
    embassy_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def recompute_balances(self):
        self.remaining_balance = (self.contract_price or 0) - (self.total_paid or 0)

    def save(self, *args, **kwargs):
        self.recompute_balances()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class CandidateVisaTracking(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="visa_tracks")
    stage = models.CharField(max_length=30, choices=VisaStage.choices, default=VisaStage.REGISTRATION)
    status = models.CharField(max_length=60, blank=True, default="")  # In progress / completed / issue
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")
    document_url = models.URLField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

class CandidatePayment(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="payments")
    installment_number = models.PositiveIntegerField(default=1)
    amount = models.DecimalField(max_digits=12, decimal_places=3)
    due_date = models.DateField(null=True, blank=True)
    paid_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    currency = models.CharField(max_length=10, choices=Currency.choices, default=Currency.TND)
    receipt_url = models.URLField(blank=True, default="")
    notes = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

class CompanyPayment(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="payments")
    total_purchased = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    down_payment = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    remaining = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    due_date = models.DateField(null=True, blank=True)

    payment_date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    currency = models.CharField(max_length=10, choices=Currency.choices, default=Currency.TND)
    method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    receipt_url = models.URLField(blank=True, default="")
    notes = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.remaining = (self.total_purchased or 0) - (self.down_payment or 0)
        super().save(*args, **kwargs)

class CandidateDocument(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="documents")
    doc_type = models.CharField(max_length=60)  # passport, cin, birth, driving, b3, photos_pdf
    file = models.FileField(upload_to="candidate_docs/", validators=[validate_pdf])
    uploaded_at = models.DateTimeField(auto_now_add=True)

class CandidateChecklist(models.Model):
    candidate = models.OneToOneField(Candidate, on_delete=models.CASCADE, related_name="checklist")
    passport_ok = models.BooleanField(default=False)
    cin_ok = models.BooleanField(default=False)
    birth_ok = models.BooleanField(default=False)
    driving_ok = models.BooleanField(default=False)
    b3_ok = models.BooleanField(default=False)
    photos_ok = models.BooleanField(default=False)

    missing_text = models.CharField(max_length=255, blank=True, default="")

    def recompute_missing(self):
        missing = []
        if not self.passport_ok: missing.append("Passport")
        if not self.cin_ok: missing.append("CIN")
        if not self.birth_ok: missing.append("Birth Certificate")
        if not self.driving_ok: missing.append("Driving License")
        if not self.b3_ok: missing.append("B3")
        if not self.photos_ok: missing.append("Photos (PDF)")
        self.missing_text = ", ".join(missing)

    def save(self, *args, **kwargs):
        self.recompute_missing()
        super().save(*args, **kwargs)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)  # internal/email/sms/whatsapp
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
