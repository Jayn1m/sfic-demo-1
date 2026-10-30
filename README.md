# Botad District Grievance Redressal & SLA Tracking AI Platform
### Problem Statement ID: PS000190 | District Development Office - Botad | Smart Cities & Urban Governance

> **"AI-based classification, routing and deadline tracking of citizens' complaints and applications using Gujarati voice and text"**

---

## 🎯 Problem Overview & Solutions Delivered

| Problem Mentioned in PS000190 | Solution Implemented in this Project |
| :--- | :--- |
| **No consolidated data across channels** (written, phone, SWAGAT) | Unified grievance intake API and omnichannel ingestion pipeline storing all complaints centrally. |
| **Delay in reaching right branch & weak follow-up** | Zero-latency AI classification using **Google Gemini AI & Gujarati NLP**; auto-routes to exact branch officer. |
| **Low literacy citizens need Gujarati voice input** | Built-in **Gujarati Voice Recording & Speech-to-Text (STT)** with Web Audio API + Gemini Multimodal Audio transcription. |
| **Repeated applications & recurring problems hard to analyse** | Machine Learning similarity clustering (**TF-IDF + Cosine Similarity**) detecting recurring village hotspots for systemic policy intervention. |
| **Applicants do not receive status updates by SMS/WhatsApp** | Automated bilingual Gujarati SMS/WhatsApp dispatch simulator logging instant notifications on filing, SLA progress, and resolution. |
| **Deadline tracking, delay alerts & area-wise dashboard** | Background **SLA Escalation Engine (APScheduler)**; visual countdown badges; Taluka/Subject analytics charts with SLA compliance %. |

---

## 🛠️ Software, Tools & Libraries Installed On Your Computer

### 1. System Tools & Runtimes
- **Python**: `v3.14.7` (with isolated virtual environment `venv/`)
- **Node.js**: `v24.19.0`
- **npm**: `v11.17.0`
- **Git**: `v2.55.0`
- **FFmpeg**: `v9.0.2` (Installed via winget and added to system `PATH` for high-fidelity audio conversion)

### 2. Backend Stack (`venv/` + Python)
- `fastapi` & `uvicorn`: Ultra-fast asynchronous REST API framework
- `google-genai`: Official Google Gemini API SDK (for Gujarati Audio STT & LLM classification)
- `pydantic`: Schema validation and typing
- `sqlalchemy[asyncio]` & `aiosqlite` & `greenlet`: Async ORM with zero-configuration SQLite database
- `scikit-learn`, `numpy`, `pandas`, `scipy`: Machine learning, TF-IDF vectorization, clustering for repeated complaints
- `apscheduler`: Cron & interval background scheduler for automated SLA deadline monitoring and escalation
- `python-multipart`, `requests`, `httpx`, `python-dotenv`: File uploads and HTTP tools

### 3. Frontend Stack (`frontend/` + React 19)
- `vite` (v8.3): Next-generation lightning-fast build tool
- `react` 19 & `react-dom`
- `tailwindcss` & `@tailwindcss/vite`: Clean styling and government portal UI
- `lucide-react`: Government & accessibility iconography
- `recharts`: Interactive analytical charts for subject-wise and area-wise distributions
- `axios`: Async API client connecting to FastAPI

---

## 🚀 How to Run the Project (One-Click)

### Quick Start:
Double-click `start_all.bat` in the root folder, or execute:

```powershell
# In terminal 1 (Backend):
.\run_backend.bat

# In terminal 2 (Frontend):
.\run_frontend.bat
```

Once running:
- **Citizen Portal**: [http://localhost:5173](http://localhost:5173)
- **FastAPI Interactive Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🏛️ Botad Jurisdiction & Departmental Routing

The project comes pre-configured with the exact local administrative structure of **Botad District (બોટાદ)**:
- **Talukas**: Botad (બોટાદ), Barwala (બરવાળા), Gadhada (ગઢડા), Ranpur (રાણપુર)
- **Gram Panchayats**: Paliyad, Kundli, Dhasa, Turkha, Kinkarvadi, Ugamedi, Navda, etc.
- **Departments & SLAs**:
  - 💧 **Water Supply & Drinking Water** (પાણી પુરવઠો): 48 hours SLA
  - ⚡ **Electricity & Power Supply / PGVCL** (વીજળી): 24 hours SLA
  - 🚯 **Sanitation & Drainage** (ગટર & સફાઈ): 72 hours SLA
  - 👵 **Social Welfare & Pensions / NSAP** (સામાજિક સુરક્ષા & પેન્શન): 168 hours SLA
  - 🛣️ **Roads & Buildings** (માર્ગ અને મકાન): 240 hours SLA
  - 📋 **Revenue & Land Records** (મહેસૂલ અને જમીન): 168 hours SLA
  - 🏥 **Health & Medical** (આરોગ્ય): 48 hours SLA
  - 🏫 **Primary Education** (શિક્ષણ): 120 hours SLA

---

## ⚙️ Configuration (`backend/.env`)

To enable live Google Gemini AI transcription and reasoning:
1. Open [Google AI Studio](https://aistudio.google.com/) and generate a free API key.
2. Edit `backend/.env` and paste:
   ```env
   GEMINI_API_KEY=AIzaSy...
   ```
*(Note: If no API key is provided, the system seamlessly operates in **Intelligent Offline/Demo Mode** using rule-based Gujarati keyword classification and voice emulation, ensuring 100% fail-safe performance during hackathon judging).*

