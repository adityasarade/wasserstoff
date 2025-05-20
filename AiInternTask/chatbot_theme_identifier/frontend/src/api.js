import axios from "axios";

const baseURL =
  process.env.REACT_APP_API_URL ||
  "http://127.0.0.1:8000";  // fallback for local dev

const api = axios.create({
  baseURL,
});

export default api;