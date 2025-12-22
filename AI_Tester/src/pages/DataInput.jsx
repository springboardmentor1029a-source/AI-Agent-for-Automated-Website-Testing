// src/pages/DataInput.jsx
import React, { useState, useEffect } from 'react';
import { useTheme } from '../context/ThemeContext';
import '../styles/DataInput.css';

// Images from assets only
import UploadIllustration from '../assets/upload-illustration.png';
import ProjectIcon from '../assets/icons/Requirements.png';

// Status icons from /src/icons (under assets/icons)
import PendingIcon from '../assets/icons/Checklist.png';
import ProcessingIcon from '../assets/icons/Process.png';
import CompleteIcon from '../assets/icons/Quality.png';
import ErrorIcon from '../assets/icons/Bug.png';

const STATUS_CONFIG = {
  pending: { label: 'Pending', icon: PendingIcon },
  processing: { label: 'Processing', icon: ProcessingIcon },
  complete: { label: 'Complete', icon: CompleteIcon },
  error: { label: 'Error', icon: ErrorIcon }
};

const DataInput = () => {
  const { theme } = useTheme();

  const [activeTab, setActiveTab] = useState('text');
  const [project, setProject] = useState('checkout-web');
  const [textInput, setTextInput] = useState('');
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [appConfig, setAppConfig] = useState({
    url: '',
    authType: 'none',
    credentials: ''
  });
  const [connectionStatus, setConnectionStatus] = useState('pending');
  const [connectionMessage, setConnectionMessage] = useState('');

  useEffect(() => {
    document.title = 'Data Input - Youval AutoQA';
  }, []);

  const handleFiles = (files) => {
    const validTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'application/zip',
      'text/plain',
      'application/json'
    ];
    const accepted = Array.from(files).filter((file) =>
      validTypes.includes(file.type)
    );
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

  const analyzeText = () => {
    if (!textInput.trim()) return;
    console.log('Analyze text input', { project, textInput });
  };

  const analyzeDocuments = () => {
    if (!uploadedFiles.length) return;
    console.log('Analyze documents', { project, uploadedFiles });
  };

  const testConnection = () => {
    if (!appConfig.url) {
      setConnectionStatus('error');
      setConnectionMessage('Enter an application URL to test connectivity.');
      return;
    }

    setConnectionStatus('processing');
    setConnectionMessage('Testing application connectivity and authentication...');

    setTimeout(() => {
      setConnectionStatus('complete');
      setConnectionMessage(
        'Connection successful. The environment is reachable for automated runs.'
      );
    }, 900);
  };

  const statusMeta = STATUS_CONFIG[connectionStatus];

  return (
    <main className={`di-page di-page--${theme}`}>
      <header className="di-header">
        <h1>Data Input</h1>
        <p>
          Provide requirements and application context so Youval AutoQA can
          design and execute the right tests for your project.
        </p>
      </header>

      <div className="di-layout">
        {/* Left side: Project selector + Tabs */}
        <section className="di-left glass-surface">
          <div className="di-project">
            <div className="di-project-main">
              <img src={ProjectIcon} alt="Project" />
              <div>
                <h2>Project Selector</h2>
                <p>Select which project this input belongs to.</p>
              </div>
            </div>
            <select
              value={project}
              onChange={(e) => setProject(e.target.value)}
            >
              <option value="checkout-web">Checkout Web</option>
              <option value="mobile-app">Mobile App</option>
              <option value="admin-portal">Admin Portal</option>
            </select>
          </div>

          <div className="di-tabs">
            {[
              ['text', 'Text Input'],
              ['file', 'File Upload'],
              ['folder', 'Folder / ZIP Upload'],
              ['recent', 'Recent Inputs']
            ].map(([id, label]) => (
              <button
                key={id}
                type="button"
                className={
                  'di-tab' + (activeTab === id ? ' di-tab--active' : '')
                }
                onClick={() => setActiveTab(id)}
              >
                {label}
              </button>
            ))}
          </div>

          <div className="di-tab-panel">
            {activeTab === 'text' && (
              <div className="di-text-panel">
                <label htmlFor="di-text">Text Requirements</label>
                <textarea
                  id="di-text"
                  rows={8}
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                  placeholder="Describe flows, rules, and edge cases in clear English."
                />
                <button
                  type="button"
                  className="btn btn-primary"
                  disabled={!textInput.trim()}
                  onClick={analyzeText}
                >
                  Analyze Text
                </button>
              </div>
            )}

            {activeTab === 'file' && (
              <div
                className="di-upload"
                onDragOver={(e) => e.preventDefault()}
                onDrop={onDrop}
              >
                <div className="di-upload-hero">
                  <img src={UploadIllustration} alt="Upload" />
                </div>
                <p className="di-upload-title">
                  Upload PDF, DOCX, XLSX, TXT, JSON, or ZIP
                </p>
                <p className="di-upload-sub">
                  Drag and drop files here, or choose from your system.
                </p>

                <label className="di-upload-button">
                  <input
                    type="file"
                    multiple
                    onChange={onFileChange}
                  />
                  <span>Select Files</span>
                </label>

                {uploadedFiles.length > 0 && (
                  <ul className="di-file-list">
                    {uploadedFiles.map((file, index) => (
                      <li key={file.name + index}>
                        <span className="di-file-name">{file.name}</span>
                        <button
                          type="button"
                          className="di-file-remove"
                          onClick={() => removeFile(index)}
                        >
                          Remove
                        </button>
                      </li>
                    ))}
                  </ul>
                )}

                <button
                  type="button"
                  className="btn btn-primary di-upload-cta"
                  disabled={uploadedFiles.length === 0}
                  onClick={analyzeDocuments}
                >
                  Analyze Documents
                </button>
              </div>
            )}

            {activeTab === 'folder' && (
              <div className="di-info-block">
                <p>
                  Bundle specifications, spreadsheets, and supporting files into
                  a single ZIP, then upload it from the File Upload tab.
                </p>
                <p>
                  Folder and file names are preserved so generated tests can
                  reference the original structure.
                </p>
              </div>
            )}

            {activeTab === 'recent' && (
              <div className="di-info-block">
                <p>Recent inputs for this project will appear here.</p>
                <p>
                  Use them to extend coverage or re-run analysis when
                  requirements evolve.
                </p>
              </div>
            )}
          </div>
        </section>

        {/* Right side: Application Configuration */}
        <aside className="di-right glass-surface">
          <h2>Application Configuration</h2>
          <p>
            Configure how Youval AutoQA connects to the application under test
            for this project.
          </p>

          <div className="di-field">
            <label htmlFor="di-url">Application URL</label>
            <input
              id="di-url"
              type="url"
              value={appConfig.url}
              onChange={(e) =>
                setAppConfig((prev) => ({ ...prev, url: e.target.value }))
              }
              placeholder="https://app.your-domain.com"
            />
          </div>

          <div className="di-field">
            <label htmlFor="di-auth">Auth Type</label>
            <select
              id="di-auth"
              value={appConfig.authType}
              onChange={(e) =>
                setAppConfig((prev) => ({ ...prev, authType: e.target.value }))
              }
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
              onChange={(e) =>
                setAppConfig((prev) => ({
                  ...prev,
                  credentials: e.target.value
                }))
              }
              placeholder="Environment variables, keys, or tokens. Store sensitive values securely in production."
            />
          </div>

          <div className="di-status-row">
            <button
              type="button"
              className="btn btn-outline"
              onClick={testConnection}
            >
              Test Connection
            </button>
            <div className="di-status">
              <span
                className={`di-status-pill di-status-pill--${connectionStatus}`}
              >
                <img src={statusMeta.icon} alt={statusMeta.label} />
                <span>{statusMeta.label}</span>
              </span>
              {connectionMessage && (
                <p className="di-status-text">{connectionMessage}</p>
              )}
            </div>
          </div>
        </aside>
      </div>
    </main>
  );
};

export default DataInput;
