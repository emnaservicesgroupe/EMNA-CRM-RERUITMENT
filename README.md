# EMNA Recruitment System (Starter CRM) — Arabic + English

This is a **ready-to-run starter** for a private CRM:
- Companies module (TND, Cash)
- Candidates module with Visa tracking
- Installments & Payments
- PDF-only document upload (Passport / CIN / Birth Certificate / Driving License / B3 / Photos as PDF)
- Role-based access (Admin, Accountant, Receptionist, Commercial Agent, Candidate, Company)
- REST API (Django + DRF)
- PostgreSQL via Docker

> Note: This is a starter you can extend to full production (UI portals, WhatsApp, etc.).
> It already includes the **database, endpoints, auth, uploads, and dashboards endpoints**.

---

## 1) Quick Start (Docker)
1. Install Docker + Docker Compose
2. From this folder:
```bash
docker compose up --build
```
3. Create admin user:
```bash
docker compose exec backend python manage.py createsuperuser
```
4. Open:
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

---

## 2) Tech
- Django + Django REST Framework
- SimpleJWT (token login)
- PostgreSQL
- Media storage for uploaded PDFs
- CORS enabled (for a future React/Next frontend)

---

## 3) Core Endpoints
- Auth:
  - POST /api/auth/login/  (email + password -> access/refresh tokens)
- Companies:
  - /api/companies/
  - /api/companies/{id}/payments/
  - /api/companies/{id}/candidates/
- Candidates:
  - /api/candidates/
  - /api/candidates/{id}/documents/
  - /api/candidates/{id}/visa/
  - /api/candidates/{id}/payments/
- Dashboard:
  - GET /api/dashboard/summary/

---

## 4) Currency & Method Defaults
- Currency: **TND**
- Method: **Cash**
(You can add EUR later if you want.)

---

## 5) PDF Only Upload Rule
Documents accept **PDF only** by default. Edit `core/validators.py` if you want JPG/PNG.

---

## 6) Next Enhancements (optional)
- Portals UI (Admin / Candidate / Company) in React or Next.js
- WhatsApp notifications (Meta WhatsApp Cloud API)
- Automated reminders (B3 expiry, embassy)
- PDF/Excel reports generation
