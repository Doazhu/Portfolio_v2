import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000/api";
const BASE_URL = process.env.REACT_APP_BASE_URL || "http://127.0.0.1:8000";

const api = axios.create({
    baseURL: API_URL,
    headers: { "Content-Type": "application/json" }
});

export const projectsAPI = {
    getAll: async (featuredOnly = false) => {
        const params = featuredOnly ? { featured_only: true } : {};
        const { data } = await api.get("/projects", { params });
        return data;
    },

    getById: async (id) => {
        const { data } = await api.get(`/projects/${id}`);
        return data;
    },

    getBySlug: async (slug) => {
        const { data } = await api.get(`/projects/slug/${slug}`);
        return data;
    },

    create: async (projectData) => {
        const { data } = await api.post("/projects", projectData);
        return data;
    },

    update: async (id, projectData) => {
        const { data } = await api.put(`/projects/${id}`, projectData);
        return data;
    },

    delete: async (id) => {
        await api.delete(`/projects/${id}`);
    }
};

export const uploadsAPI = {
    upload: async (file) => {
        const formData = new FormData();
        formData.append("file", file);
        const { data } = await axios.post(`${API_URL}/uploads`, formData, {
            headers: { "Content-Type": "multipart/form-data" }
        });
        return data;
    },

    uploadMultiple: async (files) => {
        const formData = new FormData();
        files.forEach(file => formData.append("files", file));
        const { data } = await axios.post(`${API_URL}/uploads/multiple`, formData, {
            headers: { "Content-Type": "multipart/form-data" }
        });
        return data;
    },

    delete: async (filename) => {
        await api.delete(`/uploads/${filename}`);
    },

    getUrl: (path) => path?.startsWith("http") ? path : `${BASE_URL}${path}`
};

export const skillsAPI = {
    getAll: async () => {
        const { data } = await api.get("/skills");
        return data;
    }
};

export const messagesAPI = {
    send: async (messageData) => {
        const { data } = await api.post("/messages", messageData);
        return data;
    }
};

export { api, API_URL, BASE_URL };
