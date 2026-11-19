<div align="center">

# 🎓 Aprender Diverso

### Sistema de acompanhamento educacional individualizado para alunos neurodivergentes

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](./LICENSE)

**Plataforma web que centraliza PEI, TCLE, feedbacks pedagógicos e relatórios em um só lugar.**

[✨ Funcionalidades](#-funcionalidades) • [🛠 Stack](#-stack) • [🚀 Como rodar](#-como-rodar) • [🔌 Endpoints](#-endpoints-principais) • [🤝 Contribuir](#-contribuindo)

</div>

---

## 📋 Sobre o projeto

O **Aprender Diverso** nasceu para resolver um problema real: a gestão de **PEIs** (Planos Educacionais Individualizados) e **TCLEs** (Termos de Consentimento Livre e Esclarecido) costuma ser fragmentada — planilhas aqui, documentos soltos ali, e-mails perdidos acolá.

Aqui, **professores**, **responsáveis** e **coordenação** trabalham no mesmo fluxo: cadastro → planejamento → acompanhamento → relatório. Tudo rastreável, tudo em um só lugar. 💙

> 🎯 **Missão:** dar suporte pedagógico de verdade a alunos que precisam de adaptações curriculares, sem burocracia desnecessária.

---

## 🎥 Vídeo de apresentação

> 🎬 *Em breve — grave um tour rápido pelo sistema e cole o link aqui!*
> ```markdown
> 👉 [Assista ao vídeo de apresentação](https://youtube.com/...)
> ```

---

## 📸 Capturas de tela

| 🔐 Login | 👨‍🏫 Painel do Professor |
|:---:|:---:|
| ![Login](docs/screenshots/login.png) | ![Professor](docs/screenshots/professor.png) |

| 🛡️ Painel Admin | 📝 Gestão de PEI |
|:---:|:---:|
| ![Admin](docs/screenshots/admin.png) | ![PEI](docs/screenshots/pei.png) |

> 💡 **Dica:** crie a pasta `docs/screenshots/` e coloque os prints lá. O README já está pronto pra exibi-los.

---

## ✨ Funcionalidades

<table>
<tr>
<td width="50%">

### 🔐 Autenticação & Acesso
- ✅ Login com **JWT (Bearer Token)**
- ✅ Perfis: **professor**, **responsável**, **admin**
- ✅ Proteção de rotas autenticadas
- ✅ Hash de senhas com **bcrypt**

</td>
<td width="50%">

### 🧑‍🎓 Gestão Pedagógica
- ✅ Cadastro e gestão de **alunos**
- ✅ **Turmas** e vínculo professor–turma
- ✅ Vínculo **responsável–aluno**
- ✅ **Feedbacks** pedagógicos por aluno

</td>
</tr>
<tr>
<td width="50%">

### 📝 Documentos Oficiais
- ✅ **PEI** — objetivos e adaptações
- ✅ **TCLE** — termos de consentimento
- ✅ **Relatórios** de acompanhamento

</td>
<td width="50%">

### 🖥️ Interface & Infra
- ✅ Frontend integrado (HTML/CSS/JS)
- ✅ Design responsivo
- ✅ **Health check** em `/health`
- ✅ CORS configurado

</td>
</tr>
</table>

---

## 🛠 Stack

<div align="center">

| Camada | Tecnologia |
|:---:|:---|
| 🐍 **Linguagem** | Python 3.12 |
| ⚡ **Framework** | FastAPI |
| 🚀 **Servidor** | Uvicorn |
| 🗄️ **ORM** | SQLAlchemy 2.x |
| 🐘 **Banco** | PostgreSQL (prod) · SQLite (dev) |
| ✅ **Validação** | Pydantic + pydantic-settings |
| 🔑 **Auth** | JWT (python-jose) + Passlib/bcrypt |
| 🎨 **Frontend** | HTML5 + CSS3 + JavaScript |
| 📄 **Templates** | Jinja2 + aiofiles + StaticFiles |

</div>

---

## 📁 Estrutura do projeto

```
aprender-diverso/
│
├── 📂 app/
│   ├── ⚙️  core/          # config, database, deps, security
│   ├── 🧩 models/         # modelos SQLAlchemy (Usuario, Aluno, PEI, TCLE…)
│   ├── 🛣️  routes/         # endpoints FastAPI (auth, turmas, alunos, peis…)
│   ├── 📋 schemas/        # schemas Pydantic (entrada/saída)
│   ├── 🔧 services/       # regras de negócio
│   ├── 🎨 frontend/       # HTML, CSS e JS
│   └── 🚪 main.py         # ponto de entrada da aplicação
│
├── 📄 requirements.txt
├── 🔐 .env                # variáveis de ambiente (NÃO versionar)
└── 💾 aprender_diverso.db # SQLite local (dev)
```

---

## 🚀 Como rodar

### 1️⃣ Clone o repositório
```bash
git clone https://github.com/Ricardooliv20/aprender-diverso.git
cd aprender-diverso
```

### 2️⃣ Crie e ative o ambiente virtual

```bash
python -m venv venv
```

**🐧 Linux / 🍎 macOS**
```bash
source venv/bin/activate
```

**🪟 Windows (PowerShell)**
```powershell
.\venv\Scripts\Activate.ps1
```

> ⚠️ **Deu erro de política de execução?** Rode antes:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> ```

### 3️⃣ Instale as dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure o `.env`
Crie um arquivo `.env` na raiz do projeto:

```env
APP_NAME="Aprender Diverso"
APP_VERSION="1.0.0"
DEBUG=True

# 🐘 PostgreSQL (produção)
DATABASE_URL=postgresql+psycopg://usuario:senha@localhost:5432/aprender_diverso

# 💾 SQLite (desenvolvimento) — descomente para usar
# DATABASE_URL=sqlite:///./aprender_diverso.db

SECRET_KEY=sua_chave_secreta_super_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> 🔒 **Importante:** nunca versione o `.env`. Ele já está no `.gitignore`.

### 5️⃣ Rode a aplicação 🎉
```bash
uvicorn app.main:app --reload
```

<div align="center">

### 🌐 Acesse

| 🖥️ App | 📚 Swagger | 📖 ReDoc | ❤️ Health |
|:---:|:---:|:---:|:---:|
| [localhost:8000](http://localhost:8000) | [/docs](http://localhost:8000/docs) | [/redoc](http://localhost:8000/redoc) | [/health](http://localhost:8000/health) |

</div>

---

## 🖥️ Páginas disponíveis

| 🎨 Rota | 📝 Descrição |
|:---|:---|
| `/` ou `/index.html` | 🔐 Tela de login |
| `/professor` | 👨‍🏫 Painel do professor |
| `/responsavel` | 👨‍👩‍👧 Painel do responsável |
| `/admin` | 🛡️ Painel administrativo |
| `/pei` | 📝 Gestão de PEI |
| `/tcle` | 📄 Gestão de TCLE |

---

## 🔌 Endpoints principais

| Método | 🛣️ Rota | 📝 Descrição |
|:---:|:---|:---|
| `POST` | `/auth/...` | 🔐 Login e autenticação |
| `GET/POST` | `/turmas` | 📚 Gestão de turmas |
| `GET/POST` | `/alunos` | 🧑‍🎓 Gestão de alunos |
| `GET/POST` | `/peis` | 📝 Planos Educacionais Individualizados |
| `GET/POST` | `/tcles` | 📄 Termos de Consentimento |
| `GET/POST` | `/feedbacks` | 💬 Feedbacks pedagógicos |
| `GET` | `/relatorios` | 📊 Relatórios de acompanhamento |
| `GET` | `/health` | ❤️ Status da aplicação |

> 📚 A documentação completa (parâmetros, schemas e códigos de resposta) está em **`/docs`**.

---

## 🔐 Autenticação

A API usa **JWT (Bearer Token)**. O fluxo é simples:

```mermaid
sequenceDiagram
    participant U as 👤 Usuário
    participant A as ⚡ API
    U->>A: POST /auth/login (email + senha)
    A-->>U: { access_token }
    U->>A: GET /alunos (Authorization: Bearer <token>)
    A-->>U: ✅ Dados autorizados
```

> 💡 O token expira conforme `ACCESS_TOKEN_EXPIRE_MINUTES` no `.env`.

---

## 🤝 Contribuindo

Contribuições são **muito bem-vindas**! 💙

1. 🍴 Faça um **fork** do projeto
2. 🌿 Crie uma branch: `git checkout -b feature/minha-feature`
3. 💾 Commit: `git commit -m "feat: minha feature"`
4. 🚀 Push: `git push origin feature/minha-feature`
5. 🎉 Abra um **Pull Request**

> 🐛 Encontrou um bug? Abra uma **issue**!
> 💡 Tem uma ideia? Compartilhe nas **discussions**!

---

## 📄 Licença

Este projeto está sob a licença **MIT**.
Consulte o arquivo [LICENSE](./LICENSE) para mais detalhes.

---

<div align="center">

## 👥 Contribuidores

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Ricardooliv20">
        <img src="https://github.com/Ricardooliv20.png" width="100px;" alt="Ricardo Oliveira"/><br />
        <sub><b>Ricardo Oliveira</b></sub>
      </a><br />
      <sub>💻 Desenvolvedor principal</sub>
    </td>
    <td align="center">
      <a href="https://github.com/igorsimoesgomes0-alt">
        <img src="https://github.com/igorsimoesgomes0-alt.png" width="100px;" alt="Igor Simões"/><br />
        <sub><b>Igor Simões</b></sub>
      </a><br />
      <sub>🤝 Contribuidor</sub>
    </td>
  </tr>
</table>

---

### ⭐ Gostou do projeto?

**Dê uma estrela no repositório!** Isso ajuda demais o projeto a crescer. 🌟

---

**Feito com 💙 por [Ricardo Oliveira](https://github.com/Ricardooliv20) & [Igor Simões](https://github.com/igorsimoesgomes0-alt)**

</div>
