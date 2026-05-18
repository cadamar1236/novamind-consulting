from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uvicorn
import os
import random
import uuid

app = FastAPI(title="NovaMind Strategy Hub", version="1.0.0", description="AI-driven business strategy consulting platform for Fortune 500 companies")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PORT = int(os.environ.get("COMPANY_PORT", 8000))

# ===================== MOCK DATA =====================

current_time = datetime.now()
seven_days_ago = current_time - timedelta(days=7)

clients = [
    {"id": "CL-001", "name": "GlobalTech Industries", "industry": "Technology", "revenue": "$45B", "location": "San Francisco, CA", "status": "active", "onboarded": "2024-01-15", "project_count": 3, "ai_insights_usage": 87},
    {"id": "CL-002", "name": "Pinnacle Healthcare Corp", "industry": "Healthcare", "revenue": "$28B", "location": "Boston, MA", "status": "active", "onboarded": "2024-03-22", "project_count": 2, "ai_insights_usage": 64},
    {"id": "CL-003", "name": "Apex Financial Services", "industry": "Finance", "revenue": "$62B", "location": "New York, NY", "status": "active", "onboarded": "2024-06-10", "project_count": 4, "ai_insights_usage": 92},
    {"id": "CL-004", "name": "Meridian Energy Group", "industry": "Energy", "revenue": "$19B", "location": "Houston, TX", "status": "active", "onboarded": "2024-08-05", "project_count": 1, "ai_insights_usage": 45},
    {"id": "CL-005", "name": "Atlas Manufacturing Co", "industry": "Manufacturing", "revenue": "$33B", "location": "Chicago, IL", "status": "inactive", "onboarded": "2023-11-20", "project_count": 2, "ai_insights_usage": 23},
    {"id": "CL-006", "name": "Vortex Retail Solutions", "industry": "Retail", "revenue": "$21B", "location": "Seattle, WA", "status": "active", "onboarded": "2024-09-01", "project_count": 3, "ai_insights_usage": 78},
]

projects = [
    {"id": "PRJ-101", "name": "Market Entry Strategy - APAC", "client": "GlobalTech Industries", "status": "in_progress", "progress": 72, "deadline": "2025-04-15", "team_size": 8, "ai_models_used": 3, "budget": "$850K", "priority": "high"},
    {"id": "PRJ-102", "name": "Digital Transformation Roadmap", "client": "Pinnacle Healthcare Corp", "status": "completed", "progress": 100, "deadline": "2025-01-20", "team_size": 6, "ai_models_used": 2, "budget": "$1.2M", "priority": "high"},
    {"id": "PRJ-103", "name": "Risk Assessment & Mitigation", "client": "Apex Financial Services", "status": "in_progress", "progress": 45, "deadline": "2025-06-30", "team_size": 5, "ai_models_used": 4, "budget": "$620K", "priority": "medium"},
    {"id": "PRJ-104", "name": "Supply Chain Optimization", "client": "Atlas Manufacturing Co", "status": "on_hold", "progress": 30, "deadline": "2025-08-15", "team_size": 4, "ai_models_used": 2, "budget": "$450K", "priority": "low"},
    {"id": "PRJ-105", "name": "EU Market Penetration Strategy", "client": "Vortex Retail Solutions", "status": "in_progress", "progress": 58, "deadline": "2025-07-10", "team_size": 7, "ai_models_used": 5, "budget": "$980K", "priority": "high"},
    {"id": "PRJ-106", "name": "Sustainability Framework Design", "client": "Meridian Energy Group", "status": "planning", "progress": 10, "deadline": "2025-09-01", "team_size": 3, "ai_models_used": 1, "budget": "$340K", "priority": "medium"},
]

users = [
    {"id": "USR-001", "name": "Dr. Elena Vasquez", "role": "Senior Strategy Consultant", "email": "e.vasquez@novamind.ai", "projects_active": 3, "expertise": ["AI Strategy", "Market Entry"], "rating": 4.9, "billable_hours": 148},
    {"id": "USR-002", "name": "Marcus Chen", "role": "Data Scientist", "email": "m.chen@novamind.ai", "projects_active": 2, "expertise": ["Predictive Modeling", "NLP"], "rating": 4.7, "billable_hours": 132},
    {"id": "USR-003", "name": "Sarah Okafor", "role": "Business Analyst", "email": "s.okafor@novamind.ai", "projects_active": 4, "expertise": ["Financial Analysis", "Risk Assessment"], "rating": 4.8, "billable_hours": 156},
    {"id": "USR-004", "name": "Dr. Yuki Tanaka", "role": "AI Research Lead", "email": "y.tanaka@novamind.ai", "projects_active": 2, "expertise": ["Generative AI", "Optimization"], "rating": 4.9, "billable_hours": 112},
    {"id": "USR-005", "name": "Priya Sharma", "role": "Strategy Associate", "email": "p.sharma@novamind.ai", "projects_active": 3, "expertise": ["Competitive Intelligence", "SWOT"], "rating": 4.5, "billable_hours": 98},
]

ai_insights = [
    {"id": "AI-001", "type": "Market Trend Prediction", "client": "GlobalTech Industries", "confidence": 94.2, "impact": "+18% revenue potential", "generated": "2025-02-28", "status": "actionable", "region": "APAC"},
    {"id": "AI-002", "type": "Competitive Analysis", "client": "Apex Financial Services", "confidence": 89.7, "impact": "3 new market gaps identified", "generated": "2025-03-05", "status": "actionable", "region": "North America"},
    {"id": "AI-003", "type": "Customer Sentiment Analysis", "client": "Vortex Retail Solutions", "confidence": 91.5, "impact": "NPS improvement of 12 pts", "generated": "2025-03-02", "status": "reviewed", "region": "Europe"},
    {"id": "AI-004", "type": "Regulatory Risk Forecast", "client": "Meridian Energy Group", "confidence": 86.3, "impact": "4 regulatory changes expected", "generated": "2025-02-25", "status": "actionable", "region": "Global"},
    {"id": "AI-005", "type": "Optimization Recommendation", "client": "Pinnacle Healthcare Corp", "confidence": 93.8, "impact": "22% cost reduction possible", "generated": "2025-03-07", "status": "actionable", "region": "North America"},
    {"id": "AI-006", "type": "M&A Opportunity Alert", "client": "Atlas Manufacturing Co", "confidence": 78.4, "impact": "2 acquisition targets identified", "generated": "2025-03-01", "status": "pending", "region": "Europe"},
    {"id": "AI-007", "type": "Supply Chain Disruption Warning", "client": "GlobalTech Industries", "confidence": 88.9, "impact": "Potential 15% delay risk", "generated": "2025-03-03", "status": "actionable", "region": "APAC"},
]

reports = [
    {"id": "RPT-001", "title": "Q1 2025 Market Intelligence Brief", "client": "GlobalTech Industries", "type": "quarterly", "pages": 48, "ai_generated": True, "created": "2025-03-01", "downloads": 12},
    {"id": "RPT-002", "title": "Competitive Landscape Analysis", "client": "Apex Financial Services", "type": "custom", "pages": 32, "ai_generated": True, "created": "2025-02-20", "downloads": 8},
    {"id": "RPT-003", "title": "Healthcare Digital Maturity Assessment", "client": "Pinnacle Healthcare Corp", "type": "assessment", "pages": 56, "ai_generated": False, "created": "2025-02-15", "downloads": 15},
    {"id": "RPT-004", "title": "EU Expansion Feasibility Report", "client": "Vortex Retail Solutions", "type": "feasibility", "pages": 44, "ai_generated": True, "created": "2025-03-05", "downloads": 6},
]

analytics = {
    "total_projects": 6,
    "active_projects": 4,
    "completed_projects": 1,
    "total_clients": 6,
    "active_clients": 5,
    "ai_insights_generated": 7,
    "actionable_insights": 4,
    "avg_confidence_score": 88.7,
    "client_satisfaction": 4.8,
    "revenue_generated": "$4.44M",
    "team_productivity": 87,
}

# ===================== SCHEMAS =====================

class HealthResponse(BaseModel):
    status: str
    app: str
    version: str

class InfoResponse(BaseModel):
    name: str
    tagline: str
    founded: str
    team_size: int
    headquarters: str
    ai_models_deployed: int
    fortune_500_clients: int
    avg_project_completion_time: str

class MetricsResponse(BaseModel):
    total_projects: int
    active_projects: int
    completed_projects: int
    total_clients: int
    active_clients: int
    ai_insights_generated: int
    actionable_insights: int
    avg_confidence_score: float
    client_satisfaction: float
    revenue_generated: str
    team_productivity: int

class ClientResponse(BaseModel):
    clients: List[Dict[str, Any]]

class ProjectResponse(BaseModel):
    projects: List[Dict[str, Any]]

class UserResponse(BaseModel):
    users: List[Dict[str, Any]]

class AIInsightResponse(BaseModel):
    insights: List[Dict[str, Any]]

class ReportResponse(BaseModel):
    reports: List[Dict[str, Any]]

class StatsResponse(BaseModel):
    total_reports: int
    total_insights: int
    active_users: int
    projects_by_status: Dict[str, int]
    insights_by_type: Dict[str, int]
    revenue_to_date: str

class RecentActivityItem(BaseModel):
    id: str
    type: str
    description: str
    timestamp: str
    client: Optional[str] = None
    user: Optional[str] = None

class RecentActivityResponse(BaseModel):
    activities: List[RecentActivityItem]

class ChartDataPoint(BaseModel):
    label: str
    value: float
    category: Optional[str] = None

class ChartDataResponse(BaseModel):
    chart_type: str
    title: str
    data: List[ChartDataPoint]

class CreateProjectRequest(BaseModel):
    name: str
    client: str
    deadline: str
    budget: str
    priority: str = "medium"

class CreateProjectResponse(BaseModel):
    id: str
    name: str
    client: str
    status: str
    progress: int
    deadline: str
    team_size: int
    ai_models_used: int
    budget: str
    priority: str

# ===================== ENDPOINTS =====================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="ok", app="NovaMind Strategy Hub", version="1.0.0")

@app.get("/api/info", response_model=InfoResponse)
async def get_info():
    return InfoResponse(
        name="NovaMind Consulting",
        tagline="Empowering Fortune 500 companies with AI-driven strategic intelligence",
        founded="2019",
        team_size=47,
        headquarters="New York, NY",
        ai_models_deployed=12,
        fortune_500_clients=5,
        avg_project_completion_time="4.2 months"
    )

@app.get("/api/metrics", response_model=MetricsResponse)
async def get_metrics():
    return MetricsResponse(**analytics)

@app.get("/api/clients", response_model=ClientResponse)
async def get_clients(status: Optional[str] = Query(None, regex="^(active|inactive)$")):
    if status:
        filtered = [c for c in clients if c["status"] == status]
        return ClientResponse(clients=filtered)
    return ClientResponse(clients=clients)

@app.get("/api/projects", response_model=ProjectResponse)
async def get_projects(status: Optional[str] = Query(None, regex="^(in_progress|completed|on_hold|planning)$")):
    if status:
        filtered = [p for p in projects if p["status"] == status]
        return ProjectResponse(projects=filtered)
    return ProjectResponse(projects=projects)

@app.post("/api/projects", response_model=CreateProjectResponse, status_code=201)
async def create_project(project: CreateProjectRequest):
    new_id = f"PRJ-{random.randint(107, 200)}"
    new_project = {
        "id": new_id,
        "name": project.name,
        "client": project.client,
        "status": "planning",
        "progress": 0,
        "deadline": project.deadline,
        "team_size": random.randint(3, 8),
        "ai_models_used": random.randint(1, 5),
        "budget": project.budget,
        "priority": project.priority
    }
    projects.append(new_project)
    return CreateProjectResponse(**new_project)

@app.get("/api/users", response_model=UserResponse)
async def get_users():
    return UserResponse(users=users)

@app.get("/api/ai-insights", response_model=AIInsightResponse)
async def get_ai_insights(status: Optional[str] = Query(None, regex="^(actionable|pending|reviewed)$")):
    if status:
        filtered = [i for i in ai_insights if i["status"] == status]
        return AIInsightResponse(insights=filtered)
    return AIInsightResponse(insights=ai_insights)

@app.get("/api/reports", response_model=ReportResponse)
async def get_reports():
    return ReportResponse(reports=reports)

@app.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    project_statuses = {}
    for p in projects:
        s = p["status"]
        project_statuses[s] = project_statuses.get(s, 0) + 1
    
    insight_types = {}
    for i in ai_insights:
        t = i["type"]
        insight_types[t] = insight_types.get(t, 0) + 1
    
    return StatsResponse(
        total_reports=len(reports),
        total_insights=len(ai_insights),
        active_users=sum(1 for u in users if u["projects_active"] > 0),
        projects_by_status=project_statuses,
        insights_by_type=insight_types,
        revenue_to_date="$4.44M"
    )

@app.get("/api/recent-activity", response_model=RecentActivityResponse)
async def get_recent_activity():
    activities = [
        RecentActivityItem(id="ACT-001", type="insight", description="AI Insight #AI-001 generated for GlobalTech Industries - Market Trend Prediction", timestamp="2025-03-07T10:30:00Z", client="GlobalTech Industries", user="Dr. Yuki Tanaka"),
        RecentActivityItem(id="ACT-002", type="project", description="Project PRJ-105 progress updated to 58% - EU Market Penetration", timestamp="2025-03-07T09:15:00Z", client="Vortex Retail Solutions", user="Priya Sharma"),
        RecentActivityItem(id="ACT-003", type="report", description="Report RPT-004 'EU Expansion Feasibility Report' published", timestamp="2025-03-05T14:00:00Z", client="Vortex Retail Solutions", user="Dr. Elena Vasquez"),
        RecentActivityItem(id="ACT-004", type="client", description="New client onboarded: Vortex Retail Solutions", timestamp="2025-03-01T08:00:00Z", client="Vortex Retail Solutions", user="Sarah Okafor"),
        RecentActivityItem(id="ACT-005", type="insight", description="AI Insight #AI-003 reviewed by client - Customer Sentiment Analysis", timestamp="2025-03-02T16:45:00Z", client="Vortex Retail Solutions", user="Marcus Chen"),
        RecentActivityItem(id="ACT-006", type="project", description="Project PRJ-102 completed - Digital Transformation Roadmap", timestamp="2025-01-20T12:00:00Z", client="Pinnacle Healthcare Corp", user="Dr. Elena Vasquez"),
        RecentActivityItem(id="ACT-007", type="milestone", description="Team reached 85% productivity milestone for Q1", timestamp="2025-03-06T11:30:00Z"),
        RecentActivityItem(id="ACT-008", type="insight", description="AI Insight #AI-007 generated for GlobalTech Industries - Supply Chain Disruption Warning", timestamp="2025-03-03T09:00:00Z", client="GlobalTech Industries", user="Dr. Yuki Tanaka"),
    ]
    return RecentActivityResponse(activities=activities)

@app.get("/api/chart-data", response_model=List[ChartDataResponse])
async def get_chart_data():
    return [
        ChartDataResponse(
            chart_type="bar",
            title="Project Progress by Client",
            data=[
                ChartDataPoint(label="GlobalTech Industries", value=72, category="APAC Market Entry"),
                ChartDataPoint(label="Pinnacle Healthcare", value=100, category="Digital Transformation"),
                ChartDataPoint(label="Apex Financial", value=45, category="Risk Assessment"),
                ChartDataPoint(label="Atlas Manufacturing", value=30, category="Supply Chain"),
                ChartDataPoint(label="Vortex Retail", value=58, category="EU Market Expansion"),
                ChartDataPoint(label="Meridian Energy", value=10, category="Sustainability Design"),
            ]
        ),
        ChartDataResponse(
            chart_type="line",
            title="AI Confidence Score Trend",
            data=[
                ChartDataPoint(label="Feb 15", value=86.3),
                ChartDataPoint(label="Feb 20", value=88.9),
                ChartDataPoint(label="Feb 25", value=91.2),
                ChartDataPoint(label="Mar 01", value=89.7),
                ChartDataPoint(label="Mar 05", value=93.8),
                ChartDataPoint(label="Mar 07", value=94.2),
            ]
        ),
        ChartDataResponse(
            chart_type="pie",
            title="Insights by Status",
            data=[
                ChartDataPoint(label="Actionable", value=4, category="active"),
                ChartDataPoint(label="Pending", value=1, category="pending"),
                ChartDataPoint(label="Reviewed", value=2, category="reviewed"),
            ]
        ),
        ChartDataResponse(
            chart_type="doughnut",
            title="Revenue Distribution by Client",
            data=[
                ChartDataPoint(label="GlobalTech", value=1.2, category="$1.2M"),
                ChartDataPoint(label="Apex Financial", value=0.85, category="$850K"),
                ChartDataPoint(label="Pinnacle Healthcare", value=0.98, category="$980K"),
                ChartDataPoint(label="Vortex Retail", value=0.62, category="$620K"),
                ChartDataPoint(label="Meridian Energy", value=0.45, category="$450K"),
                ChartDataPoint(label="Atlas Manufacturing", value=0.34, category="$340K"),
            ]
        ),
    ]

@app.get("/api/project/{project_id}")
async def get_project_detail(project_id: str):
    for project in projects:
        if project["id"] == project_id:
            # Return with more detailed mock data
            return {
                **project,
                "description": f"Strategic initiative for {project['client']} focusing on {project['name'].lower()}.",
                "key_risks": ["Market volatility", "Regulatory changes", "Competitive response"],
                "ai_recommendations": [
                    {"type": "entry_strategy", "confidence": 92.4, "description": "Phased market entry recommended"},
                    {"type": "partnership", "confidence": 87.1, "description": "Identify local strategic partners"},
                ],
                "team_members": [u for u in users if u["projects_active"] > 0][:3],
                "start_date": "2025-01-10",
                "last_updated": "2025-03-07",
            }
    raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

@app.post("/api/ai-insights/generate", status_code=201)
async def generate_ai_insight(client_id: str = Query(..., description="Client ID to generate insight for")):
    client_match = None
    for c in clients:
        if c["id"] == client_id:
            client_match = c
            break
    
    if not client_match:
        raise HTTPException(status_code=404, detail=f"Client {client_id} not found")
    
    insight_types = ["Market Trend Prediction", "Competitive Analysis", "Customer Sentiment Analysis", "Regulatory Risk Forecast", "Optimization Recommendation", "M&A Opportunity Alert", "Supply Chain Disruption Warning"]
    regions = ["North America", "APAC", "Europe", "Global"]
    
    new_insight = {
        "id": f"AI-{random.randint(8, 99):03d}",
        "type": random.choice(insight_types),
        "client": client_match["name"],
        "confidence": round(random.uniform(75.0, 98.0), 1),
        "impact": f"+{random.randint(5, 30)}% efficiency potential",
        "generated": current_time.strftime("%Y-%m-%d"),
        "status": random.choice(["actionable", "pending"]),
        "region": random.choice(regions)
    }
    ai_insights.append(new_insight)
    return new_insight

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)