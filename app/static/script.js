// ===================================
// Sistema Financeiro - JavaScript
// ===================================

const API_BASE = '/api';

// --- Mapas de nomes (cache) ---
let usersMap = {};
let categoriesMap = {};

// ===================================
// HELPERS
// ===================================

async function apiRequest(endpoint, method = 'GET', body = null) {
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' }
  };
  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(`${API_BASE}${endpoint}`, options);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.erro || 'Erro na requisição.');
  }
  return data;
}

function showMessage(containerId, text, isError = false) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = `<div class="message ${isError ? 'error' : 'success'}">${text}</div>`;
  setTimeout(() => { container.innerHTML = ''; }, 4000);
}

function formatDate(isoString) {
  const date = new Date(isoString);
  return date.toLocaleDateString('pt-BR') + ' ' + date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
}

function formatCurrency(value) {
  return parseFloat(value).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

function getUserName(id) {
  return usersMap[id] || `Usuário #${id}`;
}

function getCategoryName(id) {
  return categoriesMap[id] || `Categoria #${id}`;
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

async function loadMaps() {
  try {
    const users = await apiRequest('/users');
    users.forEach(u => { usersMap[u.id] = u.nome; });
  } catch (e) { /* silencioso */ }
  try {
    const cats = await apiRequest('/categories');
    cats.forEach(c => { categoriesMap[c.id] = c.nome; });
  } catch (e) { /* silencioso */ }
}

async function populateUserSelect(selectId, addAll = false) {
  const select = document.getElementById(selectId);
  if (!select) return;

  try {
    const users = await apiRequest('/users');
    select.innerHTML = addAll
      ? '<option value="">Todos os usuários</option>'
      : '<option value="">Selecione um usuário</option>';
    users.forEach(user => {
      select.innerHTML += `<option value="${user.id}">${escapeHtml(user.nome)} (${escapeHtml(user.email)})</option>`;
    });
  } catch (err) {
    console.error('Erro ao carregar usuários:', err);
  }
}

async function populateCategorySelect(selectId, userId = null) {
  const select = document.getElementById(selectId);
  if (!select) return;

  try {
    const endpoint = userId ? `/categories?user_id=${userId}` : '/categories';
    const categories = await apiRequest(endpoint);
    select.innerHTML = '<option value="">Selecione uma categoria</option>';
    categories.forEach(cat => {
      select.innerHTML += `<option value="${cat.id}">${escapeHtml(cat.nome)}</option>`;
    });
  } catch (err) {
    console.error('Erro ao carregar categorias:', err);
  }
}

// ===================================
// MODAL DE CONFIRMAÇÃO
// ===================================

function createConfirmModal() {
  if (document.getElementById('confirm-modal')) return;

  const modal = document.createElement('div');
  modal.id = 'confirm-modal';
  modal.innerHTML = `
    <div class="modal-overlay" id="modal-overlay">
      <div class="modal-box">
        <div class="modal-icon">⚠️</div>
        <h3 id="modal-title">Confirmação</h3>
        <p id="modal-text">Tem certeza?</p>
        <div class="modal-buttons">
          <button class="btn btn-modal-cancel" id="modal-cancel">Cancelar</button>
          <button class="btn btn-modal-confirm" id="modal-confirm">Excluir</button>
        </div>
      </div>
    </div>
  `;
  document.body.appendChild(modal);

  // Estilos do modal
  const style = document.createElement('style');
  style.textContent = `
    .modal-overlay {
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(4px);
      z-index: 1000;
      justify-content: center;
      align-items: center;
    }
    .modal-overlay.active {
      display: flex;
      animation: modalFadeIn 0.2s ease;
    }
    .modal-box {
      background: var(--bg-secondary);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 2rem;
      max-width: 400px;
      width: 90%;
      text-align: center;
      box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    .modal-icon {
      font-size: 2.5rem;
      margin-bottom: 0.75rem;
    }
    .modal-box h3 {
      font-size: 1.2rem;
      margin-bottom: 0.5rem;
      color: var(--text-primary);
    }
    .modal-box p {
      color: var(--text-secondary);
      font-size: 0.9rem;
      margin-bottom: 1.5rem;
      line-height: 1.5;
    }
    .modal-buttons {
      display: flex;
      gap: 0.75rem;
    }
    .btn-modal-cancel {
      flex: 1;
      background: var(--bg-input);
      color: var(--text-secondary);
      border: 1px solid var(--border);
      padding: 0.625rem 1rem;
    }
    .btn-modal-cancel:hover {
      background: var(--border);
      color: var(--text-primary);
    }
    .btn-modal-confirm {
      flex: 1;
      background: var(--danger);
      color: white;
      padding: 0.625rem 1rem;
    }
    .btn-modal-confirm:hover {
      background: var(--danger-hover);
      transform: translateY(-1px);
    }
    @keyframes modalFadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
  `;
  document.head.appendChild(style);
}

function showConfirmModal(title, text) {
  createConfirmModal();

  document.getElementById('modal-title').textContent = title;
  document.getElementById('modal-text').textContent = text;
  document.getElementById('modal-overlay').classList.add('active');

  return new Promise((resolve) => {
    const overlay = document.getElementById('modal-overlay');
    const confirmBtn = document.getElementById('modal-confirm');
    const cancelBtn = document.getElementById('modal-cancel');

    function cleanup() {
      overlay.classList.remove('active');
      confirmBtn.replaceWith(confirmBtn.cloneNode(true));
      cancelBtn.replaceWith(cancelBtn.cloneNode(true));
      overlay.replaceWith(overlay.cloneNode(true));
    }

    document.getElementById('modal-confirm').addEventListener('click', () => {
      cleanup();
      resolve(true);
    });

    document.getElementById('modal-cancel').addEventListener('click', () => {
      cleanup();
      resolve(false);
    });

    document.getElementById('modal-overlay').addEventListener('click', (e) => {
      if (e.target === document.getElementById('modal-overlay')) {
        cleanup();
        resolve(false);
      }
    });
  });
}

// ===================================
// PAGE INITIALIZATION
// ===================================

document.addEventListener('DOMContentLoaded', () => {
  const page = document.body.dataset.page;

  switch (page) {
    case 'home': initHomePage(); break;
    case 'users': initUsersPage(); break;
    case 'categories': initCategoriesPage(); break;
    case 'transactions': initTransactionsPage(); break;
    case 'history': initHistoryPage(); break;
  }
});

// ===================================
// HOME PAGE
// ===================================

async function initHomePage() {
  try {
    const [users, categories, transactions] = await Promise.all([
      apiRequest('/users'),
      apiRequest('/categories'),
      apiRequest('/transactions')
    ]);

    document.getElementById('count-users').textContent = users.length;
    document.getElementById('count-categories').textContent = categories.length;
    document.getElementById('count-transactions').textContent = transactions.length;

    const entradas = transactions
      .filter(t => t.tipo === 'entrada')
      .reduce((sum, t) => sum + t.valor, 0);
    const saidas = transactions
      .filter(t => t.tipo === 'saida')
      .reduce((sum, t) => sum + t.valor, 0);

    document.getElementById('saldo-total').textContent = formatCurrency(entradas - saidas);
  } catch (err) {
    console.error('Erro ao carregar dashboard:', err);
  }
}

// ===================================
// USERS PAGE
// ===================================

async function initUsersPage() {
  await loadUsers();

  document.getElementById('user-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const nome = document.getElementById('user-nome').value.trim();
    const email = document.getElementById('user-email').value.trim();

    if (!nome || !email) {
      showMessage('user-message', 'Preencha todos os campos.', true);
      return;
    }

    try {
      await apiRequest('/users', 'POST', { nome, email });
      showMessage('user-message', `Usuário "${nome}" criado com sucesso! ✅`);
      document.getElementById('user-form').reset();
      await loadUsers();
    } catch (err) {
      showMessage('user-message', err.message, true);
    }
  });
}

async function loadUsers() {
  const tbody = document.getElementById('users-tbody');

  try {
    const users = await apiRequest('/users');
    if (users.length === 0) {
      tbody.innerHTML = `<tr><td colspan="4">
        <div class="empty-state"><div class="icon">👤</div><p>Nenhum usuário cadastrado</p></div>
      </td></tr>`;
      return;
    }
    tbody.innerHTML = users.map(user => `
      <tr>
        <td>${user.id}</td>
        <td><strong>${escapeHtml(user.nome)}</strong></td>
        <td>${escapeHtml(user.email)}</td>
        <td><button class="btn btn-danger" data-action="delete-user" data-id="${user.id}" data-nome="${escapeHtml(user.nome)}">Excluir</button></td>
      </tr>
    `).join('');

    // Registrar eventos de exclusão via delegation
    tbody.querySelectorAll('[data-action="delete-user"]').forEach(btn => {
      btn.addEventListener('click', () => {
        deleteUser(parseInt(btn.dataset.id), btn.dataset.nome);
      });
    });
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="4">
      <div class="empty-state"><p>Erro ao carregar usuários</p></div>
    </td></tr>`;
  }
}

async function deleteUser(id, nome) {
  const confirmed = await showConfirmModal(
    'Excluir Usuário',
    `Tem certeza que deseja excluir "${nome}"? Todas as categorias e transações dele serão removidas.`
  );
  if (!confirmed) return;

  try {
    await apiRequest(`/users/${id}`, 'DELETE');
    showMessage('user-message', `Usuário "${nome}" excluído com sucesso! ✅`);
    await loadUsers();
  } catch (err) {
    showMessage('user-message', err.message, true);
  }
}

// ===================================
// CATEGORIES PAGE
// ===================================

async function initCategoriesPage() {
  await populateUserSelect('category-user-id');
  await populateUserSelect('filter-user-id', true);
  await loadCategories();

  document.getElementById('category-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const nome = document.getElementById('category-nome').value.trim();
    const user_id = parseInt(document.getElementById('category-user-id').value);

    if (!nome || !user_id) {
      showMessage('category-message', 'Preencha todos os campos.', true);
      return;
    }

    try {
      await apiRequest('/categories', 'POST', { nome, user_id });
      showMessage('category-message', `Categoria "${nome}" criada com sucesso! ✅`);
      document.getElementById('category-form').reset();
      await loadCategories();
    } catch (err) {
      showMessage('category-message', err.message, true);
    }
  });

  document.getElementById('filter-user-id').addEventListener('change', () => {
    loadCategories();
  });
}

async function loadCategories() {
  await loadMaps();
  const filterUserId = document.getElementById('filter-user-id')?.value;
  const tbody = document.getElementById('categories-tbody');

  try {
    const endpoint = filterUserId ? `/categories?user_id=${filterUserId}` : '/categories';
    const categories = await apiRequest(endpoint);

    if (categories.length === 0) {
      tbody.innerHTML = `<tr><td colspan="4">
        <div class="empty-state"><div class="icon">📂</div><p>Nenhuma categoria cadastrada</p></div>
      </td></tr>`;
      return;
    }
    tbody.innerHTML = categories.map(cat => `
      <tr>
        <td>${cat.id}</td>
        <td><strong>${escapeHtml(cat.nome)}</strong></td>
        <td>${escapeHtml(getUserName(cat.user_id))}</td>
        <td><button class="btn btn-danger" data-action="delete-category" data-id="${cat.id}" data-nome="${escapeHtml(cat.nome)}">Excluir</button></td>
      </tr>
    `).join('');

    // Registrar eventos de exclusão
    tbody.querySelectorAll('[data-action="delete-category"]').forEach(btn => {
      btn.addEventListener('click', () => {
        deleteCategory(parseInt(btn.dataset.id), btn.dataset.nome);
      });
    });
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="4">
      <div class="empty-state"><p>Erro ao carregar categorias</p></div>
    </td></tr>`;
  }
}

async function deleteCategory(id, nome) {
  const confirmed = await showConfirmModal(
    'Excluir Categoria',
    `Tem certeza que deseja excluir "${nome}"? Todas as transações vinculadas serão removidas.`
  );
  if (!confirmed) return;

  try {
    await apiRequest(`/categories/${id}`, 'DELETE');
    showMessage('category-message', `Categoria "${nome}" excluída com sucesso! ✅`);
    await loadCategories();
  } catch (err) {
    showMessage('category-message', err.message, true);
  }
}

// ===================================
// TRANSACTIONS PAGE
// ===================================

async function initTransactionsPage() {
  await populateUserSelect('tx-user-id');
  await populateUserSelect('filter-tx-user-id', true);
  await loadTransactions();

  // Quando seleciona um usuário, carrega as categorias dele
  document.getElementById('tx-user-id').addEventListener('change', async (e) => {
    const userId = e.target.value;
    const catSelect = document.getElementById('tx-category-id');
    if (userId) {
      await populateCategorySelect('tx-category-id', userId);
    } else {
      catSelect.innerHTML = '<option value="">Selecione um usuário primeiro</option>';
    }
  });

  document.getElementById('transaction-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const valor = parseFloat(document.getElementById('tx-valor').value);
    const tipo = document.getElementById('tx-tipo').value;
    const user_id = parseInt(document.getElementById('tx-user-id').value);
    const category_id = parseInt(document.getElementById('tx-category-id').value);
    const data = document.getElementById('tx-data').value || undefined;

    if (!valor || !tipo || !user_id || !category_id) {
      showMessage('tx-message', 'Preencha todos os campos obrigatórios.', true);
      return;
    }

    const body = { valor, tipo, user_id, category_id };
    if (data) body.data = data;

    try {
      await apiRequest('/transactions', 'POST', body);
      const tipoLabel = tipo === 'entrada' ? '📈 Entrada' : '📉 Saída';
      showMessage('tx-message', `${tipoLabel} de ${formatCurrency(valor)} criada com sucesso! ✅`);
      document.getElementById('transaction-form').reset();
      document.getElementById('tx-category-id').innerHTML = '<option value="">Selecione um usuário primeiro</option>';
      await loadTransactions();
    } catch (err) {
      showMessage('tx-message', err.message, true);
    }
  });

  document.getElementById('filter-tx-user-id').addEventListener('change', () => {
    loadTransactions();
  });
}

async function loadTransactions() {
  await loadMaps();
  const filterUserId = document.getElementById('filter-tx-user-id')?.value;
  const tbody = document.getElementById('transactions-tbody');
  const summaryBar = document.getElementById('tx-summary');

  try {
    const endpoint = filterUserId ? `/transactions?user_id=${filterUserId}` : '/transactions';
    const transactions = await apiRequest(endpoint);

    // Calcular resumo
    const totalEntradas = transactions.filter(t => t.tipo === 'entrada').reduce((s, t) => s + t.valor, 0);
    const totalSaidas = transactions.filter(t => t.tipo === 'saida').reduce((s, t) => s + t.valor, 0);

    if (summaryBar) {
      summaryBar.innerHTML = `
        <div class="summary-item entrada">📈 Entradas: <strong>${formatCurrency(totalEntradas)}</strong></div>
        <div class="summary-item saida">📉 Saídas: <strong>${formatCurrency(totalSaidas)}</strong></div>
        <div class="summary-item saldo">💰 Saldo: <strong>${formatCurrency(totalEntradas - totalSaidas)}</strong></div>
      `;
    }

    if (transactions.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7">
        <div class="empty-state"><div class="icon">💸</div><p>Nenhuma transação cadastrada</p></div>
      </td></tr>`;
      return;
    }

    tbody.innerHTML = transactions.map(tx => `
      <tr>
        <td>${tx.id}</td>
        <td class="valor-${tx.tipo}">${tx.tipo === 'entrada' ? '+' : '-'} ${formatCurrency(tx.valor)}</td>
        <td><span class="badge badge-${tx.tipo}">${tx.tipo}</span></td>
        <td>${escapeHtml(getCategoryName(tx.category_id))}</td>
        <td>${escapeHtml(getUserName(tx.user_id))}</td>
        <td>${formatDate(tx.data)}</td>
        <td><button class="btn btn-danger" data-action="delete-transaction" data-id="${tx.id}">Excluir</button></td>
      </tr>
    `).join('');

    // Registrar eventos de exclusão
    tbody.querySelectorAll('[data-action="delete-transaction"]').forEach(btn => {
      btn.addEventListener('click', () => {
        deleteTransaction(parseInt(btn.dataset.id));
      });
    });
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="7">
      <div class="empty-state"><p>Erro ao carregar transações</p></div>
    </td></tr>`;
  }
}

async function deleteTransaction(id) {
  const confirmed = await showConfirmModal(
    'Excluir Transação',
    `Tem certeza que deseja excluir a transação #${id}?`
  );
  if (!confirmed) return;

  try {
    await apiRequest(`/transactions/${id}`, 'DELETE');
    showMessage('tx-message', 'Transação excluída com sucesso! ✅');
    await loadTransactions();
  } catch (err) {
    showMessage('tx-message', err.message, true);
  }
}

// ===================================
// HISTORY PAGE
// ===================================

async function initHistoryPage() {
  await loadHistory();

  document.getElementById('filter-history-btn')?.addEventListener('click', () => {
    loadHistory();
  });

  // Permite filtrar ao pressionar Enter
  document.getElementById('filter-tx-id')?.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') loadHistory();
  });
}

async function loadHistory() {
  const filterTxId = document.getElementById('filter-tx-id')?.value;
  const tbody = document.getElementById('history-tbody');

  try {
    const endpoint = filterTxId
      ? `/transactions/historico?transaction_id=${filterTxId}`
      : '/transactions/historico';
    const history = await apiRequest(endpoint);

    if (history.length === 0) {
      tbody.innerHTML = `<tr><td colspan="4">
        <div class="empty-state"><div class="icon">📋</div><p>Nenhum registro no histórico</p></div>
      </td></tr>`;
      return;
    }

    tbody.innerHTML = history.map(h => `
      <tr>
        <td>${h.id}</td>
        <td>#${h.transaction_id}</td>
        <td><span class="badge badge-${h.acao}">${h.acao}</span></td>
        <td>${formatDate(h.data)}</td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="4">
      <div class="empty-state"><p>Erro ao carregar histórico</p></div>
    </td></tr>`;
  }
}
