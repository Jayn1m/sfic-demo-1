"""
Botad District Administration Metadata
District: Botad (બોટાદ)
Talukas: Botad, Barwala, Gadhada, Ranpur
Departments, Branches, Exact Officers, and SLAs (in hours)
"""

TALUKAS_AND_PANCHAYATS = {
    "Botad (બોટાદ)": [
        "Haddad (હડદડ)", "Samadhiyala (સમાધિયાળા)", "Kariyani (કારિયાણી)", 
        "Sherthali (શેરથળી)", "Nagalpar (નાગલપર)", "Paliyad (પાળિયાદ)",
        "Turkha (તુરખા)", "Tajpar (તાજપર)", "Rangpur (રંગપુર)", "Dhankanoli (ઢંકણિયાળી)"
    ],
    "Barwala (બરવાળા)": [
        "Kundli (કુંડલી)", "Rampur (રામપુર)", "Navda (નાવડા)", 
        "Bhimnath (ભીમનાથ)", "Polarpur (પોળારપુર)", "Rojid (રોજીદ)",
        "Dhadhuka (ઢાઢુકા)", "Kapuriya (કાપુરીયા)"
    ],
    "Gadhada (ગઢડા)": [
        "Dhasa (ઢસા)", "Ugamedi (ઉગામેડી)", "Ningala (નીંગાળા)", 
        "Itariya (ઇટારીયા)", "Patna (પાટણા)", "Vavdi (વાવડી)",
        "Gadhali (ગઢાળી)", "Vikaliya (વિકળિયા)"
    ],
    "Ranpur (રાણપુર)": [
        "Kinkarvadi (કિંકરવાડી)", "Dharpipla (ધરપીપળા)", "Bhudana (ભુદાણા)", 
        "Jaliya (જાળીયા)", "Kharad (ખારાડ)", "Baraniya (બારણીયા)",
        "Alau (અલાઉ)", "Bhandar (ભંડાર)"
    ]
}

DEPARTMENTS = {
    "electricity": {
        "name_en": "Electricity & Power Supply (PGVCL)",
        "name_gu": "વીજળી અને પાવર સપ્લાય (PGVCL)",
        "sla_hours": 24,
        "default_officer": "Deputy Engineer, PGVCL Botad Division",
        "taluka_officers": {
            "Botad (બોટાદ)": "Deputy Engineer, PGVCL City & Rural Sub-Division Botad (પીજીવીસીએલ બોટાદ)",
            "Barwala (બરવાળા)": "Deputy Engineer, PGVCL Barwala Sub-Division (પીજીવીસીએલ બરવાળા)",
            "Gadhada (ગઢડા)": "Deputy Engineer, PGVCL Gadhada Sub-Division (પીજીવીસીએલ ગઢડા)",
            "Ranpur (રાણપુર)": "Deputy Engineer, PGVCL Ranpur Sub-Division (પીજીવીસીએલ રાણપુર)"
        },
        "strong_phrases": [
            "લાઈટો નથી", "લાઈટ નથી", "લાઈટ ગુલ", "વીજળી નથી", "પાવર નથી", "પાવર કટ", "પાવરકટ",
            "કરંટ નથી", "કરંટ લાગે", "ડીપી બળી", "ડીપી ઉડી", "ટ્રાન્સફોર્મર બળી", "થાંભલો પડી",
            "થાંભલો નમી", "વાયર તૂટી", "તાર તૂટી", "વીજળીનો ધાંધિયો", "શોર્ટ સર્કિટ", "વોલ્ટેજ ઓછા",
            "વોલ્ટેજ નથી", "મીટર બળી", "બત્તી ગુલ", "લાઈટ બંધ", "no power", "light nathi", "power cut",
            "current nathi", "transformer issue", "electricity problem", "pgvcl complaint"
        ],
        "keywords": [
            "વીજળી", "વીજ", "લાઈટ", "લાઈટો", "લાઈટ્સ", "પાવર", "કરંટ", "શોક", "ડીપી", "dp",
            "ટ્રાન્સફોર્મર", "થાંભલો", "થાંભલા", "થાંભલાઓ", "વાયર", "વાયરો", "વાયરિંગ", "તાર",
            "સ્પાર્ક", "સ્પાર્કિંગ", "અંધારું", "બત્તી", "મીટર", "બિલ", "બીલ", "વોલ્ટેજ",
            "વોલ્ટ", "ડીમ", "ફ્યુઝ", "બળી", "પીજીવીસીએલ", "pgvcl", "લાઈનમેન", "સબસ્ટેશન",
            "ખેતી લાઈટ", "થ્રી ફેઝ", "સિંગલ ફેઝ", "લાઈટિંગ", "light", "lights", "power", "current",
            "electricity", "transformer", "pole", "wire", "voltage", "fuse", "blackout", "outage"
        ]
    },
    "water_supply": {
        "name_en": "Water Supply & Drinking Water",
        "name_gu": "પાણી પુરવઠા અને પીવાનું પાણી",
        "sla_hours": 48,
        "default_officer": "Executive Engineer, GWSSB / Taluka Water Branch",
        "taluka_officers": {
            "Botad (બોટાદ)": "Executive Engineer, GWSSB Division Botad (ગુજરાત પાણી પુરવઠા બોર્ડ બોટાદ)",
            "Barwala (બરવાળા)": "Deputy Executive Engineer, GWSSB Sub-Division Barwala",
            "Gadhada (ગઢડા)": "Deputy Executive Engineer, GWSSB Sub-Division Gadhada",
            "Ranpur (રાણપુર)": "Deputy Executive Engineer, GWSSB Sub-Division Ranpur"
        },
        "strong_phrases": [
            "પીવાનું પાણી", "પાણી નથી", "પાણી આવતું નથી", "પાઈપલાઈન લીક", "પાઈપલાઈન તૂટી",
            "નળમાં પાણી", "બોરવેલ બંધ", "હેન્ડપંપ બગડી", "ગંદુ પાણી", "પાણીની તંગી", "ટેન્કર મોકલો",
            "સંપ ખાલી", "હવાડો ખાલી", "ટાંકી ભરાતી નથી", "drinking water", "water leak", "pipeline damage",
            "no drinking water", "pani nathi"
        ],
        "keywords": [
            "પાણી", "પીવાનું", "જળ", "પાઈપ", "પાઈપલાઈન", "નળ", "નળજોડાણ", "હેન્ડપંપ", "બોર",
            "બોરવેલ", "કૂવો", "મોટર", "સંપ", "ટાંકી", "હવાડો", "લીકેજ", "ગંદુ", "વાલ્વ",
            "પમ્પિંગ", "જળસ્ત્રોત", "ડંકી", "ફિલ્ટર", "તંગી", "ટેન્કર", "water", "drinking",
            "pipeline", "pipe", "tap", "borewell", "handpump", "leakage", "leak", "tank", "valve", "pump"
        ]
    },
    "sanitation": {
        "name_en": "Sanitation & Drainage",
        "name_gu": "સ્વચ્છતા અને ગટર વ્યવસ્થા",
        "sla_hours": 72,
        "default_officer": "District Health Officer / Taluka Sanitation Officer",
        "taluka_officers": {
            "Botad (બોટાદ)": "Chief Officer, Botad Nagarpalika / Taluka Sanitation Officer Botad",
            "Barwala (બરવાળા)": "Taluka Sanitation Officer & TDO Barwala (સ્વચ્છ ભારત મિશન)",
            "Gadhada (ગઢડા)": "Chief Officer / Taluka Sanitation Officer Gadhada",
            "Ranpur (રાણપુર)": "Taluka Sanitation Officer & TDO Ranpur"
        },
        "strong_phrases": [
            "ગટર ઉભરાય", "ગટરનું પાણી", "ગટર બ્લોક", "કચરાના ઢગલા", "કચરો ઉપાડતા નથી", "સંડાસ બ્લોક",
            "જાહેર શૌચાલય", "ગંદકી બહુ છે", "દુર્ગંધ આવે છે", "બદબૂ આવે છે", "દવા છંટકાવ કરો",
            "મચ્છરનો ઉપદ્રવ", "gutter overflow", "garbage cleaning", "drainage blocked"
        ],
        "keywords": [
            "ગટર", "ગટરો", "કચરો", "કચરા", "કચરાપેટી", "ગંદકી", "સફાઈ", "સાફ", "ઉકરડો",
            "નાળા", "નાળી", "બદબૂ", "દુર્ગંધ", "વાસ", "શૌચાલય", "સંડાસ", "ટોયલેટ", "માખી",
            "મચ્છર", "રોગચાળો", "જંતુનાશક", "છંટકાવ", "સફાઈ કામદાર", "પ્લાસ્ટિક", "નિકાલ",
            "drainage", "gutter", "garbage", "trash", "waste", "cleanliness", "toilet", "mosquito", "smell"
        ]
    },
    "roads_buildings": {
        "name_en": "Roads & Civil Infrastructure",
        "name_gu": "માર્ગ અને મકાન (રસ્તા)",
        "sla_hours": 240,
        "default_officer": "Executive Engineer, R&B (Panchayat) Division Botad",
        "taluka_officers": {
            "Botad (બોટાદ)": "Executive Engineer, R&B (Panchayat) Division Botad (માર્ગ અને મકાન શાખા)",
            "Barwala (બરવાળા)": "Deputy Executive Engineer, R&B Sub-Division Barwala",
            "Gadhada (ગઢડા)": "Deputy Executive Engineer, R&B Sub-Division Gadhada",
            "Ranpur (રાણપુર)": "Deputy Executive Engineer, R&B Sub-Division Ranpur"
        },
        "strong_phrases": [
            "રસ્તો તૂટી ગયો", "રસ્તા પર ખાડા", "મોટા ખાડા પડ્યા", "ડામર રોડ તૂટી", "સીસી રોડ મંજૂર",
            "પેવર બ્લોક બેસી", "પુલ તૂટી ગયો", "રસ્તો ધોવાઈ ગયો", "વાહન ચાલી શકતા નથી", "સ્પીડ બ્રેકર બનાવો",
            "road damage", "pothole problem", "broken bridge", "paver block"
        ],
        "keywords": [
            "રસ્તો", "રસ્તા", "રોડ", "માર્ગ", "ખાડા", "ખાડો", "ખાડાઓ", "ડામર", "મેટલ",
            "સીસી રોડ", "પુલ", "બ્રિજ", "નાળું", "પેવર", "બ્લોક", "તૂટેલો", "ધોવાણ",
            "સમારકામ", "ફૂટપાથ", "સ્પીડ બ્રેકર", "બમ્પ", "પુલિયો", "કાચો રસ્તો", "road",
            "roads", "street", "pothole", "potholes", "bridge", "asphalt", "tar", "cc road", "pavement"
        ]
    },
    "social_welfare": {
        "name_en": "Social Welfare & Pensions",
        "name_gu": "સામાજિક સુરક્ષા અને પેન્શન",
        "sla_hours": 168,
        "default_officer": "District Social Welfare Officer (DDO Branch)",
        "taluka_officers": {
            "Botad (બોટાદ)": "District Social Welfare Officer, DDO Office Botad (સમાજ કલ્યાણ શાખા)",
            "Barwala (બરવાળા)": "Social Welfare Inspector & TDO Branch Barwala",
            "Gadhada (ગઢડા)": "Social Welfare Inspector & TDO Branch Gadhada",
            "Ranpur (રાણપુર)": "Social Welfare Inspector & TDO Branch Ranpur"
        },
        "strong_phrases": [
            "વિધવા સહાય", "વૃદ્ધ પેન્શન", "દિવ્યાંગ સહાય", "પેન્શન જમા નથી", "પેન્શન આવ્યું નથી",
            "રેશન કાર્ડ", "રેશનકાર્ડ માં નામ", "અનાજ મળતું નથી", "આયુષ્માન કાર્ડ", "ગંગા સ્વરૂપા",
            "કુંવરબાઈનું મામેરું", "સહાયના હપ્તા", "widow pension", "old age pension", "ration card"
        ],
        "keywords": [
            "પેન્શન", "પેંશન", "વૃદ્ધ", "વૃદ્ધાવસ્થા", "વિધવા", "દિવ્યાંગ", "વિકલાંગ", "અપંગ",
            "સહાય", "યોજના", "આયુષ્માન", "રેશન", "રેશનકાર્ડ", "કૂપન", "અનાજ", "હપ્તો",
            "ખાતામાં", "ગંગા સ્વરૂપા", "મામેરું", "કલ્યાણ", "pension", "widow", "elderly", "disability",
            "handicap", "ration", "welfare", "scheme", "subsidy", "ayushman"
        ]
    },
    "revenue_land": {
        "name_en": "Revenue & Panchayat Land Records",
        "name_gu": "મહેસૂલ અને જમીન બાબત",
        "sla_hours": 168,
        "default_officer": "Mamlatdar & Chitnis to Collector / TDO Botad",
        "taluka_officers": {
            "Botad (બોટાદ)": "Mamlatdar & Taluka Development Officer (TDO) Botad (મહેસૂલ શાખા)",
            "Barwala (બરવાળા)": "Mamlatdar & Taluka Development Officer Barwala",
            "Gadhada (ગઢડા)": "Mamlatdar & Taluka Development Officer Gadhada",
            "Ranpur (રાણપુર)": "Mamlatdar & Taluka Development Officer Ranpur"
        },
        "strong_phrases": [
            "૭/૧૨ ની નકલ", "૮-અ ની નકલ", "જમીન માપણી", "ગેરકાયદે દબાણ", "તલાટી સહી નથી કરતા",
            "વારસાઈ નોંધ", "ખેતરમાં જવાનો રસ્તો દબાવ્યો", "સીમાડો તોડી નાખ્યો", "હક પત્રક નોંધ",
            "ખેડૂત નોંધણી", "7/12 record", "land encroachment", "talati signature"
        ],
        "keywords": [
            "જમીન", "ખેતર", "૭/૧૨", "૭ ૧૨", "8a", "૮-અ", "૮ અ", "તલાટી", "તલાટી કમ મંત્રી",
            "મામલતદાર", "મહેસૂલ", "દબાણ", "સીમાડો", "માપણી", "વારસાઈ", "નોંધ", "એન્ટ્રી",
            "નકલ", "ખેડૂત", "દસ્તાવેજ", "સર્વે નંબર", "હક પત્રક", "પંચાયત દફતર", "land", "revenue",
            "talati", "mamlatdar", "encroachment", "survey", "7/12", "8-a", "farm"
        ]
    },
    "health_medical": {
        "name_en": "Health & Medical Services",
        "name_gu": "આરોગ્ય અને તબીબી સેવાઓ",
        "sla_hours": 48,
        "default_officer": "Chief District Health Officer (CDHO) Botad",
        "taluka_officers": {
            "Botad (બોટાદ)": "Chief District Health Officer (CDHO) & Medical Superintendent Botad",
            "Barwala (બરવાળા)": "Taluka Health Officer (THO) & Medical Officer CHC Barwala",
            "Gadhada (ગઢડા)": "Taluka Health Officer (THO) & Medical Officer CHC Gadhada",
            "Ranpur (રાણપુર)": "Taluka Health Officer (THO) & Medical Officer CHC Ranpur"
        },
        "strong_phrases": [
            "ડોક્ટર હાજર નથી", "દવા મળતી નથી", "પીએચસી બંધ", "૧૦૮ એમ્બ્યુલન્સ", "હોસ્પિટલમાં સારવાર",
            "દવાખાને કોઈ નથી", "પ્રસૂતિ સહાય", "ડેન્ગ્યુ તાવ", "મેલેરિયા", "doctor absent",
            "no medicines", "phc closed", "ambulance delay"
        ],
        "keywords": [
            "દવાખાનું", "હોસ્પિટલ", "પીએચસી", "phc", "સીએચસી", "chc", "આરોગ્ય કેન્દ્ર", "ડોક્ટર",
            "તબીબ", "દવા", "દવાઓ", "ઇન્જેક્શન", "એમ્બ્યુલન્સ", "૧૦૮", "108", "નર્સ",
            "પ્રસૂતિ", "બીમારી", "તાવ", "રોગ", "ડેન્ગ્યુ", "મેલેરિયા", "સારવાર", "hospital",
            "doctor", "clinic", "medicine", "medicines", "ambulance", "treatment", "health", "nurse"
        ]
    },
    "education": {
        "name_en": "Primary Education & Schools",
        "name_gu": "પ્રાથમિક શિક્ષણ અને શાળાઓ",
        "sla_hours": 120,
        "default_officer": "District Primary Education Officer (DPEO) Botad",
        "taluka_officers": {
            "Botad (બોટાદ)": "District Primary Education Officer (DPEO) & TPEO Botad",
            "Barwala (બરવાળા)": "Taluka Primary Education Officer (TPEO) Barwala",
            "Gadhada (ગઢડા)": "Taluka Primary Education Officer (TPEO) Gadhada",
            "Ranpur (રાણપુર)": "Taluka Primary Education Officer (TPEO) Ranpur"
        },
        "strong_phrases": [
            "શાળામાં શિક્ષક નથી", "શિક્ષકો સમયસર આવતા નથી", "ઓરડા જર્જરિત", "મધ્યાહન ભોજન ખરાબ",
            "ચોપડા મળ્યા નથી", "યુનિફોર્મ મળ્યો નથી", "આંગણવાડી બંધ", "પીવાનું પાણી શાળામાં નથી",
            "teacher absent", "school room damaged", "midday meal issue"
        ],
        "keywords": [
            "શાળા", "શાળાઓ", "નિશાળ", "સ્કૂલ", "શિક્ષક", "શિક્ષકો", "માસ્તર", "ઓરડા",
            "ઓરડો", "ક્લાસરૂમ", "મધ્યાહન ભોજન", "ભોજન", "ચોપડા", "પુસ્તક", "પુસ્તકો",
            "યુનિફોર્મ", "પ્રાથમિક શાળા", "બાલમંદિર", "આંગણવાડી", "વિદ્યાર્થી", "વિદ્યાર્થીઓ",
            "ભણતર", "શિક્ષણ", "school", "schools", "teacher", "teachers", "classroom", "midday meal", "book"
        ]
    },
    "general_admin": {
        "name_en": "District Grievance & General Administration",
        "name_gu": "સામાન્ય વહીવટ અને જિલ્લા ફરિયાદ નિવારણ કક્ષ",
        "sla_hours": 72,
        "default_officer": "Resident Additional Collector (RAC) & Chitnis to DDO Botad",
        "taluka_officers": {
            "Botad (બોટાદ)": "Resident Additional Collector (RAC) & Chitnis to DDO Botad",
            "Barwala (બરવાળા)": "Taluka Development Officer (TDO) Barwala",
            "Gadhada (ગઢડા)": "Taluka Development Officer (TDO) Gadhada",
            "Ranpur (રાણપુર)": "Taluka Development Officer (TDO) Ranpur"
        },
        "strong_phrases": [
            "અરજી કરી હતી", "જવાબ નથી મળતો", "ધક્કા થાય છે", "અધિકારી ગેરહાજર", "સરપંચ સાંભળતા નથી",
            "પંચાયતમાં કામ નથી થતું", "DDO સાહેબને અરજી", "સ્વાગત ફરિયાદ"
        ],
        "keywords": [
            "વહીવટ", "કચેરી", "અરજી", "ફરિયાદ", "સરપંચ", "પંચાયત", "ડીડીઓ", "ddo", "ટીડીઓ", "tdo",
            "કલેક્ટર", "collector", "સ્વાગત", "swagat", "જનસેવા", "દાખલો", "પ્રમાણપત્ર", "certificate"
        ]
    }
}

def get_assigned_officer_for_taluka(dept_key: str, taluka_name: str) -> str:
    """
    Returns the exact designated branch officer for the specific Taluka.
    """
    dept = DEPARTMENTS.get(dept_key)
    if not dept:
        return "District Grievance Redressal Officer, DDO Office Botad"
    
    # Try exact taluka match
    taluka_officers = dept.get("taluka_officers", {})
    if taluka_name in taluka_officers:
        return taluka_officers[taluka_name]
    
    # Try partial name match (e.g. 'Botad' in 'Botad (બોટાદ)')
    for t_key, officer in taluka_officers.items():
        clean_key = t_key.split(' ')[0].strip().lower()
        if clean_key in taluka_name.lower():
            return officer
            
    return dept.get("default_officer", "Concerned Branch Officer, DDO Botad")
