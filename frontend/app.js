/* ── Config ──────────────────────────────────────────────────── */
const API = 'http://localhost:8000';

/* ── DOM refs ────────────────────────────────────────────────── */
const textarea     = document.getElementById('journal-input');
const charCountEl  = document.getElementById('char-count');
const saveBtn      = document.getElementById('save-btn');
const insightsSec  = document.getElementById('insights-section');
const topbarDate   = document.getElementById('topbar-date');
const entryList    = document.getElementById('entry-list');
const sidebar      = document.getElementById('sidebar');
const sidebarOver  = document.getElementById('sidebar-overlay');
const openSidebar  = document.getElementById('open-sidebar');
const closeSidebar = document.getElementById('sidebar-close');
const modalBack    = document.getElementById('modal-backdrop');
const modalDate    = document.getElementById('modal-date');
const modalContent = document.getElementById('modal-content');
const modalInsights= document.getElementById('modal-insights');
const modalDelete  = document.getElementById('modal-delete');
const modalClose   = document.getElementById('modal-close');

/* ── Colour maps ─────────────────────────────────────────────── */
const MOOD_COLORS = {
  teal:   '#1D9E75',
  blue:   '#2B6CB0',
  amber:  '#C47A1E',
  coral:  '#C05337',
  purple: '#5B4DBE',
};

/* ── State ───────────────────────────────────────────────────── */
let activeEntryId = null;

/* ── Init ────────────────────────────────────────────────────── */
(function init() {
  // Set topbar date
  topbarDate.textContent = new Date().toLocaleDateString('en-GB', {
    weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
  });

  // Char counter
  textarea.addEventListener('input', () => {
    charCountEl.textContent = textarea.value.length;
  });

  // Save button
  saveBtn.addEventListener('click', handleSave);

  // Sidebar
  openSidebar.addEventListener('click', openSidebarPanel);
  closeSidebar.addEventListener('click', closeSidebarPanel);
  sidebarOver.addEventListener('click', closeSidebarPanel);

  // Modal close
  modalClose.addEventListener('click', closeModal);
  modalBack.addEventListener('click', (e) => { if (e.target === modalBack) closeModal(); });

  // Load existing entries into sidebar
  loadEntries();
})();

/* ── Save entry ──────────────────────────────────────────────── */
async function handleSave() {
  const content = textarea.value.trim();
  if (!content) return showToast('Please write something first.');

  saveBtn.disabled = true;
  saveBtn.textContent = 'Saving…';

  try {
    // 1. Save the entry
    const entry = await post('/entries', { content });

    // 2. Show loading skeletons while insights are generated
    renderSkeletons();

    // 3. Generate insights
    const { insights } = await post('/insights', { entry_id: entry.id });

    // 4. Render insights
    renderInsights(insights);

    // 5. Refresh sidebar
    loadEntries();

    // 6. Clear textarea
    textarea.value = '';
    charCountEl.textContent = '0';

    showToast('Entry saved ✓');
  } catch (err) {
    insightsSec.innerHTML = '';
    showToast('Something went wrong. Is the backend running?');
    console.error(err);
  } finally {
    saveBtn.disabled = false;
    saveBtn.textContent = 'Save entry';
  }
}

/* ── Render helpers ──────────────────────────────────────────── */
function renderSkeletons() {
  insightsSec.innerHTML = `
    <p class="insights-heading">Analysing your entry…</p>
    ${['60%','80%','45%'].map(w => `
      <div class="skeleton-card">
        <div class="skeleton-line" style="width:${w}"></div>
        <div class="skeleton-line" style="width:90%"></div>
        <div class="skeleton-line" style="width:70%"></div>
      </div>`).join('')}
  `;
}

function renderInsights(insights, container = insightsSec) {
  if (!insights) { container.innerHTML = ''; return; }
  const { mood, summary, actions, themes } = insights;
  const moodColor = MOOD_COLORS[mood?.color] || MOOD_COLORS.teal;
  const pct = Math.round(((mood?.score ?? 5) / 10) * 100);

  container.innerHTML = `
    <p class="insights-heading">Today's insights</p>

    <!-- Mood card -->
    <div class="insight-card">
      <div class="insight-card-header">
        <span class="insight-tag">Mood</span>
      </div>
      <div class="mood-row">
        <span class="mood-label" style="color:${moodColor}">${esc(mood?.label ?? '—')}</span>
        <div class="mood-bar-track">
          <div class="mood-bar-fill" style="width:${pct}%;background:${moodColor}"></div>
        </div>
        <span class="mood-score">${mood?.score ?? '?'}/10</span>
      </div>
      ${themes?.length ? `
        <div class="themes-row">
          ${themes.map(t => `<span class="theme-pill">${esc(t)}</span>`).join('')}
        </div>` : ''}
    </div>

    <!-- Summary card -->
    <div class="insight-card">
      <div class="insight-card-header">
        <span class="insight-tag">Summary</span>
      </div>
      <p class="summary-text">${esc(summary ?? '')}</p>
    </div>

    <!-- Actions card -->
    <div class="insight-card">
      <div class="insight-card-header">
        <span class="insight-tag">Reflections</span>
      </div>
      <div class="action-list">
        ${(actions ?? []).map(a => `
          <div class="action-item">
            <div class="action-dot"></div>
            <span>${esc(a)}</span>
          </div>`).join('')}
      </div>
    </div>
  `;
}

/* ── Sidebar ─────────────────────────────────────────────────── */
function openSidebarPanel() {
  sidebar.classList.add('open');
  sidebarOver.classList.add('visible');
}
function closeSidebarPanel() {
  sidebar.classList.remove('open');
  sidebarOver.classList.remove('visible');
}

async function loadEntries() {
  try {
    const entries = await get('/entries');
    renderEntryList(entries);
  } catch {
    /* backend might not be running yet */
  }
}

function renderEntryList(entries) {
  if (!entries.length) {
    entryList.innerHTML = '<li class="entry-list-empty">No entries yet.</li>';
    return;
  }
  entryList.innerHTML = entries.map(e => {
    const moodColor = e.insights?.mood?.color
      ? MOOD_COLORS[e.insights.mood.color]
      : '#9E9890';
    const moodLabel = e.insights?.mood?.label ?? '';
    const preview = e.content.slice(0, 80) + (e.content.length > 80 ? '…' : '');
    const dateStr = formatDate(e.date);
    return `
      <li class="entry-list-item" data-id="${e.id}">
        <div class="entry-list-date">
          <span class="mood-dot" style="background:${moodColor}"></span>
          ${dateStr}${moodLabel ? ' · ' + esc(moodLabel) : ''}
        </div>
        <div class="entry-list-preview">${esc(preview)}</div>
      </li>`;
  }).join('');

  entryList.querySelectorAll('.entry-list-item').forEach(li => {
    li.addEventListener('click', () => {
      const id = parseInt(li.dataset.id, 10);
      openEntryModal(id, entries);
      closeSidebarPanel();
    });
  });
}

/* ── Modal ───────────────────────────────────────────────────── */
function openEntryModal(id, entries) {
  const entry = entries.find(e => e.id === id);
  if (!entry) return;

  activeEntryId = id;
  modalDate.textContent = formatDate(entry.date);
  modalContent.textContent = entry.content;

  if (entry.insights) {
    renderInsights(entry.insights, modalInsights);
  } else {
    modalInsights.innerHTML = '<p style="font-size:.85rem;color:var(--text-3);padding:.5rem 0;font-style:italic;">No insights generated for this entry.</p>';
  }

  modalBack.classList.add('open');
}

function closeModal() {
  modalBack.classList.remove('open');
  activeEntryId = null;
}

modalDelete.addEventListener('click', async () => {
  if (!activeEntryId) return;
  if (!confirm('Delete this entry? This cannot be undone.')) return;
  try {
    await del(`/entries/${activeEntryId}`);
    closeModal();
    loadEntries();
    showToast('Entry deleted.');
  } catch {
    showToast('Could not delete entry.');
  }
});

/* ── API helpers ─────────────────────────────────────────────── */
async function get(path) {
  const res = await fetch(API + path);
  if (!res.ok) throw new Error(`GET ${path} → ${res.status}`);
  return res.json();
}

async function post(path, body) {
  const res = await fetch(API + path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `POST ${path} → ${res.status}`);
  }
  return res.json();
}

async function del(path) {
  const res = await fetch(API + path, { method: 'DELETE' });
  if (!res.ok) throw new Error(`DELETE ${path} → ${res.status}`);
}

/* ── Utils ───────────────────────────────────────────────────── */
function esc(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function formatDate(iso) {
  if (!iso) return '';
  const [y, m, d] = iso.split('-').map(Number);
  return new Date(y, m - 1, d).toLocaleDateString('en-GB', {
    day: 'numeric', month: 'long', year: 'numeric',
  });
}

let toastTimer;
function showToast(msg) {
  let toast = document.querySelector('.toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.className = 'toast';
    document.body.appendChild(toast);
  }
  clearTimeout(toastTimer);
  toast.textContent = msg;
  toast.classList.add('show');
  toastTimer = setTimeout(() => toast.classList.remove('show'), 3000);
}
