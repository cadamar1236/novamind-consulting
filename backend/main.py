import os
import re
import uuid
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text, Column, String, Integer, Float, DateTime, Text, Boolean, Date
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
import uvicorn

DATABASE_URL = os.environ.get("DATABASE_URL", "")
COMPANY_SLUG = re.sub(r"[^a-z0-9_]", "_", os.environ.get("COMPANY_SLUG", "company").lower())
PORT = int(os.environ.get("COMPANY_PORT", 8000))

db_engine = None
SessionLocal = None

class Base(DeclarativeBase):
    pass

if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    db_engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        connect_args={"options": f"-csearch_path={COMPANY_SLUG},public"},
    )
    SessionLocal = sessionmaker(bind=db_engine)
    with db_engine.connect() as _conn:
        _conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{COMPANY_SLUG}"'))
        _conn.commit()

class Strategy(Base):
    __tablename__ = "strategies"
    __table_args__ = {"schema": COMPANY_SLUG}
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text)
    approach = Column(String)
    industry = Column(String)
    client_id = Column(String)
    roi_percentage = Column(Float)
    risk_level = Column(String)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Market(Base):
    __tablename__ = "markets"
    __table_args__ = {"schema": COMPANY_SLUG}
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    region = Column(String, nullable=False)
    industry = Column(String)
    market_size = Column(Float)
    growth_rate = Column(Float)
    entry_difficulty = Column(String)
    key_players = Column(Text)
    ai_insight = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Client(Base):
    __tablename__ = "clients"
    __table_args__ = {"schema": COMPANY_SLUG}
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    company = Column(String)
    industry = Column(String)
    revenue = Column(Float)
    employee_count = Column(Integer)
    contact_email = Column(String)
    contact_phone = Column(String)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

class Report(Base):
    __tablename__ = "reports"
    __table_args__ = {"schema": COMPANY_SLUG}
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    type = Column(String)
    client_id = Column(String)
    market_id = Column(String)
    strategy_id = Column(String)
    summary = Column(Text)
    key_findings = Column(Text)
    recommendations = Column(Text)
    status = Column(String, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

if db_engine:
    Base.metadata.create_all(db_engine)

def get_db():
    if not SessionLocal:
        raise HTTPException(status_code=503, detail="Database not available")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def _seed_if_empty(db: Session):
    if db.query(Strategy).count() == 0:
        strategies = [
            Strategy(
                id=str(uuid.uuid4()),
                name="AI-Powered Market Disruption",
                description="Leverage machine learning to identify and exploit market gaps in emerging economies",
                approach="Predictive analytics + scenario modeling",
                industry="Technology",
                roi_percentage=340.0,
                risk_level="Moderate",
                status="active"
            ),
            Strategy(
                id=str(uuid.uuid4()),
                name="Digital Transformation Roadmap",
                description="End-to-end digital transformation strategy for traditional manufacturing firms",
                approach="Agile transformation + AI automation",
                industry="Manufacturing",
                roi_percentage=280.0,
                risk_level="Low",
                status="active"
            ),
            Strategy(
                id=str(uuid.uuid4()),
                name="Healthcare Market Entry Framework",
                description="Regulatory-aware market entry strategy for health-tech companies entering European markets",
                approach="Compliance-first expansion",
                industry="Healthcare",
                roi_percentage=220.0,
                risk_level="High",
                status="draft"
            ),
            Strategy(
                id=str(uuid.uuid4()),
                name="Sustainable Energy Transition Plan",
                description="Strategic roadmap for energy companies transitioning to renewable sources",
                approach="Phased decarbonization + carbon credit optimization",
                industry="Energy",
                roi_percentage=190.0,
                risk_level="Moderate",
                status="review"
            ),
        ]
        db.add_all(strategies)

        markets = [
            Market(
                id=str(uuid.uuid4()),
                region="Southeast Asia",
                industry="Technology",
                market_size=850000000000.0,
                growth_rate=14.5,
                entry_difficulty="Medium",
                key_players="Grab, Gojek, Sea Limited, Alibaba",
                ai_insight="Digital adoption rate accelerating 3x faster than global average"
            ),
            Market(
                id=str(uuid.uuid4()),
                region="Nordic Countries",
                industry="Healthcare",
                market_size=320000000000.0,
                growth_rate=8.2,
                entry_difficulty="High",
                key_players="Novo Nordisk, AstraZeneca, Getinge",
                ai_insight="Strong regulatory framework but high adoption of digital health solutions"
            ),
            Market(
                id=str(uuid.uuid4()),
                region="Middle East",
                industry="Energy",
                market_size=1200000000000.0,
                growth_rate=6.8,
                entry_difficulty="Medium",
                key_players="Saudi Aramco, ADNOC, Qatar Energy",
                ai_insight="Government diversification mandates creating new opportunities in renewables"
            ),
            Market(
                id=str(uuid.uuid4()),
                region="Latin America",
                industry="Financial Services",
                market_size=450000000000.0,
                growth_rate=11.3,
                entry_difficulty="Medium",
                key_players="Nubank, Mercado Pago, PicPay",
                ai_insight="Fintech adoption outpacing traditional banking 4:1 in unbanked populations"
            ),
        ]
        db.add_all(markets)

        clients = [
            Client(
                id=str(uuid.uuid4()),
                name="Sarah Chen",
                company="TechVentures Global",
                industry="Technology",
                revenue=2500000000.0,
                employee_count=3400,
                contact_email="schen@techventures.com",
                contact_phone="+1-415-555-0123",
                status="active"
            ),
            Client(
                id=str(uuid.uuid4()),
                name="Marcus Rodriguez",
                company="MediCorp International",
                industry="Healthcare",
                revenue=5800000000.0,
                employee_count=12000,
                contact_email="mrodriguez@medicorp.com",
                contact_phone="+1-617-555-0456",
                status="active"
            ),
            Client(
                id=str(uuid.uuid4()),
                name="Emma Williams",
                company="GreenFuture Energy",
                industry="Energy",
                revenue=8900000000.0,
                employee_count=8500,
                contact_email="ewilliams@greenfuture.com",
                contact_phone="+44-20-7946-0789",
                status="review"
            ),
            Client(
                id=str(uuid.uuid4()),
                name="Dr. Akira Tanaka",
                company="FinServe Asia",
                industry="Financial Services",
                revenue=12000000000.0,
                employee_count=15000,
                contact_email="atanaka@finserve.com",
                contact_phone="+65-6234-5678",
                status="active"
            ),
        ]
        db.add_all(clients)

        reports = [
            Report(
                id=str(uuid.uuid4()),
                title="SE Asia Tech Market Entry Analysis",
                type="Market Analysis",
                market_id=markets[0].id,
                client_id=clients[0].id,
                summary="Comprehensive analysis of Southeast Asian technology market with AI-powered competitive intelligence",
                key_findings="Three key market gaps identified in ed-tech, logistics automation, and digital banking",
                recommendations="Partner with local logistics providers and pursue regulatory sandbox programs",
                status="completed"
            ),
            Report(
                id=str(uuid.uuid4()),
                title="Healthcare Regulatory Compliance Framework",
                type="Strategy Report",
                market_id=markets[1].id,
                client_id=clients[1].id,
                summary="EU-wide regulatory compliance strategy for health-tech market expansion",
                key_findings="MDR certification timeline can be compressed by 40% using AI-assisted documentation",
                recommendations="Begin parallel certification processes in Germany and Netherlands as test markets",
                status="draft"
            ),
            Report(
                id=str(uuid.uuid4()),
                title="Renewable Energy Investment Roadmap",
                type="Investment Strategy",
                market_id=markets[2].id,
                client_id=clients[2].id,
                summary="Strategic investment plan for transitioning 60% of portfolio to renewable assets by 2030",
                key_findings="Solar and wind investments show 22% higher IRR than traditional energy in current conditions",
                recommendations="Phased approach: 30% allocation to solar in Year 1, 40% to wind in Year 2, 30% to emerging tech Year 3",
                status="review"
            ),
            Report(
                id=str(uuid.uuid4()),
                title="Digital Banking Disruption Strategy",
                type="Competitive Analysis",
                market_id=markets[3].id,
                client_id=clients[3].id,
                summary="Analysis of fintech disruptors in Latin America and defensive strategy for traditional banks",
                key_findings="Nubank's AI-based credit scoring model reduces default rates by 35% vs traditional methods",
                recommendations="Acquire or partner with leading fintech platform; invest in AI-native banking infrastructure",
                status="completed"
            ),
        ]
        db.add_all(reports)

        db.commit()
        print(f"[{COMPANY_SLUG}] Seeded initial data")

if db_engine:
    with SessionLocal() as db:
        _seed_if_empty(db)

app = FastAPI(title="NovaMind Consulting API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class StrategyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    approach: Optional[str] = None
    industry: Optional[str] = None
    client_id: Optional[str] = None
    roi_percentage: Optional[float] = None
    risk_level: Optional[str] = None
    status: Optional[str] = "active"

class StrategyResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    approach: Optional[str] = None
    industry: Optional[str] = None
    client_id: Optional[str] = None
    roi_percentage: Optional[float] = None
    risk_level: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

class MarketCreate(BaseModel):
    region: str
    industry: Optional[str] = None
    market_size: Optional[float] = None
    growth_rate: Optional[float] = None
    entry_difficulty: Optional[str] = None
    key_players: Optional[str] = None
    ai_insight: Optional[str] = None

class MarketResponse(BaseModel):
    id: str
    region: str
    industry: Optional[str] = None
    market_size: Optional[float] = None
    growth_rate: Optional[float] = None
    entry_difficulty: Optional[str] = None
    key_players: Optional[str] = None
    ai_insight: Optional[str] = None
    created_at: datetime

class ClientCreate(BaseModel):
    name: str
    company: Optional[str] = None
    industry: Optional[str] = None
    revenue: Optional[float] = None
    employee_count: Optional[int] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    status: Optional[str] = "active"

class ClientResponse(BaseModel):
    id: str
    name: str
    company: Optional[str] = None
    industry: Optional[str] = None
    revenue: Optional[float] = None
    employee_count: Optional[int] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    status: str
    created_at: datetime

class ReportCreate(BaseModel):
    title: str
    type: Optional[str] = None
    client_id: Optional[str] = None
    market_id: Optional[str] = None
    strategy_id: Optional[str] = None
    summary: Optional[str] = None
    key_findings: Optional[str] = None
    recommendations: Optional[str] = None
    status: Optional[str] = "draft"

class ReportResponse(BaseModel):
    id: str
    title: str
    type: Optional[str] = None
    client_id: Optional[str] = None
    market_id: Optional[str] = None
    strategy_id: Optional[str] = None
    summary: Optional[str] = None
    key_findings: Optional[str] = None
    recommendations: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

# Health & Info
@app.get("/health")
def health_check():
    return {"status": "ok", "schema": COMPANY_SLUG, "db": bool(db_engine)}

@app.get("/api/info")
def company_info():
    return {
        "name": "NovaMind Consulting",
        "tagline": "AI-Powered Strategy for Fortune 500",
        "description": "A consulting firm that uses AI to provide Fortune 500 companies with data-driven business strategy and market entry recommendations.",
        "founded": "2019",
        "headquarters": "San Francisco, CA",
        "team_size": 180,
        "specialties": ["AI Strategy", "Market Entry", "Data Analytics", "Digital Transformation"],
        "industries": ["Technology", "Healthcare", "Energy", "Financial Services"],
        "notable_clients": 42,
        "success_rate": 94.7
    }

# Strategies endpoints
@app.get("/api/strategies", response_model=list[StrategyResponse])
def list_strategies(db: Session = Depends(get_db)):
    return db.query(Strategy).order_by(Strategy.created_at.desc()).all()

@app.post("/api/strategies", response_model=StrategyResponse, status_code=status.HTTP_201_CREATED)
def create_strategy(strategy: StrategyCreate, db: Session = Depends(get_db)):
    db_strategy = Strategy(
        id=str(uuid.uuid4()),
        name=strategy.name,
        description=strategy.description,
        approach=strategy.approach,
        industry=strategy.industry,
        client_id=strategy.client_id,
        roi_percentage=strategy.roi_percentage,
        risk_level=strategy.risk_level,
        status=strategy.status
    )
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    return db_strategy

@app.get("/api/strategies/{strategy_id}", response_model=StrategyResponse)
def get_strategy(strategy_id: str, db: Session = Depends(get_db)):
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy

@app.put("/api/strategies/{strategy_id}", response_model=StrategyResponse)
def update_strategy(strategy_id: str, strategy: StrategyCreate, db: Session = Depends(get_db)):
    db_strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not db_strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    for key, value in strategy.dict(exclude_unset=True).items():
        setattr(db_strategy, key, value)
    db_strategy.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_strategy)
    return db_strategy

@app.delete("/api/strategies/{strategy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_strategy(strategy_id: str, db: Session = Depends(get_db)):
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    db.delete(strategy)
    db.commit()

# Markets endpoints
@app.get("/api/markets", response_model=list[MarketResponse])
def list_markets(db: Session = Depends(get_db)):
    return db.query(Market).order_by(Market.created_at.desc()).all()

@app.post("/api/markets", response_model=MarketResponse, status_code=status.HTTP_201_CREATED)
def create_market(market: MarketCreate, db: Session = Depends(get_db)):
    db_market = Market(
        id=str(uuid.uuid4()),
        region=market.region,
        industry=market.industry,
        market_size=market.market_size,
        growth_rate=market.growth_rate,
        entry_difficulty=market.entry_difficulty,
        key_players=market.key_players,
        ai_insight=market.ai_insight
    )
    db.add(db_market)
    db.commit()
    db.refresh(db_market)
    return db_market

@app.get("/api/markets/{market_id}", response_model=MarketResponse)
def get_market(market_id: str, db: Session = Depends(get_db)):
    market = db.query(Market).filter(Market.id == market_id).first()
    if not market:
        raise HTTPException(status_code=404, detail="Market not found")
    return market

@app.put("/api/markets/{market_id}", response_model=MarketResponse)
def update_market(market_id: str, market: MarketCreate, db: Session = Depends(get_db)):
    db_market = db.query(Market).filter(Market.id == market_id).first()
    if not db_market:
        raise HTTPException(status_code=404, detail="Market not found")
    for key, value in market.dict(exclude_unset=True).items():
        setattr(db_market, key, value)
    db.commit()
    db.refresh(db_market)
    return db_market

@app.delete("/api/markets/{market_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_market(market_id: str, db: Session = Depends(get_db)):
    market = db.query(Market).filter(Market.id == market_id).first()
    if not market:
        raise HTTPException(status_code=404, detail="Market not found")
    db.delete(market)
    db.commit()

# Clients endpoints
@app.get("/api/clients", response_model=list[ClientResponse])
def list_clients(db: Session = Depends(get_db)):
    return db.query(Client).order_by(Client.created_at.desc()).all()

@app.post("/api/clients", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    db_client = Client(
        id=str(uuid.uuid4()),
        name=client.name,
        company=client.company,
        industry=client.industry,
        revenue=client.revenue,
        employee_count=client.employee_count,
        contact_email=client.contact_email,
        contact_phone=client.contact_phone,
        status=client.status
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.get("/api/clients/{client_id}", response_model=ClientResponse)
def get_client(client_id: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@app.put("/api/clients/{client_id}", response_model=ClientResponse)
def update_client(client_id: str, client: ClientCreate, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    for key, value in client.dict(exclude_unset=True).items():
        setattr(db_client, key, value)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.delete("/api/clients/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()

# Reports endpoints
@app.get("/api/reports", response_model=list[ReportResponse])
def list_reports(db: Session = Depends(get_db)):
    return db.query(Report).order_by(Report.created_at.desc()).all()

@app.post("/api/reports", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    db_report = Report(
        id=str(uuid.uuid4()),
        title=report.title,
        type=report.type,
        client_id=report.client_id,
        market_id=report.market_id,
        strategy_id=report.strategy_id,
        summary=report.summary,
        key_findings=report.key_findings,
        recommendations=report.recommendations,
        status=report.status
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@app.get("/api/reports/{report_id}", response_model=ReportResponse)
def get_report(report_id: str, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@app.put("/api/reports/{report_id}", response_model=ReportResponse)
def update_report(report_id: str, report: ReportCreate, db: Session = Depends(get_db)):
    db_report = db.query(Report).filter(Report.id == report_id).first()
    if not db_report:
        raise HTTPException(status_code=404, detail="Report not found")
    for key, value in report.dict(exclude_unset=True).items():
        setattr(db_report, key, value)
    db_report.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_report)
    return db_report

@app.delete("/api/reports/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(report_id: str, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    db.delete(report)
    db.commit()

# Metrics endpoint
@app.get("/api/metrics")
def get_metrics(db: Session = Depends(get_db)):
    strategies_count = db.query(Strategy).count()
    markets_count = db.query(Market).count()
    clients_count = db.query(Client).count()
    reports_count = db.query(Report).count()
    
    active_clients = db.query(Client).filter(Client.status == "active").count()
    completed_reports = db.query(Report).filter(Report.status == "completed").count()
    
    avg_roi = db.query(Strategy.roi_percentage).filter(Strategy.roi_percentage.isnot(None)).all()
    avg_roi_value = sum(r[0] for r in avg_roi) / len(avg_roi) if avg_roi else 0
    
    total_market_value = db.query(Market.market_size).filter(Market.market_size.isnot(None)).all()
    total_market = sum(m[0] for m in total_market_value) if total_market_value else 0
    
    return {
        "total_strategies": strategies_count,
        "total_markets": markets_count,
        "total_clients": clients_count,
        "total_reports": reports_count,
        "active_clients": active_clients,
        "completed_reports": completed_reports,
        "average_roi_percentage": round(avg_roi_value, 2),
        "total_market_value_analyzed": round(total_market, 2),
        "success_rate": 94.7
    }

# Dashboard endpoints
@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    total_clients = db.query(Client).count()
    active_strategies = db.query(Strategy).filter(Strategy.status == "active").count()
    completed_reports = db.query(Report).filter(Report.status == "completed").count()
    
    clients_by_industry = {}
    for client in db.query(Client.industry, Client.id).all():
        industry = client.industry or "Unknown"
        if industry not in clients_by_industry:
            clients_by_industry[industry] = 0
        clients_by_industry[industry] += 1
    
    return {
        "total_clients": total_clients,
        "active_strategies": active_strategies,
        "completed_reports": completed_reports,
        "clients_by_industry": clients_by_industry,
        "engagement_rate": 87.3,
        "client_retention": 92.1
    }

@app.get("/api/recent-activity")
def get_recent_activity(db: Session = Depends(get_db)):
    recent_reports = db.query(Report).order_by(Report.created_at.desc()).limit(5).all()
    recent_clients = db.query(Client).order_by(Client.created_at.desc()).limit(3).all()
    
    activities = []
    
    for report in recent_reports:
        activities.append({
            "type": "report",
            "action": "created",
            "title": f"Report: {report.title}",
            "status": report.status,
            "timestamp": report.created_at.isoformat()
        })
    
    for client in recent_clients:
        activities.append({
            "type": "client",
            "action": "onboarded",
            "title": f"Client: {client.name} - {client.company}",
            "status": client.status,
            "timestamp": client.created_at.isoformat()
        })
    
    activities.sort(key=lambda x: x["timestamp"], reverse=True)
    return activities[:10]

@app.get("/api/chart-data")
def get_chart_data(db: Session = Depends(get_db)):
    strategies_by_risk = {}
    for strategy in db.query(Strategy.risk_level, Strategy.id).all():
        risk = strategy.risk_level or "Unspecified"
        if risk not in strategies_by_risk:
            strategies_by_risk[risk] = 0
        strategies_by_risk[risk] += 1
    
    markets_by_difficulty = {}
    for market in db.query(Market.entry_difficulty, Market.id).all():
        difficulty = market.entry_difficulty or "Unspecified"
        if difficulty not in markets_by_difficulty:
            markets_by_difficulty[difficulty] = 0
        markets_by_difficulty[difficulty] += 1
    
    roi_by_industry = []
    for ind in db.query(Strategy.industry).distinct().all():
        if ind[0]:
            avg = db.query(Strategy.roi_percentage).filter(
                Strategy.industry == ind[0],
                Strategy.roi_percentage.isnot(None)
            ).all()
            if avg:
                avg_val = sum(a[0] for a in avg) / len(avg)
                roi_by_industry.append({"industry": ind[0], "average_roi": round(avg_val, 2)})
    
    return {
        "strategies_by_risk_level": strategies_by_risk,
        "markets_by_entry_difficulty": markets_by_difficulty,
        "average_roi_by_industry": roi_by_industry,
        "monthly_engagement": [
            {"month": "Jan", "value": 42},
            {"month": "Feb", "value": 55},
            {"month": "Mar", "value": 48},
            {"month": "Apr", "value": 63},
            {"month": "May", "value": 71},
            {"month": "Jun", "value": 58}
        ]
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)