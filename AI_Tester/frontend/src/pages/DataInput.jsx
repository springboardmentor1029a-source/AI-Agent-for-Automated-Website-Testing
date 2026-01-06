import React, { useState, useEffect } from "react";
import { useTheme } from "../context/ThemeContext";
import "../styles/DataInput.css";

import UploadIllustration from "../assets/upload-illustration.png";
import ProjectIcon from "../assets/icons/Requirements.png";

import PendingIcon from "../assets/icons/Checklist.png";
import ProcessingIcon from "../assets/icons/Process.png";
import CompleteIcon from "../assets/icons/Quality.png";
import ErrorIcon from "../assets/icons/Bug.png";

const API_BASE = import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8000";

const STATUS_CONFIG = {
  pending: { label: "Pending", icon: PendingIcon },
  processing: { label: "Processing", icon: ProcessingIcon },
  complete: { label: "Complete", icon: CompleteIcon },
  error: { label: "Error", icon: ErrorIcon },
};

async function safeJson(res) {
  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    return { error: "Non-JSON response", raw: text };
  }
}

const DataInput = () => {
  const theme = useTheme();

  const [activeTab, setActiveTab] = useState("text");
  const [project, setProject] = useState("checkout-web");

  const [textInput, setTextInput] = useState("");
  const [uploadedFiles, setUploadedFiles] = useState([]);

  const [appConfig, setAppConfig] = useState({
    url: "",
    authType: "none",
    credentials: "",
  });

  const [connectionStatus, setConnectionStatus] = useState("pending");
  const [connectionMessage, setConnectionMessage] = useState("");

  const [analysisStatus, setAnalysisStatus] = useState("pending");
  const [analysisMessage, setAnalysisMessage] = useState("");
  const [lastAnalysis, setLastAnalysis] = useState(null);

  useEffect(() => {
    document.title = "Data Input - Youval AutoQA";
  }, []);

  const handleFiles = (files) => {
    const validTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      "application/zip",
      "text/plain",
      "application/json",
    ];
    const accepted = Array.from(files).filter((file) => validTypes.includes(file.type));
    setUploadedFiles((prev) => [...prev, ...accepted]);
  };

  const onDrop = (event) => {
    event.preventDefault();
    event.stopPropagation();
    handleFiles(event.dataTransfer.files);
  };

  const onFileChange = (event) => {
    handleFiles(event.target.files);
  };

  const removeFile = (index) => {
    setUploadedFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const testConnection = async () => {
    if (!appConfig.url) {
      setConnectionStatus("error");
      setConnectionMessage("Enter an application URL to test connectivity.");
      return;
    }

    setConnectionStatus("processing");
    setConnectionMessage("Testing application connectivity...");

    try {
      const res = await fetch(`${API_BASE}/api/health`);
      if (!res.ok) throw new Error(`Backend health failed (${res.status})`);
      setConnectionStatus("complete");
      setConnectionMessage("Backend reachable. App URL saved for analysis/run.");
    } catch (e) {
      setConnectionStatus("error");
      setConnectionMessage(`Backend not reachable: ${e.message}`);
    }
  };

  const analyzeText = async () => {
    if (!textInput.trim()) return;

    if (!appConfig.url.trim()) {
      setAnalysisStatus("error");
      setAnalysisMessage("Please enter Application URL (right panel) before analyzing.");
      return;
    }

    setAnalysisStatus("processing");
    setAnalysisMessage("Sending requirement text to AI backend...");

    try {
      const body = {
        projectId: project,
        applicationUrl: appConfig.url,
        targetType: "website",
        requirementText: textInput,
      };

      const res = await fetch(`${API_BASE}/api/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const data = await safeJson(res);
      if (!res.ok) throw new Error(data?.detail || data?.message || `Analyze failed (${res.status})`);

      setLastAnalysis(data);
      setAnalysisStatus("complete");
      setAnalysisMessage("Analysis saved. Open Analysis Review to approve scenario.");
    } catch (e) {
      setAnalysisStatus("error");
      setAnalysisMessage(e.message);
    }
  };

  const analyzeDocuments = async () => {
    if (!uploadedFiles.length) return;

    if (!appConfig.url.trim()) {
      setAnalysisStatus("error");
      setAnalysisMessage("Please enter Application URL (right panel) before analyzing.");
      return;
    }

    setAnalysisStatus("processing");
    setAnalysisMessage("Uploading file to AI backend for analysis...");

    try {
      const file = uploadedFiles[0];
      const form = new FormData();
      form.append("projectId", project);
      form.append("applicationUrl", appConfig.url);
      form.append("targetType", "website");
      form.append("file", file);

      const res = await fetch(`${API_BASE}/api/analyze/upload`, {
        method: "POST",
        body: form,
      });

      const data = await safeJson(res);
      if (!res.ok) throw new Error(data?.detail || data?.message || `Upload analyze failed (${res.status})`);

      setLastAnalysis(data);
      setAnalysisStatus("complete");
      setAnalysisMessage("Analysis saved from uploaded file. Open Analysis Review to approve scenario.");
    } catch (e) {
      setAnalysisStatus("error");
      setAnalysisMessage(e.message);
    }
  };

  const statusMeta = STATUS_CONFIG[connectionStatus] || STATUS_CONFIG.pending;
  const analysisMeta = STATUS_CONFIG[analysisStatus] || STATUS_CONFIG.pending;

  return (
    <main className={`di-page di-page--${theme}`}>
      <header className="di-header">
        <h1>Data Input</h1>
        <p>
          Provide requirements and application context so Youval AutoQA can design and execute the right tests for your
          project.
        </p>
      </header>

      <div className="di-layout">
        <section className="di-left glass-surface">
          <div className="di-project">
            <div className="di-project-main">
              <img src={ProjectIcon} alt="Project" />
              <div>
                <h2>Project Selector</h2>
                <p>Select which project this input belongs to.</p>
              </div>
            </div>

            <select value={project} onChange={(e) => setProject(e.target.value)}>
              <option value="checkout-web">Checkout Web</option>
              <option value="mobile-app">Mobile App</option>
              <option value="admin-portal">Admin Portal</option>
            </select>
          </div>

          <div className="di-tabs">
            {[
              { id: "text", label: "Text Input" },
              { id: "file", label: "File Upload" },
              { id: "folder", label: "Folder ZIP Upload" },
              { id: "recent", label: "Recent Inputs" },
            ].map(({ id, label }) => (
              <button
                key={id}
                type="button"
                className={`di-tab ${activeTab === id ? "di-tab--active" : ""}`}
                onClick={() => setActiveTab(id)}
              >
                {label}
              </button>
            ))}
          </div>

          <div className="di-tab-panel">
            {activeTab === "text" && (
              <div className="di-text-panel">
                <label htmlFor="di-text">Text Requirements</label>
                <textarea
                  id="di-text"
                  rows={8}
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                  placeholder="Describe flows, rules, and edge cases in clear English."
                />
                <button type="button" className="btn btn-primary" disabled={!textInput.trim()} onClick={analyzeText}>
                  Analyze Text
                </button>
              </div>
            )}

            {activeTab === "file" && (
              <div className="di-upload" onDragOver={(e) => e.preventDefault()} onDrop={onDrop}>
                <div className="di-upload-hero">
                  <img src={UploadIllustration} alt="Upload" />
                  <p className="di-upload-title">Upload PDF, DOCX, XLSX, TXT, JSON, or ZIP</p>
                  <p className="di-upload-sub">Drag and drop files here, or choose from your system.</p>

                  <label className="di-upload-button">
                    <input type="file" multiple onChange={onFileChange} />
                    <span>Select Files</span>
                  </label>
                </div>

                {uploadedFiles.length > 0 && (
                  <>
                    <ul className="di-file-list">
                      {uploadedFiles.map((file, index) => (
                        <li key={`${file.name}-${index}`}>
                          <span className="di-file-name">{file.name}</span>
                          <button type="button" className="di-file-remove" onClick={() => removeFile(index)}>
                            Remove
                          </button>
                        </li>
                      ))}
                    </ul>

                    <button
                      type="button"
                      className="btn btn-primary di-upload-cta"
                      disabled={uploadedFiles.length === 0}
                      onClick={analyzeDocuments}
                    >
                      Analyze Documents
                    </button>
                  </>
                )}
              </div>
            )}

            {activeTab === "folder" && (
              <div className="di-info-block">
                <p>Bundle specifications into a single ZIP, then upload it from the File Upload tab.</p>
                <p>Folder and file names are preserved so generated tests can reference the original structure.</p>
              </div>
            )}

            {activeTab === "recent" && (
              <div className="di-info-block">
                <p>Recent inputs for this project will appear here.</p>
                <p>Use them to extend coverage or re-run analysis when requirements evolve.</p>
              </div>
            )}
          </div>

          <div style={{ marginTop: 16 }}>
            <div className="di-status">
              <span className={`di-status-pill di-status-pill--${analysisStatus}`}>
                <img src={analysisMeta.icon} alt={analysisMeta.label} />
                <span>{analysisMeta.label}</span>
              </span>
              <p className="di-status-text">{analysisMessage}</p>
            </div>

            {lastAnalysis?.scenario?.title && (
              <div className="di-info-block" style={{ marginTop: 10 }}>
                <p>
                  Latest scenario: <strong>{lastAnalysis.scenario.title}</strong>
                </p>
              </div>
            )}
          </div>
        </section>

        <aside className="di-right glass-surface">
          <h2>Application Configuration</h2>
          <p>Configure how Youval AutoQA connects to the application under test for this project.</p>

          <div className="di-field">
            <label htmlFor="di-url">Application URL</label>
            <input
              id="di-url"
              type="url"
              value={appConfig.url}
              onChange={(e) => setAppConfig((prev) => ({ ...prev, url: e.target.value }))}
              placeholder="https://app.your-domain.com"
            />
          </div>

          <div className="di-field">
            <label htmlFor="di-auth">Auth Type</label>
            <select
              id="di-auth"
              value={appConfig.authType}
              onChange={(e) => setAppConfig((prev) => ({ ...prev, authType: e.target.value }))}
            >
              <option value="none">None</option>
              <option value="basic">Basic Auth</option>
              <option value="bearer">Bearer Token</option>
              <option value="api-key">API Key</option>
            </select>
          </div>

          <div className="di-field">
            <label htmlFor="di-creds">Credentials / Token</label>
            <textarea
              id="di-creds"
              rows={4}
              value={appConfig.credentials}
              onChange={(e) => setAppConfig((prev) => ({ ...prev, credentials: e.target.value }))}
              placeholder="Environment variables, keys, or tokens."
            />
          </div>

          <div className="di-status-row">
            <button type="button" className="btn btn-outline" onClick={testConnection}>
              Test Backend Connection
            </button>

            <div className="di-status">
              <span className={`di-status-pill di-status-pill--${connectionStatus}`}>
                <img src={statusMeta.icon} alt={statusMeta.label} />
                <span>{statusMeta.label}</span>
              </span>
              <p className="di-status-text">{connectionMessage}</p>
            </div>
          </div>
        </aside>
      </div>
    </main>
  );
};

export default DataInput;
