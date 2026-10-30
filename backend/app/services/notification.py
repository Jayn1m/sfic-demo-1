import sys

async def send_citizen_sms_update(
    phone_number: str,
    ticket_id: str,
    applicant_name: str,
    event_type: str,
    dept_name_gu: str,
    officer: str,
    deadline_str: str,
    remarks: str = ""
) -> str:
    """
    Sends or simulates an automated SMS/WhatsApp update in Gujarati to the applicant.
    """
    if event_type == "REGISTERED":
        msg = (
            f"નમસ્તે {applicant_name}, આપની ફરિયાદ નં. {ticket_id} સફળતાપૂર્વક નોંધાઈ છે. "
            f"તેને {dept_name_gu} શાખા ({officer}) ને મોકલવામાં આવી છે. "
            f"નિરાકરણની સમયમર્યાદા: {deadline_str}. - DDO Botad Redressal Cell"
        )
    elif event_type == "RESOLVED":
        msg = (
            f"નમસ્તે {applicant_name}, આપની ફરિયાદ નં. {ticket_id} નું નિરાકરણ કરવામાં આવ્યું છે. "
            f"નોંધ: {remarks or 'કામગીરી પૂર્ણ કરવામાં આવી છે.'} - DDO Botad Redressal Cell"
        )
    elif event_type == "ESCALATED":
        msg = (
            f"અગત્યની સૂચના: આપની ફરિયાદ નં. {ticket_id} સમયમર્યાદા પૂર્ણ થવાથી ઉચ્ચ અધિકારીશ્રી (TDO/DDO બોટાદ) "
            f"કક્ષાએ એસ્કેલેટ કરવામાં આવી છે. તાત્કાલિક પગલાં લેવામાં આવી રહ્યા છે."
        )
    else:
        msg = (
            f"નમસ્તે {applicant_name}, ફરિયાદ નં. {ticket_id} પર નવી પ્રગતિ: {remarks}. "
            f"- DDO Botad"
        )

    # Safe UTF-8 console output for Windows cmd/powershell
    try:
        print(f"\n================ [SMS/WHATSAPP DISPATCH] ================")
        print(f"TO: +91 {phone_number}")
        print(f"EVENT: {event_type}")
        print(f"MESSAGE: {msg.encode('utf-8', errors='replace').decode('utf-8')}")
        print(f"==========================================================\n")
    except Exception:
        pass
    
    return msg

