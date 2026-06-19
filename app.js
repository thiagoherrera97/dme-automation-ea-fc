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

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').catch(() => {});
  });
}
