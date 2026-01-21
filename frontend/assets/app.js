const DEFAULT_CODE = `sun_we
    chilla_we "Hello Jatti!"
ja_we
`;

const samples = [
  {
    name: 'Hello',
    code: DEFAULT_CODE,
  },
  {
    name: 'If/Else',
    code: `sun_we
    chal_oye x ban 5
    je x vadha_hai 3
        chilla_we "big"
    nahin_taan
        chilla_we "small"
ja_we
`,
  },
  {
    name: 'Loops',
    code: `sun_we
    chal_oye total ban 0
    har_ek i range_banao(1, 6)
        chal_oye total ban total + i
    chilla_we total
ja_we
`,
  },
  {
    name: 'Try/Pakad',
    code: `sun_we
    chal_koshish_karle
        chal_oye x ban 10 / 0
    pakad err
        chilla_we err
ja_we
`,
  },
];

function $(id) {
  return document.getElementById(id);
}

function setStatus(text, kind = 'info') {
  const el = $('status');
  el.textContent = text ? `(${text})` : '';
  el.style.color = kind === 'error' ? 'var(--danger)' : kind === 'ok' ? 'var(--ok)' : 'var(--muted)';
}

function appendOutput(text) {
  const out = $('output');
  out.textContent = text;
}

async function runCode(cm) {
  setStatus('running…');
  $('runBtn').disabled = true;

  try {
    const resp = await fetch('/api/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code: cm.getValue() }),
    });

    const data = await resp.json().catch(() => null);
    if (!data) {
      setStatus('bad response', 'error');
      appendOutput('Server returned a non-JSON response.');
      return;
    }

    if (!resp.ok || !data.success) {
      setStatus('error', 'error');

      if (resp.status === 401 || data?.error === 'Unauthorized') {
        appendOutput(
          'Unauthorized. Click "Demo Mode" (top bar) or use admin access, then try again.'
        );
      } else {
        appendOutput(data.output || data.error || 'Unknown error');
      }
      return;
    }

    setStatus('ok', 'ok');
    appendOutput(data.output ?? '');
  } catch (e) {
    setStatus('offline?', 'error');
    appendOutput(String(e));
  } finally {
    $('runBtn').disabled = false;
  }
}

(function init() {
  const select = $('sampleSelect');
  for (const s of samples) {
    const opt = document.createElement('option');
    opt.value = s.name;
    opt.textContent = s.name;
    select.appendChild(opt);
  }

  const cm = CodeMirror.fromTextArea($('codeArea'), {
    lineNumbers: true,
    tabSize: 4,
    indentUnit: 4,
    theme: 'material-darker',
    mode: 'python',
  });

  cm.setValue(DEFAULT_CODE);

  select.addEventListener('change', () => {
    const s = samples.find(x => x.name === select.value);
    cm.setValue(s ? s.code : DEFAULT_CODE);
  });

  $('runBtn').addEventListener('click', () => runCode(cm));
  $('clearBtn').addEventListener('click', () => {
    appendOutput('');
    setStatus('');
  });

  // Ctrl/Cmd+Enter
  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      runCode(cm);
    }
  });
})();
