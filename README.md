# DME Automation EA FC

Projeto para automatizar tarefas repetitivas do EA FC Web App com foco em uso no iPhone.

## MVP atual

Uma dashboard mobile-first para planejar o fluxo, registrar restrições e servir de base para o automação futura.

## Como rodar

```bash
python3 server.py
```

Depois abra `http://localhost:8000`.

## API local

- `GET /api/health`
- `GET /api/state`
- `POST /api/observations`
- `POST /api/plans`
- `POST /api/approvals`

## Arquitetura recomendada

### 1) Frontend mobile-first
- Uma interface web responsiva ou PWA.
- Acessível no Safari do iPhone.
- Responsável por mostrar fila, status, log e ações manuais.

### 2) Backend de automação
- Serviço que executa o fluxo real de automação.
- Mantém sessão, estado da conta e fila de tarefas.
- Não depende do Safari do iPhone para a lógica principal.

### 3) Motor de automação
- Interage com o EA FC Web App.
- Trabalha por etapas: abrir tela, selecionar SBC, preencher requisitos, confirmar, repetir.
- Deve tolerar mudanças de interface com seletores e fallback.

### 4) Persistência
- Salvar:
  - conta/sessão
  - preferências
  - tarefas pendentes
  - últimos fluxos executados

### 5) Execução segura
- Nunca automatizar 2FA.
- Quando houver verificação humana, pausar e pedir intervenção.
- Registrar erros e recargas de página.

## Por que não usar só bookmarklet no iPhone

- Funciona apenas como atalho.
- É frágil em páginas dinâmicas.
- Perde estado facilmente.
- Fica difícil manter fluxo longo e repetível.

## O que o bookmarklet pode fazer

- Disparar uma ação rápida na página atual.
- Ler elementos visíveis.
- Abrir um painel simples.

## O que deve ficar no backend

- Regras de automação.
- Sequência de cliques.
- Repetições.
- Logs.
- Controle de tarefas.

## Fluxo inicial sugerido

1. Login manual.
2. Abrir a Home.
3. Navegar até SBC.
4. Selecionar um desafio.
5. Montar a solução.
6. Confirmar.
7. Repetir conforme configuração.

## Próximo passo

Definir o primeiro fluxo alvo e transformar isso em um protótipo pequeno.
