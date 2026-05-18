import os
import uuid
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import random

app = FastAPI(title="NovaStrategy", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PORT = int(os.environ.get("COMPANY_PORT", 8000))

# --- MOCK DATA ---

team_members = [
    {"id": "tm-001", "name": "Dr. Elena Vasquez", "role": "CEO & Chief Strategist", "email": "e.vasquez@novamind.com", "specialization": "Corporate Strategy", "years_experience": 18},
    {"id": "tm-002", "name": "Marcus Chen", "role": "Head of AI Research", "email": "m.chen@novamind.com", "specialization": "Machine Learning", "years_experience": 12},
    {"id": "tm-003", "name": "Sarah Okafor", "role": "Senior Consultant", "email": "s.okafor@novamind.com", "specialization": "Market Entry Strategy", "years_experience": 9},
    {"id": "tm-004", "name": "James Thornton", "role": "Data Analytics Lead", "email": "j.thornton@novamind.com", "specialization": "Data Science", "years_experience": 11},
    {"id": "tm-005", "name": "Priya Sharma", "role": "AI Solutions Architect", "email": "p.sharma@novamind.com", "specialization": "NLP & Recommendation Systems", "years_experience": 8},
    {"id": "tm-006", "name": "David Kim", "role": "Junior Consultant", "email": "d.kim@novamind.com", "specialization": "Financial Modeling", "years_experience": 3},
    {"id": "tm-007", "name": "Aisha Patel", "role": "Client Success Manager", "email": "a.patel@novamind.com", "specialization": "Account Management", "years_experience": 7},
    {"id": "tm-008", "name": "Liam O'Brien", "role": "Research Analyst", "email": "l.obrien@novamind.com", "specialization": "Competitive Intelligence", "years_experience": 5},
]

clients = [
    {"id": "cli-001", "name": "Aether Global Inc.", "industry": "Technology", "revenue_range": "$10B-$50B", "region": "North America", "status": "active", "contact_email": "contact@aetherglobal.com", "acquisition_date": "2023-03-15", "lifetime_value": 4200000},
    {"id": "cli-002", "name": "Veridian Financial", "industry": "Financial Services", "revenue_range": "$5B-$20B", "region": "Europe", "status": "active", "contact_email": "info@veridianfin.com", "acquisition_date": "2023-07-01", "lifetime_value": 3800000},
    {"id": "cli-003", "name": "TerraNova Pharmaceuticals", "industry": "Healthcare", "revenue_range": "$20B-$50B", "region": "North America", "status": "active", "contact_email": "bizdev@terranovapharma.com", "acquisition_date": "2024-01-10", "lifetime_value": 5100000},
    {"id": "cli-004", "name": "OmniRetail Corp.", "industry": "Retail", "revenue_range": "$5B-$15B", "region": "Asia Pacific", "status": "active", "contact_email": "partnerships@omniretail.asia", "acquisition_date": "2024-04-22", "lifetime_value": 2900000},
    {"id": "cli-005", "name": "Sapphire Energy", "industry": "Energy", "revenue_range": "$30B-$80B", "region": "Middle East", "status": "active", "contact_email": "strategy@sapphireenergy.ae", "acquisition_date": "2024-06-05", "lifetime_value": 6700000},
    {"id": "cli-006", "name": "Crestview Manufacturing", "industry": "Manufacturing", "revenue_range": "$2B-$8B", "region": "Europe", "status": "inactive", "contact_email": "info@crestviewmfg.eu", "acquisition_date": "2023-09-18", "lifetime_value": 1800000},
    {"id": "cli-007", "name": "NexGen Logistics", "industry": "Transportation", "revenue_range": "$1B-$5B", "region": "North America", "status": "active", "contact_email": "hello@nexgenlogistics.com", "acquisition_date": "2025-01-12", "lifetime_value": 2100000},
]

engagements = [
    {"id": "eng-001", "client_id": "cli-001", "title": "AI-Driven Market Expansion Strategy", "type": "Market Entry", "status": "in_progress", "start_date": "2024-08-01", "end_date": "2025-02-28", "team_lead": "Dr. Elena Vasquez", "team_members": ["Marcus Chen", "Priya Sharma"], "budget": 850000, "hours_billed": 2200, "description": "Develop AI models to identify optimal markets for Aether Global's cloud expansion in Southeast Asia."},
    {"id": "eng-002", "client_id": "cli-002", "title": "Digital Transformation Roadmap", "type": "Digital Strategy", "status": "in_progress", "start_date": "2024-09-15", "end_date": "2025-06-30", "team_lead": "James Thornton", "team_members": ["Sarah Okafor", "Liam O'Brien"], "budget": 1200000, "hours_billed": 3400, "description": "Create a data-driven digital transformation roadmap for Veridian's retail banking division."},
    {"id": "eng-003", "client_id": "cli-003", "title": "Competitive Intelligence & Market Positioning", "type": "Competitive Analysis", "status": "completed", "start_date": "2024-03-01", "end_date": "2024-11-30", "team_lead": "Sarah Okafor", "team_members": ["David Kim", "Aisha Patel"], "budget": 650000, "hours_billed": 1800, "description": "Analyzed TerraNova's competitors and recommended repositioning for their oncology pipeline."},
    {"id": "eng-004", "client_id": "cli-004", "title": "OmniChannel Retail Strategy", "type": "Retail Strategy", "status": "in_progress", "start_date": "2024-11-01", "end_date": "2025-08-31", "team_lead": "Priya Sharma", "team_members": ["Marcus Chen", "Aisha Patel", "Liam O'Brien"], "budget": 1500000, "hours_billed": 4100, "description": "Building a predictive analytics engine to optimize OmniRetail's inventory and personalization."},
    {"id": "eng-005", "client_id": "cli-005", "title": "Energy Transition Feasibility Study", "type": "Market Entry", "status": "planning", "start_date": "2025-02-01", "end_date": "2025-10-31", "team_lead": "Dr. Elena Vasquez", "team_members": ["James Thornton", "Sarah Okafor"], "budget": 980000, "hours_billed": 500, "description": "Assess feasibility of Sapphire Energy entering renewable hydrogen markets in Europe."},
    {"id": "eng-006", "client_id": "cli-006", "title": "Supply Chain Optimization", "type": "Operations", "status": "completed", "start_date": "2023-10-01", "end_date": "2024-06-30", "team_lead": "James Thornton", "team_members": ["David Kim"], "budget": 450000, "hours_billed": 1200, "description": "Optimized Crestview's supply chain using AI-driven demand forecasting."},
    {"id": "eng-007", "client_id": "cli-007", "title": "Last-Mile Delivery AI Optimization", "type": "Operations", "status": "in_progress", "start_date": "2025-01-15", "end_date": "2025-09-30", "team_lead": "Marcus Chen", "team_members": ["Priya Sharma", "Liam O'Brien"], "budget": 720000, "hours_billed": 1600, "description": "Develop AI routing algorithms to reduce NexGen's last-mile delivery costs by 18%."},
    {"id": "eng-008", "client_id": "cli-001", "title": "Post-Merger Integration Strategy", "type": "M&A Advisory", "status": "planning", "start_date": "2025-03-01", "end_date": "2025-12-31", "team_lead": "Dr. Elena Vasquez", "team_members": ["Aisha Patel", "David Kim"], "budget": 1100000, "hours_billed": 200, "description": "Advise Aether Global on post-merger integration with a recently acquired AI startup."},
]

ai_reports = [
    {"id": "rep-001", "engagement_id": "eng-001", "title": "Southeast Asia Market Attractiveness Index", "report_type": "Market Analysis", "created_date": "2024-10-15", "model_version": "NovaPredict v3.2", "confidence_score": 0.87, "key_findings": ["Vietnam and Indonesia show highest growth potential", "Regulatory barriers moderate in financial services sector", "Recommend phased entry starting Q3 2025"], "data_points": 12500, "file_url": "/reports/rep-001.pdf"},
    {"id": "rep-002", "engagement_id": "eng-002", "title": "Digital Maturity Assessment", "report_type": "Assessment", "created_date": "2024-11-20", "model_version": "NovaAssess v2.1", "confidence_score": 0.92, "key_findings": ["Veridian scores 67/100 on digital maturity", "Customer analytics gap identified", "AI chatbot deployment could reduce call volume 40%"], "data_points": 8900, "file_url": "/reports/rep-002.pdf"},
    {"id": "rep-003", "engagement_id": "eng-003", "title": "Oncology Competitive Landscape", "report_type": "Competitive Intelligence", "created_date": "2024-06-10", "model_version": "NovaIntel v4.0", "confidence_score": 0.9, "key_findings": ["Three emerging biotechs threaten TerraNova's pipeline", "Pricing pressure expected from biosimilars by 2027", "Recommend strategic partnerships in immuno-oncology"], "data_points": 18700, "file_url": "/reports/rep-003.pdf"},
    {"id": "rep-004", "engagement_id": "eng-004", "title": "Customer Segmentation & Personalization Model", "report_type": "Analytics", "created_date": "2025-01-05", "model_version": "NovaSeg v1.5", "confidence_score": 0.84, "key_findings": ["6 distinct customer segments identified", "Loyalty program redesign could lift retention 15%", "Personalized recommendations increase basket size 22%"], "data_points": 35000, "file_url": "/reports/rep-004.pdf"},
    {"id": "rep-005", "engagement_id": "eng-005", "title": "European Green Hydrogen Market Analysis", "report_type": "Market Analysis", "created_date": "2025-02-28", "model_version": "NovaPredict v3.3", "confidence_score": 0.79, "key_findings": ["Germany and Netherlands lead infrastructure development", "Subsidy landscape favorable for early movers", "ROI breakeven projected at 7-year horizon"], "data_points": 14300, "file_url": "/reports/rep-005.pdf"},
    {"id": "rep-006", "engagement_id": "eng-007", "title": "Route Optimization Algorithm Performance", "report_type": "Performance Analysis", "created_date": "2025-02-15", "model_version": "NovaRoute v2.0", "confidence_score": 0.91, "key_findings": ["12.4% reduction in delivery time achieved", "Fuel costs decreased by 8.7% in pilot", "Scalability across 500+ routes confirmed"], "data_points": 22000, "file_url": "/reports/rep-006.pdf"},
    {"id": "rep-007", "engagement_id": "eng-002", "title": "Customer Churn Prediction Model", "report_type": "Predictive Modeling", "created_date": "2024-12-18", "model_version": "NovaChurn v1.0", "confidence_score": 0.88, "key_findings": ["High-risk segment: customers aged 25-35 with 3+ complaints", "Model accuracy 92% on test set", "Proactive retention campaigns could save $18M annually"], "data_points": 42000, "file_url": "/reports/rep-007.pdf"},
]

# --- Pydantic Models ---

class ContactCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., max_length=200)
    phone: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    source: Optional[str] = "direct"

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    source: Optional[str] = None

class DealCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    value: float = Field(..., ge=0)
    stage: str = Field(..., pattern="^(lead|qualified|proposal|negotiation|closed_won|closed_lost)$")
    contact_id: str = Field(..., min_length=1)
    probability: float = Field(..., ge=0.0, le=1.0)
    expected_close_date: str

class PipelineStage(BaseModel):
    stage: str
    count: int
    total_value: float

# --- Endpoints ---

@app.get("/health")
def health():
    return {"status": "ok", "app": "NovaStrategy", "version": "1.0.0"}

@app.get("/api/info")
def api_info():
    return {
        "company": "NovaMind Consulting",
        "app": "NovaStrategy",
        "tagline": "AI-Powered Strategy for the Fortune 500",
        "founded": "2019",
        "headquarters": "San Francisco, CA",
        "team_size": 48,
        "clients_served": 18,
        "avg_engagement_value": 850000,
        "specialties": ["Market Entry Strategy", "Digital Transformation", "Competitive Intelligence", "AI-Driven Analytics"],
        "certifications": ["ISO 9001:2023", "SOC 2 Type II", "GDPR Compliant"],
        "mission": "Empower Fortune 500 companies with data-driven business strategy and market entry recommendations using cutting-edge AI."
    }

@app.get("/api/metrics")
def api_metrics():
    return {
        "active_engagements": 5,
        "total_clients": 7,
        "active_clients": 6,
        "total_revenue_ytd": 5870000,
        "pipeline_value": 3200000,
        "avg_client_lifetime_value": 3800000,
        "ai_reports_generated": 47,
        "team_utilization_rate": 0.82,
        "client_satisfaction_score": 4.7,
        "avg_engagement_duration_days": 245,
        "repeat_client_rate": 0.71,
        "quarterly_growth_rate": 0.12
    }

@app.get("/api/contacts")
def get_contacts():
    contacts = [
        {"id": "con-001", "name": "Jennifer Walsh", "email": "j.walsh@aetherglobal.com", "phone": "+1-415-555-0123", "company": "Aether Global Inc.", "title": "VP of Strategy", "source": "referral", "created_date": "2023-02-10", "last_contacted": "2025-01-20"},
        {"id": "con-002", "name": "Thomas Richter", "email": "t.richter@veridianfin.com", "phone": "+49-30-555-7890", "company": "Veridian Financial", "title": "Chief Digital Officer", "source": "conference", "created_date": "2023-06-14", "last_contacted": "2025-02-05"},
        {"id": "con-003", "name": "Dr. Lisa Chang", "email": "l.chang@terranovapharma.com", "phone": "+1-617-555-4567", "company": "TerraNova Pharmaceuticals", "title": "Head of Business Development", "source": "linkedin", "created_date": "2023-11-28", "last_contacted": "2025-01-28"},
        {"id": "con-004", "name": "Kenji Nakamura", "email": "k.nakamura@omniretail.asia", "phone": "+81-3-555-2345", "company": "OmniRetail Corp.", "title": "Director of Innovation", "source": "direct", "created_date": "2024-03-05", "last_contacted": "2025-02-12"},
        {"id": "con-005", "name": "Fatima Al-Rashid", "email": "f.alrashid@sapphireenergy.ae", "phone": "+971-4-555-6789", "company": "Sapphire Energy", "title": "VP of Corporate Strategy", "source": "referral", "created_date": "2024-05-20", "last_contacted": "2025-02-01"},
        {"id": "con-006", "name": "Olivia Dupont", "email": "o.dupont@crestviewmfg.eu", "phone": "+33-1-555-3456", "company": "Crestview Manufacturing", "title": "Supply Chain Director", "source": "email_campaign", "created_date": "2023-08-22", "last_contacted": "2024-09-15"},
        {"id": "con-007", "name": "Michael Torres", "email": "m.torres@nexgenlogistics.com", "phone": "+1-312-555-9012", "company": "NexGen Logistics", "title": "COO", "source": "direct", "created_date": "2024-12-01", "last_contacted": "2025-02-18"},
        {"id": "con-008", "name": "Dr. Sarah Mitchell", "email": "s.mitchell@innovatebio.com", "phone": "+1-650-555-1111", "company": "InnovateBio", "title": "CEO", "source": "conference", "created_date": "2025-01-15", "last_contacted": "2025-02-10"},
    ]
    return {"count": len(contacts), "contacts": contacts}

@app.get("/api/deals")
def get_deals():
    deals = [
        {"id": "deal-001", "title": "Aether Global AI Expansion Phase 2", "value": 920000, "stage": "negotiation", "contact_id": "con-001", "contact_name": "Jennifer Walsh", "probability": 0.75, "expected_close_date": "2025-04-30", "created_date": "2025-01-10"},
        {"id": "deal-002", "title": "Veridian Retail Banking AI Suite", "value": 1450000, "stage": "proposal", "contact_id": "con-002", "contact_name": "Thomas Richter", "probability": 0.6, "expected_close_date": "2025-05-15", "created_date": "2025-02-01"},
        {"id": "deal-003", "title": "TerraNova Market Entry Europe", "value": 780000, "stage": "lead", "contact_id": "con-003", "contact_name": "Dr. Lisa Chang", "probability": 0.2, "expected_close_date": "2025-07-01", "created_date": "2025-02-12"},
        {"id": "deal-004", "title": "OmniRetail Supply Chain AI", "value": 1150000, "stage": "qualified", "contact_id": "con-004", "contact_name": "Kenji Nakamura", "probability": 0.45, "expected_close_date": "2025-06-30", "created_date": "2025-01-25"},
        {"id": "deal-005", "title": "Sapphire Energy Hydrogen Feasibility Phase 2", "value": 1100000, "stage": "proposal", "contact_id": "con-005", "contact_name": "Fatima Al-Rashid", "probability": 0.65, "expected_close_date": "2025-04-01", "created_date": "2025-02-05"},
        {"id": "deal-006", "title": "NexGen Fleet Optimization Platform", "value": 680000, "stage": "qualified", "contact_id": "con-007", "contact_name": "Michael Torres", "probability": 0.4, "expected_close_date": "2025-08-01", "created_date": "2025-02-20"},
        {"id": "deal-007", "title": "InnovateBio Launch Strategy Consulting", "value": 350000, "stage": "lead", "contact_id": "con-008", "contact_name": "Dr. Sarah Mitchell", "probability": 0.15, "expected_close_date": "2025-09-01", "created_date": "2025-03-01"},
        {"id": "deal-008", "title": "Aether Global M&A Advisory Retainer", "value": 2200000, "stage": "lead", "contact_id": "con-001", "contact_name": "Jennifer Walsh", "probability": 0.1, "expected_close_date": "2025-12-31", "created_date": "2025-02-28"},
    ]
    return {"count": len(deals), "deals": deals}

@app.get("/api/pipeline")
def get_pipeline():
    stages_data = [
        {"stage": "lead", "count": 3, "total_value": 3330000},
        {"stage": "qualified", "count": 2, "total_value": 1830000},
        {"stage": "proposal", "count": 2, "total_value": 2550000},
        {"stage": "negotiation", "count": 1, "total_value": 920000},
        {"stage": "closed_won", "count": 0, "total_value": 0},
        {"stage": "closed_lost", "count": 0, "total_value": 0},
    ]
    total_pipeline = sum(s["total_value"] for s in stages_data)
    return {"stages": stages_data, "total_pipeline_value": total_pipeline, "total_deals": sum(s["count"] for s in stages_data)}

@app.get("/api/clients")
def get_clients():
    return {"count": len(clients), "clients": clients}

@app.get("/api/engagements")
def get_engagements():
    return {"count": len(engagements), "engagements": engagements}

@app.get("/api/engagements/{engagement_id}")
def get_engagement(engagement_id: str):
    for eng in engagements:
        if eng["id"] == engagement_id:
            return eng
    raise HTTPException(status_code=404, detail="Engagement not found")

@app.get("/api/ai-reports")
def get_ai_reports():
    return {"count": len(ai_reports), "reports": ai_reports}

@app.get("/api/ai-reports/{report_id}")
def get_ai_report(report_id: str):
    for rep in ai_reports:
        if rep["id"] == report_id:
            return rep
    raise HTTPException(status_code=404, detail="Report not found")

@app.get("/api/team-members")
def get_team_members():
    return {"count": len(team_members), "team_members": team_members}

@app.post("/api/contacts")
def create_contact(contact: ContactCreate):
    new_contact = contact.model_dump()
    new_contact["id"] = f"con-{uuid.uuid4().hex[:8]}"
    new_contact["created_date"] = datetime.now().strftime("%Y-%m-%d")
    new_contact["last_contacted"] = datetime.now().strftime("%Y-%m-%d")
    contacts_list = [c for c in get_contacts()["contacts"]] if False else []
    return {"message": "Contact created", "contact": new_contact}

@app.put("/api/contacts/{contact_id}")
def update_contact(contact_id: str, contact: ContactUpdate):
    return {"message": "Contact updated", "contact_id": contact_id, "updated_fields": contact.model_dump(exclude_none=True)}

@app.post("/api/deals")
def create_deal(deal: DealCreate):
    new_deal = deal.model_dump()
    new_deal["id"] = f"deal-{uuid.uuid4().hex[:8]}"
    new_deal["created_date"] = datetime.now().strftime("%Y-%m-%d")
    return {"message": "Deal created", "deal": new_deal}

@app.get("/api/stats")
def get_stats():
    active_engagements_budget = sum(e["budget"] for e in engagements if e["status"] == "in_progress")
    completed_engagements = sum(1 for e in engagements if e["status"] == "completed")
    total_hours = sum(e["hours_billed"] for e in engagements)
    avg_hours_per_engagement = round(total_hours / len(engagements), 1) if engagements else 0
    return {
        "active_engagements_count": sum(1 for e in engagements if e["status"] in ["in_progress", "planning"]),
        "completed_engagements_count": completed_engagements,
        "active_budget_total": active_engagements_budget,
        "total_hours_billed": total_hours,
        "avg_hours_per_engagement": avg_hours_per_engagement,
        "reports_generated": len(ai_reports),
        "avg_report_confidence": round(sum(r["confidence_score"] for r in ai_reports) / len(ai_reports), 2),
        "team_size": len(team_members)
    }

@app.get("/api/recent-activity")
def get_recent_activity():
    activities = [
        {"type": "report_generated", "description": "Route Optimization Algorithm Performance report completed for NexGen Logistics", "timestamp": "2025-02-15T14:30:00Z", "user": "Marcus Chen", "engagement_id": "eng-007"},
        {"type": "deal_created", "description": "New deal: InnovateBio Launch Strategy Consulting ($350,000)", "timestamp": "2025-03-01T09:15:00Z", "user": "Sarah Okafor", "deal_id": "deal-007"},
        {"type": "engagement_status", "description": "Sapphire Energy feasibility study moved to planning phase", "timestamp": "2025-02-25T11:00:00Z", "user": "Dr. Elena Vasquez", "engagement_id": "eng-005"},
        {"type": "contact_added", "description": "New contact: Dr. Sarah Mitchell (CEO, InnovateBio)", "timestamp": "2025-01-15T16:45:00Z", "user": "Aisha Patel", "contact_id": "con-008"},
        {"type": "report_generated", "description": "European Green Hydrogen Market Analysis report completed for Sapphire Energy", "timestamp": "2025-02-28T13:00:00Z", "user": "James Thornton", "engagement_id": "eng-005"},
        {"type": "deal_stage_change", "description": "Aether Global AI Expansion Phase 2 moved to negotiation stage", "timestamp": "2025-02-20T10:30:00Z", "user": "Aisha Patel", "deal_id": "deal-001"},
        {"type": "engagement_milestone", "description": "OmniRetail project: Customer segmentation model delivered ahead of schedule", "timestamp": "2025-01-05T15:00:00Z", "user": "Priya Sharma", "engagement_id": "eng-004"},
        {"type": "team_update", "description": "Liam O'Brien joined OmniRetail engagement team", "timestamp": "2025-02-10T08:00:00Z", "user": "Dr. Elena Vasquez", "engagement_id": "eng-004"},
    ]
    return {"activities": activities}

@app.get("/api/chart-data")
def get_chart_data():
    monthly_revenue = [
        {"month": "2024-09", "revenue": 420000, "new_clients": 1},
        {"month": "2024-10", "revenue": 510000, "new_clients": 0},
        {"month": "2024-11", "revenue": 480000, "new_clients": 1},
        {"month": "2024-12", "revenue": 550000, "new_clients": 0},
        {"month": "2025-01", "revenue": 680000, "new_clients": 2},
        {"month": "2025-02", "revenue": 720000, "new_clients": 1},
    ]
    engagement_status_distribution = {
        "in_progress": 4,
        "planning": 2,
        "completed": 2,
    }
    report_types = {
        "Market Analysis": 2,
        "Competitive Intelligence": 1,
        "Predictive Modeling": 1,
        "Assessment": 1,
        "Analytics": 1,
        "Performance Analysis": 1,
    }
    return {
        "monthly_revenue": monthly_revenue,
        "engagement_status_distribution": engagement_status_distribution,
        "report_types": report_types
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)