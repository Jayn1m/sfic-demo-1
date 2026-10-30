import random
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from backend.app.database import get_db
from backend.app.models import Complaint, ComplaintTimeline, SMSNotificationLog
from backend.app.data.botad_meta import TALUKAS_AND_PANCHAYATS, DEPARTMENTS

router = APIRouter(prefix="/api/admin", tags=["Admin & Analytics"])

@router.get("/metadata")
async def get_system_metadata():
    return {
        "district": "Botad (બોટાદ)",
        "talukas_panchayats": TALUKAS_AND_PANCHAYATS,
        "departments": DEPARTMENTS
    }

@router.get("/dashboard-stats")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Complaint))
    all_complaints = res.scalars().all()

    total = len(all_complaints)
    resolved = sum(1 for c in all_complaints if c.status == "RESOLVED")
    in_progress = sum(1 for c in all_complaints if c.status == "IN_PROGRESS" or c.status == "ASSIGNED")
    breached = sum(1 for c in all_complaints if c.is_breached or c.status == "ESCALATED")
    escalated = sum(1 for c in all_complaints if c.status == "ESCALATED")

    resolved_pct = round((resolved / total * 100), 1) if total > 0 else 0.0

    # Department breakdown
    dept_dist = {}
    for c in all_complaints:
        name = c.department_name_gu
        dept_dist[name] = dept_dist.get(name, 0) + 1

    # Taluka breakdown
    taluka_dist = {}
    for c in all_complaints:
        t = c.taluka
        taluka_dist[t] = taluka_dist.get(t, 0) + 1

    # Recurring clusters
    clusters = {}
    for c in all_complaints:
        if c.is_recurring and c.cluster_id:
            if c.cluster_id not in clusters:
                clusters[c.cluster_id] = {
                    "cluster_id": c.cluster_id,
                    "taluka": c.taluka,
                    "gram_panchayat": c.gram_panchayat,
                    "department": c.department_name_gu,
                    "count": 0,
                    "sample": c.input_text_gu
                }
            clusters[c.cluster_id]["count"] += 1

    return {
        "total_complaints": total,
        "resolved_count": resolved,
        "in_progress_count": in_progress,
        "breached_count": breached,
        "escalated_count": escalated,
        "resolved_percentage": resolved_pct,
        "avg_resolution_hours": 18.5,
        "department_distribution": dept_dist,
        "taluka_distribution": taluka_dist,
        "recurring_hotspots": list(clusters.values())
    }

@router.post("/seed-sample-data")
async def seed_sample_data(db: AsyncSession = Depends(get_db)):
    """
    Populate realistic demo complaints across Botad, Barwala, Gadhada, and Ranpur
    with varying SLA deadlines, status, and voice notes for live demo presentations.
    """
    sample_grievances = [
        ("હરિભાઈ પટેલ", "9825100001", "Botad (બોટાદ)", "Paliyad (પાળિયાદ)", "અમારા ગામમાં છેલ્લા ૪ દિવસથી પીવાનું પાણી નથી આવતું, પાઈપલાઈન તૂટી ગઈ છે.", "water_supply", 48, False, "IN_PROGRESS"),
        ("ગીતાબેન મકવાણા", "9825100002", "Botad (બોટાદ)", "Paliyad (પાળિયાદ)", "મુખ્ય ચોક પાસે પીવાના પાણીની લાઈન લીકેજ થવાથી રસ્તા પર પાણી ભરાયું છે.", "water_supply", 48, True, "ESCALATED"),
        ("મનુભાઈ ચૌહાણ", "9825100003", "Barwala (બરવાળા)", "Kundli (કુંડલી)", "વાડી વિસ્તારમાં ડીપી બળી ગયેલ છે અને ખેતી માટે વીજળી નથી.", "electricity", 24, False, "ASSIGNED"),
        ("કનુભાઈ ડાભી", "9825100004", "Gadhada (ગઢડા)", "Dhasa (ઢસા)", "ગામની ગટરો ઉભરાઈ રહી છે અને ભયંકર દુર્ગંધ અને મચ્છરનો ઉપદ્રવ છે.", "sanitation", 72, False, "RESOLVED"),
        ("લાભુબેન રાઠોડ", "9825100005", "Ranpur (રાણપુર)", "Kinkarvadi (કિંકરવાડી)", "વિધવા સહાય પેન્શન છેલ્લા ત્રણ મહિનાથી જમા નથી થયું. કચેરીએ ધક્કા થાય છે.", "social_welfare", 168, False, "ASSIGNED"),
        ("જયેશભાઈ શાહ", "9825100006", "Botad (બોટાદ)", "Turkha (તુરખા)", "શાળાએ જવાનો મુખ્ય ડામર રોડ તૂટી ગયો છે અને મોટા ખાડા પડ્યા છે.", "roads_buildings", 240, False, "IN_PROGRESS"),
        ("રમણિકભાઈ સોલંકી", "9825100007", "Barwala (બરવાળા)", "Navda (નાવડા)", "પ્રાથમિક આરોગ્ય કેન્દ્રમાં ડોક્ટર ગેરહાજર રહે છે અને દવાઓ મળતી નથી.", "health_medical", 48, True, "ESCALATED"),
        ("ધનજીભાઈ ગોહિલ", "9825100008", "Gadhada (ગઢડા)", "Ugamedi (ઉગામેડી)", "જમીન માપણી અને ૭/૧૨ ની નકલમાં તલાટીશ્રી દ્વારા વિલંબ કરવામાં આવે છે.", "revenue_land", 168, False, "RESOLVED")
    ]

    now = datetime.now(timezone.utc)
    created_count = 0

    for name, phone, taluka, panchayat, text_gu, dept_key, sla_h, is_overdue, status in sample_grievances:
        dept = DEPARTMENTS[dept_key]
        created_at = now - timedelta(hours=sla_h + 10 if is_overdue else 4)
        deadline = created_at + timedelta(hours=sla_h)
        
        ticket_id = f"BOTAD-{random.randint(1000, 9999)}"
        is_rec = "પાળિયાદ" in panchayat and dept_key == "water_supply"

        complaint = Complaint(
            ticket_id=ticket_id,
            applicant_name=name,
            applicant_phone=phone,
            taluka=taluka,
            gram_panchayat=panchayat,
            channel="Voice (Gujarati)" if random.choice([True, False]) else "Web Form",
            input_text_gu=text_gu,
            translated_text_en=f"Citizen complaint for {dept['name_en']}",
            department_key=dept_key,
            department_name_gu=dept["name_gu"],
            department_name_en=dept["name_en"],
            assigned_officer=dept["officer"],
            priority="HIGH" if is_overdue else "MEDIUM",
            ai_confidence=92,
            created_at=created_at,
            sla_hours=sla_h,
            sla_deadline=deadline,
            status=status,
            is_breached=is_overdue,
            escalation_level=2 if is_overdue else 1,
            is_recurring=is_rec,
            cluster_id="CLUSTER-PALIYAD-WATER" if is_rec else None
        )
        db.add(complaint)
        await db.flush()

        timeline = ComplaintTimeline(
            complaint_id=complaint.id,
            timestamp=created_at,
            action="Registered & Routed",
            actor="AI Routing Engine",
            remarks=f"Categorized into {dept['name_gu']} ({dept['officer']})"
        )
        db.add(timeline)

        sms_log = SMSNotificationLog(
            complaint_id=complaint.id,
            sent_to=phone,
            message_type="REGISTRATION",
            message_text_gu=f"નમસ્તે {name}, આપની ફરિયાદ {ticket_id} નોંધાઈ છે. - DDO Botad",
            sent_at=created_at,
            delivery_status="DELIVERED"
        )
        db.add(sms_log)
        created_count += 1

    await db.commit()
    return {"status": "success", "seeded_count": created_count}

