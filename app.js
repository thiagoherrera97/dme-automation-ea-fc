const constraints = [
  'Não fazer transferências',
  'Não vender jogadores',
  'Não concluir DME sem autorização',
  'Explorar apenas telas e botões quando não houver autorização',
];

const flow = [
  'Abrir EA FC Web App e validar sessão',
  'Ir para FUTGenie no próprio web app',
  'Ler a tela atual e os requisitos do desafio',
  'Mapear botões e opções do solver',
  'Pedir aprovação antes de qualquer ação destrutiva',
];

const buttons = [
  'Auto Complete',
  'Exchange Players',
  'Use Squad Builder',
  'Clear Squad',
  'More FUTGenie Options',
  'Quick complete',
  'Search SBCs...',
  'Work Area',
  'Submit',
];

const architecture = [
  'Frontend mobile-first para iPhone',
  'Backend separado para automação futura',
  'Camada de aprovação humana para ações destrutivas',
  'Registro de estado e auditoria',
  'Parser de telas como base do fluxo',
];

const safety = [
  ['Nunca submeter DME automaticamente', 'Se o fluxo exigir DME, parar e pedir autorização.'],
  ['Nunca vender jogadores', 'Somente após aprovação explícita e instrução específica.'],
  ['Nunca mover jogadores para troca', 'Preservar o clube por padrão.'],
  ['Somente exploração livre', 'Inspecionar telas, botões e estados sem consumir ativos.'],
];

function mountList(id, items) {
  const root = document.getElementById(id);
  root.innerHTML = items.map((item) => `<li>${item}</li>`).join('');
}

function mountChips(id, items) {
  const root = document.getElementById(id);
  root.innerHTML = items.map((item) => `<span class="chip">${item}</span>`).join('');
}

function mountSafety() {
  const root = document.getElementById('safety');
  root.innerHTML = safety
    .map(
      ([title, description], index) => `
        <label class="safety-item">
          <input type="checkbox" ${index === 3 ? 'checked' : ''} />
          <div>
            <strong>${title}</strong>
            <p>${description}</p>
          </div>
        </label>
      `,
    )
    .join('');
}

mountList('constraints', constraints);
mountList('flow', flow);
mountChips('buttons', buttons);
mountList('architecture', architecture);
mountSafety();

async function refreshBackendStatus() {
  const root = document.getElementById('backend-status');
  try {
    const response = await fetch('/api/state');
    const state = await response.json();
    root.innerHTML = `
      <strong>Mode:</strong> ${state.mode}<br />
      <strong>Approval required:</strong> ${state.approval_required ? 'yes' : 'no'}<br />
      <strong>Last observation:</strong> ${state.last_observation}<br />
      <strong>Last plan:</strong> ${state.last_plan}<br />
      <strong>Plans:</strong> ${state.plans.length}<br />
      <strong>Observations:</strong> ${state.observations.length}
    `;
  } catch {
    root.textContent = 'Backend offline';
  }
}

async function loadWorkflow() {
  const root = document.getElementById('workflow-status');
  const approval = document.getElementById('approval-preview');
  root.textContent = 'Carregando…';
  const response = await fetch('/api/flows/daily-common-gold-upgrade');
  const workflow = await response.json();
  root.innerHTML = `
    <strong>${workflow.name}</strong><br />
    ${workflow.summary}<br />
    <strong>Requirements:</strong>
    <ul>${workflow.requirements.map((item) => `<li>${item}</li>`).join('')}</ul>
    <strong>Safe steps:</strong>
    <ol>${workflow.safe_steps.map((item) => `<li>${item}</li>`).join('')}</ol>
    <strong>Approval gate:</strong>
    <ul>${workflow.gated_steps.map((item) => `<li>${item}</li>`).join('')}</ul>
  `;
  approval.classList.add('visible');
  approval.innerHTML = `
    <h3>Approval preview</h3>
    <p><strong>Squad:</strong> ${workflow.approval_preview.squad_name}</p>
    <p><strong>Formation:</strong> ${workflow.approval_preview.formation}</p>
    <p><strong>Rating:</strong> ${workflow.approval_preview.rating} | <strong>Chemistry:</strong> ${workflow.approval_preview.chemistry}</p>
    <p><strong>Slots:</strong> ${workflow.approval_preview.players.join(' · ')}</p>
    <div class="approval-actions">
      <button id="approve-workflow" class="approval-button primary" type="button">Submit</button>
      <button id="cancel-workflow" class="approval-button secondary" type="button">Cancel</button>
    </div>
  `;
  document.getElementById('approve-workflow').addEventListener('click', async () => {
    await fetch('/api/approvals', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        approved: true,
        note: 'Daily Common Gold Upgrade approved',
      }),
    });
    await refreshBackendStatus();
    approval.querySelector('.approval-actions').insertAdjacentHTML(
      'afterend',
      '<p style="color: var(--accent-2); margin-top: 10px;">Approval saved. No SBC submitted automatically.</p>',
    );
  });
  document.getElementById('cancel-workflow').addEventListener('click', () => {
    approval.classList.remove('visible');
    approval.innerHTML = '';
  });
}

async function captureSnapshot() {
  const root = document.getElementById('ea-snapshot');
  root.textContent = 'Capturando…';
  const response = await fetch('/api/ea/snapshot');
  const snapshot = await response.json();
  if (!response.ok) {
    root.textContent = `Snapshot failed: ${snapshot.error}`;
    return;
  }
  root.innerHTML = `
    <strong>${snapshot.title}</strong><br />
    <strong>URL:</strong> ${snapshot.url}<br />
    <strong>Nav:</strong> ${snapshot.nav.join(' · ')}<br />
    <strong>Buttons:</strong> ${snapshot.buttons.slice(0, 12).join(' · ')}<br />
    <strong>Preview:</strong><br />
    <pre>${snapshot.body_preview.replace(/[<>&]/g, (c) => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;' }[c]))}</pre>
  `;
}

document.getElementById('record-observation').addEventListener('click', async () => {
  await fetch('/api/observations', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      source: 'frontend',
      note: 'Planning dashboard reviewed',
    }),
  });
  await refreshBackendStatus();
});

document.getElementById('load-workflow').addEventListener('click', async () => {
  await loadWorkflow();
  const response = await fetch('/api/flows/daily-common-gold-upgrade/plan', { method: 'POST' });
  const result = await response.json();
  document.getElementById('workflow-status').innerHTML += `
    <br /><strong>Generated plan:</strong> ${result.plan.name}
  `;
  await refreshBackendStatus();
});

document.getElementById('capture-snapshot').addEventListener('click', captureSnapshot);

refreshBackendStatus();

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').catch(() => {});
  });
}
