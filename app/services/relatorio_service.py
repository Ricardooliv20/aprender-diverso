import json
from typing import Optional

from jinja2 import Template
from sqlalchemy.orm import Session

from app.models.aluno import Aluno
from app.models.feedback import Feedback
from app.models.pei import PEI
from app.models.relatorio import Relatorio
from app.services import feedback_service

# ---------- TEMPLATE DO RELATÓRIO ----------
TEMPLATE_RELATORIO = """RELATÓRIO BIMESTRAL DE ACOMPANHAMENTO INDIVIDUALIZADO
========================================================

Aluno(a): {{ aluno.nome }}
Turma: {{ turma_nome }}
Período: {{ periodo }}
Data de emissão: {{ data_emissao }}

--------------------------------------------------------
1. PANORAMA GERAL
--------------------------------------------------------
Durante o período, foram registrados {{ total_feedbacks }} micro-feedbacks
pelos professores, abrangendo as dimensões de foco, regulação sensorial,
interação social e execução de tarefas.

Médias observadas no período:
  • Foco e atenção:        {{ percentuais.foco }}%
  • Regulação sensorial:   {{ percentuais.sensorial }}%
  • Interação social:      {{ percentuais.social }}%
  • Execução de tarefas:   {{ percentuais.tarefas }}%

--------------------------------------------------------
2. DESTAQUES POSITIVOS
--------------------------------------------------------
{% if destaques %}{% for d in destaques %}  • {{ d }}
{% endfor %}{% else %}  • Sem dados suficientes para gerar destaques.
{% endif %}
--------------------------------------------------------
3. PONTOS DE ATENÇÃO
--------------------------------------------------------
{% if atencao %}{% for a in atencao %}  • {{ a }}
{% endfor %}{% else %}  • Nenhum ponto crítico identificado no período.
{% endif %}
--------------------------------------------------------
4. PLANO EDUCACIONAL INDIVIDUALIZADO (PEI)
--------------------------------------------------------
{% if pei %}
Resumo: {{ pei.resumo or "Não informado" }}

Objetivos:
{% for obj in objetivos %}  • [{{ obj.status }}] {{ obj.descricao }}
{% endfor %}
Adaptações:
{% for adp in adaptacoes %}  • {{ adp.descricao }}
{% endfor %}
{% else %}  • PEI ainda não cadastrado para este aluno.
{% endif %}
--------------------------------------------------------
5. CONSIDERAÇÕES FINAIS
--------------------------------------------------------
Este relatório foi gerado automaticamente pela plataforma Aprender Diverso
a partir dos micro-feedbacks registrados pelos professores. Recomenda-se
que seja lido em conjunto com a equipe pedagógica e a família, visando
fortalecer a parceria escola-família em prol do desenvolvimento integral
do(a) aluno(a).

Documento emitido em conformidade com a LGPD (Lei 13.709/2018).
"""


def gerar_relatorio(
    db: Session,
    aluno_id: int,
    periodo: str,
    gerado_por_id: int,
) -> Relatorio:
    # 1. Busca o aluno
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise ValueError("Aluno não encontrado")

    turma_nome = aluno.turma.nome if aluno.turma else "Não informada"

    # 2. Busca feedbacks
    feedbacks = feedback_service.listar_por_aluno(db, aluno_id, limite=1000)
    if len(feedbacks) == 0:
        raise ValueError("Este aluno ainda não possui feedbacks registrados")

    # 3. Calcula percentuais
    percentuais = feedback_service.calcular_percentuais(feedbacks)

    # 4. Gera destaques e pontos de atenção
    destaques = _gerar_destaques(percentuais)
    atencao = _gerar_pontos_atencao(percentuais)

    # 5. Busca PEI
    pei = db.query(PEI).filter(PEI.aluno_id == aluno_id).first()
    objetivos = pei.objetivos if pei else []
    adaptacoes = pei.adaptacoes if pei else []

    # 6. Renderiza template
    from datetime import datetime
    template = Template(TEMPLATE_RELATORIO)
    conteudo = template.render(
        aluno=aluno,
        turma_nome=turma_nome,
        periodo=periodo,
        data_emissao=datetime.now().strftime("%d/%m/%Y %H:%M"),
        total_feedbacks=len(feedbacks),
        percentuais=percentuais,
        destaques=destaques,
        atencao=atencao,
        pei=pei,
        objetivos=objetivos,
        adaptacoes=adaptacoes,
    )

    # 7. Salva no banco
    relatorio = Relatorio(
        aluno_id=aluno_id,
        gerado_por_id=gerado_por_id,
        periodo=periodo,
        conteudo=conteudo,
        percentuais=json.dumps(percentuais),
    )
    db.add(relatorio)
    db.commit()
    db.refresh(relatorio)
    return relatorio


def listar_por_aluno(db: Session, aluno_id: int):
    return (
        db.query(Relatorio)
        .filter(Relatorio.aluno_id == aluno_id)
        .order_by(Relatorio.criado_em.desc())
        .all()
    )


def obter_por_id(db: Session, relatorio_id: int) -> Optional[Relatorio]:
    return db.query(Relatorio).filter(Relatorio.id == relatorio_id).first()


# ---------- HELPERS ----------

def _gerar_destaques(percentuais: dict) -> list:
    destaques = []
    if percentuais["foco"] >= 70:
        destaques.append("Bom desempenho em foco e atenção sustentada.")
    if percentuais["sensorial"] >= 70:
        destaques.append("Boa regulação sensorial no ambiente escolar.")
    if percentuais["social"] >= 70:
        destaques.append("Interação social positiva com colegas e professores.")
    if percentuais["tarefas"] >= 70:
        destaques.append("Boa execução e conclusão de tarefas propostas.")
    return destaques


def _gerar_pontos_atencao(percentuais: dict) -> list:
    atencao = []
    if percentuais["foco"] < 50:
        atencao.append("Dificuldade em manter foco por longos períodos — considerar pausas.")
    if percentuais["sensorial"] < 50:
        atencao.append("Necessidade de apoio em regulação sensorial.")
    if percentuais["social"] < 50:
        atencao.append("Pouca interação social observada — incentivar atividades em grupo.")
    if percentuais["tarefas"] < 50:
        atencao.append("Dificuldade em concluir tarefas — considerar adaptações.")
    return atencao