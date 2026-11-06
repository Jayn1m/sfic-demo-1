import React, { useState, useEffect, useRef } from 'react';
import { 
  Mic, MicOff, Send, Search, CheckCircle, Clock, AlertTriangle, 
  Building2, Phone, MapPin, ShieldAlert, Sparkles, RefreshCw, 
  MessageSquare, Layers, UserCheck, Check, ArrowRight, Sun, Moon
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, 
  PieChart, Pie, Cell, Legend 
} from 'recharts';
import { translations } from './data/translations';
import { api } from './services/api';

const COLORS = ['#2563eb', '#16a34a', '#eab308', '#dc2626', '#8b5cf6', '#ec4899', '#06b6d4'];

export default function App() {
  const [lang, setLang] = useState('gu'); // 'gu' or 'en'
  const [activeTab, setActiveTab] = useState('file'); // 'file', 'track', 'admin'
  const t = translations[lang];

  // Day / Night Theme State (persisted to localStorage)
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('botad_theme') || 'light';
  });

  useEffect(() => {
    localStorage.setItem('botad_theme', theme);
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'light' ? 'dark' : 'light'));
  };

  // Metadata
  const [meta, setMeta] = useState({ talukas_panchayats: {}, departments: {} });
  const [selectedTaluka, setSelectedTaluka] = useState('');
  const [selectedPanchayat, setSelectedPanchayat] = useState('');
  
  // Grievance Form State
  const [applicantName, setApplicantName] = useState('');
  const [applicantPhone, setApplicantPhone] = useState('');
  const [grievanceText, setGrievanceText] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submissionResult, setSubmissionResult] = useState(null);

  // Voice Recording State
  const [isRecording, setIsRecording] = useState(false);
  const [speechLang, setSpeechLang] = useState('gu-IN');
  const [speechError, setSpeechError] = useState('');
  const [usedVoiceInput, setUsedVoiceInput] = useState(false);
  const recognitionRef = useRef(null);

  // Tracking State
  const [trackQuery, setTrackQuery] = useState('');
  const [trackedComplaint, setTrackedComplaint] = useState(null);
  const [isTracking, setIsTracking] = useState(false);
  const [trackError, setTrackError] = useState('');

  // Admin Dashboard State
  const [stats, setStats] = useState(null);
  const [complaintsList, setComplaintsList] = useState([]);
  const [isLoadingAdmin, setIsLoadingAdmin] = useState(false);
  const [selectedComplaintForAction, setSelectedComplaintForAction] = useState(null);
  const [officerRemarks, setOfficerRemarks] = useState('');
  const [actionStatus, setActionStatus] = useState('RESOLVED');

  // Load Metadata on mount
  useEffect(() => {
    fetchMetadata();
  }, []);

  const fetchMetadata = async () => {
    try {
      const res = await api.getMetadata();
      setMeta(res.data);
      const talukas = Object.keys(res.data.talukas_panchayats || {});
      if (talukas.length > 0) {
        setSelectedTaluka(talukas[0]);
        setSelectedPanchayat(res.data.talukas_panchayats[talukas[0]][0] || '');
      }
    } catch (err) {
      console.error("Failed to load metadata", err);
    }
  };

  // Load Admin Data when tab opens
  useEffect(() => {
    if (activeTab === 'admin') {
      loadAdminData();
    }
  }, [activeTab]);

  const loadAdminData = async () => {
    setIsLoadingAdmin(true);
    try {
      const [statsRes, listRes] = await Promise.all([
        api.getDashboardStats(),
        api.listComplaints()
      ]);
      setStats(statsRes.data);
      setComplaintsList(listRes.data);
    } catch (err) {
      console.error("Failed to load admin data", err);
    } finally {
      setIsLoadingAdmin(false);
    }
  };

  const seedDemoData = async () => {
    try {
      await api.seedSampleData();
      await loadAdminData();
      alert("ડેમો ડેટા સફળતાપૂર્વક લોડ કરવામાં આવ્યો છે! (Sample data loaded)");
    } catch (err) {
      alert("Error seeding data: " + err.message);
    }
  };

  // Handle Taluka Change
  const handleTalukaChange = (e) => {
    const taluka = e.target.value;
    setSelectedTaluka(taluka);
    const panchayats = meta.talukas_panchayats[taluka] || [];
    setSelectedPanchayat(panchayats[0] || '');
  };

  // Voice Recording Handlers
  const startRecording = () => {
    setSpeechError('');
    setUsedVoiceInput(true);

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setSpeechError(
        lang === 'gu'
          ? "તમારા બ્રાઉઝરમાં સ્પીચ રેકગ્નિશન ઉપલબ્ધ નથી. કૃપા કરીને Google Chrome અથવા Microsoft Edge વાપરો."
          : "Web Speech Recognition is not supported in this browser. Please use Google Chrome or Microsoft Edge."
      );
      return;
    }

    try {
      if (recognitionRef.current) {
        try { recognitionRef.current.abort(); } catch (e) {}
      }

      const recognition = new SpeechRecognition();
      recognition.lang = speechLang; // 'gu-IN' (Gujarati), 'hi-IN', or 'en-IN'
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.maxAlternatives = 1;
      recognitionRef.current = recognition;

      let accumulatedFinal = '';

      recognition.onstart = () => {
        setIsRecording(true);
        setSpeechError('');
      };

      recognition.onresult = (event) => {
        let currentInterim = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const res = event.results[i];
          if (res.isFinal) {
            accumulatedFinal += res[0].transcript + ' ';
          } else {
            currentInterim += res[0].transcript;
          }
        }
        const fullLiveText = (accumulatedFinal + currentInterim).trim();
        if (fullLiveText) {
          setGrievanceText(fullLiveText);
        }
      };

      recognition.onerror = (event) => {
        console.warn("Speech recognition error:", event.error);
        if (event.error === 'not-allowed') {
          setSpeechError(
            lang === 'gu'
              ? "માઇક્રોફોન પરવાનગી બ્લોક છે. કૃપા કરીને બ્રાઉઝર એડ્રેસ બારમાં માઇક્રોફોનને Allow કરો."
              : "Microphone permission denied. Please allow microphone access in your browser."
          );
        } else if (event.error === 'network') {
          setSpeechError(
            lang === 'gu'
              ? "ઇન્ટરનેટ કનેક્શન તપાસો (Google સ્પીચ સર્વિસ કનેક્ટ થઈ શકી નથી)."
              : "Network error connecting to speech recognition service."
          );
        } else if (event.error === 'no-speech') {
          return;
        } else {
          setSpeechError(`Notice: ${event.error}`);
        }
        setIsRecording(false);
      };

      recognition.onend = () => {
        setIsRecording(false);
      };

      recognition.start();
      setIsRecording(true);
    } catch (err) {
      console.error("Failed to start speech recognition:", err);
      setSpeechError(err.message || "Failed to start speech recognition.");
      setIsRecording(false);
    }
  };

  const stopRecording = () => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch (e) {
        console.error("Error stopping recognition:", e);
      }
    }
    setIsRecording(false);
  };

  // Preset Gujarati Voice/Text Grievance helper
  const applyPreset = (text, taluka, panchayat) => {
    setGrievanceText(text);
    if (taluka) setSelectedTaluka(taluka);
    if (panchayat) setSelectedPanchayat(panchayat);
  };

  // Submit Grievance
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!applicantName || !applicantPhone || !grievanceText) {
      alert("કૃપા કરીને નામ, ફોન અને ફરિયાદની વિગત દાખલ કરો.");
      return;
    }

    setIsSubmitting(true);
    try {
      let res;
      res = await api.submitText({
        applicant_name: applicantName,
        applicant_phone: applicantPhone,
        taluka: selectedTaluka,
        gram_panchayat: selectedPanchayat,
        grievance_text: grievanceText,
        channel: usedVoiceInput ? "Voice (Gujarati)" : "Web Form"
      });

      setSubmissionResult(res.data);
      setGrievanceText('');
      setUsedVoiceInput(false);
    } catch (err) {
      alert("Error submitting grievance: " + (err.response?.data?.detail || err.message));
    } finally {
      setIsSubmitting(false);
    }
  };

  // Tracking Handler
  const handleTrack = async (e) => {
    e.preventDefault();
    if (!trackQuery.trim()) return;
    setIsTracking(true);
    setTrackError('');
    setTrackedComplaint(null);
    try {
      const res = await api.getComplaint(trackQuery.trim());
      setTrackedComplaint(res.data);
    } catch (err) {
      setTrackError("આ ટિકિટ ID અથવા મોબાઇલ નંબર માટે કોઈ ફરિયાદ મળી નથી.");
    } finally {
      setIsTracking(false);
    }
  };

  // Update Status by Officer
  const handleOfficerUpdate = async () => {
    if (!selectedComplaintForAction) return;
    try {
      await api.updateStatus(selectedComplaintForAction.ticket_id, {
        new_status: actionStatus,
        officer_name: selectedComplaintForAction.assigned_officer || "DDO Branch Officer",
        remarks: officerRemarks || "Action taken by branch authority."
      });
      setSelectedComplaintForAction(null);
      setOfficerRemarks('');
      await loadAdminData();
    } catch (err) {
      alert("Error updating status: " + err.message);
    }
  };

  // Format Recharts data
  const deptChartData = stats?.department_distribution 
    ? Object.entries(stats.department_distribution).map(([name, count]) => ({ name, count }))
    : [];

  const talukaChartData = stats?.taluka_distribution 
    ? Object.entries(stats.taluka_distribution).map(([name, count]) => ({ name: name.split(' ')[0], count }))
    : [];

  return (
    <div className={`min-h-screen ${theme === 'dark' ? 'bg-slate-950 text-slate-100' : 'bg-slate-100 text-slate-800'} flex flex-col font-sans transition-colors duration-200`}>
      
      {/* Top Government Header */}
      <header className={`bg-gradient-to-r ${theme === 'dark' ? 'from-slate-950 via-slate-900 to-indigo-950 border-b border-slate-800' : 'from-blue-900 via-indigo-900 to-blue-950'} text-white shadow-lg sticky top-0 z-50 transition-colors`}>
        <div className="max-w-7xl mx-auto px-4 py-3 flex flex-col md:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-amber-500 rounded-full flex items-center justify-center font-bold text-slate-900 shadow-md border-2 border-white text-xl">
              બો
            </div>
            <div>
              <div className="text-xs uppercase tracking-wider text-amber-300 font-semibold">
                District Development Office - Botad (જિલ્લા વિકાસ અધિકારી કચેરી)
              </div>
              <h1 className="text-lg md:text-xl font-bold tracking-tight">
                {t.appTitle}
              </h1>
            </div>
          </div>

          <div className="flex items-center gap-2.5 flex-wrap justify-center">
            {/* Quick Demo Seed Button */}
            <button 
              onClick={seedDemoData}
              className="text-xs bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold px-3 py-1.5 rounded-md flex items-center gap-1 shadow transition cursor-pointer"
              title="Preload 8 realistic demo complaints across Botad"
            >
              <RefreshCw className="w-3.5 h-3.5" /> Demo Seed
            </button>

            {/* Day / Night Theme Toggle */}
            <button
              onClick={toggleTheme}
              className={`text-xs font-bold px-3 py-1.5 rounded-md flex items-center gap-1.5 shadow transition border cursor-pointer ${
                theme === 'dark' 
                  ? 'bg-slate-800 hover:bg-slate-700 text-amber-300 border-slate-600' 
                  : 'bg-white hover:bg-slate-100 text-slate-900 border-white/80'
              }`}
              title={theme === 'dark' ? "દિવસ થીમ પર સ્વિચ કરો (Light Theme)" : "રાત્રિ થીમ પર સ્વિચ કરો (Dark Theme)"}
            >
              {theme === 'dark' ? (
                <>
                  <Sun className="w-3.5 h-3.5 text-amber-400" />
                  <span>{lang === 'gu' ? 'દિવસ થીમ' : 'Day Mode'}</span>
                </>
              ) : (
                <>
                  <Moon className="w-3.5 h-3.5 text-indigo-700" />
                  <span>{lang === 'gu' ? 'રાત્રિ થીમ' : 'Night Mode'}</span>
                </>
              )}
            </button>

            {/* Language Toggle */}
            <div className="bg-blue-800/80 p-0.5 rounded-lg border border-blue-700 flex text-xs font-semibold">
              <button 
                onClick={() => setLang('gu')}
                className={`px-2.5 py-1 rounded-md transition ${lang === 'gu' ? 'bg-amber-400 text-slate-950 font-bold shadow' : 'text-blue-100'}`}
              >
                ગુજરાતી
              </button>
              <button 
                onClick={() => setLang('en')}
                className={`px-2.5 py-1 rounded-md transition ${lang === 'en' ? 'bg-amber-400 text-slate-950 font-bold shadow' : 'text-blue-100'}`}
              >
                English
              </button>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="max-w-7xl mx-auto px-4 border-t border-blue-800/60 flex space-x-1 md:space-x-4 overflow-x-auto text-sm font-medium">
          <button
            onClick={() => setActiveTab('file')}
            className={`py-3 px-3 md:px-5 flex items-center gap-2 border-b-2 transition whitespace-nowrap ${
              activeTab === 'file' 
                ? 'border-amber-400 text-amber-300 font-bold bg-blue-800/40' 
                : 'border-transparent text-blue-200 hover:text-white'
            }`}
          >
            <Mic className="w-4 h-4" /> {t.tabFile}
          </button>
          
          <button
            onClick={() => setActiveTab('track')}
            className={`py-3 px-3 md:px-5 flex items-center gap-2 border-b-2 transition whitespace-nowrap ${
              activeTab === 'track' 
                ? 'border-amber-400 text-amber-300 font-bold bg-blue-800/40' 
                : 'border-transparent text-blue-200 hover:text-white'
            }`}
          >
            <Search className="w-4 h-4" /> {t.tabTrack}
          </button>

          <button
            onClick={() => setActiveTab('admin')}
            className={`py-3 px-3 md:px-5 flex items-center gap-2 border-b-2 transition whitespace-nowrap ${
              activeTab === 'admin' 
                ? 'border-amber-400 text-amber-300 font-bold bg-blue-800/40' 
                : 'border-transparent text-blue-200 hover:text-white'
            }`}
          >
            <Building2 className="w-4 h-4" /> {t.tabAdmin}
          </button>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 py-6 flex-1 w-full">
        
        {/* ================= TAB 1: FILE GRIEVANCE ================= */}
        {activeTab === 'file' && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            {/* Left Column: Form & Voice Input */}
            <div className={`lg:col-span-7 ${theme === 'dark' ? 'bg-slate-900 border-slate-800 text-white' : 'bg-white border-slate-200 text-slate-800'} rounded-xl shadow-md border p-6 transition-colors`}>
              
              {/* Literacy Voice Banner */}
              <div className={`mb-5 ${theme === 'dark' ? 'bg-amber-950/40 border-amber-500/80 text-amber-200' : 'bg-gradient-to-r from-amber-50 to-orange-50 border-amber-500 text-amber-900'} border-l-4 p-4 rounded-r-lg flex items-start gap-3`}>
                <Mic className={`w-6 h-6 ${theme === 'dark' ? 'text-amber-400' : 'text-amber-600'} mt-0.5 shrink-0`} />
                <div>
                  <h3 className={`font-bold text-sm ${theme === 'dark' ? 'text-amber-300' : 'text-amber-900'}`}>
                    {lang === 'gu' ? 'ઓછું ભણેલા નાગરિકો માટે સરળ અવાજ સુવિધા' : 'Voice Input for Easy Access'}
                  </h3>
                  <p className={`text-xs mt-0.5 ${theme === 'dark' ? 'text-amber-200/90' : 'text-amber-800'}`}>
                    {t.citizenNotice}
                  </p>
                </div>
              </div>

              {/* Big Gujarati Voice Recording Control */}
              <div className={`mb-6 p-4 ${theme === 'dark' ? 'bg-slate-800/60 border-slate-700' : 'bg-slate-50 border-slate-200'} border rounded-xl flex flex-col items-center justify-center text-center transition-colors`}>
                <div className="flex flex-col sm:flex-row items-center justify-between w-full mb-3 gap-2">
                  <div className={`text-xs font-semibold ${theme === 'dark' ? 'text-slate-300' : 'text-slate-600'} uppercase tracking-wider`}>
                    {lang === 'gu' ? 'ગુજરાતી અવાજ (વોઇસ) ઇનપુટ' : 'Voice Input to Text'}
                  </div>
                  
                  {/* Speech Language Selector */}
                  <div className={`flex text-xs ${theme === 'dark' ? 'bg-slate-700' : 'bg-slate-200'} p-0.5 rounded-lg font-medium`}>
                    <button
                      type="button"
                      onClick={() => setSpeechLang('gu-IN')}
                      className={`px-2.5 py-1 rounded-md transition ${speechLang === 'gu-IN' ? 'bg-indigo-600 text-white font-bold shadow-sm' : theme === 'dark' ? 'text-slate-300 hover:text-white' : 'text-slate-700 hover:text-slate-900'}`}
                    >
                      ગુજરાતી (gu-IN)
                    </button>
                    <button
                      type="button"
                      onClick={() => setSpeechLang('en-IN')}
                      className={`px-2.5 py-1 rounded-md transition ${speechLang === 'en-IN' ? 'bg-indigo-600 text-white font-bold shadow-sm' : theme === 'dark' ? 'text-slate-300 hover:text-white' : 'text-slate-700 hover:text-slate-900'}`}
                    >
                      English (en-IN)
                    </button>
                    <button
                      type="button"
                      onClick={() => setSpeechLang('hi-IN')}
                      className={`px-2.5 py-1 rounded-md transition ${speechLang === 'hi-IN' ? 'bg-indigo-600 text-white font-bold shadow-sm' : theme === 'dark' ? 'text-slate-300 hover:text-white' : 'text-slate-700 hover:text-slate-900'}`}
                    >
                      हिंदी (hi-IN)
                    </button>
                  </div>
                </div>

                <button
                  type="button"
                  onClick={isRecording ? stopRecording : startRecording}
                  className={`relative p-5 rounded-full transition-all transform active:scale-95 shadow-lg flex items-center justify-center cursor-pointer ${
                    isRecording 
                      ? 'bg-red-600 text-white animate-pulse ring-4 ring-red-300' 
                      : 'bg-indigo-600 hover:bg-indigo-700 text-white hover:shadow-indigo-200'
                  }`}
                  title={isRecording ? "બોલવાનું બંધ કરવા ક્લિક કરો" : "બોલવા માટે ક્લિક કરો"}
                >
                  {isRecording ? <MicOff className="w-8 h-8" /> : <Mic className="w-8 h-8" />}
                </button>

                <div className={`mt-3 text-sm font-medium ${theme === 'dark' ? 'text-slate-200' : 'text-slate-700'}`}>
                  {isRecording ? (
                    <span className="text-red-500 font-bold flex items-center gap-2">
                      <span className="w-2.5 h-2.5 rounded-full bg-red-600 animate-ping"></span>
                      {lang === 'gu' ? 'તમારો અવાજ સાંભળી રહ્યો છે... બોલો (નીચે આપોઆપ ટાઇપ થશે)...' : 'Listening... Speak now (auto-typing below)...'}
                    </span>
                  ) : (
                    <span>{t.voiceBtnStart}</span>
                  )}
                </div>

                {speechError && (
                  <div className={`mt-3 p-2 ${theme === 'dark' ? 'bg-red-950/60 border-red-800 text-red-300' : 'bg-red-50 border-red-200 text-red-700'} border rounded-lg text-xs font-medium w-full text-center`}>
                    ⚠️ {speechError}
                  </div>
                )}

                {/* Gujarati Quick Voice Presets for Testing */}
                <div className={`mt-4 pt-3 border-t ${theme === 'dark' ? 'border-slate-700' : 'border-slate-200'} w-full text-left`}>
                  <div className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'} font-medium mb-1.5`}>
                    {lang === 'gu' ? 'વારંવાર પૂછાતી ફરિયાદોના નમૂના (ક્લિક કરો):' : 'Sample Gujarati Presets (Click to autofill):'}
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    <button
                      type="button"
                      onClick={() => applyPreset("અમારા ગામ પાળિયાદમાં છેલ્લા ૪ દિવસથી પીવાનું પાણી નથી આવતું, પાઈપલાઈન લીક થાય છે.", "Botad (બોટાદ)", "Paliyad (પાળિયાદ)")}
                      className={`text-xs ${theme === 'dark' ? 'bg-blue-950/70 hover:bg-blue-900/90 text-blue-300 border-blue-800' : 'bg-blue-50 hover:bg-blue-100 text-blue-700 border-blue-200'} px-2 py-1 rounded border transition cursor-pointer`}
                    >
                      💧 પીવાનું પાણી & લીકેજ (પાળિયાદ)
                    </button>
                    <button
                      type="button"
                      onClick={() => applyPreset("કુંડલી ગામમાં ખેતીવાડી ડીપી બળી ગઈ છે અને ૩ દિવસથી લાઈટ નથી.", "Barwala (બરવાળા)", "Kundli (કુંડલી)")}
                      className={`text-xs ${theme === 'dark' ? 'bg-amber-950/70 hover:bg-amber-900/90 text-amber-300 border-amber-800' : 'bg-amber-50 hover:bg-amber-100 text-amber-700 border-amber-200'} px-2 py-1 rounded border transition cursor-pointer`}
                    >
                      ⚡ વીજળી / ડીપી (કુંડલી)
                    </button>
                    <button
                      type="button"
                      onClick={() => applyPreset("ઢસા ગામમાં ગટરો ઉભરાય છે અને રોગચાળો ફેલાવવાનો ભય છે.", "Gadhada (ગઢડા)", "Dhasa (ઢસા)")}
                      className={`text-xs ${theme === 'dark' ? 'bg-emerald-950/70 hover:bg-emerald-900/90 text-emerald-300 border-emerald-800' : 'bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border-emerald-200'} px-2 py-1 rounded border transition cursor-pointer`}
                    >
                      🚯 ગટર & સફાઈ (ઢસા)
                    </button>
                    <button
                      type="button"
                      onClick={() => applyPreset("વિધવા સહાય પેન્શન ૩ મહિનાથી જમા થયું નથી.", "Ranpur (રાણપુર)", "Kinkarvadi (કિંકરવાડી)")}
                      className={`text-xs ${theme === 'dark' ? 'bg-purple-950/70 hover:bg-purple-900/90 text-purple-300 border-purple-800' : 'bg-purple-50 hover:bg-purple-100 text-purple-700 border-purple-200'} px-2 py-1 rounded border transition cursor-pointer`}
                    >
                      👵 પેન્શન યોજના (રાણપુર)
                    </button>
                  </div>
                </div>
              </div>

              {/* Form Input */}
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className={`block text-xs font-semibold ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'} mb-1`}>
                      {t.nameLabel} *
                    </label>
                    <input
                      type="text"
                      required
                      placeholder="દા.ત. રમેશભાઈ પટેલ"
                      value={applicantName}
                      onChange={(e) => setApplicantName(e.target.value)}
                      className={`w-full px-3 py-2 border ${theme === 'dark' ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-400' : 'bg-white border-slate-300 text-slate-900 placeholder-slate-400'} rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none`}
                    />
                  </div>

                  <div>
                    <label className={`block text-xs font-semibold ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'} mb-1`}>
                      {t.phoneLabel} *
                    </label>
                    <input
                      type="tel"
                      required
                      placeholder="દા.ત. 9825100001"
                      value={applicantPhone}
                      onChange={(e) => setApplicantPhone(e.target.value)}
                      className={`w-full px-3 py-2 border ${theme === 'dark' ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-400' : 'bg-white border-slate-300 text-slate-900 placeholder-slate-400'} rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none`}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className={`block text-xs font-semibold ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'} mb-1`}>
                      {t.talukaLabel} *
                    </label>
                    <select
                      value={selectedTaluka}
                      onChange={handleTalukaChange}
                      className={`w-full px-3 py-2 border ${theme === 'dark' ? 'bg-slate-800 border-slate-700 text-white' : 'bg-white border-slate-300 text-slate-900'} rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none`}
                    >
                      {Object.keys(meta.talukas_panchayats || {}).map((taluka) => (
                        <option key={taluka} value={taluka} className={theme === 'dark' ? 'bg-slate-800 text-white' : 'bg-white text-slate-900'}>{taluka}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className={`block text-xs font-semibold ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'} mb-1`}>
                      {t.panchayatLabel} *
                    </label>
                    <select
                      value={selectedPanchayat}
                      onChange={(e) => setSelectedPanchayat(e.target.value)}
                      className={`w-full px-3 py-2 border ${theme === 'dark' ? 'bg-slate-800 border-slate-700 text-white' : 'bg-white border-slate-300 text-slate-900'} rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none`}
                    >
                      {(meta.talukas_panchayats[selectedTaluka] || []).map((panchayat) => (
                        <option key={panchayat} value={panchayat} className={theme === 'dark' ? 'bg-slate-800 text-white' : 'bg-white text-slate-900'}>{panchayat}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div>
                  <label className={`block text-xs font-semibold ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'} mb-1`}>
                    {t.grievanceLabel} *
                  </label>
                  <textarea
                    rows={4}
                    required
                    placeholder="તમારી સમસ્યા અથવા અરજી વિગતવાર લખો અથવા ઉપર આપેલ માઈક્રોફોનથી બોલો..."
                    value={grievanceText}
                    onChange={(e) => setGrievanceText(e.target.value)}
                    className={`w-full px-3 py-2 border ${theme === 'dark' ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-400' : 'bg-white border-slate-300 text-slate-900 placeholder-slate-400'} rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none`}
                  />
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full py-3 bg-gradient-to-r from-blue-700 to-indigo-700 hover:from-blue-800 hover:to-indigo-800 text-white font-bold rounded-lg shadow-md hover:shadow-lg transition flex items-center justify-center gap-2 disabled:opacity-50 cursor-pointer"
                >
                  {isSubmitting ? (
                    <>
                      <RefreshCw className="w-4 h-4 animate-spin" /> AI રૂટીંગ & વર્ગીકરણ થઈ રહ્યું છે...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4 text-amber-300" /> {t.submitBtn}
                    </>
                  )}
                </button>
              </form>
            </div>

            {/* Right Column: AI Auto-Routing & Instant Live Result */}
            <div className="lg:col-span-5 space-y-4">
              {submissionResult ? (
                <div className={`${theme === 'dark' ? 'bg-slate-900 border-emerald-500/80 text-white' : 'bg-white border-green-500 text-slate-800'} rounded-xl shadow-md border-2 p-6 animate-fadeIn transition-colors`}>
                  <div className="flex items-center gap-2 text-emerald-500 font-bold text-lg mb-3">
                    <CheckCircle className="w-6 h-6 text-emerald-500" />
                    <span>ફરિયાદ સફળતાપૂર્વક નોંધાઈ ગઈ!</span>
                  </div>

                  <div className={`${theme === 'dark' ? 'bg-emerald-950/40 border-emerald-800/80' : 'bg-green-50 border-green-200'} rounded-lg p-3 border mb-4`}>
                    <div className={`text-xs ${theme === 'dark' ? 'text-emerald-300' : 'text-green-800'} font-medium`}>ટિકિટ ID (Ticket Reference No):</div>
                    <div className={`text-2xl font-black ${theme === 'dark' ? 'text-emerald-400' : 'text-green-950'} tracking-wider`}>
                      {submissionResult.ticket_id}
                    </div>
                  </div>

                  {/* AI Classification Card */}
                  <div className="space-y-3 text-sm">
                    <div className={`flex items-center justify-between pb-2 border-b ${theme === 'dark' ? 'border-slate-800' : 'border-slate-100'}`}>
                      <span className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'} font-medium`}>AI વર્ગીકૃત શાખા:</span>
                      <span className={`font-bold ${theme === 'dark' ? 'text-indigo-300 bg-indigo-950/80 border-indigo-800' : 'text-indigo-900 bg-indigo-50 border-indigo-200'} px-2 py-0.5 rounded border text-xs`}>
                        {submissionResult.department_name_gu}
                      </span>
                    </div>

                    <div className={`flex items-center justify-between pb-2 border-b ${theme === 'dark' ? 'border-slate-800' : 'border-slate-100'}`}>
                      <span className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'} font-medium`}>સોંપાયેલ અધિકારીશ્રી:</span>
                      <span className={`font-medium ${theme === 'dark' ? 'text-slate-200' : 'text-slate-800'} text-xs text-right max-w-[200px]`}>
                        {submissionResult.assigned_officer}
                      </span>
                    </div>

                    <div className={`flex items-center justify-between pb-2 border-b ${theme === 'dark' ? 'border-slate-800' : 'border-slate-100'}`}>
                      <span className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'} font-medium`}>SLA સમયમર્યાદા (Deadline):</span>
                      <span className="font-bold text-red-500 flex items-center gap-1 text-xs">
                        <Clock className="w-3.5 h-3.5" /> {submissionResult.sla_hours} કલાક ({new Date(submissionResult.sla_deadline).toLocaleDateString()})
                      </span>
                    </div>

                    <div className={`flex items-center justify-between pb-2 border-b ${theme === 'dark' ? 'border-slate-800' : 'border-slate-100'}`}>
                      <span className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'} font-medium`}>AI અગ્રતા (Priority):</span>
                      <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                        submissionResult.priority === 'HIGH' || submissionResult.priority === 'EMERGENCY'
                          ? theme === 'dark' ? 'bg-red-950 text-red-300 border border-red-800' : 'bg-red-100 text-red-800'
                          : theme === 'dark' ? 'bg-blue-950 text-blue-300 border border-blue-800' : 'bg-blue-100 text-blue-800'
                      }`}>
                        {submissionResult.priority}
                      </span>
                    </div>

                    {submissionResult.is_recurring && (
                      <div className={`p-2.5 ${theme === 'dark' ? 'bg-amber-950/50 border-amber-800 text-amber-200' : 'bg-amber-50 border-amber-300 text-amber-900'} border rounded-lg text-xs font-semibold flex items-center gap-2`}>
                        <AlertTriangle className="w-4 h-4 text-amber-500 shrink-0" />
                        <span>AI ચેતવણી: આ વિસ્તારમાં વારંવાર આવતી ફરિયાદ તરીકે ચિહ્નિત!</span>
                      </div>
                    )}
                  </div>

                  {/* SMS Update Simulator Banner */}
                  <div className={`mt-5 p-3 ${theme === 'dark' ? 'bg-slate-950 border border-slate-800' : 'bg-slate-900'} text-white rounded-lg text-xs space-y-1`}>
                    <div className="text-amber-400 font-bold flex items-center gap-1">
                      <MessageSquare className="w-3.5 h-3.5" /> SMS ડિસ્પેચ સિમ્યુલેટર (+91 {submissionResult.applicant_phone}):
                    </div>
                    <p className="text-slate-300 text-[11px] leading-relaxed">
                      "નમસ્તે {submissionResult.applicant_name}, આપની ફરિયાદ નં. {submissionResult.ticket_id} સફળતાપૂર્વક નોંધાઈ છે. તેને {submissionResult.department_name_gu} ને મોકલવામાં આવી છે. - DDO Botad"
                    </p>
                  </div>

                  <button
                    onClick={() => {
                      setTrackQuery(submissionResult.ticket_id);
                      setActiveTab('track');
                    }}
                    className={`mt-4 w-full py-2 ${theme === 'dark' ? 'bg-slate-800 hover:bg-slate-700 text-slate-200 border-slate-700' : 'bg-slate-100 hover:bg-slate-200 text-slate-800 border-slate-300'} font-bold text-xs rounded-lg transition flex items-center justify-center gap-1 border cursor-pointer`}
                  >
                    આ ફરિયાદને ટ્રેકિંગ પેજ પર જુઓ <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              ) : (
                <div className={`${theme === 'dark' ? 'bg-slate-900 border-slate-800 text-slate-300' : 'bg-white border-slate-200 text-slate-800'} rounded-xl shadow-md border p-6 flex flex-col items-center justify-center text-center min-h-[350px] transition-colors`}>
                  <div className={`w-16 h-16 rounded-full ${theme === 'dark' ? 'bg-indigo-950/80 text-indigo-400' : 'bg-blue-50 text-blue-600'} flex items-center justify-center mb-4`}>
                    <Sparkles className="w-8 h-8" />
                  </div>
                  <h3 className={`font-bold ${theme === 'dark' ? 'text-white' : 'text-slate-800'} text-base mb-1`}>
                    સ્વચાલિત AI રૂટીંગ એન્જિન
                  </h3>
                  <p className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'} max-w-xs leading-relaxed`}>
                    જ્યારે તમે ગુજરાતીમાં ફરિયાદ બોલો અથવા લખો છો, ત્યારે AI આપોઆપ વિષય (પાણી, વીજળી, રસ્તા વગેરે) ઓળખીને સંબંધિત તાલુક/જિલ્લા શાખા અધિકારીને મોકલે છે અને કાયદેસર SLA ડેડલાઇન નક્કી કરે છે.
                  </p>
                </div>
              )}
            </div>

          </div>
        )}

        {/* ================= TAB 2: TRACK APPLICATION ================= */}
        {activeTab === 'track' && (
          <div className="max-w-4xl mx-auto space-y-6">
            
            {/* Search Box */}
            <div className={`${theme === 'dark' ? 'bg-slate-900 border-slate-800 text-white' : 'bg-white border-slate-200 text-slate-900'} rounded-xl shadow-md border p-6 transition-colors`}>
              <h2 className={`text-base font-bold ${theme === 'dark' ? 'text-white' : 'text-slate-900'} mb-2`}>
                {t.trackTitle}
              </h2>
              <form onSubmit={handleTrack} className="flex gap-2">
                <input
                  type="text"
                  placeholder={t.trackPlaceholder}
                  value={trackQuery}
                  onChange={(e) => setTrackQuery(e.target.value)}
                  className={`flex-1 px-4 py-2.5 border ${theme === 'dark' ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-400' : 'border-slate-300 text-slate-900 placeholder-slate-400'} rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none`}
                />
                <button
                  type="submit"
                  disabled={isTracking}
                  className="px-6 py-2.5 bg-blue-700 hover:bg-blue-800 text-white font-bold text-sm rounded-lg shadow transition flex items-center gap-2 cursor-pointer"
                >
                  <Search className="w-4 h-4" /> {t.trackBtn}
                </button>
              </form>

              {trackError && (
                <div className={`mt-3 text-sm ${theme === 'dark' ? 'text-red-400' : 'text-red-600'} font-medium`}>
                  {trackError}
                </div>
              )}
            </div>

            {/* Complaint Detail Card */}
            {trackedComplaint && (
              <div className={`${theme === 'dark' ? 'bg-slate-900 border-slate-800 text-slate-200' : 'bg-white border-slate-200 text-slate-800'} rounded-xl shadow-md border overflow-hidden animate-fadeIn transition-colors`}>
                
                {/* Header Strip */}
                <div className={`p-4 text-white flex flex-col md:flex-row items-start md:items-center justify-between gap-3 ${
                  trackedComplaint.is_breached || trackedComplaint.status === 'ESCALATED'
                    ? 'bg-red-700'
                    : trackedComplaint.status === 'RESOLVED'
                    ? 'bg-emerald-700'
                    : 'bg-indigo-800'
                }`}>
                  <div>
                    <div className="text-xs opacity-90">અરજી સંદર્ભ નંબર (Ticket ID):</div>
                    <div className="text-xl font-black tracking-wider">{trackedComplaint.ticket_id}</div>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="text-xs bg-black/20 px-3 py-1 rounded-full font-bold">
                      {trackedComplaint.status}
                    </span>
                    {trackedComplaint.remaining_hours !== null && (
                      <span className="text-xs bg-white text-slate-900 font-bold px-3 py-1 rounded-full shadow flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5" /> 
                        {trackedComplaint.remaining_hours > 0 
                          ? `${trackedComplaint.remaining_hours} કલાક બાકી (SLA)`
                          : `SLA સમય પૂર્ણ (${Math.abs(trackedComplaint.remaining_hours)} કલાક વિલંબ)`}
                      </span>
                    )}
                  </div>
                </div>

                {/* Progress Timeline Stepper */}
                <div className={`p-6 border-b ${theme === 'dark' ? 'border-slate-800 bg-slate-800/40 text-slate-300' : 'border-slate-100 bg-slate-50/50 text-slate-800'}`}>
                  <div className="grid grid-cols-4 gap-2 text-center text-xs">
                    
                    <div className="flex flex-col items-center">
                      <div className="w-8 h-8 rounded-full bg-emerald-600 text-white flex items-center justify-center font-bold mb-1 shadow">
                        ✓
                      </div>
                      <span className={`font-semibold ${theme === 'dark' ? 'text-slate-200' : 'text-slate-800'}`}>નોંધણી</span>
                      <span className={`text-[10px] ${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'}`}>Registered</span>
                    </div>

                    <div className="flex flex-col items-center">
                      <div className="w-8 h-8 rounded-full bg-emerald-600 text-white flex items-center justify-center font-bold mb-1 shadow">
                        ✓
                      </div>
                      <span className={`font-semibold ${theme === 'dark' ? 'text-slate-200' : 'text-slate-800'}`}>AI વર્ગીકરણ</span>
                      <span className={`text-[10px] ${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'}`}>Routed to Branch</span>
                    </div>

                    <div className="flex flex-col items-center">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold mb-1 shadow ${
                        trackedComplaint.status === 'RESOLVED' 
                          ? 'bg-emerald-600 text-white' 
                          : 'bg-blue-600 text-white animate-pulse'
                      }`}>
                        {trackedComplaint.status === 'RESOLVED' ? '✓' : '3'}
                      </div>
                      <span className={`font-semibold ${theme === 'dark' ? 'text-slate-200' : 'text-slate-800'}`}>શાખા તપાસ</span>
                      <span className={`text-[10px] ${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'}`}>Under Action</span>
                    </div>

                    <div className="flex flex-col items-center">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold mb-1 shadow ${
                        trackedComplaint.status === 'RESOLVED'
                          ? 'bg-emerald-600 text-white'
                          : theme === 'dark' ? 'bg-slate-700 text-slate-400' : 'bg-slate-300 text-slate-600'
                      }`}>
                        {trackedComplaint.status === 'RESOLVED' ? '✓' : '4'}
                      </div>
                      <span className={`font-semibold ${theme === 'dark' ? 'text-slate-200' : 'text-slate-800'}`}>નિરાકરણ</span>
                      <span className={`text-[10px] ${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'}`}>Resolved</span>
                    </div>

                  </div>
                </div>

                {/* Details Grid */}
                <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                  
                  <div className="space-y-3">
                    <h3 className={`font-bold text-xs uppercase ${theme === 'dark' ? 'text-slate-400' : 'text-slate-400'} tracking-wider`}>
                      અરજદાર & સ્થળ વિગત
                    </h3>
                    <div className={`text-sm ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>
                      <span className={theme === 'dark' ? 'text-slate-400' : 'text-slate-500'}>નામ:</span> <strong className={theme === 'dark' ? 'text-white' : 'text-slate-900'}>{trackedComplaint.applicant_name}</strong>
                    </div>
                    <div className={`text-sm ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>
                      <span className={theme === 'dark' ? 'text-slate-400' : 'text-slate-500'}>સંપર્ક:</span> <span className="font-mono">{trackedComplaint.applicant_phone}</span>
                    </div>
                    <div className={`text-sm ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>
                      <span className={theme === 'dark' ? 'text-slate-400' : 'text-slate-500'}>સ્થળ:</span> <strong className={theme === 'dark' ? 'text-white' : 'text-slate-900'}>{trackedComplaint.gram_panchayat}, {trackedComplaint.taluka}</strong>
                    </div>
                    <div className={`text-sm ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>
                      <span className={theme === 'dark' ? 'text-slate-400' : 'text-slate-500'}>માધ્યમ:</span> <span className={`${theme === 'dark' ? 'bg-slate-800 text-slate-300' : 'bg-slate-100 text-slate-800'} px-2 py-0.5 rounded text-xs`}>{trackedComplaint.channel}</span>
                    </div>
                    
                    <div className={`mt-3 p-3 ${theme === 'dark' ? 'bg-slate-800/80 border-slate-700 text-slate-200' : 'bg-slate-50 border-slate-200 text-slate-800'} rounded-lg border`}>
                      <div className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'} font-semibold mb-1`}>ફરિયાદનું લખાણ:</div>
                      <p className="text-xs italic">
                        "{trackedComplaint.input_text_gu}"
                      </p>
                    </div>
                  </div>

                  <div className="space-y-3">
                    <h3 className={`font-bold text-xs uppercase ${theme === 'dark' ? 'text-slate-400' : 'text-slate-400'} tracking-wider`}>
                      શાખા & ડેડલાઇન મોનિટરિંગ
                    </h3>
                    <div className={`text-sm ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>
                      <span className={theme === 'dark' ? 'text-slate-400' : 'text-slate-500'}>સંબંધિત શાખા:</span> <strong className={theme === 'dark' ? 'text-indigo-400' : 'text-indigo-900'}>{trackedComplaint.department_name_gu}</strong>
                    </div>
                    <div className={`text-sm ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>
                      <span className={theme === 'dark' ? 'text-slate-400' : 'text-slate-500'}>{t.assignedOfficer}:</span> <strong className={`text-xs ${theme === 'dark' ? 'text-slate-200' : 'text-slate-800'}`}>{trackedComplaint.assigned_officer}</strong>
                    </div>
                    <div className={`text-sm ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>
                      <span className={theme === 'dark' ? 'text-slate-400' : 'text-slate-500'}>SLA કલાક:</span> <strong className={theme === 'dark' ? 'text-white' : 'text-slate-900'}>{trackedComplaint.sla_hours} કલાક</strong>
                    </div>
                    <div className={`text-sm ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>
                      <span className={theme === 'dark' ? 'text-slate-400' : 'text-slate-500'}>આખરી તારીખ:</span> <strong className={theme === 'dark' ? 'text-white' : 'text-slate-900'}>{new Date(trackedComplaint.sla_deadline).toLocaleString()}</strong>
                    </div>
                    <div className={`text-sm ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'}`}>
                      <span className={theme === 'dark' ? 'text-slate-400' : 'text-slate-500'}>એસ્કેલેશન સ્તર:</span> <span className={`${theme === 'dark' ? 'bg-amber-950 text-amber-300 border border-amber-800' : 'bg-amber-100 text-amber-900'} px-2 py-0.5 rounded text-xs font-bold`}>લેવલ {trackedComplaint.escalation_level} ({trackedComplaint.escalation_level === 1 ? 'પંચાયત/શાખા' : trackedComplaint.escalation_level === 2 ? 'TDO' : 'DDO બોટાદ'})</span>
                    </div>
                  </div>

                </div>

                {/* Audit Timeline */}
                <div className={`p-6 ${theme === 'dark' ? 'bg-slate-900/60 border-slate-800' : 'bg-slate-50 border-slate-200'} border-t`}>
                  <h3 className={`font-bold text-xs uppercase ${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'} tracking-wider mb-3`}>
                    {t.timelineTitle}
                  </h3>
                  <div className="space-y-2">
                    {(trackedComplaint.timelines || []).map((tl) => (
                      <div key={tl.id} className={`text-xs flex items-start gap-2 ${theme === 'dark' ? 'bg-slate-800 border-slate-700 text-slate-200' : 'bg-white border-slate-200 text-slate-800'} p-2.5 rounded border`}>
                        <Clock className="w-3.5 h-3.5 text-blue-500 mt-0.5 shrink-0" />
                        <div className="flex-1">
                          <span className={`font-bold ${theme === 'dark' ? 'text-white' : 'text-slate-800'}`}>{tl.action}</span>
                          <span className={`text-[10px] ml-2 ${theme === 'dark' ? 'text-slate-400' : 'text-slate-400'}`}>({new Date(tl.timestamp).toLocaleString()})</span>
                          {tl.remarks && <p className={`${theme === 'dark' ? 'text-slate-300' : 'text-slate-600'} mt-0.5`}>{tl.remarks}</p>}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* SMS Audit History */}
                <div className={`p-6 ${theme === 'dark' ? 'bg-slate-950 border-t border-slate-800' : 'bg-slate-900'} text-white`}>
                  <h3 className="font-bold text-xs uppercase text-amber-400 tracking-wider mb-3 flex items-center gap-1.5">
                    <MessageSquare className="w-3.5 h-3.5" /> {t.smsHistoryTitle}
                  </h3>
                  <div className="space-y-2">
                    {(trackedComplaint.sms_logs || []).map((sms) => (
                      <div key={sms.id} className={`text-xs ${theme === 'dark' ? 'bg-slate-900 border-slate-800' : 'bg-slate-800 border-slate-700'} p-2.5 rounded border`}>
                        <div className="flex justify-between text-slate-400 text-[10px] mb-1">
                          <span>SMS TYPE: {sms.message_type}</span>
                          <span>{new Date(sms.sent_at).toLocaleString()}</span>
                        </div>
                        <p className="text-slate-200">{sms.message_text_gu}</p>
                      </div>
                    ))}
                  </div>
                </div>

              </div>
            )}
          </div>
        )}

        {/* ================= TAB 3: ADMIN & DDO DASHBOARD ================= */}
        {activeTab === 'admin' && (
          <div className="space-y-6">
            
            {/* KPI Cards Row */}
            {stats && (
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                
                <div className={`${theme === 'dark' ? 'bg-slate-900 border-slate-800 text-white' : 'bg-white border-slate-200 text-slate-900'} p-4 rounded-xl shadow-sm border transition-colors`}>
                  <div className={`text-xs font-semibold ${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'} uppercase`}>{t.kpiTotal}</div>
                  <div className={`text-2xl font-black ${theme === 'dark' ? 'text-white' : 'text-slate-900'} mt-1`}>{stats.total_complaints}</div>
                  <div className="text-[11px] text-blue-500 mt-1 font-medium">તમામ માધ્યમો</div>
                </div>

                <div className={`${theme === 'dark' ? 'bg-slate-900 border-emerald-900/60' : 'bg-white border-slate-200'} p-4 rounded-xl shadow-sm border transition-colors`}>
                  <div className={`text-xs font-semibold ${theme === 'dark' ? 'text-emerald-400' : 'text-emerald-600'} uppercase`}>{t.kpiResolved}</div>
                  <div className={`text-2xl font-black ${theme === 'dark' ? 'text-emerald-400' : 'text-emerald-700'} mt-1`}>{stats.resolved_count}</div>
                  <div className={`text-[11px] ${theme === 'dark' ? 'text-emerald-400' : 'text-emerald-600'} mt-1 font-medium`}>{stats.resolved_percentage}% નિકાલ દર</div>
                </div>

                <div className={`${theme === 'dark' ? 'bg-slate-900 border-blue-900/60' : 'bg-white border-slate-200'} p-4 rounded-xl shadow-sm border transition-colors`}>
                  <div className={`text-xs font-semibold ${theme === 'dark' ? 'text-blue-400' : 'text-blue-600'} uppercase`}>{t.kpiInProgress}</div>
                  <div className={`text-2xl font-black ${theme === 'dark' ? 'text-blue-400' : 'text-blue-700'} mt-1`}>{stats.in_progress_count}</div>
                  <div className={`text-[11px] ${theme === 'dark' ? 'text-blue-400' : 'text-blue-500'} mt-1`}>પ્રગતિ હેઠળ</div>
                </div>

                <div className={`${theme === 'dark' ? 'bg-slate-900 border-red-900/60 bg-red-950/20' : 'bg-white border-red-200 bg-red-50/30'} p-4 rounded-xl shadow-sm border transition-colors`}>
                  <div className={`text-xs font-semibold ${theme === 'dark' ? 'text-red-400' : 'text-red-600'} uppercase`}>{t.kpiBreached}</div>
                  <div className={`text-2xl font-black ${theme === 'dark' ? 'text-red-400' : 'text-red-600'} mt-1`}>{stats.breached_count}</div>
                  <div className={`text-[11px] ${theme === 'dark' ? 'text-red-400' : 'text-red-500'} mt-1 font-bold`}>ડેડલાઇન વીતી ગયેલ</div>
                </div>

                <div className={`${theme === 'dark' ? 'bg-slate-900 border-amber-900/60 bg-amber-950/20' : 'bg-white border-amber-200 bg-amber-50/30'} p-4 rounded-xl shadow-sm border transition-colors`}>
                  <div className={`text-xs font-semibold ${theme === 'dark' ? 'text-amber-400' : 'text-amber-700'} uppercase`}>DDO એસ્કેલેશન</div>
                  <div className={`text-2xl font-black ${theme === 'dark' ? 'text-amber-400' : 'text-amber-800'} mt-1`}>{stats.escalated_count}</div>
                  <div className={`text-[11px] ${theme === 'dark' ? 'text-amber-400' : 'text-amber-700'} mt-1`}>ઉચ્ચ કક્ષાએ મોકલેલ</div>
                </div>

              </div>
            )}

            {/* Analytics Charts Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              
              {/* Subject-wise Bar Chart */}
              <div className={`${theme === 'dark' ? 'bg-slate-900 border-slate-800 text-white' : 'bg-white border-slate-200 text-slate-800'} p-5 rounded-xl shadow-md border transition-colors`}>
                <h3 className={`font-bold text-sm ${theme === 'dark' ? 'text-white' : 'text-slate-800'} mb-3 flex items-center gap-2`}>
                  <Layers className="w-4 h-4 text-blue-500" />
                  વિષયવાર ફરિયાદ વર્ગીકરણ (Subject-wise Breakdown)
                </h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={deptChartData}>
                      <XAxis dataKey="name" tick={{ fontSize: 10, fill: theme === 'dark' ? '#94a3b8' : '#475569' }} interval={0} angle={-15} textAnchor="end" height={50} />
                      <YAxis allowDecimals={false} tick={{ fill: theme === 'dark' ? '#94a3b8' : '#475569' }} />
                      <Tooltip contentStyle={theme === 'dark' ? { backgroundColor: '#1e293b', borderColor: '#334155', color: '#f8fafc' } : {}} />
                      <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Area-wise (Taluka) Breakdown Chart */}
              <div className={`${theme === 'dark' ? 'bg-slate-900 border-slate-800 text-white' : 'bg-white border-slate-200 text-slate-800'} p-5 rounded-xl shadow-md border transition-colors`}>
                <h3 className={`font-bold text-sm ${theme === 'dark' ? 'text-white' : 'text-slate-800'} mb-3 flex items-center gap-2`}>
                  <MapPin className="w-4 h-4 text-emerald-500" />
                  તાલુકાવાર ફરિયાદ ભારણ (Taluka-wise Load)
                </h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={talukaChartData}>
                      <XAxis dataKey="name" tick={{ fontSize: 11, fill: theme === 'dark' ? '#94a3b8' : '#475569' }} />
                      <YAxis allowDecimals={false} tick={{ fill: theme === 'dark' ? '#94a3b8' : '#475569' }} />
                      <Tooltip contentStyle={theme === 'dark' ? { backgroundColor: '#1e293b', borderColor: '#334155', color: '#f8fafc' } : {}} />
                      <Bar dataKey="count" fill="#10b981" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

            </div>

            {/* AI Recurring Complaint Clusters (Policy Interventions) */}
            {stats?.recurring_hotspots && stats.recurring_hotspots.length > 0 && (
              <div className={`${theme === 'dark' ? 'bg-amber-950/30 border-amber-800/80 text-amber-200' : 'bg-amber-50 border-amber-300 text-amber-900'} border-2 rounded-xl p-5 shadow-sm transition-colors`}>
                <div className={`flex items-center gap-2 ${theme === 'dark' ? 'text-amber-300' : 'text-amber-900'} font-bold text-sm mb-3`}>
                  <AlertTriangle className="w-5 h-5 text-amber-500" />
                  <span>{t.hotspotsTitle}</span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {stats.recurring_hotspots.map((cluster, idx) => (
                    <div key={idx} className={`${theme === 'dark' ? 'bg-slate-900 border-amber-900/60 text-slate-300' : 'bg-white border-amber-200 text-slate-600'} p-3 rounded-lg border text-xs space-y-1 shadow-sm`}>
                      <div className="flex justify-between items-center">
                        <strong className={`${theme === 'dark' ? 'text-amber-300' : 'text-amber-950'} font-bold text-sm`}>{cluster.gram_panchayat} ({cluster.taluka})</strong>
                        <span className={`${theme === 'dark' ? 'bg-amber-950 text-amber-300 border border-amber-800' : 'bg-amber-100 text-amber-900'} font-bold px-2 py-0.5 rounded`}>
                          {cluster.count + 1} ફરિયાદો ક્લસ્ટર
                        </span>
                      </div>
                      <div className={theme === 'dark' ? 'text-slate-400' : 'text-slate-600'}>શાખા: <strong className={theme === 'dark' ? 'text-white' : 'text-slate-800'}>{cluster.department}</strong></div>
                      <p className={`${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'} italic`}>"{cluster.sample}"</p>
                      <div className={`text-[11px] ${theme === 'dark' ? 'text-indigo-400 border-slate-800' : 'text-indigo-700 border-slate-100'} font-semibold pt-1 border-t`}>
                        💡 DDO નીતિ સૂચના: આ ગામમાં કાયમી પાઈપલાઈન નવીનીકરણ જરૂરિયાત.
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Complaints Management Table with Action Modals */}
            <div className={`${theme === 'dark' ? 'bg-slate-900 border-slate-800 text-slate-300' : 'bg-white border-slate-200 text-slate-700'} rounded-xl shadow-md border overflow-hidden transition-colors`}>
              <div className={`p-4 border-b ${theme === 'dark' ? 'border-slate-800' : 'border-slate-200'} flex justify-between items-center`}>
                <h3 className={`font-bold text-sm ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>
                  તમામ અરજીઓ / ફરિયાદો & SLA સ્થિતિ
                </h3>
                <button
                  onClick={loadAdminData}
                  className={`text-xs ${theme === 'dark' ? 'bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700' : 'bg-slate-100 hover:bg-slate-200 text-slate-700'} px-3 py-1.5 rounded flex items-center gap-1 font-semibold cursor-pointer`}
                >
                  <RefreshCw className="w-3 h-3" /> રીફ્રેશ
                </button>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className={`${theme === 'dark' ? 'bg-slate-800/90 text-slate-300 border-slate-700' : 'bg-slate-50 text-slate-500 border-slate-200'} uppercase font-semibold text-[10px] border-b`}>
                    <tr>
                      <th className="p-3">ટિકિટ ID</th>
                      <th className="p-3">અરજદાર & ગામ</th>
                      <th className="p-3">વિષય / શાખા</th>
                      <th className="p-3">અગ્રતા</th>
                      <th className="p-3">SLA બાકી સમય</th>
                      <th className="p-3">સ્થિતિ</th>
                      <th className="p-3 text-right">ક્રિયા (Action)</th>
                    </tr>
                  </thead>
                  <tbody className={`divide-y ${theme === 'dark' ? 'divide-slate-800' : 'divide-slate-100'}`}>
                    {complaintsList.map((c) => (
                      <tr key={c.id} className={`${theme === 'dark' ? 'hover:bg-slate-800/50' : 'hover:bg-slate-50'} transition`}>
                        <td className={`p-3 font-mono font-bold ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>
                          {c.ticket_id}
                          {c.is_recurring && (
                            <span className={`ml-1 text-[10px] ${theme === 'dark' ? 'bg-amber-950 text-amber-300 border border-amber-800' : 'bg-amber-100 text-amber-800'} px-1 rounded font-normal`}>
                              પુનરાવર્તિત
                            </span>
                          )}
                        </td>
                        <td className="p-3">
                          <div className={`font-semibold ${theme === 'dark' ? 'text-slate-200' : 'text-slate-900'}`}>{c.applicant_name}</div>
                          <div className={`text-[10px] ${theme === 'dark' ? 'text-slate-400' : 'text-slate-400'}`}>{c.gram_panchayat}, {c.taluka}</div>
                        </td>
                        <td className="p-3">
                          <div className={`font-medium ${theme === 'dark' ? 'text-indigo-400' : 'text-indigo-900'}`}>{c.department_name_gu}</div>
                          <div className={`text-[10px] ${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'} truncate max-w-[180px]`}>{c.input_text_gu}</div>
                        </td>
                        <td className="p-3">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            c.priority === 'HIGH' || c.priority === 'EMERGENCY'
                              ? theme === 'dark' ? 'bg-red-950 text-red-300 border border-red-800' : 'bg-red-100 text-red-800'
                              : theme === 'dark' ? 'bg-slate-800 text-slate-300' : 'bg-slate-100 text-slate-700'
                          }`}>
                            {c.priority}
                          </span>
                        </td>
                        <td className="p-3">
                          {c.status === 'RESOLVED' ? (
                            <span className="text-emerald-500 font-bold flex items-center gap-1">
                              <Check className="w-3.5 h-3.5" /> પૂર્ણ થયેલ
                            </span>
                          ) : c.remaining_hours !== null && c.remaining_hours <= 0 ? (
                            <span className="text-red-500 font-bold flex items-center gap-1">
                              <AlertTriangle className="w-3.5 h-3.5" /> SLA વિલંબ
                            </span>
                          ) : (
                            <span className="text-blue-500 font-medium">
                              {c.remaining_hours} કલાક બાકી
                            </span>
                          )}
                        </td>
                        <td className="p-3">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            c.status === 'RESOLVED'
                              ? theme === 'dark' ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' : 'bg-emerald-100 text-emerald-800'
                              : c.status === 'ESCALATED'
                              ? theme === 'dark' ? 'bg-red-950 text-red-300 border border-red-800' : 'bg-red-100 text-red-800'
                              : theme === 'dark' ? 'bg-blue-950 text-blue-300 border border-blue-800' : 'bg-blue-100 text-blue-800'
                          }`}>
                            {c.status}
                          </span>
                        </td>
                        <td className="p-3 text-right">
                          <button
                            onClick={() => setSelectedComplaintForAction(c)}
                            className={`font-bold px-2.5 py-1 rounded text-xs transition border cursor-pointer ${
                              theme === 'dark' 
                                ? 'bg-indigo-950/80 hover:bg-indigo-900 text-indigo-300 border-indigo-800' 
                                : 'bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border-indigo-200'
                            }`}
                          >
                            અપડેટ કરો
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Officer Action Modal */}
            {selectedComplaintForAction && (
              <div className="fixed inset-0 bg-slate-950/70 backdrop-blur-xs flex items-center justify-center p-4 z-50">
                <div className={`${theme === 'dark' ? 'bg-slate-900 text-white border border-slate-700' : 'bg-white text-slate-900'} rounded-xl shadow-xl max-w-md w-full p-6 animate-scaleIn`}>
                  <h3 className={`font-bold text-base ${theme === 'dark' ? 'text-white' : 'text-slate-900'} mb-1`}>
                    ફરિયાદ નિકાલ / સ્થિતિ અપડેટ
                  </h3>
                  <div className={`text-xs ${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'} mb-4`}>
                    ટિકિટ: <strong>{selectedComplaintForAction.ticket_id}</strong> | અરજદાર: <strong>{selectedComplaintForAction.applicant_name}</strong>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <label className={`block text-xs font-semibold ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'} mb-1`}>
                        નવી સ્થિતિ (New Status):
                      </label>
                      <select
                        value={actionStatus}
                        onChange={(e) => setActionStatus(e.target.value)}
                        className={`w-full px-3 py-2 border ${theme === 'dark' ? 'bg-slate-800 border-slate-700 text-white' : 'bg-white border-slate-300 text-slate-900'} rounded-lg text-sm`}
                      >
                        <option value="IN_PROGRESS" className={theme === 'dark' ? 'bg-slate-800 text-white' : ''}>કામગીરી ચાલુ (IN_PROGRESS)</option>
                        <option value="RESOLVED" className={theme === 'dark' ? 'bg-slate-800 text-white' : ''}>નિરાકરણ પૂર્ણ (RESOLVED)</option>
                        <option value="ESCALATED" className={theme === 'dark' ? 'bg-slate-800 text-white' : ''}>ઉચ્ચ કક્ષાએ એસ્કેલેટ (ESCALATED)</option>
                      </select>
                    </div>

                    <div>
                      <label className={`block text-xs font-semibold ${theme === 'dark' ? 'text-slate-300' : 'text-slate-700'} mb-1`}>
                        અધિકારીની કામગીરી નોંધ (Remarks for SMS):
                      </label>
                      <textarea
                        rows={3}
                        placeholder="દા.ત. પાઈપલાઈન રીપેર કરી પાણી પુરવઠો શરૂ કરાયો છે."
                        value={officerRemarks}
                        onChange={(e) => setOfficerRemarks(e.target.value)}
                        className={`w-full px-3 py-2 border ${theme === 'dark' ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-400' : 'bg-white border-slate-300 text-slate-900 placeholder-slate-400'} rounded-lg text-sm`}
                      />
                    </div>

                    <div className={`p-2.5 ${theme === 'dark' ? 'bg-blue-950/60 border-blue-900 text-blue-300' : 'bg-blue-50 border-blue-200 text-blue-900'} border rounded text-xs`}>
                      ℹ️ સ્થિતિ અપડેટ થતા અરજદારના મોબાઇલ ({selectedComplaintForAction.applicant_phone}) પર આપોઆપ SMS મોકલવામાં આવશે.
                    </div>

                    <div className="flex justify-end gap-2 pt-2">
                      <button
                        type="button"
                        onClick={() => setSelectedComplaintForAction(null)}
                        className={`px-4 py-2 border ${theme === 'dark' ? 'border-slate-700 text-slate-300 hover:bg-slate-800' : 'border-slate-300 text-slate-700 hover:bg-slate-100'} font-semibold rounded-lg text-xs cursor-pointer`}
                      >
                        રદ કરો
                      </button>
                      <button
                        type="button"
                        onClick={handleOfficerUpdate}
                        className="px-5 py-2 bg-indigo-700 hover:bg-indigo-800 text-white font-bold rounded-lg text-xs shadow cursor-pointer"
                      >
                        અપડેટ કરો & SMS મોકલો
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}

          </div>
        )}

      </main>

      {/* Footer */}
      <footer className={`${theme === 'dark' ? 'bg-slate-950 text-slate-400 border-slate-800' : 'bg-slate-900 text-slate-400 border-slate-800'} text-xs py-4 px-4 text-center border-t mt-8 transition-colors`}>
        <p>
          District Development Office - Botad | Smart Cities & Urban Governance (PS000190)
        </p>
        <p className="mt-1 text-slate-500">
          AI Grievance Classification, Automated Routing & SLA Tracking System • Powered by Google Gemini AI & FastAPI
        </p>
      </footer>

    </div>
  );
}
