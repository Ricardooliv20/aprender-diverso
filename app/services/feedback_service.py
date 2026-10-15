from datetime import datetime, timedelta
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.aluno import Aluno
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate


def listar_por_aluno(
    db: Session, aluno_id: int, limite: int = 50
) -> List[Feedback]:
    """Retorna feedbacks de um aluno, mais recentes primeiro."""
    return (
        db.query(Feedback)
        .filter(Feedback.aluno_id == aluno_id)
        .order_by(Feedback.criado_em.desc())
        .limit(limite)
        .all()
    )


def obter_por_id(db: Session, feedback_id: int) -> Optional[Feedback]:
    return db.query(Feedback).filter(Feedback.id == feedback_id).first()


def criar(
    db: Session, dados: FeedbackCreate, professor_id: int
) -> Feedback:
    # valida aluno
    if not db.query(Aluno).filter(Aluno.id == dados.aluno_id).first():
        raise ValueError("Aluno não encontrado")

    feedback = Feedback(
        aluno_id=dados.aluno_id,
        professor_id=professor_id,
        categorias=dados.categorias,
        observacao=dados.observacao,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


def deletar(db: Session, feedback: Feedback) -> None:
    db.delete(feedback)
    db.commit()


# ---------- ESTATÍSTICAS PARA O DASHBOARD ----------

VALORES_NUMERICOS = {
    "foco": {"otimo": 100, "bom": 75, "regular": 50, "dificuldade": 25},
    "sensorial": {"calmo": 100, "retraido": 50, "agitado": 40, "sobrecarga": 20},
    "social": {"colaborativo": 100, "participativo": 85, "isolado": 40, "conflito": 20},
    "tarefas": {"concluiu": 100, "parcial": 60, "nao-concluiu": 30, "recusou": 10},
}


def calcular_percentuais(feedbacks: List[Feedback]) -> Dict[str, int]:
    """Calcula percentual médio por categoria."""
    if not feedbacks:
        return {"foco": 0, "sensorial": 0, "social": 0, "tarefas": 0}

    soma = {"foco": 0, "sensorial": 0, "social": 0, "tarefas": 0}
    contagem = {"foco": 0, "sensorial": 0, "social": 0, "tarefas": 0}

    for fb in feedbacks:
        for cat, val in fb.categorias.items():
            if cat in VALORES_NUMERICOS and val in VALORES_NUMERICOS[cat]:
                soma[cat] += VALORES_NUMERICOS[cat][val]
                contagem[cat] += 1

    return {
        cat: (round(soma[cat] / contagem[cat]) if contagem[cat] > 0 else 0)
        for cat in ["foco", "sensorial", "social", "tarefas"]
    }


def agrupar_por_semana(feedbacks: List[Feedback]) -> Dict:
    """Agrupa feedbacks em 6 semanas e retorna médias por categoria."""
    hoje = datetime.utcnow()
    semanas = []

    for i in range(5, -1, -1):
        inicio = hoje - timedelta(days=(i * 7) + 6)
        fim = hoje - timedelta(days=(i * 7))
        semanas.append(
            {
                "label": "Atual" if i == 0 else f"Sem {6 - i}",
                "inicio": inicio,
                "fim": fim,
                "dados": {"foco": [], "sensorial": [], "social": [], "tarefas": []},
            }
        )

    for fb in feedbacks:
        for s in semanas:
            if s["inicio"] <= fb.criado_em <= s["fim"]:
                for cat, val in fb.categorias.items():
                    if cat in VALORES_NUMERICOS and val in VALORES_NUMERICOS[cat]:
                        s["dados"][cat].append(VALORES_NUMERICOS[cat][val])
                break

    def media(arr):
        return round(sum(arr) / len(arr)) if arr else 0

    return {
        "labels": [s["label"] for s in semanas],
        "foco": [media(s["dados"]["foco"]) for s in semanas],
        "sensorial": [media(s["dados"]["sensorial"]) for s in semanas],
        "social": [media(s["dados"]["social"]) for s in semanas],
        "tarefas": [media(s["dados"]["tarefas"]) for s in semanas],
    }