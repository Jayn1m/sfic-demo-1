from datetime import datetime, timezone
from sqlalchemy import select
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from backend.app.database import async_session
from backend.app.models import Complaint, ComplaintTimeline, SMSNotificationLog
from backend.app.services.notification import send_citizen_sms_update

scheduler = AsyncIOScheduler()

async def check_sla_breaches_and_escalate():
    """
    Periodic job that checks for complaints that exceeded their SLA deadline.
    Flags them as is_breached=True, bumps escalation_level, and triggers SMS alerts.
    """
    now = datetime.now(timezone.utc)
    async with async_session() as session:
        # Query open complaints past deadline that haven't been escalated to Level 3 yet
        query = select(Complaint).where(
            Complaint.status.in_(["ASSIGNED", "IN_PROGRESS"]),
            Complaint.sla_deadline < now,
            Complaint.is_breached == False
        )
        result = await session.execute(query)
        delayed_complaints = result.scalars().all()

        for c in delayed_complaints:
            c.is_breached = True
            c.status = "ESCALATED"
            c.escalation_level = min(3, c.escalation_level + 1)
            
            level_name = "TDO (Taluka Development Officer)" if c.escalation_level == 2 else "DDO (District Development Officer - Botad)"
            
            # Add timeline entry
            timeline = ComplaintTimeline(
                complaint_id=c.id,
                action="SLA Breached & Escalated",
                actor="System SLA Engine",
                remarks=f"Time deadline expired. Escalated to {level_name} for priority resolution."
            )
            session.add(timeline)

            # Send SMS Alert
            msg = await send_citizen_sms_update(
                phone_number=c.applicant_phone,
                ticket_id=c.ticket_id,
                applicant_name=c.applicant_name,
                event_type="ESCALATED",
                dept_name_gu=c.department_name_gu,
                officer=level_name,
                deadline_str="સમયમર્યાદા સમાપ્ત",
                remarks=f"Escalated to {level_name}"
            )
            
            sms_log = SMSNotificationLog(
                complaint_id=c.id,
                sent_to=c.applicant_phone,
                message_type="DELAY_ALERT",
                message_text_gu=msg,
                delivery_status="DELIVERED"
            )
            session.add(sms_log)

        if delayed_complaints:
            await session.commit()
            print(f"[SLA ENGINE] Checked SLAs: {len(delayed_complaints)} overdue complaints escalated!")

def start_sla_scheduler():
    scheduler.add_job(check_sla_breaches_and_escalate, "interval", seconds=30)
    scheduler.start()

