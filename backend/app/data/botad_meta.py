"""
Botad District Administration Metadata
District: Botad (બોટાદ)
Talukas: Botad, Barwala, Gadhada, Ranpur
Departments, Branches, and Service Level Agreements (SLAs in hours)
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
    "water_supply": {
        "name_en": "Water Supply & Drinking Water",
        "name_gu": "પાણી પુરવઠા અને પીવાનું પાણી",
        "sla_hours": 48,
        "officer": "Executive Engineer, GWSSB / Taluka Water Branch",
        "keywords": ["પાણી", "પીવાનું પાણી", "પાઈપલાઈન", "મોટર", "હેન્ડપંપ", "લીકેજ", "borwell", "water", "pipeline", "leakage", "drinking water"]
    },
    "electricity": {
        "name_en": "Electricity & Power Supply (PGVCL)",
        "name_gu": "વીજળી અને પાવર સપ્લાય (PGVCL)",
        "sla_hours": 24,
        "officer": "Deputy Engineer, PGVCL Botad Division",
        "keywords": ["વીજળી", "લાઈટ", "થાંભલો", "ડીપી", "વાયર", "પાવર કટ", "ટ્રાન્સફોર્મર", "light", "electricity", "transformer", "pole", "wire"]
    },
    "sanitation": {
        "name_en": "Sanitation & Drainage",
        "name_gu": "સ્વચ્છતા અને ગટર વ્યવસ્થા",
        "sla_hours": 72,
        "officer": "District Health Officer / Taluka Sanitation Officer",
        "keywords": ["ગટર", "કચરો", "સફાઈ", "ગંદકી", "શૌચાલય", "ઉકરડો", "drainage", "gutter", "garbage", "waste", "cleanliness", "toilet"]
    },
    "roads_buildings": {
        "name_en": "Roads & Civil Infrastructure",
        "name_gu": "માર્ગ અને મકાન (રસ્તા)",
        "sla_hours": 240,
        "officer": "Executive Engineer, R&B Department Botad",
        "keywords": ["રસ્તો", "ખાડા", "ડામર", "પુલ", "સીસી રોડ", "માર્ગ", "road", "pothole", "bridge", "pavement", "asphalt"]
    },
    "social_welfare": {
        "name_en": "Social Welfare & Pensions",
        "name_gu": "સામાજિક સુરક્ષા અને પેન્શન",
        "sla_hours": 168,
        "officer": "District Social Welfare Officer (DDO Branch)",
        "keywords": ["પેન્શન", "વૃદ્ધ પેન્શન", "વિધવા સહાય", "દિવ્યાંગ", "સહાય", "યોજના", "pension", "widow", "handicap", "scheme", "benefit", "nsap"]
    },
    "revenue_land": {
        "name_en": "Revenue & Panchayat Land Records",
        "name_gu": "મહેસૂલ અને જમીન બાબત",
        "sla_hours": 168,
        "officer": "Mamlatdar & Chitnis to Collector / TDO Botad",
        "keywords": ["જમીન", "દબાણ", "૭/૧૨", "૮-અ", "તલાટી", "મહેસૂલ", "નકલ", "land", "encroachment", "talati", "record"]
    },
    "health_medical": {
        "name_en": "Health & Medical Services",
        "name_gu": "આરોગ્ય અને તબીબી સેવાઓ",
        "sla_hours": 48,
        "officer": "Chief District Health Officer (CDHO) Botad",
        "keywords": ["દવાખાનું", "હોસ્પિટલ", "ડોક્ટર", "દવા", "આરોગ્ય કેન્દ્ર", "પીએચસી", "hospital", "phc", "doctor", "medicine"]
    },
    "education": {
        "name_en": "Primary Education & Schools",
        "name_gu": "પ્રાથમિક શિક્ષણ અને શાળાઓ",
        "sla_hours": 120,
        "officer": "District Primary Education Officer (DPEO) Botad",
        "keywords": ["શાળા", "શિક્ષક", "ઓરડા", "મધ્યાહન ભોજન", "પુસ્તક", "school", "teacher", "classroom", "midday meal"]
    }
}

