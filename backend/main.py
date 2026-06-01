import os
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, Enum as SAEnum
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import random
import enum

DATABASE_URL = os.environ.get("DATABASE_URL", "")
COMPANY_SLUG = os.environ.get("COMPANY_SLUG", "novamind")
PORT = int(os.environ.get("COMPANY_PORT", 8000))

db_engine = None
SessionLocal = None


class Base(DeclarativeBase):
    pass


if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    db_engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(bind=db_engine)


# --- Database Models ---
class UserModel(Base):
    __tablename__ = f"{COMPANY_SLUG}_users"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(String, nullable=False)
    department = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ClientModel(Base):
    __tablename__ = f"{COMPANY_SLUG}_clients"
    
    id = Column(String, primary_key=True)
    company_name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    revenue_range = Column(String, nullable=False)
    region = Column(String, nullable=False)
    status = Column(String, nullable=False)
    assigned_user_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ProjectModel(Base):
    __tablename__ = f"{COMPANY_SLUG}_projects"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    client_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    budget = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    lead_analyst_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class AnalysisModel(Base):
    __tablename__ = f"{COMPANY_SLUG}_analyses"
    
    id = Column(String, primary_key=True)
    project_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=True)
    key_findings = Column(Text, nullable=True)
    created_by = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ReportModel(Base):
    __tablename__ = f"{COMPANY_SLUG}_reports"
    
    id = Column(String, primary_key=True)
    project_id = Column(String, nullable=False)
    analysis_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    status = Column(String, nullable=False)
    executive_summary = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
    generated_by = Column(String, nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow)


# --- Mock Data ---
MOCK_USERS = [
    {
        "id": "usr_001",
        "name": "Dr. Sarah Chen",
        "email": "sarah.chen@novamind.ai",
        "role": "Chief AI Strategist",
        "department": "Strategy",
        "created_at": "2024-01-15T09:00:00"
    },
    {
        "id": "usr_002",
        "name": "James Rodriguez",
        "email": "james.rodriguez@novamind.ai",
        "role": "Senior Data Analyst",
        "department": "Analytics",
        "created_at": "2024-02-01T10:00:00"
    },
    {
        "id": "usr_003",
        "name": "Emily Nakamura",
        "email": "emily.nakamura@novamind.ai",
        "role": "Market Research Lead",
        "department": "Research",
        "created_at": "2024-02-15T11:00:00"
    },
    {
        "id": "usr_004",
        "name": "Marcus Williams",
        "email": "marcus.williams@novamind.ai",
        "role": "AI Implementation Specialist",
        "department": "Technology",
        "created_at": "2024-03-01T08:00:00"
    },
    {
        "id": "usr_005",
        "name": "Olivia Patel",
        "email": "olivia.patel@novamind.ai",
        "role": "Client Success Director",
        "department": "Client Relations",
        "created_at": "2024-03-10T09:30:00"
    },
    {
        "id": "usr_006",
        "name": "Dr. Robert Kim",
        "email": "robert.kim@novamind.ai",
        "role": "Data Science Lead",
        "department": "Analytics",
        "created_at": "2024-03-20T10:00:00"
    }
]

MOCK_CLIENTS = [
    {
        "id": "cli_001",
        "company_name": "GlobalTech Industries",
        "industry": "Technology",
        "revenue_range": "$10B-$50B",
        "region": "North America",
        "status": "active",
        "assigned_user_id": "usr_001",
        "created_at": "2024-01-20T09:00:00"
    },
    {
        "id": "cli_002",
        "company_name": "EuroFinance Group",
        "industry": "Financial Services",
        "revenue_range": "$5B-$20B",
        "region": "Europe",
        "status": "active",
        "assigned_user_id": "usr_005",
        "created_at": "2024-02-05T10:00:00"
    },
    {
        "id": "cli_003",
        "company_name": "Pacific Health Systems",
        "industry": "Healthcare",
        "revenue_range": "$3B-$15B",
        "region": "Asia Pacific",
        "status": "active",
        "assigned_user_id": "usr_003",
        "created_at": "2024-02-18T11:00:00"
    },
    {
        "id": "cli_004",
        "company_name": "RetailMax Corporation",
        "industry": "Retail",
        "revenue_range": "$2B-$10B",
        "region": "North America",
        "status": "onboarding",
        "assigned_user_id": "usr_005",
        "created_at": "2024-03-05T09:00:00"
    },
    {
        "id": "cli_005",
        "company_name": "GreenEnergy Solutions",
        "industry": "Energy",
        "revenue_range": "$1B-$5B",
        "region": "Europe",
        "status": "proposal",
        "assigned_user_id": "usr_001",
        "created_at": "2024-03-15T10:00:00"
    },
    {
        "id": "cli_006",
        "company_name": "AeroSpace Dynamics",
        "industry": "Aerospace",
        "revenue_range": "$8B-$30B",
        "region": "North America",
        "status": "active",
        "assigned_user_id": "usr_002",
        "created_at": "2024-03-22T11:00:00"
    },
    {
        "id": "cli_007",
        "company_name": "MediTech Innovations",
        "industry": "Healthcare Technology",
        "revenue_range": "$500M-$2B",
        "region": "Europe",
        "status": "onboarding",
        "assigned_user_id": "usr_003",
        "created_at": "2024-04-01T09:00:00"
    }
]

MOCK_PROJECTS = [
    {
        "id": "prj_001",
        "name": "Global Market Entry Strategy - APAC",
        "client_id": "cli_001",
        "type": "Market Entry",
        "status": "in_progress",
        "budget": 2500000.00,
        "start_date": "2024-03-01T00:00:00",
        "end_date": "2024-09-30T00:00:00",
        "lead_analyst_id": "usr_001",
        "created_at": "2024-02-15T09:00:00"
    },
    {
        "id": "prj_002",
        "name": "AI-Driven Cost Optimization",
        "client_id": "cli_002",
        "type": "Operational Efficiency",
        "status": "in_progress",
        "budget": 1800000.00,
        "start_date": "2024-03-15T00:00:00",
        "end_date": "2024-10-15T00:00:00",
        "lead_analyst_id": "usr_006",
        "created_at": "2024-02-28T10:00:00"
    },
    {
        "id": "prj_003",
        "name": "Healthcare Digital Transformation",
        "client_id": "cli_003",
        "type": "Digital Transformation",
        "status": "planning",
        "budget": 3200000.00,
        "start_date": "2024-04-01T00:00:00",
        "end_date": "2025-03-31T00:00:00",
        "lead_analyst_id": "usr_003",
        "created_at": "2024-03-10T11:00:00"
    },
    {
        "id": "prj_004",
        "name": "Retail Analytics Platform",
        "client_id": "cli_004",
        "type": "Technology Implementation",
        "status": "planning",
        "budget": 1500000.00,
        "start_date": "2024-05-01T00:00:00",
        "end_date": "2024-12-31T00:00:00",
        "lead_analyst_id": "usr_004",
        "created_at": "2024-03-20T09:00:00"
    },
    {
        "id": "prj_005",
        "name": "Renewable Energy Market Analysis",
        "client_id": "cli_005",
        "type": "Market Research",
        "status": "proposal",
        "budget": 800000.00,
        "start_date": "2024-06-01T00:00:00",
        "end_date": "2024-11-30T00:00:00",
        "lead_analyst_id": "usr_002",
        "created_at": "2024-04-01T10:00:00"
    },
    {
        "id": "prj_006",
        "name": "Supply Chain AI Optimization",
        "client_id": "cli_006",
        "type": "AI Implementation",
        "status": "in_progress",
        "budget": 2800000.00,
        "start_date": "2024-02-01T00:00:00",
        "end_date": "2024-11-30T00:00:00",
        "lead_analyst_id": "usr_004",
        "created_at": "2024-01-20T11:00:00"
    },
    {
        "id": "prj_007",
        "name": "MedTech Go-to-Market Strategy",
        "client_id": "cli_007",
        "type": "Market Entry",
        "status": "planning",
        "budget": 1200000.00,
        "start_date": "2024-05-15T00:00:00",
        "end_date": "2025-02-28T00:00:00",
        "lead_analyst_id": "usr_003",
        "created_at": "2024-04-10T09:00:00"
    }
]

MOCK_ANALYSES = [
    {
        "id": "anl_001",
        "project_id": "prj_001",
        "type": "Competitive Landscape",
        "description": "Deep analysis of competitors in Southeast Asian markets",
        "status": "completed",
        "confidence_score": 0.92,
        "key_findings": "Three major competitors identified; market gap in mid-tier pricing",
        "created_by": "usr_002",
        "created_at": "2024-03-20T14:00:00"
    },
    {
        "id": "anl_002",
        "project_id": "prj_001",
        "type": "Customer Segmentation",
        "description": "AI-driven customer segmentation for APAC markets",
        "status": "in_progress",
        "confidence_score": 0.85,
        "key_findings": "Four distinct segments identified; premium segment shows 40% growth potential",
        "created_by": "usr_003",
        "created_at": "2024-04-05T10:00:00"
    },
    {
        "id": "anl_003",
        "project_id": "prj_002",
        "type": "Process Mining",
        "description": "Analyzing operational workflows for AI optimization opportunities",
        "status": "completed",
        "confidence_score": 0.88,
        "key_findings": "32% reduction potential in operational costs through AI automation",
        "created_by": "usr_006",
        "created_at": "2024-03-28T09:00:00"
    },
    {
        "id": "anl_004",
        "project_id": "prj_003",
        "type": "Technology Assessment",
        "description": "Evaluating current tech stack for digital transformation readiness",
        "status": "completed",
        "confidence_score": 0.90,
        "key_findings": "Legacy system migration needed; recommended cloud-native architecture",
        "created_by": "usr_004",
        "created_at": "2024-04-01T11:00:00"
    },
    {
        "id": "anl_005",
        "project_id": "prj_006",
        "type": "Supply Chain Analytics",
        "description": "AI-powered supply chain optimization analysis",
        "status": "completed",
        "confidence_score": 0.94,
        "key_findings": "18% improvement in logistics efficiency achievable with ML routing",
        "created_by": "usr_002",
        "created_at": "2024-03-15T15:00:00"
    },
    {
        "id": "anl_006",
        "project_id": "prj_006",
        "type": "Predictive Maintenance",
        "description": "AI models for predicting equipment maintenance needs",
        "status": "in_progress",
        "confidence_score": 0.82,
        "key_findings": "Predictive accuracy at 87%; potential for 25% reduction in downtime",
        "created_by": "usr_006",
        "created_at": "2024-04-08T13:00:00"
    },
    {
        "id": "anl_007",
        "project_id": "prj_001",
        "type": "Regulatory Analysis",
        "description": "Compliance and regulatory landscape assessment for APAC entry",
        "status": "completed",
        "confidence_score": 0.91,
        "key_findings": "Moderate regulatory barriers; data localization requirements in 3 countries",
        "created_by": "usr_001",
        "created_at": "2024-04-10T08:00:00"
    }
]

MOCK_REPORTS = [
    {
        "id": "rpt_001",
        "project_id": "prj_001",
        "analysis_id": "anl_001",
        "title": "Competitive Landscape Report: Southeast Asia",
        "status": "final",
        "executive_summary": "Comprehensive analysis reveals significant market opportunity in emerging economies of Southeast Asia, with projected CAGR of 15.2% over next 3 years.",
        "recommendations": "Focus on mid-market segment first; leverage partnerships with local distributors; invest in localized AI solutions",
        "generated_by": "usr_001",
        "generated_at": "2024-04-01T16:00:00"
    },
    {
        "id": "rpt_002",
        "project_id": "prj_002",
        "analysis_id": "anl_003",
        "title": "Operational Efficiency Optimization Report",
        "status": "final",
        "executive_summary": "AI-driven process mining identified $580M in annual cost savings opportunities across 12 key operational areas.",
        "recommendations": "Implement RPA in 6 high-impact processes; deploy ML-based demand forecasting; automate invoice processing",
        "generated_by": "usr_006",
        "generated_at": "2024-04-10T14:00:00"
    },
    {
        "id": "rpt_003",
        "project_id": "prj_003",
        "analysis_id": "anl_004",
        "title": "Digital Transformation Readiness Assessment",
        "status": "draft",
        "executive_summary": "Organization shows 65% digital maturity score; critical gaps identified in data infrastructure and workforce skills.",
        "recommendations": "Phased migration to cloud; invest in data lakes; comprehensive training program for 2,000 employees",
        "generated_by": "usr_004",
        "generated_at": "2024-04-15T11:00:00"
    },
    {
        "id": "rpt_004",
        "project_id": "prj_006",
        "analysis_id": "anl_005",
        "title": "Supply Chain AI Optimization: Phase 1 Results",
        "status": "final",
        "executive_summary": "Initial AI implementation shows 12% cost reduction in logistics operations with full-scale rollout projected to achieve 18% savings.",
        "recommendations": "Expand ML routing to all distribution centers; integrate real-time demand sensing; automated supplier selection",
        "generated_by": "usr_002",
        "generated_at": "2024-04-05T09:00:00"
    },
    {
        "id": "rpt_005",
        "project_id": "prj_001",
        "analysis_id": "anl_007",
        "title": "APAC Regulatory Compliance Analysis",
        "status": "final",
        "executive_summary": "Regulatory environment ranges from favorable (Singapore, Vietnam) to restrictive (China, India). Data sovereignty and AI ethics laws pose key challenges.",
        "recommendations": "Establish local data centers in key markets; partner with regional compliance firms; develop AI ethics framework",
        "generated_by": "usr_001",
        "generated_at": "2024-04-18T15:00:00"
    },
    {
        "id": "rpt_006",
        "project_id": "prj_002",
        "analysis_id": "anl_003",
        "title": "Quarterly Performance Dashboard",
        "status": "draft",
        "executive_summary": "Q1 2024 performance exceeds targets by 15% in cost reduction initiatives; customer satisfaction score at 4.2/5.0.",
        "recommendations": "Scale successful automation to additional departments; invest in customer success team; Q2 target: 22% cost reduction",
        "generated_by": "usr_006",
        "generated_at": "2024-04-20T13:00:00"
    },
    {
        "id": "rpt_007",
        "project_id": "prj_001",
        "analysis_id": "anl_002",
        "title": "APAC Customer Segmentation Analysis",
        "status": "draft",
        "executive_summary": "Preliminary segmentation identifies 4 primary customer personas with distinct needs and willingness to pay for AI-powered solutions.",
        "recommendations": "Develop targeted marketing campaigns for each segment; premium pricing strategy for enterprise tier",
        "generated_by": "usr_003",
        "generated_at": "2024-04-22T10:00:00"
    }
]


# --- Pydantic Models ---
class UserCreate(BaseModel):
    name: str
    email: str
    role: str
    department: str


class ClientCreate(BaseModel):
    company_name: str
    industry: str
    revenue_range: str
    region: str
    status: str = "proposal"
    assigned_user_id: str = None


class ProjectCreate(BaseModel):
    name: str
    client_id: str
    type: str
    status: str = "planning"
    budget: float
    start_date: str
    end_date: str = None
    lead_analyst_id: str = None


class AnalysisCreate(BaseModel):
    project_id: str
    type: str
    description: str = None
    status: str = "planned"
    confidence_score: float = None
    key_findings: str = None
    created_by: str = None


class ReportCreate(BaseModel):
    project_id: str
    analysis_id: str
    title: str
    status: str = "draft"
    executive_summary: str = None
    recommendations: str = None
    generated_by: str = None


# --- FastAPI App ---
app = FastAPI(title="NovaMind AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    if db_engine:
        Base.metadata.create_all(db_engine)


# --- Helper Functions ---
def get_db():
    if SessionLocal:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        yield None


def generate_id(prefix: str) -> str:
    return f"{prefix}_{random.randint(100, 999)}"


# --- Health & Info Endpoints ---
@app.get("/health")
async def health():
    return {"status": "ok", "app": "NovaMind AI", "version": "1.0.0"}


@app.get("/api/info")
async def get_info():
    return {
        "name": "NovaMind Consulting",
        "app_name": "NovaMind AI",
        "tagline": "Transforming Fortune 500 Strategy with Artificial Intelligence",
        "founded": "2019",
        "team_size": 150,
        "headquarters": "San Francisco, CA",
        "specialties": [
            "AI Strategy Consulting",
            "Market Entry Analytics",
            "Operational AI Implementation",
            "Predictive Business Intelligence"
        ],
        "clients_served": 47,
        "ai_models_deployed": 230
    }


@app.get("/api/metrics")
async def get_metrics():
    return {
        "active_projects": 42,
        "total_revenue_ytd": 18500000.00,
        "avg_project_value": 2100000.00,
        "client_satisfaction_score": 4.7,
        "ai_accuracy_rate": 0.94,
        "project_completion_rate": 0.88,
        "team_utilization": 0.82,
        "new_clients_this_quarter": 8,
        "analyses_conducted": 156,
        "reports_generated": 89
    }


# --- CRM Domain Endpoints ---
@app.get("/api/contacts")
async def get_contacts():
    if SessionLocal:
        db = next(get_db())
        try:
            users = db.query(UserModel).all()
            return [
                {
                    "id": u.id,
                    "name": u.name,
                    "email": u.email,
                    "role": u.role,
                    "department": u.department,
                    "created_at": u.created_at.isoformat()
                }
                for u in users
            ]
        finally:
            db.close()
    return MOCK_USERS


@app.post("/api/contacts")
async def create_contact(contact: UserCreate):
    new_id = generate_id("usr")
    if SessionLocal:
        db = next(get_db())
        try:
            new_user = UserModel(
                id=new_id,
                name=contact.name,
                email=contact.email,
                role=contact.role,
                department=contact.department,
                created_at=datetime.utcnow()
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "role": new_user.role,
                "department": new_user.department,
                "created_at": new_user.created_at.isoformat()
            }
        finally:
            db.close()
    else:
        new_item = {
            "id": new_id,
            "name": contact.name,
            "email": contact.email,
            "role": contact.role,
            "department": contact.department,
            "created_at": datetime.utcnow().isoformat()
        }
        MOCK_USERS.append(new_item)
        return new_item


@app.get("/api/deals")
async def get_deals():
    if SessionLocal:
        db = next(get_db())
        try:
            projects = db.query(ProjectModel).all()
            return [
                {
                    "id": p.id,
                    "name": p.name,
                    "client_id": p.client_id,
                    "type": p.type,
                    "status": p.status,
                    "budget": p.budget,
                    "start_date": p.start_date.isoformat(),
                    "end_date": p.end_date.isoformat() if p.end_date else None,
                    "lead_analyst_id": p.lead_analyst_id,
                    "created_at": p.created_at.isoformat()
                }
                for p in projects
            ]
        finally:
            db.close()
    return MOCK_PROJECTS


@app.post("/api/deals")
async def create_deal(deal: ProjectCreate):
    new_id = generate_id("prj")
    if SessionLocal:
        db = next(get_db())
        try:
            new_project = ProjectModel(
                id=new_id,
                name=deal.name,
                client_id=deal.client_id,
                type=deal.type,
                status=deal.status,
                budget=deal.budget,
                start_date=datetime.fromisoformat(deal.start_date),
                end_date=datetime.fromisoformat(deal.end_date) if deal.end_date else None,
                lead_analyst_id=deal.lead_analyst_id,
                created_at=datetime.utcnow()
            )
            db.add(new_project)
            db.commit()
            db.refresh(new_project)
            return {
                "id": new_project.id,
                "name": new_project.name,
                "client_id": new_project.client_id,
                "type": new_project.type,
                "status": new_project.status,
                "budget": new_project.budget,
                "start_date": new_project.start_date.isoformat(),
                "end_date": new_project.end_date.isoformat() if new_project.end_date else None,
                "lead_analyst_id": new_project.lead_analyst_id,
                "created_at": new_project.created_at.isoformat()
            }
        finally:
            db.close()
    else:
        new_item = {
            "id": new_id,
            "name": deal.name,
            "client_id": deal.client_id,
            "type": deal.type,
            "status": deal.status,
            "budget": deal.budget,
            "start_date": deal.start_date,
            "end_date": deal.end_date,
            "lead_analyst_id": deal.lead_analyst_id,
            "created_at": datetime.utcnow().isoformat()
        }
        MOCK_PROJECTS.append(new_item)
        return new_item


@app.get("/api/pipeline")
async def get_pipeline():
    stages = {
        "proposal": [],
        "planning": [],
        "in_progress": [],
        "completed": []
    }
    projects = MOCK_PROJECTS if not SessionLocal else []
    if SessionLocal:
        db = next(get_db())
        try:
            projects = db.query(ProjectModel).all()
        finally:
            db.close()
    
    for p in projects:
        stage = p.status if p.status in stages else "planning"
        stages[stage].append({
            "id": p.id if isinstance(p.id, str) else p.id,
            "name": p.name if isinstance(p.name, str) else p.name,
            "client_id": p.client_id if isinstance(p.client_id, str) else p.client_id,
            "type": p.type if isinstance(p.type, str) else p.type,
            "budget": p.budget if isinstance(p.budget, (int, float)) else p.budget,
            "start_date": (p.start_date.isoformat() if hasattr(p, 'start_date') and p.start_date else str(p.start_date)) if not isinstance(p, dict) else p.get("start_date", ""),
            "lead": p.lead_analyst_id if isinstance(p.lead_analyst_id, str) else p.lead_analyst_id
        })
    
    return {
        "stages": stages,
        "totals": {k: len(v) for k, v in stages.items()}
    }


@app.get("/api/analyses")
async def get_analyses():
    if SessionLocal:
        db = next(get_db())
        try:
            analyses = db.query(AnalysisModel).all()
            return [
                {
                    "id": a.id,
                    "project_id": a.project_id,
                    "type": a.type,
                    "description": a.description,
                    "status": a.status,
                    "confidence_score": a.confidence_score,
                    "key_findings": a.key_findings,
                    "created_by": a.created_by,
                    "created_at": a.created_at.isoformat()
                }
                for a in analyses
            ]
        finally:
            db.close()
    return MOCK_ANALYSES


@app.post("/api/analyses")
async def create_analysis(analysis: AnalysisCreate):
    new_id = generate_id("anl")
    if SessionLocal:
        db = next(get_db())
        try:
            new_analysis = AnalysisModel(
                id=new_id,
                project_id=analysis.project_id,
                type=analysis.type,
                description=analysis.description,
                status=analysis.status,
                confidence_score=analysis.confidence_score,
                key_findings=analysis.key_findings,
                created_by=analysis.created_by,
                created_at=datetime.utcnow()
            )
            db.add(new_analysis)
            db.commit()
            db.refresh(new_analysis)
            return {
                "id": new_analysis.id,
                "project_id": new_analysis.project_id,
                "type": new_analysis.type,
                "description": new_analysis.description,
                "status": new_analysis.status,
                "confidence_score": new_analysis.confidence_score,
                "key_findings": new_analysis.key_findings,
                "created_by": new_analysis.created_by,
                "created_at": new_analysis.created_at.isoformat()
            }
        finally:
            db.close()
    else:
        new_item = {
            "id": new_id,
            "project_id": analysis.project_id,
            "type": analysis.type,
            "description": analysis.description,
            "status": analysis.status,
            "confidence_score": analysis.confidence_score,
            "key_findings": analysis.key_findings,
            "created_by": analysis.created_by,
            "created_at": datetime.utcnow().isoformat()
        }
        MOCK_ANALYSES.append(new_item)
        return new_item


@app.get("/api/reports")
async def get_reports():
    if SessionLocal:
        db = next(get_db())
        try:
            reports = db.query(ReportModel).all()
            return [
                {
                    "id": r.id,
                    "project_id": r.project_id,
                    "analysis_id": r.analysis_id,
                    "title": r.title,
                    "status": r.status,
                    "executive_summary": r.executive_summary,
                    "recommendations": r.recommendations,
                    "generated_by": r.generated_by,
                    "generated_at": r.generated_at.isoformat()
                }
                for r in reports
            ]
        finally:
            db.close()
    return MOCK_REPORTS


@app.post("/api/reports")
async def create_report(report: ReportCreate):
    new_id = generate_id("rpt")
    if SessionLocal:
        db = next(get_db())
        try:
            new_report = ReportModel(
                id=new_id,
                project_id=report.project_id,
                analysis_id=report.analysis_id,
                title=report.title,
                status=report.status,
                executive_summary=report.executive_summary,
                recommendations=report.recommendations,
                generated_by=report.generated_by,
                generated_at=datetime.utcnow()
            )
            db.add(new_report)
            db.commit()
            db.refresh(new_report)
            return {
                "id": new_report.id,
                "project_id": new_report.project_id,
                "analysis_id": new_report.analysis_id,
                "title": new_report.title,
                "status": new_report.status,
                "executive_summary": new_report.executive_summary,
                "recommendations": new_report.recommendations,
                "generated_by": new_report.generated_by,
                "generated_at": new_report.generated_at.isoformat()
            }
        finally:
            db.close()
    else:
        new_item = {
            "id": new_id,
            "project_id": report.project_id,
            "analysis_id": report.analysis_id,
            "title": report.title,
            "status": report.status,
            "executive_summary": report.executive_summary,
            "recommendations": report.recommendations,
            "generated_by": report.generated_by,
            "generated_at": datetime.utcnow().isoformat()
        }
        MOCK_REPORTS.append(new_item)
        return new_item


@app.get("/api/stats")
async def get_stats():
    total_projects = len(MOCK_PROJECTS) if not SessionLocal else 42
    total_analyses = len(MOCK_ANALYSES) if not SessionLocal else 156
    total_reports = len(MOCK_REPORTS) if not SessionLocal else 89
    
    return {
        "total_contacts": len(MOCK_USERS) if not SessionLocal else 34,
        "total_clients": len(MOCK_CLIENTS) if not SessionLocal else 47,
        "active_projects": total_projects,
        "total_analyses": total_analyses,
        "total_reports": total_reports,
        "avg_confidence_score": 0.89,
        "projects_by_status": {
            "proposal": 5,
            "planning": 12,
            "in_progress": 18,
            "completed": 7
        },
        "monthly_growth": 0.15
    }


@app.get("/api/recent-activity")
async def get_recent_activity():
    activities = [
        {
            "id": "act_001",
            "type": "report_generated",
            "description": "APAC Customer Segmentation Analysis completed",
            "user": "Emily Nakamura",
            "timestamp": "2024-04-22T10:00:00"
        },
        {
            "id": "act_002",
            "type": "analysis_updated",
            "description": "Predictive Maintenance model confidence improved to 87%",
            "user": "Dr. Robert Kim",
            "timestamp": "2024-04-21T15:30:00"
        },
        {
            "id": "act_003",
            "type": "client_onboarded",
            "description": "MediTech Innovations onboarded as new client",
            "user": "Olivia Patel",
            "timestamp": "2024-04-20T09:15:00"
        },
        {
            "id": "act