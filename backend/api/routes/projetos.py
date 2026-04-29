from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.projeto_service import listar_csvs, salvar_novo_projeto, listar_formatos_suportados

router = APIRouter(tags=["Projetos"])


@router.get("/projetos-csv/")
def projetos_csv():
    return {"csvs": listar_csvs()}


@router.get("/formatos-suportados/")
def formatos_suportados():
    return listar_formatos_suportados()


@router.post("/novo-projeto/")
async def novo_projeto(
    nome_projeto: str = Form(...),
    arquivo_projeto: UploadFile = File(...)
):
    try:
        return salvar_novo_projeto(nome_projeto, arquivo_projeto)
    except Exception as erro:
        raise HTTPException(status_code=400, detail=str(erro))
