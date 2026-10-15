from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.core.database import Base, engine

# Modelos
from app.models.usuario import Usuario  # noqa: F401
from app.models.turma import Turma  # noqa: F401
from app.models.aluno import Aluno  # noqa: F401
from app.models.professor_turma import ProfessorTurma  # noqa: F401
from app.models.responsavel_aluno import ResponsavelAluno  # noqa: F401
from app.models.pei import PEI, ObjetivoPEI, AdaptacaoPEI  # noqa: F401
from app.models.feedback import Feedback  # noqa: F401
from app.models.tcle import TCLE  # noqa: F401
from app.models.relatorio import Relatorio  # noqa: F401

# Rotas
from app.routes import auth, turmas, alunos, feedbacks, peis, tcles, relatorios

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="API do sistema de acompanhamento educacional individualizado",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- ROTAS DA API ----------
app.include_router(auth.router)
app.include_router(turmas.router)
app.include_router(alunos.router)
app.include_router(feedbacks.router)
app.include_router(peis.router)
app.include_router(tcles.router)
app.include_router(relatorios.router)


# ---------- HEALTH CHECK ----------
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}


# ---------- SERVE O FRONTEND ----------
FRONTEND_DIR = Path(__file__).parent / "frontend"

# Arquivos estáticos
app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")


# ---------- ROTAS DAS PÁGINAS (sem .html e com .html) ----------

@app.get("/", include_in_schema=False)
def servir_login():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/index.html", include_in_schema=False)
def servir_login_html():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/professor", include_in_schema=False)
def servir_professor():
    return FileResponse(FRONTEND_DIR / "professor.html")


@app.get("/professor.html", include_in_schema=False)
def servir_professor_html():
    return FileResponse(FRONTEND_DIR / "professor.html")


@app.get("/responsavel", include_in_schema=False)
def servir_responsavel():
    return FileResponse(FRONTEND_DIR / "responsavel.html")


@app.get("/responsavel.html", include_in_schema=False)
def servir_responsavel_html():
    return FileResponse(FRONTEND_DIR / "responsavel.html")


@app.get("/admin", include_in_schema=False)
def servir_admin():
    return FileResponse(FRONTEND_DIR / "admin.html")


@app.get("/admin.html", include_in_schema=False)
def servir_admin_html():
    return FileResponse(FRONTEND_DIR / "admin.html")


@app.get("/pei", include_in_schema=False)
def servir_pei():
    return FileResponse(FRONTEND_DIR / "pei.html")


@app.get("/pei.html", include_in_schema=False)
def servir_pei_html():
    return FileResponse(FRONTEND_DIR / "pei.html")


@app.get("/tcle", include_in_schema=False)
def servir_tcle():
    return FileResponse(FRONTEND_DIR / "tcle.html")


@app.get("/tcle.html", include_in_schema=False)
def servir_tcle_html():
    return FileResponse(FRONTEND_DIR / "tcle.html")