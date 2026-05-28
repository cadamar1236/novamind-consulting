import os
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, Boolean
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import random

DATABASE_URL = os.environ.get("DATABASE_URL", "")
COMPANY_SLUG = os.environ.get("COMPANY_SLUG", "nova_consulting")
db_engine = None
SessionLocal = None

class Base(DeclarativeBase):
    pass

if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    db_engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(bind=db_engine)

PORT = int(os.environ.get("COMPANY_PORT", 8000))

app = FastAPI(title="NovaMind Insights", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define Models
class Contact(Base):
    __tablename__ = f"{COMPANY_SLUG}_contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50))
    company_id = Column(Integer, nullable=False)
    position = Column(String(255))
    industry = Column(String(255))
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

class Deal(Base):
    __tablename__ = f"{COMPANY_SLUG}_deals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    value = Column(Float, nullable=False)
    stage = Column(String(100), nullable=False)
    company_id = Column(Integer, nullable=False)
    contact_id = Column(Integer, nullable=False)
    probability = Column(Integer, default=50)
    expected_close_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class Company(Base):
    __tablename__ = f"{COMPANY_SLUG}_companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    industry = Column(String(255))
    size = Column(String(100))
    revenue = Column(Float)
    location = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class Interaction(Base):
    __tablename__ = f"{COMPANY_SLUG}_interactions"
    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, nullable=False)
    deal_id = Column(Integer)
    type = Column(String(100), nullable=False)
    notes = Column(Text)
    outcome = Column(String(255))
    date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class Report(Base):
    __tablename__ = f"{COMPANY_SLUG}_reports"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)
    data = Column(Text)
    generated_for = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables on startup
if db_engine:
    Base.metadata.create_all(bind=db_engine)

# Pydantic models
class ContactCreate(BaseModel):
    name: str
    email: str
    phone: str = ""
    company_id: int = 0
    position: str = ""
    industry: str = ""
    status: str = "active"

class DealCreate(BaseModel):
    name: str
    value: float
    stage: str
    company_id: int
    contact_id: int
    probability: int = 50
    expected_close_date: str = ""

class InteractionCreate(BaseModel):
    contact_id: int
    deal_id: int = 0
    type: str
    notes: str = ""
    outcome: str = ""

class ReportCreate(BaseModel):
    name: str
    type: str
    data: str = ""
    generated_for: str = ""

# Mock Data
MOCK_CONTACTS = [
    {"id": 1, "name": "Sarah Johnson", "email": "sarah.j@acmecorp.com", "phone": "+1-555-0101", "company_id": 1, "position": "VP of Strategy", "industry": "Technology", "status": "active", "created_at": "2024-11-15T10:00:00Z"},
    {"id": 2, "name": "Michael Chen", "email": "m.chen@globaltech.com", "phone": "+1-555-0102", "company_id": 2, "position": "CEO", "industry": "Technology", "status": "active", "created_at": "2024-11-20T14:30:00Z"},
    {"id": 3, "name": "Emily Rodriguez", "email": "emily.r@financecorp.com", "phone": "+1-555-0103", "company_id": 3, "position": "Director of Analytics", "industry": "Finance", "status": "active", "created_at": "2024-12-01T09:15:00Z"},
    {"id": 4, "name": "James Wilson", "email": "j.wilson@retailmax.com", "phone": "+1-555-0104", "company_id": 4, "position": "COO", "industry": "Retail", "status": "active", "created_at": "2024-12-05T11:45:00Z"},
    {"id": 5, "name": "Lisa Thompson", "email": "lisa.t@healthfirst.com", "phone": "+1-555-0105", "company_id": 5, "position": "Chief Medical Officer", "industry": "Healthcare", "status": "active", "created_at": "2024-12-10T16:00:00Z"},
    {"id": 6, "name": "David Park", "email": "d.park@energysolutions.com", "phone": "+1-555-0106", "company_id": 6, "position": "VP Business Development", "industry": "Energy", "status": "active", "created_at": "2024-12-15T08:30:00Z"},
    {"id": 7, "name": "Anna Martinez", "email": "anna.m@manufacturing.com", "phone": "+1-555-0107", "company_id": 7, "position": "Supply Chain Director", "industry": "Manufacturing", "status": "active", "created_at": "2025-01-05T13:00:00Z"},
    {"id": 8, "name": "Robert Kim", "email": "r.kim@datasystems.com", "phone": "+1-555-0108", "company_id": 8, "position": "CTO", "industry": "Technology", "status": "active", "created_at": "2025-01-10T10:45:00Z"},
]

MOCK_DEALS = [
    {"id": 1, "name": "Enterprise AI Strategy", "value": 250000.0, "stage": "Negotiation", "company_id": 1, "contact_id": 1, "probability": 85, "expected_close_date": "2025-03-15T00:00:00Z", "created_at": "2025-01-10T09:00:00Z"},
    {"id": 2, "name": "Market Entry Analysis - APAC", "value": 180000.0, "stage": "Proposal", "company_id": 2, "contact_id": 2, "probability": 70, "expected_close_date": "2025-04-01T00:00:00Z", "created_at": "2025-01-15T11:30:00Z"},
    {"id": 3, "name": "Digital Transformation Roadmap", "value": 320000.0, "stage": "Discovery", "company_id": 3, "contact_id": 3, "probability": 60, "expected_close_date": "2025-05-01T00:00:00Z", "created_at": "2025-01-20T14:00:00Z"},
    {"id": 4, "name": "Data Analytics Framework", "value": 195000.0, "stage": "Qualification", "company_id": 4, "contact_id": 4, "probability": 45, "expected_close_date": "2025-06-01T00:00:00Z", "created_at": "2025-02-01T10:00:00Z"},
    {"id": 5, "name": "Operational Efficiency Audit", "value": 150000.0, "stage": "Closed Won", "company_id": 5, "contact_id": 5, "probability": 100, "expected_close_date": "2025-02-28T00:00:00Z", "created_at": "2024-12-20T08:30:00Z"},
    {"id": 6, "name": "Sustainability Strategy", "value": 275000.0, "stage": "Negotiation", "company_id": 6, "contact_id": 6, "probability": 80, "expected_close_date": "2025-03-30T00:00:00Z", "created_at": "2025-01-25T16:15:00Z"},
    {"id": 7, "name": "Supply Chain Optimization", "value": 210000.0, "stage": "Proposal", "company_id": 7, "contact_id": 7, "probability": 65, "expected_close_date": "2025-04-15T00:00:00Z", "created_at": "2025-02-05T12:00:00Z"},
    {"id": 8, "name": "AI Implementation Program", "value": 450000.0, "stage": "Discovery", "company_id": 8, "contact_id": 8, "probability": 55, "expected_close_date": "2025-05-15T00:00:00Z", "created_at": "2025-02-10T09:45:00Z"},
]

MOCK_COMPANIES = [
    {"id": 1, "name": "Acme Corporation", "industry": "Technology", "size": "5000+", "revenue": 5000000000.0, "location": "San Francisco, CA", "created_at": "2024-01-01T00:00:00Z"},
    {"id": 2, "name": "GlobalTech Solutions", "industry": "Technology", "size": "1000-5000", "revenue": 1200000000.0, "location": "New York, NY", "created_at": "2024-01-05T00:00:00Z"},
    {"id": 3, "name": "FinanceCorp International", "industry": "Finance", "size": "1000-5000", "revenue": 2500000000.0, "location": "Chicago, IL", "created_at": "2024-01-10T00:00:00Z"},
    {"id": 4, "name": "RetailMax Group", "industry": "Retail", "size": "5000+", "revenue": 8000000000.0, "location": "Los Angeles, CA", "created_at": "2024-01-15T00:00:00Z"},
    {"id": 5, "name": "HealthFirst Medical", "industry": "Healthcare", "size": "1000-5000", "revenue": 3500000000.0, "location": "Boston, MA", "created_at": "2024-01-20T00:00:00Z"},
    {"id": 6, "name": "Energy Solutions Inc.", "industry": "Energy", "size": "500-1000", "revenue": 800000000.0, "location": "Houston, TX", "created_at": "2024-02-01T00:00:00Z"},
    {"id": 7, "name": "ManufacturingCo", "industry": "Manufacturing", "size": "5000+", "revenue": 4000000000.0, "location": "Detroit, MI", "created_at": "2024-02-05T00:00:00Z"},
    {"id": 8, "name": "DataSystems Corp", "industry": "Technology", "size": "500-1000", "revenue": 600000000.0, "location": "Seattle, WA", "created_at": "2024-02-10T00:00:00Z"},
]

MOCK_INTERACTIONS = [
    {"id": 1, "contact_id": 1, "deal_id": 1, "type": "Meeting", "notes": "Discussed AI strategy implementation timeline and resource requirements", "outcome": "Positive - moving to next phase", "date": "2025-01-15T10:00:00Z", "created_at": "2025-01-15T10:00:00Z"},
    {"id": 2, "contact_id": 2, "deal_id": 2, "type": "Call", "notes": "Reviewed market entry proposal for Southeast Asian markets", "outcome": "Interested - requested additional data", "date": "2025-01-20T14:30:00Z", "created_at": "2025-01-20T14:30:00Z"},
    {"id": 3, "contact_id": 3, "deal_id": 3, "type": "Email", "notes": "Sent digital transformation case studies and ROI projections", "outcome": "Engaged - scheduling follow-up", "date": "2025-01-25T09:15:00Z", "created_at": "2025-01-25T09:15:00Z"},
    {"id": 4, "contact_id": 4, "deal_id": 4, "type": "Meeting", "notes": "Presented data analytics framework proposal to executive team", "outcome": "Positive - legal review pending", "date": "2025-02-05T11:00:00Z", "created_at": "2025-02-05T11:00:00Z"},
    {"id": 5, "contact_id": 5, "deal_id": 5, "type": "Call", "notes": "Finalized operational efficiency audit contract details", "outcome": "Closed - contract signed", "date": "2025-02-10T16:00:00Z", "created_at": "2025-02-10T16:00:00Z"},
    {"id": 6, "contact_id": 6, "deal_id": 6, "type": "Meeting", "notes": "Workshop on sustainability metrics and reporting standards", "outcome": "Productive - defined scope", "date": "2025-02-15T13:30:00Z", "created_at": "2025-02-15T13:30:00Z"},
]

MOCK_REPORTS = [
    {"id": 1, "name": "Q1 2025 Pipeline Analysis", "type": "Pipeline", "data": "{\"total_deals\": 24, "total_value\": 4500000, "win_rate\": 0.72}", "generated_for": "Executive Team", "created_at": "2024-12-01T08:00:00Z"},
    {"id": 2, "name": "Monthly Contact Engagement", "type": "Engagement", "data": "{\"total_contacts\": 156, "active_contacts": 89, "interaction_rate\": 0.65}", "generated_for": "Sales Team", "created_at": "2025-01-01T08:00:00Z"},
    {"id": 3, "name": "Deal Stage Distribution", "type": "Deal Health", "data": "{\"discovery\": 5, "qualification\": 4, "proposal\": 3, "negotiation\": 2, "closed_won\": 1}", "generated_for": "Management", "created_at": "2025-01-15T10:00:00Z"},
    {"id": 4, "name": "Industry Sector Insights", "type": "Industry Analysis", "data": "{\"technology\": 0.35, "finance\": 0.20, "healthcare\": 0.15, "retail\": 0.12, "energy\": 0.10, "manufacturing\": 0.08}", "generated_for": "Strategy Team", "created_at": "2025-02-01T09:00:00Z"},
    {"id": 5, "name": "Revenue Forecast Q2 2025", "type": "Forecast", "data": "{\"expected_revenue\": 3250000, "confidence_high\": 0.85, "confidence_low\": 0.60}", "generated_for": "Board of Directors", "created_at": "2025-02-15T14:00:00Z"},
]

# Helpers
def get_db():
    if SessionLocal:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        yield None

# Core Endpoints
@app.get("/health")
def health_check():
    return {"status": "ok", "app": "NovaMind Insights", "version": "1.0.0"}

@app.get("/api/info")
def get_info():
    return {
        "name": "NovaMind Consulting",
        "app_name": "NovaMind Insights",
        "tagline": "Transforming data into strategy for Fortune 500 leaders",
        "founded": "2020",
        "team_size": 85,
        "industry_focus": ["Technology", "Finance", "Healthcare", "Energy", "Retail", "Manufacturing"],
        "headquarters": "New York, NY",
        "certifications": ["ISO 27001", "GDPR Compliant", "SOC 2 Type II"]
    }

@app.get("/api/metrics")
def get_metrics():
    return {
        "active_deals": 18,
        "pipeline_value": 4500000.0,
        "won_revenue_ytd": 2150000.0,
        "average_deal_size": 250000.0,
        "win_rate_percent": 68,
        "contacts_in_pipeline": 156,
        "conversion_rate_percent": 22,
        "interaction_rate_per_week": 37,
        "total_revenue_target": 8000000.0,
        "quarterly_progress_percent": 52
    }

# Domain-specific endpoints for CRM

# Contacts
@app.get("/api/contacts")
def get_contacts():
    if SessionLocal:
        db = SessionLocal()
        contacts = db.query(Contact).all()
        db.close()
        return [{"id": c.id, "name": c.name, "email": c.email, "phone": c.phone, "company_id": c.company_id, "position": c.position, "industry": c.industry, "status": c.status, "created_at": c.created_at.isoformat()} for c in contacts]
    return MOCK_CONTACTS

@app.post("/api/contacts")
def create_contact(contact: ContactCreate):
    if SessionLocal:
        db = SessionLocal()
        new_contact = Contact(name=contact.name, email=contact.email, phone=contact.phone, company_id=contact.company_id, position=contact.position, industry=contact.industry, status=contact.status)
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        db.close()
        return {"id": new_contact.id, "name": new_contact.name, "email": new_contact.email, "phone": new_contact.phone, "company_id": new_contact.company_id, "position": new_contact.position, "industry": new_contact.industry, "status": new_contact.status, "created_at": new_contact.created_at.isoformat()}
    new_id = max(c["id"] for c in MOCK_CONTACTS) + 1
    new_entry = {"id": new_id, **contact.dict(), "created_at": datetime.utcnow().isoformat() + "Z"}
    MOCK_CONTACTS.append(new_entry)
    return new_entry

# Deals
@app.get("/api/deals")
def get_deals():
    if SessionLocal:
        db = SessionLocal()
        deals = db.query(Deal).all()
        db.close()
        return [{"id": d.id, "name": d.name, "value": d.value, "stage": d.stage, "company_id": d.company_id, "contact_id": d.contact_id, "probability": d.probability, "expected_close_date": d.expected_close_date.isoformat() if d.expected_close_date else "", "created_at": d.created_at.isoformat()} for d in deals]
    return MOCK_DEALS

@app.post("/api/deals")
def create_deal(deal: DealCreate):
    if SessionLocal:
        db = SessionLocal()
        new_deal = Deal(name=deal.name, value=deal.value, stage=deal.stage, company_id=deal.company_id, contact_id=deal.contact_id, probability=deal.probability)
        if deal.expected_close_date:
            new_deal.expected_close_date = datetime.fromisoformat(deal.expected_close_date.replace("Z", "+00:00"))
        db.add(new_deal)
        db.commit()
        db.refresh(new_deal)
        db.close()
        return {"id": new_deal.id, "name": new_deal.name, "value": new_deal.value, "stage": new_deal.stage, "company_id": new_deal.company_id, "contact_id": new_deal.contact_id, "probability": new_deal.probability, "expected_close_date": new_deal.expected_close_date.isoformat() if new_deal.expected_close_date else "", "created_at": new_deal.created_at.isoformat()}
    new_id = max(d["id"] for d in MOCK_DEALS) + 1
    new_entry = {"id": new_id, **deal.dict(), "created_at": datetime.utcnow().isoformat() + "Z"}
    MOCK_DEALS.append(new_entry)
    return new_entry

# Pipeline
@app.get("/api/pipeline")
def get_pipeline():
    stages = ["Discovery", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]
    pipeline_data = {}
    for stage in stages:
        if SessionLocal:
            db = SessionLocal()
            stage_deals = db.query(Deal).filter(Deal.stage == stage).all()
            db.close()
        else:
            stage_deals = [d for d in MOCK_DEALS if d["stage"] == stage]
        pipeline_data[stage] = {
            "count": len(stage_deals),
            "total_value": sum(d["value"] if isinstance(d, dict) else d.value for d in stage_deals)
        }
    return pipeline_data

# Interactions
@app.get("/api/interactions")
def get_interactions():
    if SessionLocal:
        db = SessionLocal()
        interactions = db.query(Interaction).all()
        db.close()
        return [{"id": i.id, "contact_id": i.contact_id, "deal_id": i.deal_id, "type": i.type, "notes": i.notes, "outcome": i.outcome, "date": i.date.isoformat(), "created_at": i.created_at.isoformat()} for i in interactions]
    return MOCK_INTERACTIONS

@app.post("/api/interactions")
def create_interaction(interaction: InteractionCreate):
    if SessionLocal:
        db = SessionLocal()
        new_interaction = Interaction(contact_id=interaction.contact_id, deal_id=interaction.deal_id, type=interaction.type, notes=interaction.notes, outcome=interaction.outcome)
        db.add(new_interaction)
        db.commit()
        db.refresh(new_interaction)
        db.close()
        return {"id": new_interaction.id, "contact_id": new_interaction.contact_id, "deal_id": new_interaction.deal_id, "type": new_interaction.type, "notes": new_interaction.notes, "outcome": new_interaction.outcome, "date": new_interaction.date.isoformat(), "created_at": new_interaction.created_at.isoformat()}
    new_id = max(i["id"] for i in MOCK_INTERACTIONS) + 1
    new_entry = {"id": new_id, **interaction.dict(), "date": datetime.utcnow().isoformat() + "Z", "created_at": datetime.utcnow().isoformat() + "Z"}
    MOCK_INTERACTIONS.append(new_entry)
    return new_entry

# Companies
@app.get("/api/companies")
def get_companies():
    if SessionLocal:
        db = SessionLocal()
        companies = db.query(Company).all()
        db.close()
        return [{"id": c.id, "name": c.name, "industry": c.industry, "size": c.size, "revenue": c.revenue, "location": c.location, "created_at": c.created_at.isoformat()} for c in companies]
    return MOCK_COMPANIES

# Reports
@app.get("/api/reports")
def get_reports():
    if SessionLocal:
        db = SessionLocal()
        reports = db.query(Report).all()
        db.close()
        return [{"id": r.id, "name": r.name, "type": r.type, "data": r.data, "generated_for": r.generated_for, "created_at": r.created_at.isoformat()} for r in reports]
    return MOCK_REPORTS

@app.post("/api/reports")
def create_report(report: ReportCreate):
    if SessionLocal:
        db = SessionLocal()
        new_report = Report(name=report.name, type=report.type, data=report.data, generated_for=report.generated_for)
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        db.close()
        return {"id": new_report.id, "name": new_report.name, "type": new_report.type, "data": new_report.data, "generated_for": new_report.generated_for, "created_at": new_report.created_at.isoformat()}
    new_id = max(r["id"] for r in MOCK_REPORTS) + 1
    new_entry = {"id": new_id, **report.dict(), "created_at": datetime.utcnow().isoformat() + "Z"}
    MOCK_REPORTS.append(new_entry)
    return new_entry

# Additional CRM analytics endpoints
@app.get("/api/stats")
def get_stats():
    return {
        "total_contacts": 156,
        "active_contacts": 89,
        "total_deals": 24,
        "deals_won_this_month": 3,
        "deals_lost_this_month": 1,
        "average_cycle_days": 45,
        "total_companies": 48,
        "interactions_this_week": 37,
        "pipeline_value": 4500000.0,
        "forecasted_revenue": 3250000.0
    }

@app.get("/api/recent-activity")
def get_recent_activity():
    return [
        {"id": 1, "type": "deal_closed", "description": "Deal 'Operational Efficiency Audit' closed with HealthFirst Medical", "value": 150000.0, "timestamp": "2025-02-28T16:30:00Z", "user": "AI Assistant"},
        {"id": 2, "type": "meeting", "description": "Strategy meeting with GlobalTech Solutions CEO", "timestamp": "2025-02-27T10:00:00Z", "user": "John Smith"},
        {"id": 3, "type": "contact_added", "description": "New contact added: Robert Kim from DataSystems Corp", "timestamp": "2025-02-25T14:15:00Z", "user": "Sarah Chen"},
        {"id": 4, "type": "proposal_sent", "description": "Enterprise AI Strategy proposal sent to Acme Corporation", "value": 250000.0, "timestamp": "2025-02-24T09:45:00Z", "user": "AI Assistant"},
        {"id": 5, "type": "report_generated", "description": "AI-powered revenue forecast report generated for Board of Directors", "timestamp": "2025-02-23T11:00:00Z", "user": "System"}
    ]

@app.get("/api/chart-data")
def get_chart_data():
    return {
        "pipeline_by_stage": {
            "labels": ["Discovery", "Qualification", "Proposal", "Negotiation", "Closed Won"],
            "values": [450000, 520000, 680000, 850000, 2150000],
            "counts": [5, 4, 3, 2, 1]
        },
        "monthly_revenue": {
            "labels": ["Oct", "Nov", "Dec", "Jan", "Feb"],
            "values": [150000, 180000, 220000, 310000, 420000]
        },
        "industry_distribution": {
            "labels": ["Technology", "Finance", "Healthcare", "Retail", "Energy", "Manufacturing"],
            "values": [35, 20, 15, 12, 10, 8]
        },
        "engagement_trend": {
            "labels": ["Week 1", "Week 2", "Week 3", "Week 4"],
            "values": [28, 32, 35, 37]
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)