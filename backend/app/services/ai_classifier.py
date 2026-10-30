import os
import json
from google import genai
from backend.app.data.botad_meta import DEPARTMENTS

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and api_key.strip() and api_key != "your_gemini_api_key_here":
        try:
            return genai.Client(api_key=api_key)
        except Exception as e:
            print(f"Warning: Failed to initialize Gemini Client: {e}")
            return None
    return None

def fallback_rule_based_classification(text_gu: str) -> dict:
    """
    Robust rule-based keyword matcher for Gujarati citizen grievances.
    Ensures 100% offline reliability for hackathons.
    """
    text_lower = text_gu.lower()
    best_dept = "water_supply"
    max_matches = -1

    for dept_key, info in DEPARTMENTS.items():
        matches = sum(1 for kw in info["keywords"] if kw in text_lower)
        if matches > max_matches:
            max_matches = matches
            best_dept = dept_key

    # Priority determination
    priority = "MEDIUM"
    emergency_kws = ["આગ", "અકસ્માત", "કરંટ", "શોક", "તાત્કાલિક", "મૃત્યુ", "ઇમરજન્સી", "danger", "urgent", "emergency"]
    high_kws = ["પીવાનું પાણી", "તૂટી ગઈ", "બંધ છે", "૪ દિવસ", "૫ દિવસ", "અઠવાડિયું", "ગંદકી", "બીમારી"]
    
    if any(kw in text_lower for kw in emergency_kws):
        priority = "EMERGENCY"
    elif any(kw in text_lower for kw in high_kws):
        priority = "HIGH"

    dept_info = DEPARTMENTS[best_dept]
    return {
        "department_key": best_dept,
        "department_name_gu": dept_info["name_gu"],
        "department_name_en": dept_info["name_en"],
        "assigned_officer": dept_info["officer"],
        "priority": priority,
        "sla_hours": dept_info["sla_hours"],
        "ai_confidence": 88 if max_matches > 0 else 70,
        "summary_en": f"Citizen grievance regarding {dept_info['name_en']}"
    }

async def classify_and_route_complaint(text_gu: str, taluka: str, gram_panchayat: str) -> dict:
    """
    Classify Gujarati grievance using Gemini AI, with automatic fallback.
    """
    client = get_gemini_client()
    if client:
        prompt = f"""
You are the AI Redressal Routing Engine for the District Development Office (DDO) - Botad, Gujarat.
A citizen filed the following complaint in Gujarati:
Location: Taluka: {taluka}, Gram Panchayat: {gram_panchayat}
Complaint Text (Gujarati): "{text_gu}"

Available Departments:
- water_supply: Water Supply, drinking water, pipeline leaks, borewell, handpump
- electricity: Electricity, PGVCL, pole, transformer, wire sparking, power outage
- sanitation: Sanitation, drainage overflow, gutters, village waste cleaning
- roads_buildings: Roads, potholes, CC roads, bridges, asphalt
- social_welfare: Pensions (Vrudh Sahay, Vidhva Sahay), Divyang aid, government social schemes
- revenue_land: Land records, 7/12, talati dispute, encroachment
- health_medical: PHC, government hospital, doctor absence, medicine shortage
- education: Primary school, teacher absence, classroom condition, mid-day meal

Output strictly a valid JSON object with the following fields:
{{
  "department_key": "one of the keys listed above",
  "priority": "EMERGENCY" | "HIGH" | "MEDIUM" | "LOW",
  "confidence_percentage": integer between 70 and 99,
  "summary_en": "one concise English sentence describing the problem",
  "recommended_action": "action to be taken by the assigned branch officer"
}}
"""
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            result = json.loads(response.text)
            dept_key = result.get("department_key", "water_supply")
            if dept_key not in DEPARTMENTS:
                dept_key = "water_supply"

            dept_info = DEPARTMENTS[dept_key]
            return {
                "department_key": dept_key,
                "department_name_gu": dept_info["name_gu"],
                "department_name_en": dept_info["name_en"],
                "assigned_officer": dept_info["officer"],
                "priority": result.get("priority", "MEDIUM"),
                "sla_hours": dept_info["sla_hours"],
                "ai_confidence": result.get("confidence_percentage", 95),
                "summary_en": result.get("summary_en", f"Grievance regarding {dept_info['name_en']}")
            }
        except Exception as e:
            print(f"Gemini API error, using intelligent fallback: {e}")

    # Fallback to keyword matching
    return fallback_rule_based_classification(text_gu)

