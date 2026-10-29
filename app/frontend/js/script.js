/* ============================================================
   APRENDER DIVERSO - SCRIPT GLOBAL
   ============================================================ */

const API_URL = window.location.origin;
const ALUNO_ID_PADRAO = 1;

// Trava global para evitar múltiplos envios
let enviandoFeedback = false;

// ============================================================
// UTILITÁRIOS
// ============================================================

function salvarToken(token, usuario) {
    localStorage.setItem('token', token);
    localStorage.setItem('usuario', JSON.stringify(usuario));
}

function obterToken() {
    return localStorage.getItem('token');
}

function obterUsuarioLogado() {
    const dados = localStorage.getItem('usuario');
    return dados ? JSON.parse(dados) : null;
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('usuario');
    window.location.href = '/';
}

function exigirLogin() {
    const token = obterToken();
    if (!token) {
        alert('Sessão expirada. Faça login novamente.');
        window.location.href = '/';
        return false;
    }
    return true;
}

async function apiFetch(caminho, opcoes = {}) {
    const token = obterToken();
    const headers = {
        'Content-Type': 'application/json',
        ...(opcoes.headers || {}),
    };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const resposta = await fetch(`${API_URL}${caminho}`, { ...opcoes, headers });

    if (resposta.status === 401) {
        alert('Sessão expirada. Faça login novamente.');
        logout();
        throw new Error('Não autorizado');
    }
    if (!resposta.ok) {
        const erro = await resposta.json().catch(() => ({}));
        throw new Error(erro.detail || 'Erro na requisição');
    }
    if (resposta.status === 204) return null;
    return resposta.json();
}

// ============================================================
// INICIALIZAÇÃO
// ============================================================

document.addEventListener('DOMContentLoaded', () => {

    // LOGIN
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (evento) => {
            evento.preventDefault();
            const email = document.getElementById('email').value.trim();
            const senha = document.getElementById('senha').value;
            const perfilEsperado = document.getElementById('perfil').value;

            if (!perfilEsperado) return alert('Selecione um perfil.');
            
            const botao = loginForm.querySelector('button[type="submit"]');
            botao.disabled = true;
            botao.textContent = 'Entrando...';

            try {
                const formData = new URLSearchParams();
                formData.append('username', email);
                formData.append('password', senha);

                const resposta = await fetch(`${API_URL}/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: formData,
                });

                if (!resposta.ok) throw new Error('E-mail ou senha incorretos');
                const dados = await resposta.json();
                
                if (dados.usuario.perfil !== perfilEsperado) {
                    throw new Error(`Este usuário é "${dados.usuario.perfil}". Selecione o perfil correto.`);
                }

                salvarToken(dados.access_token, dados.usuario);
                const rotas = { professor: '/professor', responsavel: '/responsavel', admin: '/admin' };
                window.location.href = rotas[dados.usuario.perfil] || '/';
            } catch (erro) {
                alert(erro.message);
            } finally {
                botao.disabled = false;
                botao.textContent = 'Entrar';
            }
        });
    }

    // NOME NO TOPBAR
    const usuarioInfo = document.getElementById('usuarioInfo');
    if (usuarioInfo) {
        const usuario = obterUsuarioLogado();
        if (usuario) {
            const icones = { professor: '👩‍🏫', responsavel: '👨‍👩‍👧', admin: '⚙️' };
            usuarioInfo.textContent = `${icones[usuario.perfil] || '👤'} ${usuario.nome}`;
        }
    }

    // DROPDOWN DE ALUNOS
    const selectAluno = document.getElementById('aluno');
    const selectAlunoPei = document.getElementById('alunoPei');
    if ((selectAluno || selectAlunoPei) && exigirLogin()) {
        carregarAlunos();
    }

    // TELA DO PROFESSOR (FEEDBACK)
    const formFeedback = document.getElementById('formFeedback');
    if (formFeedback && exigirLogin()) {
        document.querySelectorAll('.tag').forEach(tag => {
            tag.addEventListener('click', () => {
                const categoria = tag.dataset.categoria;
                document.querySelectorAll(`.tag[data-categoria="${categoria}"]`).forEach(t => {
                    t.classList.remove('selecionada');
                    t.setAttribute('aria-pressed', 'false');
                });
                tag.classList.add('selecionada');
                tag.setAttribute('aria-pressed', 'true');
            });
        });

        const observacao = document.getElementById('observacao');
        const contador = document.getElementById('contadorObs');
        if (observacao && contador) {
            observacao.addEventListener('input', () => {
                contador.textContent = `${observacao.value.length} / 280 caracteres`;
            });
        }

        formFeedback.addEventListener('submit', async (evento) => {
            evento.preventDefault();

            // 🚨 TRAVA ANTI-DUPLICAÇÃO
            if (enviandoFeedback) return;
            enviandoFeedback = true;

            const alunoId = document.getElementById('aluno').value;
            if (!alunoId) {
                enviandoFeedback = false;
                return alert('Selecione um aluno.');
            }

            const categorias = {};
            document.querySelectorAll('.tag.selecionada').forEach(t => {
                categorias[t.dataset.categoria] = t.dataset.valor;
            });

            if (Object.keys(categorias).length === 0) {
                enviandoFeedback = false;
                return alert('Selecione ao menos uma categoria.');
            }

            try {
                await apiFetch('/feedbacks/', {
                    method: 'POST',
                    body: JSON.stringify({
                        aluno_id: parseInt(alunoId),
                        categorias,
                        observacao: observacao ? observacao.value.trim() : null,
                    }),
                });

                alert('✔ Feedback registrado com sucesso!');
                formFeedback.reset();
                document.querySelectorAll('.tag.selecionada').forEach(t => {
                    t.classList.remove('selecionada');
                    t.setAttribute('aria-pressed', 'false');
                });
                if (contador) contador.textContent = '0 / 280 caracteres';
            } catch (erro) {
                alert('Erro ao registrar: ' + erro.message);
            } finally {
                enviandoFeedback = false; // Libera a trava
            }
        });
    }

    // TELA DO RESPONSÁVEL
    if (document.getElementById('graficoEvolucao') && exigirLogin()) {
        carregarDashboard();
    }

    // TELA DO TCLE
    const aceite = document.getElementById('aceite');
    const btnAceitar = document.getElementById('btnAceitar');
    if (aceite && btnAceitar && exigirLogin()) {
        carregarTcle();
    }

    // TELA DO ADMIN
    if (document.getElementById('tabelaTurmas') && exigirLogin()) {
        carregarTurmasAdmin();
        carregarAlunosAdmin();
    }

    // LOGOUT
    document.querySelectorAll('.btn-sair').forEach(btn => {
        btn.addEventListener('click', (e) => { e.preventDefault(); logout(); });
    });
});

// ============================================================
// FUNÇÕES AUXILIARES
// ============================================================

async function carregarAlunos() {
    try {
        const alunos = await apiFetch('/alunos/');
        const selectAluno = document.getElementById('aluno');
        const selectAlunoPei = document.getElementById('alunoPei');
        const html = alunos.length === 0 
            ? '<option value="">Nenhum aluno cadastrado</option>'
            : '<option value="">-- Escolha um aluno --</option>' + alunos.map(a => `<option value="${a.id}">${a.nome}</option>`).join('');

        if (selectAluno) selectAluno.innerHTML = html;
        if (selectAlunoPei) selectAlunoPei.innerHTML = html;
    } catch (erro) {
        console.error('Erro ao carregar alunos:', erro);
    }
}

async function carregarDashboard() {
    try {
        const stats = await apiFetch(`/feedbacks/aluno/${ALUNO_ID_PADRAO}/estatisticas`);
        const cards = document.querySelectorAll('.card-resumo');
        if (cards[0]) cards[0].querySelector('.resumo-valor').textContent = stats.total_feedbacks;
        if (cards[1]) cards[1].querySelector('.resumo-valor').textContent = stats.percentuais.foco + '%';
        if (cards[2]) cards[2].querySelector('.resumo-valor').textContent = stats.percentuais.social + '%';
        if (cards[3]) cards[3].querySelector('.resumo-valor').textContent = stats.percentuais.tarefas + '%';

        renderizarGrafico(stats.grafico);
        const feedbacks = await apiFetch(`/feedbacks/aluno/${ALUNO_ID_PADRAO}`);
        renderizarFeedbacks(feedbacks);
    } catch (erro) {
        alert('Erro ao carregar dados: ' + erro.message);
    }
}

function renderizarGrafico(dados) {
    const canvas = document.getElementById('graficoEvolucao');
    if (!canvas) return;
    new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
            labels: dados.labels,
            datasets: [
                { label: '🎯 Foco', data: dados.foco, borderColor: '#4A90A4', tension: 0.35 },
                { label: '🌊 Sensorial', data: dados.sensorial, borderColor: '#7CB342', tension: 0.35 },
                { label: '🤝 Social', data: dados.social, borderColor: '#E67E22', tension: 0.35 },
                { label: '📚 Tarefas', data: dados.tarefas, borderColor: '#8E44AD', tension: 0.35 }
            ]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });
}

function renderizarFeedbacks(feedbacks) {
    const lista = document.querySelector('.lista-feedbacks');
    if (!lista) return;
    if (feedbacks.length === 0) {
        lista.innerHTML = '<li class="feedback-item feedback-vazio"><p>📭 Nenhum feedback registrado.</p></li>';
        return;
    }
    lista.innerHTML = feedbacks.slice(0, 5).map(fb => `
        <li class="feedback-item">
            <div class="feedback-data">${new Date(fb.criado_em).toLocaleString('pt-BR')}</div>
            <div class="feedback-texto">${Object.entries(fb.categorias).map(([k,v]) => `<span class="badge badge-neutro">${k}: ${v}</span>`).join('')}</div>
            ${fb.observacao ? `<p class="feedback-obs">"${fb.observacao}"</p>` : ''}
        </li>
    `).join('');
}

async function carregarTcle() {
    try {
        const tcle = await apiFetch(`/tcles/aluno/${ALUNO_ID_PADRAO}`);
        const aceite = document.getElementById('aceite');
        const btnAceitar = document.getElementById('btnAceitar');
        
        if (tcle.aceito) {
            aceite.checked = true;
            btnAceitar.textContent = '✔ Termo já aceito';
            btnAceitar.disabled = true;
            atualizarStatusTcle(tcle);
        }
        
        aceite.addEventListener('change', () => { btnAceitar.disabled = !aceite.checked; });
        
        btnAceitar.addEventListener('click', async () => {
            btnAceitar.disabled = true;
            btnAceitar.textContent = 'Registrando...';
            try {
                const novo = await apiFetch(`/tcles/aluno/${ALUNO_ID_PADRAO}/aceitar`, { method: 'POST' });
                alert('✔ Termo aceito!');
                atualizarStatusTcle(novo);
            } catch (e) {
                alert('Erro: ' + e.message);
                btnAceitar.disabled = false;
                btnAceitar.textContent = '✔ Aceitar Termo';
            }
        });
    } catch (e) {
        document.getElementById('btnAceitar').addEventListener('click', () => alert('TCLE não encontrado.'));
    }
}

function atualizarStatusTcle(tcle) {
    const card = document.querySelector('.card-status-tcle');
    if (!card) return;
    card.style.background = 'linear-gradient(135deg, #E8F5E9 0%, #FFFFFF 100%)';
    card.querySelector('.status-icon').textContent = '✔';
    card.querySelector('.status-titulo').textContent = 'Termo aceito';
    card.querySelector('.status-titulo').style.color = '#2E7D32';
}

async function carregarTurmasAdmin() {
    const tbody = document.getElementById('tabelaTurmas');
    if (!tbody) return;
    try {
        const turmas = await apiFetch('/turmas/');
        tbody.innerHTML = turmas.map(t => `<tr><td>${t.id}</td><td>${t.nome}</td><td>${t.ano_letivo}</td><td>${t.turno}</td></tr>`).join('');
    } catch (e) { tbody.innerHTML = `<tr><td colspan="4">Erro: ${e.message}</td></tr>`; }
}

async function carregarAlunosAdmin() {
    const tbody = document.getElementById('tabelaAlunos');
    if (!tbody) return;
    try {
        const alunos = await apiFetch('/alunos/');
        const turmas = await apiFetch('/turmas/');
        const mapa = {}; turmas.forEach(t => mapa[t.id] = t.nome);
        tbody.innerHTML = alunos.map(a => `<tr><td>${a.id}</td><td>${a.nome}</td><td>${a.diagnostico || '—'}</td><td>${mapa[a.turma_id] || '—'}</td></tr>`).join('');
    } catch (e) { tbody.innerHTML = `<tr><td colspan="4">Erro: ${e.message}</td></tr>`; }
}

// ============================================================
// ADMIN - MODAIS
// ============================================================

function abrirModal(titulo, camposHtml, aoSalvar) {
    const modal = document.getElementById('modalCadastro');
    document.getElementById('modalTitulo').textContent = titulo;
    document.getElementById('camposModal').innerHTML = camposHtml;
    modal.style.display = 'flex';

    const form = document.getElementById('formCadastro');
    const novoForm = form.cloneNode(true);
    form.parentNode.replaceChild(novoForm, form);
    novoForm.addEventListener('submit', async (e) => { e.preventDefault(); await aoSalvar(); });
}

function fecharModal() { document.getElementById('modalCadastro').style.display = 'none'; }

function abrirCadastroTurma() {
    const html = `
        <div class="form-group"><label>Nome da turma *</label><input type="text" id="turma_nome" required></div>
        <div class="form-group"><label>Ano letivo *</label><input type="number" id="turma_ano" value="2026" required></div>
        <div class="form-group"><label>Turno *</label><select id="turma_turno"><option value="manha">Manhã</option><option value="tarde">Tarde</option></select></div>
    `;
    abrirModal('🏫 Nova Turma', html, async () => {
        try {
            await apiFetch('/turmas/', { method: 'POST', body: JSON.stringify({
                nome: document.getElementById('turma_nome').value,
                ano_letivo: parseInt(document.getElementById('turma_ano').value),
                turno: document.getElementById('turma_turno').value
            })});
            alert('✔ Turma cadastrada!'); fecharModal(); carregarTurmasAdmin();
        } catch (e) { alert(e.message); }
    });
}

function abrirCadastroAluno() {
    apiFetch('/turmas/').then(turmas => {
        const opts = turmas.map(t => `<option value="${t.id}">${t.nome}</option>`).join('');
        const html = `
            <div class="form-group"><label>Nome *</label><input type="text" id="aluno_nome" required></div>
            <div class="form-group"><label>Nascimento *</label><input type="date" id="aluno_data" required></div>
            <div class="form-group"><label>Turma *</label><select id="aluno_turma">${opts}</select></div>
        `;
        abrirModal('👥 Novo Aluno', html, async () => {
            try {
                await apiFetch('/alunos/', { method: 'POST', body: JSON.stringify({
                    nome: document.getElementById('aluno_nome').value,
                    data_nascimento: document.getElementById('aluno_data').value,
                    turma_id: parseInt(document.getElementById('aluno_turma').value)
                })});
                alert('✔ Aluno cadastrado!'); fecharModal(); carregarAlunosAdmin();
            } catch (e) { alert(e.message); }
        });
    });
}

function abrirCadastroProfessor() {
    const html = `
        <div class="form-group"><label>Nome *</label><input type="text" id="prof_nome" required></div>
        <div class="form-group"><label>E-mail *</label><input type="email" id="prof_email" required></div>
        <div class="form-group"><label>Senha *</label><input type="password" id="prof_senha" required></div>
    `;
    abrirModal('👩‍🏫 Novo Professor', html, async () => {
        try {
            await apiFetch('/auth/registrar', { method: 'POST', body: JSON.stringify({
                nome: document.getElementById('prof_nome').value,
                email: document.getElementById('prof_email').value,
                senha: document.getElementById('prof_senha').value,
                perfil: 'professor'
            })});
            alert('✔ Professor cadastrado!'); fecharModal();
        } catch (e) { alert(e.message); }
    });
}

function abrirCadastroResponsavel() {
    const html = `
        <div class="form-group"><label>Nome *</label><input type="text" id="resp_nome" required></div>
        <div class="form-group"><label>E-mail *</label><input type="email" id="resp_email" required></div>
        <div class="form-group"><label>Senha *</label><input type="password" id="resp_senha" required></div>
    `;
    abrirModal('👨‍👩‍👧 Novo Responsável', html, async () => {
        try {
            await apiFetch('/auth/registrar', { method: 'POST', body: JSON.stringify({
                nome: document.getElementById('resp_nome').value,
                email: document.getElementById('resp_email').value,
                senha: document.getElementById('resp_senha').value,
                perfil: 'responsavel'
            })});
            alert('✔ Responsável cadastrado!'); fecharModal();
        } catch (e) { alert(e.message); }
    });
}