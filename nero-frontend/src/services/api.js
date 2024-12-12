import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

const api = axios.create({
    baseURL: API_URL,
});

// Add Authorization header if token exists
api.interceptors.request.use((config) => {
    const token = localStorage.getItem("accessToken");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;
