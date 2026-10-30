from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class ComplaintCreateText(BaseModel):
    applicant_name: str = Field(..., example="રમેશભાઈ પટેલ")
    applicant_phone: str = Field(..., example="9876543210")
    taluka: str = Field(..., example="Botad (બોટાદ)")
    gram_panchayat: str = Field(..., example="Paliyad (પાળિયાદ)")
    grievance_text: str = Field(..., example="અમારા ગામમાં છેલ્લા ૪ દિવસથી પીવાનું પાણી નથી આવતું અને પાઈપલાઈન તૂટી ગઈ છે.")
    channel: Optional[str] = "Web Form"

class ComplaintResponse(BaseModel):
    id: int
    ticket_id: str
    applicant_name: str
    applicant_phone: str
    taluka: str
    gram_panchayat: str
    channel: str
    input_text_gu: str
    translated_text_en: Optional[str] = None
    department_key: str
    department_name_gu: str
    department_name_en: str
    assigned_officer: str
    priority: str
    ai_confidence: int
    created_at: datetime
    sla_hours: int
    sla_deadline: datetime
    status: str
    is_breached: bool
    escalation_level: int
    is_recurring: bool
    remaining_hours: Optional[float] = None

    class Config:
        from_attributes = True

class TimelineItem(BaseModel):
    id: int
    timestamp: datetime
    action: str
    actor: str
    remarks: Optional[str] = None

    class Config:
        from_attributes = True

class SMSLogItem(BaseModel):
    id: int
    sent_to: str
    message_type: str
    message_text_gu: str
    sent_at: datetime
    delivery_status: str

    class Config:
        from_attributes = True

class ComplaintDetailResponse(ComplaintResponse):
    timelines: List[TimelineItem] = []
    sms_logs: List[SMSLogItem] = []

class StatusUpdateRequest(BaseModel):
    new_status: str = Field(..., example="RESOLVED") # IN_PROGRESS, RESOLVED, ESCALATED
    officer_name: str = Field(..., example="Executive Engineer, GWSSB")
    remarks: str = Field(..., example="પાઈપલાઈન સમારકામ પૂર્ણ થયું છે. પાણી પુરવઠો શરૂ કરાયો છે.")

class DashboardStats(BaseModel):
    total_complaints: int
    resolved_count: int
    in_progress_count: int
    breached_count: int
    escalated_count: int
    resolved_percentage: float
    avg_resolution_hours: float
    department_distribution: dict
    taluka_distribution: dict
    recurring_hotspots: list

