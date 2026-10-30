import axios from 'axios';

const API_BASE = '/api';

export const api = {
  // Complaints
  submitText: (data) => axios.post(`${API_BASE}/complaints/submit-text`, data),
  submitVoice: (formData) => axios.post(`${API_BASE}/complaints/submit-voice`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  transcribeVoice: (formData) => axios.post(`${API_BASE}/complaints/transcribe-voice`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getComplaint: (ticketOrPhone) => axios.get(`${API_BASE}/complaints/${ticketOrPhone}`),
  listComplaints: (params) => axios.get(`${API_BASE}/complaints/`, { params }),
  updateStatus: (ticketId, data) => axios.patch(`${API_BASE}/complaints/${ticketId}/status`, data),

  // Admin & Metadata
  getMetadata: () => axios.get(`${API_BASE}/admin/metadata`),
  getDashboardStats: () => axios.get(`${API_BASE}/admin/dashboard-stats`),
  seedSampleData: () => axios.post(`${API_BASE}/admin/seed-sample-data`),
};

