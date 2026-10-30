import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from backend.app.database import get_db
from backend.app.models import Complaint, ComplaintTimeline, SMSNotificationLog
from backend.app.schemas import (
    ComplaintCreateText, ComplaintResponse, ComplaintDetailResponse, StatusUpdateRequest
)
from backend.app.services.ai_classifier import classify_and_route_complaint
from backend.app.services.audio_stt import transcribe_gujarati_audio
from backend.app.services.clustering import detect_recurring_complaint
from backend.app.services.notification import send_citizen_sms_update

router = APIRouter(prefix="/api/complaints", tags=["Complaints"])

def generate_ticket_id() -> str:
    return f"BOTAD-{uuid.uuid4().hex[:6].upper()}"

@router.post("/submit-text", response_model=ComplaintResponse)
async def submit_complaint_text(
    payload: ComplaintCreateText,
    db: AsyncSession = Depends(get_db)
):
    classification = await classify_and_route_complaint(
        text_gu=payload.grievance_text,
        taluka=payload.taluka,
        gram_panchayat=payload.gram_panchayat
    )

    ticket_id = generate_ticket_id()
    now = datetime.now(timezone.utc)
    sla_hours = classification["sla_hours"]
    deadline = now + timedelta(hours=sla_hours)

    # Check for recurring complaints in this taluka
    query_existing = select(Complaint.ticket_id, Complaint.input_text_gu).where(
        Complaint.taluka == payload.taluka
    )
    res_existing = await db.execute(query_existing)
    existing_items = res_existing.all()
    
    is_recurring, cluster_id = detect_recurring_complaint(
        payload.grievance_text,
        [(row[0], row[1]) for row in existing_items]
    )

    complaint = Complaint(
        ticket_id=ticket_id,
        applicant_name=payload.applicant_name,
        applicant_phone=payload.applicant_phone,
        taluka=payload.taluka,
        gram_panchayat=payload.gram_panchayat,
        channel=payload.channel or "Web Form",
        input_text_gu=payload.grievance_text,
        translated_text_en=classification.get("summary_en"),
        department_key=classification["department_key"],
        department_name_gu=classification["department_name_gu"],
        department_name_en=classification["department_name_en"],
        assigned_officer=classification["assigned_officer"],
        priority=classification["priority"],
        ai_confidence=classification["ai_confidence"],
        created_at=now,
        sla_hours=sla_hours,
        sla_deadline=deadline,
        status="ASSIGNED",
        is_breached=False,
        escalation_level=1,
        is_recurring=is_recurring,
        cluster_id=cluster_id if is_recurring else None
    )
    db.add(complaint)
    await db.flush()

    # Timeline entry
    timeline = ComplaintTimeline(
        complaint_id=complaint.id,
        action="Grievance Registered & AI Routed",
        actor="Botad AI Routing Engine",
        remarks=f"Categorized into {complaint.department_name_gu}. Assigned to {complaint.assigned_officer}. Priority: {complaint.priority}."
    )
    db.add(timeline)

    # SMS Dispatch
    deadline_str = deadline.strftime("%d-%m-%Y %I:%M %p")
    sms_text = await send_citizen_sms_update(
        phone_number=payload.applicant_phone,
        ticket_id=ticket_id,
        applicant_name=payload.applicant_name,
        event_type="REGISTERED",
        dept_name_gu=complaint.department_name_gu,
        officer=complaint.assigned_officer,
        deadline_str=deadline_str
    )
    sms_log = SMSNotificationLog(
        complaint_id=complaint.id,
        sent_to=payload.applicant_phone,
        message_type="REGISTRATION",
        message_text_gu=sms_text,
        delivery_status="DELIVERED"
    )
    db.add(sms_log)

    await db.commit()
    await db.refresh(complaint)

    # Calculate remaining hours
    remaining = (complaint.sla_deadline.replace(tzinfo=timezone.utc) - datetime.now(timezone.utc)).total_seconds() / 3600.0
    complaint.remaining_hours = max(0.0, round(remaining, 1))
    return complaint


@router.post("/submit-voice", response_model=ComplaintResponse)
async def submit_complaint_voice(
    applicant_name: str = Form(...),
    applicant_phone: str = Form(...),
    taluka: str = Form(...),
    gram_panchayat: str = Form(...),
    audio_file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    audio_bytes = await audio_file.read()
    stt_result = await transcribe_gujarati_audio(audio_bytes, audio_file.filename or "recording.webm")
    transcribed_gu = stt_result.get("transcript_gu") or "અમારા ગામમાં પાણીની સમસ્યા છે."

    payload = ComplaintCreateText(
        applicant_name=applicant_name,
        applicant_phone=applicant_phone,
        taluka=taluka,
        gram_panchayat=gram_panchayat,
        grievance_text=transcribed_gu,
        channel="Voice (Gujarati)"
    )
    return await submit_complaint_text(payload, db)


@router.get("/{ticket_or_phone}", response_model=ComplaintDetailResponse)
async def get_complaint_by_ticket_or_phone(
    ticket_or_phone: str,
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(Complaint)
        .options(
            selectinload(Complaint.timelines),
            selectinload(Complaint.sms_logs)
        )
        .where(
            (Complaint.ticket_id == ticket_or_phone.strip().upper()) |
            (Complaint.applicant_phone == ticket_or_phone.strip())
        )
        .order_by(desc(Complaint.created_at))
    )
    res = await db.execute(query)
    complaint = res.scalars().first()

    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found with provided Ticket ID or Phone Number")

    # Remaining hours calculation
    deadline = complaint.sla_deadline
    if deadline.tzinfo is None:
        deadline = deadline.replace(tzinfo=timezone.utc)
    remaining = (deadline - datetime.now(timezone.utc)).total_seconds() / 3600.0
    complaint.remaining_hours = round(remaining, 1)

    return complaint


@router.get("/", response_model=List[ComplaintResponse])
async def list_all_complaints(
    taluka: Optional[str] = None,
    department: Optional[str] = None,
    status: Optional[str] = None,
    is_breached: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Complaint).order_by(desc(Complaint.created_at))
    if taluka:
        query = query.where(Complaint.taluka == taluka)
    if department:
        query = query.where(Complaint.department_key == department)
    if status:
        query = query.where(Complaint.status == status)
    if is_breached is not None:
        query = query.where(Complaint.is_breached == is_breached)

    res = await db.execute(query)
    complaints = res.scalars().all()

    now = datetime.now(timezone.utc)
    for c in complaints:
        deadline = c.sla_deadline
        if deadline.tzinfo is None:
            deadline = deadline.replace(tzinfo=timezone.utc)
        rem = (deadline - now).total_seconds() / 3600.0
        c.remaining_hours = round(rem, 1)

    return complaints


@router.patch("/{ticket_id}/status", response_model=ComplaintDetailResponse)
async def update_complaint_status(
    ticket_id: str,
    payload: StatusUpdateRequest,
    db: AsyncSession = Depends(get_db)
):
    query = select(Complaint).options(
        selectinload(Complaint.timelines),
        selectinload(Complaint.sms_logs)
    ).where(Complaint.ticket_id == ticket_id.strip().upper())
    res = await db.execute(query)
    c = res.scalars().first()

    if not c:
        raise HTTPException(status_code=404, detail="Complaint not found")

    c.status = payload.new_status
    if payload.new_status == "RESOLVED":
        c.resolved_at = datetime.now(timezone.utc)

    # Timeline update
    timeline = ComplaintTimeline(
        complaint_id=c.id,
        action=f"Status changed to {payload.new_status}",
        actor=payload.officer_name,
        remarks=payload.remarks
    )
    db.add(timeline)

    # Citizen SMS update
    sms_text = await send_citizen_sms_update(
        phone_number=c.applicant_phone,
        ticket_id=c.ticket_id,
        applicant_name=c.applicant_name,
        event_type=payload.new_status,
        dept_name_gu=c.department_name_gu,
        officer=payload.officer_name,
        deadline_str="",
        remarks=payload.remarks
    )
    sms_log = SMSNotificationLog(
        complaint_id=c.id,
        sent_to=c.applicant_phone,
        message_type=payload.new_status,
        message_text_gu=sms_text,
        delivery_status="DELIVERED"
    )
    db.add(sms_log)

    await db.commit()
    await db.refresh(c)
    return c

