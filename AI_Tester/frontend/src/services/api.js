// src/services/api.js
const API_BASE = import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8000";

async function safeJson(res) {
  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    return { error: "Non-JSON response", raw: text };
  }
}

async function get(path) {
  const res = await fetch(`${API_BASE}${path}`);
  const data = await safeJson(res);
  if (!res.ok) {
    throw new Error(data?.detail || data?.message || `GET ${path} failed (${res.status})`);
  }
  return data;
}

async function post(path, body, isFormData = false) {
  const options = {
    method: "POST",
    body: isFormData ? body : JSON.stringify(body),
  };
  if (!isFormData) {
    options.headers = { "Content-Type": "application/json" };
  }
  const res = await fetch(`${API_BASE}${path}`, options);
  const data = await safeJson(res);
  if (!res.ok || data?.status === "error") {
    throw new Error(data?.message || data?.detail || `POST ${path} failed (${res.status})`);
  }
  return data;
}

export { API_BASE, get, post, safeJson };
