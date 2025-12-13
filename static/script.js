document.addEventListener('DOMContentLoaded', () => {
  // Elements
  const runBtn = document.getElementById('runBtn');
  const clearBtn = document.getElementById('clearBtn');
  const instructionEl = document.getElementById('instruction');
  const outputEl = document.getElementById('resultContainer');
  const statusEl = document.getElementById('status');
  const targetEl = document.getElementById('targetUrl');
  const helpBtn = document.getElementById('helpBtn');
  const executeCheckbox = document.getElementById('executeMode');
  const getStarted = document.getElementById('getStarted');

  // Metric counters
  document.querySelectorAll('.metric-value').forEach(el => {
    const target = Number(el.dataset.target || 0);
    if (!target) return;
    let current = 0;
    const step = Math.max(1, Math.floor(target / 80));
    const id = setInterval(() => {
      current += step;
      if (current >= target) { current = target; clearInterval(id); }
      if (String(el.textContent).trim().endsWith('%')) el.textContent = current + '%';
      else if (String(el.textContent).trim().endsWith('h')) el.textContent = current + 'h';
      else el.textContent = current.toLocaleString();
    }, 16);
  });

  // Pretty JSON fallback
  function pretty(obj) {
    try { return JSON.stringify(obj, null, 2); }
    catch (e) { return String(obj); }
  }

  // Render user friendly summary from result object
  function renderUserFriendly(res) {
    // accept either top-level format or nested result (some tests returned nested)
    const info = res.result ? res.result : res;

    const instruction = info.instruction || '—';
    const mode = info.mode || (res.mode || 'simulate');
    const target = info.target || res.target || '—';
    const duration = info.duration_sec ?? res.duration_sec ?? '—';
    const steps = info.step_results || info.steps || [];

    let html = `<div><h3 class="summary-title">Run Summary</h3>`;
    html += `<div class="summary-box">`;
    html += `<p><strong>Instruction:</strong> ${escapeHtml(instruction)}</p>`;
    html += `<p><strong>Mode:</strong> ${escapeHtml(mode)}</p>`;
    html += `<p><strong>Target:</strong> ${escapeHtml(target)}</p>`;
    html += `<p><strong>Duration:</strong> ${duration === '—' ? '—' : Number(duration).toFixed(2) + 's'}</p>`;
    html += `</div>`;

    html += `<h4 style="margin-top:12px; color:var(--text-strong)">Steps Performed</h4>`;
    if (!steps || steps.length === 0) {
      html += `<p style="color:var(--muted)">No detailed steps returned.</p>`;
    } else {
      html += `<ol class="steps-list">`;
      steps.forEach((step, idx) => {
        const action = step.action || step.type || 'action';
        const detail = step.detail || step.value || '';
        const status = (step.status || 'ok').toLowerCase();
        const screenshot = step.screenshot || step.image || null;
        const statusClass = ['ok','simulated','executed'].includes(status) ? 'ok' : (status.includes('timeout') ? 'timeout' : (status.includes('error') ? 'error' : 'simulated'));
        html += `<li class="step-item">`;
        html += `<strong>${escapeHtml(capitalize(action))}</strong> — ${escapeHtml(detail)} `;
        html += `<span class="status-tag ${statusClass}">${escapeHtml(status)}</span>`;
        if (screenshot) {
          // normalize screenshot path: allow both "screenshots\..." and "screenshots/..."
          const normalized = screenshot.replace(/\\\\/g,'/').replace(/\\/g,'/');
          html += `<div style="margin-top:6px;"><a class="screenshot-link" href="/static/${encodeURI(normalized)}" target="_blank" rel="noopener">View Screenshot</a></div>`;
        }
        html += `</li>`;
      });
      html += `</ol>`;
    }

    // raw JSON collapsible
    html += `<details style="margin-top:12px; color:var(--text-soft)"><summary style="cursor:pointer">Show raw response</summary><pre style="margin-top:8px; background:#021027; padding:10px; border-radius:8px; color:#cfeff7; max-height:420px; overflow:auto">${escapeHtml(pretty(res))}</pre></details>`;

    html += `</div>`;
    return html;
  }

  // escape html
  function escapeHtml(s) {
    if (s === null || s === undefined) return '';
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function capitalize(s) {
    if (!s) return s;
    return String(s).charAt(0).toUpperCase() + String(s).slice(1);
  }

  // Run test
  runBtn.addEventListener('click', async () => {
    const instruction = instructionEl.value.trim();
    const target = (targetEl.value || '/test').trim();
    const mode = executeCheckbox && executeCheckbox.checked ? 'execute' : 'simulate';

    if (!instruction) {
      alert('Please enter a test instruction.');
      instructionEl.focus();
      return;
    }

    statusEl.textContent = 'Running…';
    outputEl.innerHTML = '<div class="summary-box">Preparing test…</div>';
    runBtn.disabled = true;

    try {
      const resp = await fetch('/api/run_test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ instruction, target, mode })
      });

      if (!resp.ok) {
        const text = await resp.text();
        statusEl.textContent = 'Error';
        outputEl.textContent = text;
        return;
      }

      const data = await resp.json();
      statusEl.textContent = (data.status || (data.result && data.result.status) || 'done');
      outputEl.innerHTML = renderUserFriendly(data);
      outputEl.scrollTop = 0;
    } catch (err) {
      statusEl.textContent = 'Network error';
      outputEl.textContent = String(err);
    } finally {
      runBtn.disabled = false;
    }
  });

  // Clear button
  clearBtn?.addEventListener('click', () => {
    instructionEl.value = '';
    outputEl.textContent = 'No output yet.';
    statusEl.textContent = 'Waiting for input...';
  });

  // Panels tactile click animation
  document.querySelectorAll('.panel').forEach(panel => {
    panel.addEventListener('click', () => {
      panel.classList.add('clicked');
      setTimeout(() => panel.classList.remove('clicked'), 420);
    });
  });

  // Help modal
  helpBtn?.addEventListener('click', () => {
    showModal({
      title: 'Quick Help',
      body: `
        <p>Example instructions:</p>
        <pre>open /test and type "Harshitha Somu" into Name and click Submit</pre>
        <p>Toggle <strong>Run in real browser</strong> to execute with Playwright (server must support execute mode).</p>
        <p>Screenshots (if produced) will be linked in the results.</p>
      `
    });
  });

  getStarted?.addEventListener('click', () => {
    instructionEl?.focus();
    instructionEl?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });

  // Modal helper
  function showModal({ title = 'Info', body = '' } = {}) {
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.inset = 0;
    overlay.style.background = 'rgba(2,6,23,0.6)';
    overlay.style.display = 'grid';
    overlay.style.placeItems = 'center';
    overlay.style.zIndex = 9999;

    const card = document.createElement('div');
    card.style.background = '#071426';
    card.style.border = '1px solid rgba(255,255,255,0.04)';
    card.style.padding = '20px';
    card.style.borderRadius = '12px';
    card.style.maxWidth = '760px';
    card.style.width = '90%';
    card.style.color = 'var(--text-soft)';
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <strong style="color:var(--text-strong); font-size:1.05rem;">${title}</strong>
        <button aria-label="Close" id="modalClose" style="background:transparent;border:none;color:var(--text-soft);font-size:1.1rem;cursor:pointer">✕</button>
      </div>
      <div style="font-size:0.95rem; line-height:1.5; color:var(--text-soft)">${body}</div>
    `;
    overlay.appendChild(card);
    document.body.appendChild(overlay);

    const close = () => { overlay.remove(); };
    document.getElementById('modalClose')?.addEventListener('click', close);
    overlay.addEventListener('click', (e) => { if (e.target === overlay) close(); });
  }

  // Close modal on Escape
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      document.querySelectorAll('div[role="dialog"]').forEach(d => d.remove());
    }
  });
});
