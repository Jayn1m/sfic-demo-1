from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String(50), unique=True, index=True, nullable=False)
    
    # Applicant details
    applicant_name = Column(String(100), nullable=False)
    applicant_phone = Column(String(20), nullable=False, index=True)
    taluka = Column(String(50), nullable=False)
    gram_panchayat = Column(String(100), nullable=False)
    
    # Input source & content
    channel = Column(String(50), default="Web Form")  # Voice (Gujarati), Web Form, SWAGAT, Phone
    input_text_gu = Column(Text, nullable=False)
    translated_text_en = Column(Text, nullable=True)
    voice_audio_path = Column(String(255), nullable=True)
    
    # AI Classification & Routing
    department_key = Column(String(50), nullable=False)
    department_name_gu = Column(String(100), nullable=False)
    department_name_en = Column(String(100), nullable=False)
    assigned_officer = Column(String(150), nullable=False)
    priority = Column(String(20), default="MEDIUM")  # EMERGENCY, HIGH, MEDIUM, LOW
    ai_confidence = Column(Integer, default=90)
    
    # SLA & Deadlines
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    sla_hours = Column(Integer, default=48)
    sla_deadline = Column(DateTime, nullable=False)
    resolved_at = Column(DateTime, nullable=True)
    status = Column(String(30), default="ASSIGNED")  # ASSIGNED, IN_PROGRESS, RESOLVED, ESCALATED
    is_breached = Column(Boolean, default=False)
    escalation_level = Column(Integer, default=1)  # 1: Panchayat/Branch, 2: TDO, 3: DDO
    
    # Repeated / Recurring clustering
    cluster_id = Column(String(50), nullable=True)
    is_recurring = Column(Boolean, default=False)
    
    # Timeline updates & SMS audit
    timelines = relationship("ComplaintTimeline", back_populates="complaint", cascade="all, delete-orphan")
    sms_logs = relationship("SMSNotificationLog", back_populates="complaint", cascade="all, delete-orphan")


class ComplaintTimeline(Base):
    __tablename__ = "complaint_timelines"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    action = Column(String(100), nullable=False)
    actor = Column(String(100), default="AI Routing Engine")
    remarks = Column(Text, nullable=True)
    
    complaint = relationship("Complaint", back_populates="timelines")


class SMSNotificationLog(Base):
    __tablename__ = "sms_notification_logs"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    sent_to = Column(String(20), nullable=False)
    message_type = Column(String(50), nullable=False)  # REGISTRATION, ROUTED, DELAY_ALERT, RESOLVED
    message_text_gu = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    delivery_status = Column(String(30), default="DELIVERED")

    complaint = relationship("Complaint", back_populates="sms_logs")

