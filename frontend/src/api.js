import axios from "axios";

const API = "http://localhost:8000/api";


// ===============================
// MAIN DATASET UPLOAD
// ===============================

export const uploadFile = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return axios.post(`${API}/upload`, formData);
};


// ===============================
// FORECAST DATASET UPLOAD
// ===============================

export const uploadForecastFile = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return axios.post(`${API}/forecast-upload`, formData);
};


// ===============================
// ANALYTICS DATA
// ===============================

export const get = (datasetId, path) => {
  return axios.get(`${API}/datasets/${datasetId}/${path}`);
};