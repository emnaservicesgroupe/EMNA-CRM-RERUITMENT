from django.core.exceptions import ValidationError

def validate_pdf(file_obj):
    name = (file_obj.name or "").lower()
    if not name.endswith(".pdf"):
        raise ValidationError("PDF only.")
