/* ============================================================
   APRENDER DIVERSO - SCRIPT GLOBAL
   Integrado com API FastAPI (backend real)
   ============================================================ */

// ============================================================
// CONFIGURAÇÕES
// ============================================================

const API_URL = window.location.origin;
const ALUNO_ID_PADRAO = 1;

// ============================================================
// UTILITÁRIOS DE AUTENTICAÇÃO
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

// ============================================================
// CHAMADAS À API
// ============================================================

async function apiFetch(caminho, opcoes = {}) {
    const token = obterToken();

    const headers = {
        'Content-Type': 'application/json',
        ...(opcoes.headers || {}),
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const resposta = await fetch(`${API_URL}${caminho}`, {
        ...opcoes,
        headers,
    });

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
// CAMADA DE DADOS (via API)
// ============================================================

async function listarFeedbacksAluno(alunoId) {
    return apiFetch(`/feedbacks/aluno/${alunoId}`);
}

async function salvarFeedback(dados) {
    return apiFetch('/feedbacks/', {
        method: 'POST',
        body: JSON.stringify(dados),
    });
}

async function obterEstatisticas(alunoId) {
    return apiFetch(`/feedbacks/aluno/${alunoId}/estatisticas`);
}

async function obterTcle(alunoId) {
    return apiFetch(`/tcles/aluno/${alunoId}`);
}

async function aceitarTcle(alunoId) {
    return apiFetch(`/tcles/aluno/${alunoId}/aceitar`, {
        method: 'POST',
    });
}

// ============================================================
// INICIALIZAÇÃO
// ============================================================

document.addEventListener('DOMContentLoaded', () => {

    /* -------- TELA DE LOGIN -------- */
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (evento) => {
            evento.preventDefault();

            const email = document.getElementById('email').value.trim();
            const senha = document.getElementById('senha').value;
            const perfilEsperado = document.getElementById('perfil').value;

            if (!perfilEsperado) {
                alert('Por favor, selecione um perfil de acesso.');
                return;
            }

            const botao = loginForm.querySelector('button[type="submit"]');
            const textoOriginal = botao.textContent;
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

                if (!resposta.ok) {
                    const erro = await resposta.json().catch(() => ({}));
                    throw new Error(erro.detail || 'E-mail ou senha incorretos');
                }

                const dados = await resposta.json();
                const usuario = dados.usuario;

                if (usuario.perfil !== perfilEsperado) {
                    throw new Error(
                        `Este usuário é "${usuario.perfil}". Selecione o perfil correto.`
                    );
                }

                salvarToken(dados.access_token, usuario);

                const rotas = {
                    professor: '/professor',
                    responsavel: '/responsavel',
                    admin: '/admin',
                };
                window.location.href = rotas[usuario.perfil] || '/';

            } catch (erro) {
                alert(erro.message);
            } finally {
                botao.disabled = false;
                botao.textContent = textoOriginal;
            }
        });
    }

    /* -------- ATUALIZAR NOME DO USUÁRIO NO TOPBAR -------- */
    const usuarioInfo = document.getElementById('usuarioInfo');
    if (usuarioInfo) {
        const usuario = obterUsuarioLogado();
        if (usuario) {
            const icones = {
                professor: '👩‍🏫',
                responsavel: '👨‍👩‍👧',
                admin: '⚙️',
            };
            const icone = icones[usuario.perfil] || '👤';
            usuarioInfo.textContent = `${icone} ${usuario.nome}`;
        }
    }

    /* -------- POPULAR DROPDOWN DE ALUNOS -------- */
    const selectAluno = document.getElementById('aluno');
    const selectAlunoPei = document.getElementById('alunoPei');

    if (selectAluno || selectAlunoPei) {
        if (exigirLogin()) {
            carregarAlunos();
        }
    }

    /* -------- TELA DO PROFESSOR -------- */
    const formFeedback = document.getElementById('formFeedback');
    if (formFeedback) {
        if (!exigirLogin()) return;

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

            const alunoId = document.getElementById('aluno').value;
            if (!alunoId) {
                alert('Selecione um aluno.');
                return;
            }

            const categorias = {};
            document.querySelectorAll('.tag.selecionada').forEach(t => {
                categorias[t.dataset.categoria] = t.dataset.valor;
            });

            if (Object.keys(categorias).length === 0) {
                alert('Selecione ao menos uma categoria.');
                return;
            }

            try {
                await salvarFeedback({
                    aluno_id: parseInt(alunoId),
                    categorias,
                    observacao: observacao ? observacao.value.trim() : null,
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
            }
        });
    }

    /* -------- TELA DO RESPONSÁVEL -------- */
    if (document.getElementById('graficoEvolucao')) {
        if (!exigirLogin()) return;
        carregarDashboard();
    }

    /* -------- TELA DO TCLE -------- */
    const aceite = document.getElementById('aceite');
    const btnAceitar = document.getElementById('btnAceitar');

    if (aceite && btnAceitar) {
        if (!exigirLogin()) return;
        carregarTcle();
    }

    /* -------- TELA DO ADMIN -------- */
    if (document.getElementById('tabelaTurmas')) {
        if (exigirLogin()) {
            carregarTurmasAdmin();
            carregarAlunosAdmin();
        }
    }

    /* -------- LOGOUT -------- */
    const botoesSair = document.querySelectorAll('.btn-sair');
    botoesSair.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            logout();
        });
    });

});

// ============================================================
// CARREGAR ALUNOS (para o dropdown)
// ============================================================

async function carregarAlunos() {
    try {
        const alunos = await apiFetch('/alunos/');

        const selectAluno = document.getElementById('aluno');
        const selectAlunoPei = document.getElementById('alunoPei');

        if (alunos.length === 0) {
            const htmlVazio = '<option value="">Nenhum aluno cadastrado</option>';
            if (selectAluno) selectAluno.innerHTML = htmlVazio;
            if (selectAlunoPei) selectAlunoPei.innerHTML = htmlVazio;
            return;
        }

        const opcoes = alunos
            .map(a => `<option value="${a.id}">${a.nome}</option>`)
            .join('');

        const htmlOpcoes = '<option value="">-- Escolha um aluno --</option>' + opcoes;

        if (selectAluno) selectAluno.innerHTML = htmlOpcoes;
        if (selectAlunoPei) selectAlunoPei.innerHTML = htmlOpcoes;

    } catch (erro) {
        console.error('Erro ao carregar alunos:', erro);
        alert('Erro ao carregar alunos: ' + erro.message);
    }
}

// ============================================================
// TCLE
// ============================================================

async function carregarTcle() {
    const aceite = document.getElementById('aceite');
    const btnAceitar = document.getElementById('btnAceitar');

    try {
        const tcle = await obterTcle(ALUNO_ID_PADRAO);

        if (tcle.aceito) {
            aceite.checked = true;
            btnAceitar.textContent = '✔ Termo já aceito';
            btnAceitar.disabled = true;
            atualizarStatusTcle(tcle);
        }

        aceite.addEventListener('change', () => {
            btnAceitar.disabled = !aceite.checked;
        });

        btnAceitar.addEventListener('click', async () => {
            btnAceitar.disabled = true;
            btnAceitar.textContent = 'Registrando...';

            try {
                const tcleAtualizado = await aceitarTcle(ALUNO_ID_PADRAO);
                alert('✔ Termo aceito com sucesso!');
                atualizarStatusTcle(tcleAtualizado);
                btnAceitar.textContent = '✔ Termo aceito';
            } catch (erro) {
                alert('Erro ao aceitar o TCLE: ' + erro.message);
                btnAceitar.disabled = false;
                btnAceitar.textContent = '✔ Aceitar Termo';
            }
        });

    } catch (erro) {
        console.error('Erro ao carregar TCLE:', erro);
        aceite.addEventListener('change', () => {
            btnAceitar.disabled = !aceite.checked;
        });
        btnAceitar.addEventListener('click', () => {
            alert('TCLE ainda não foi criado no sistema. Peça ao administrador.');
        });
    }
}

function atualizarStatusTcle(tcle) {
    const card = document.querySelector('.card-status-tcle');
    if (!card) return;

    const data = tcle.aceito_em
        ? new Date(tcle.aceito_em).toLocaleString('pt-BR')
        : '';

    card.style.background = 'linear-gradient(135deg, #E8F5E9 0%, #FFFFFF 100%)';
    card.style.borderLeftColor = '#7CB342';
    card.querySelector('.status-icon').textContent = '✔';
    card.querySelector('.status-titulo').textContent = 'Termo aceito';
    card.querySelector('.status-titulo').style.color = '#2E7D32';
    card.querySelector('.status-descricao').innerHTML =
        `Você aceitou o termo em <strong>${data}</strong>. O acompanhamento está liberado.`;
}

// ============================================================
// DASHBOARD DO RESPONSÁVEL
// ============================================================

async function carregarDashboard() {
    try {
        const stats = await obterEstatisticas(ALUNO_ID_PADRAO);

        const cards = document.querySelectorAll('.card-resumo');
        if (cards[0]) cards[0].querySelector('.resumo-valor').textContent = stats.total_feedbacks;
        if (cards[1]) cards[1].querySelector('.resumo-valor').textContent = stats.percentuais.foco + '%';
        if (cards[2]) cards[2].querySelector('.resumo-valor').textContent = stats.percentuais.social + '%';
        if (cards[3]) cards[3].querySelector('.resumo-valor').textContent = stats.percentuais.tarefas + '%';

        renderizarGrafico(stats.grafico);

        const feedbacks = await listarFeedbacksAluno(ALUNO_ID_PADRAO);
        renderizarFeedbacks(feedbacks);

    } catch (erro) {
        console.error('Erro no dashboard:', erro);
        alert('Erro ao carregar dados: ' + erro.message);
    }
}

function renderizarGrafico(dados) {
    const canvas = document.getElementById('graficoEvolucao');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dados.labels,
            datasets: [
                {
                    label: '🎯 Foco',
                    data: dados.foco,
                    borderColor: '#4A90A4',
                    backgroundColor: 'rgba(74, 144, 164, 0.1)',
                    tension: 0.35, borderWidth: 3,
                    pointRadius: 5, pointBackgroundColor: '#4A90A4'
                },
                {
                    label: '🌊 Regulação Sensorial',
                    data: dados.sensorial,
                    borderColor: '#7CB342',
                    backgroundColor: 'rgba(124, 179, 66, 0.1)',
                    tension: 0.35, borderWidth: 3,
                    pointRadius: 5, pointBackgroundColor: '#7CB342'
                },
                {
                    label: '🤝 Interação Social',
                    data: dados.social,
                    borderColor: '#E67E22',
                    backgroundColor: 'rgba(230, 126, 34, 0.1)',
                    tension: 0.35, borderWidth: 3,
                    pointRadius: 5, pointBackgroundColor: '#E67E22'
                },
                {
                    label: '📚 Execução de Tarefas',
                    data: dados.tarefas,
                    borderColor: '#8E44AD',
                    backgroundColor: 'rgba(142, 68, 173, 0.1)',
                    tension: 0.35, borderWidth: 3,
                    pointRadius: 5, pointBackgroundColor: '#8E44AD'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: { family: 'Nunito', size: 13 },
                        color: '#2C3E50',
                        padding: 14,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true, max: 100,
                    ticks: { callback: (v) => v + '%' }
                }
            }
        }
    });
}

function renderizarFeedbacks(feedbacks) {
    const lista = document.querySelector('.lista-feedbacks');
    if (!lista) return;

    if (feedbacks.length === 0) {
        lista.innerHTML = `
            <li class="feedback-item feedback-vazio">
                <p>📭 Nenhum feedback registrado ainda.</p>
            </li>
        `;
        return;
    }

    const ROTULOS = {
        foco: { otimo: 'Ótimo', bom: 'Bom', regular: 'Regular', dificuldade: 'Dificuldade' },
        sensorial: { calmo: 'Calmo', agitado: 'Agitado', sobrecarga: 'Sobrecarga', retraido: 'Retraído' },
        social: { participativo: 'Participativo', colaborativo: 'Colaborativo', isolado: 'Isolado', conflito: 'Conflito' },
        tarefas: { concluiu: 'Concluiu', parcial: 'Parcial', 'nao-concluiu': 'Não concluiu', recusou: 'Recusou' }
    };
    const ICONES = { foco: '🎯', sensorial: '🌊', social: '🤝', tarefas: '📚' };

    lista.innerHTML = feedbacks.slice(0, 5).map(fb => {
        const badges = Object.entries(fb.categorias).map(([cat, val]) => {
            const rotulo = ROTULOS[cat]?.[val] || val;
            const icone = ICONES[cat] || '•';
            return `<span class="badge badge-neutro">${icone} ${rotulo}</span>`;
        }).join('');

        const data = new Date(fb.criado_em).toLocaleString('pt-BR');

        return `
            <li class="feedback-item">
                <div class="feedback-data">${data}</div>
                <div class="feedback-texto">${badges}</div>
                ${fb.observacao ? `<p class="feedback-obs">"${fb.observacao}"</p>` : ''}
            </li>
        `;
    }).join('');
}

// ============================================================
// ADMIN — CADASTROS
// ============================================================

function abrirModal(titulo, camposHtml, aoSalvar) {
    const modal = document.getElementById('modalCadastro');
    const modalTitulo = document.getElementById('modalTitulo');
    const camposModal = document.getElementById('camposModal');
    const form = document.getElementById('formCadastro');

    modalTitulo.textContent = titulo;
    camposModal.innerHTML = camposHtml;
    modal.style.display = 'flex';

    const novoForm = form.cloneNode(true);
    form.parentNode.replaceChild(novoForm, form);

    novoForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await aoSalvar();
    });
}

function fecharModal() {
    document.getElementById('modalCadastro').style.display = 'none';
}

function abrirCadastroTurma() {
    const html = `
        <div class="form-group">
            <label for="turma_nome">Nome da turma *</label>
            <input type="text" id="turma_nome" required placeholder="Ex: 6º Ano A">
        </div>
        <div class="form-group">
            <label for="turma_ano">Ano letivo *</label>
            <input type="number" id="turma_ano" required value="2026" min="2020" max="2100">
        </div>
        <div class="form-group">
            <label for="turma_turno">Turno *</label>
            <select id="turma_turno" required>
                <option value="manha">Manhã</option>
                <option value="tarde">Tarde</option>
                <option value="noite">Noite</option>
                <option value="integral">Integral</option>
            </select>
        </div>
    `;

    abrirModal('🏫 Nova Turma', html, async () => {
        try {
            await apiFetch('/turmas/', {
                method: 'POST',
                body: JSON.stringify({
                    nome: document.getElementById('turma_nome').value.trim(),
                    ano_letivo: parseInt(document.getElementById('turma_ano').value),
                    turno: document.getElementById('turma_turno').value,
                }),
            });
            alert('✔ Turma cadastrada!');
            fecharModal();
            carregarTurmasAdmin();
        } catch (erro) {
            alert('Erro: ' + erro.message);
        }
    });
}

function abrirCadastroAluno() {
    apiFetch('/turmas/').then(turmas => {
        const opcoesTurmas = turmas.map(t =>
            `<option value="${t.id}">${t.nome} (${t.ano_letivo})</option>`
        ).join('');

        const html = `
            <div class="form-group">
                <label for="aluno_nome">Nome do aluno *</label>
                <input type="text" id="aluno_nome" required>
            </div>
            <div class="form-group">
                <label for="aluno_data">Data de nascimento *</label>
                <input type="date" id="aluno_data" required>
            </div>
            <div class="form-group">
                <label for="aluno_diag">Diagnóstico</label>
                <input type="text" id="aluno_diag" placeholder="Ex: TEA Nível 1">
            </div>
            <div class="form-group">
                <label for="aluno_obs">Observações</label>
                <textarea id="aluno_obs" rows="2"></textarea>
            </div>
            <div class="form-group">
                <label for="aluno_turma">Turma *</label>
                <select id="aluno_turma" required>
                    <option value="">Selecione...</option>
                    ${opcoesTurmas}
                </select>
            </div>
        `;

        abrirModal('👥 Novo Aluno', html, async () => {
            try {
                await apiFetch('/alunos/', {
                    method: 'POST',
                    body: JSON.stringify({
                        nome: document.getElementById('aluno_nome').value.trim(),
                        data_nascimento: document.getElementById('aluno_data').value,
                        diagnostico: document.getElementById('aluno_diag').value.trim() || null,
                        observacoes: document.getElementById('aluno_obs').value.trim() || null,
                        turma_id: parseInt(document.getElementById('aluno_turma').value),
                    }),
                });
                alert('✔ Aluno cadastrado!');
                fecharModal();
                carregarAlunosAdmin();
            } catch (erro) {
                alert('Erro: ' + erro.message);
            }
        });
    });
}

function abrirCadastroProfessor() {
    const html = `
        <div class="form-group">
            <label for="prof_nome">Nome completo *</label>
            <input type="text" id="prof_nome" required>
        </div>
        <div class="form-group">
            <label for="prof_email">E-mail *</label>
            <input type="email" id="prof_email" required>
        </div>
        <div class="form-group">
            <label for="prof_senha">Senha (mín. 6 caracteres) *</label>
            <input type="password" id="prof_senha" required minlength="6">
        </div>
        <div class="form-group">
            <label for="prof_tel">Telefone</label>
            <input type="tel" id="prof_tel">
        </div>
    `;

    abrirModal('👩‍🏫 Novo Professor', html, async () => {
        try {
            await apiFetch('/auth/registrar', {
                method: 'POST',
                body: JSON.stringify({
                    nome: document.getElementById('prof_nome').value.trim(),
                    email: document.getElementById('prof_email').value.trim(),
                    senha: document.getElementById('prof_senha').value,
                    perfil: 'professor',
                    telefone: document.getElementById('prof_tel').value.trim() || null,
                }),
            });
            alert('✔ Professor cadastrado!');
            fecharModal();
        } catch (erro) {
            alert('Erro: ' + erro.message);
        }
    });
}

function abrirCadastroResponsavel() {
    const html = `
        <div class="form-group">
            <label for="resp_nome">Nome completo *</label>
            <input type="text" id="resp_nome" required>
        </div>
        <div class="form-group">
            <label for="resp_email">E-mail *</label>
            <input type="email" id="resp_email" required>
        </div>
        <div class="form-group">
            <label for="resp_senha">Senha (mín. 6 caracteres) *</label>
            <input type="password" id="resp_senha" required minlength="6">
        </div>
        <div class="form-group">
            <label for="resp_tel">Telefone</label>
            <input type="tel" id="resp_tel">
        </div>
    `;

    abrirModal('👨‍👩‍👧 Novo Responsável', html, async () => {
        try {
            await apiFetch('/auth/registrar', {
                method: 'POST',
                body: JSON.stringify({
                    nome: document.getElementById('resp_nome').value.trim(),
                    email: document.getElementById('resp_email').value.trim(),
                    senha: document.getElementById('resp_senha').value,
                    perfil: 'responsavel',
                    telefone: document.getElementById('resp_tel').value.trim() || null,
                }),
            });
            alert('✔ Responsável cadastrado!');
            fecharModal();
        } catch (erro) {
            alert('Erro: ' + erro.message);
        }
    });
}

async function carregarTurmasAdmin() {
    const tbody = document.getElementById('tabelaTurmas');
    if (!tbody) return;

    try {
        const turmas = await apiFetch('/turmas/');
        if (turmas.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;">Nenhuma turma cadastrada.</td></tr>';
            return;
        }
        tbody.innerHTML = turmas.map(t => `
            <tr>
                <td>${t.id}</td>
                <td><strong>${t.nome}</strong></td>
                <td>${t.ano_letivo}</td>
                <td>${t.turno}</td>
            </tr>
        `).join('');
    } catch (erro) {
        tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;color:#C0392B;">Erro: ${erro.message}</td></tr>`;
    }
}

async function carregarAlunosAdmin() {
    const tbody = document.getElementById('tabelaAlunos');
    if (!tbody) return;

    try {
        const alunos = await apiFetch('/alunos/');
        const turmas = await apiFetch('/turmas/');
        const mapaTurmas = {};
        turmas.forEach(t => mapaTurmas[t.id] = t.nome);

        if (alunos.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;">Nenhum aluno cadastrado.</td></tr>';
            return;
        }
        tbody.innerHTML = alunos.map(a => `
            <tr>
                <td>${a.id}</td>
                <td><strong>${a.nome}</strong></td>
                <td>${a.diagnostico || '—'}</td>
                <td>${mapaTurmas[a.turma_id] || '—'}</td>
            </tr>
        `).join('');
    } catch (erro) {
        tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;color:#C0392B;">Erro: ${erro.message}</td></tr>`;
    }
}